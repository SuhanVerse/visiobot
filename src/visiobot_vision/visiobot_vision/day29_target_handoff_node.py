#!/usr/bin/env python3
# =============================================================================
# Day 29: YOLO-to-Nav2 Target Handoff (With Cooldown Memory)
# VisioBot Vision Package
#
# Architecture:
#   - State Machine: PATROL -> APPROACH -> COOLDOWN -> PATROL
#   - A background thread spins a Node that subscribes to YOLO.
#   - The main thread runs Nav2 patrol.
#   - When a target is detected, the background Node triggers a handoff, 
#     preempts the Nav2 task, and takes over /cmd_vel using IBVS.
#   - Once the target is reached, it enters a COOLDOWN state for 10s to 
#     ignore the camera, allowing Nav2 to resume patrol and drive away 
#     without getting trapped in a target-fixation loop.
# =============================================================================

import time
import threading
import rclpy
from rclpy.node import Node
from rclpy.executors import SingleThreadedExecutor
from geometry_msgs.msg import PoseStamped, Twist
from vision_msgs.msg import Detection2DArray
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult

class HandoffNode(Node):
    def __init__(self):
        super().__init__('day29_handoff_node')
        
        # State Machine definition
        self.state = 'PATROL' 
        self.handoff_triggered = False

        # IBVS Proportional Gains
        self.k_w = 0.002   
        self.k_v = 0.005   
        self.max_w = 0.5
        self.max_v = 1.0
        
        self.image_width = 640
        self.cx = self.image_width / 2.0
        self.target_height = 120.0  
        
        self.latest_error_x = 0.0
        self.latest_error_z = 0.0
        self.last_target_time = 0.0
        
        # Memory / Cooldown Settings
        self.cooldown_start_time = 0.0
        self.cooldown_duration = 10.0 # Ignore the camera for 10s after reaching a target
        
        # ROS 2 Interfaces
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.yolo_sub = self.create_subscription(Detection2DArray, '/yolo/detections', self.yolo_callback, 10)
        
        # Control Loop for IBVS (runs at 10Hz)
        self.servo_timer = self.create_timer(0.1, self.servo_loop)
        
        self.get_logger().info('Day 29 Handoff Node (With Memory) Initialized.')

    def yolo_callback(self, msg):
        if not msg.detections:
            return
            
        # COOLDOWN CHECK: Ignore camera input if we recently interacted with a target
        if self.state == 'COOLDOWN':
            return 
            
        detection = msg.detections[0]
        if not detection.results:
            return
            
        score = detection.results[0].hypothesis.score
        class_id = detection.results[0].hypothesis.class_id
        
        # Confidence Threshold Check
        if score > 0.60:
            self.last_target_time = time.time()
            
            # Calculate errors for Visual Servoing
            current_height = detection.bbox.size_y
            target_x = detection.bbox.center.position.x
            
            self.latest_error_x = target_x - self.cx
            error_z = self.target_height - current_height
            
            if error_z < 0: 
                error_z = 0.0 
                
            self.latest_error_z = error_z
            
            # State Transition: Patrol -> Approach
            if self.state == 'PATROL':
                self.get_logger().warn(f'>>> Target [{class_id}] spotted (conf={score:.2f})! Preempting Nav2 Patrol! <<<')
                self.state = 'APPROACH'
                self.handoff_triggered = True

    def servo_loop(self):
        if self.state == 'APPROACH':
            # TIMEOUT / TARGET LOST LOGIC
            if time.time() - self.last_target_time > 3.0:
                self.get_logger().warn('>>> Target lost for 3s. Returning to PATROL! <<<')
                self.state = 'PATROL'
                self.handoff_triggered = False
                self.stop_robot()
                return
                
            # TARGET REACHED LOGIC
            if self.latest_error_z == 0.0:
                self.get_logger().info('Target reached! Final alignment complete.')
                self.stop_robot()
                
                # Activate Cooldown to prevent looping
                self.state = 'COOLDOWN'
                self.cooldown_start_time = time.time()
                self.handoff_triggered = False
                self.get_logger().warn(f'Entering COOLDOWN for {self.cooldown_duration}s to avoid re-targeting.')
                return

            # EXECUTE IBVS
            twist = Twist()
            raw_w = -self.k_w * self.latest_error_x
            twist.angular.z = max(min(raw_w, self.max_w), -self.max_w)
            
            raw_v = self.k_v * self.latest_error_z
            twist.linear.x = max(min(raw_v, self.max_v), -self.max_v)
            
            self.cmd_pub.publish(twist)
            
        elif self.state == 'COOLDOWN':
            # Check if cooldown is finished
            if time.time() - self.cooldown_start_time > self.cooldown_duration:
                self.get_logger().info('Cooldown finished. Camera memory cleared. Resuming active hunting.')
                self.state = 'PATROL'

    def stop_robot(self):
        self.cmd_pub.publish(Twist())


def make_pose(nav: BasicNavigator, x: float, y: float, yaw_z: float = 0.0, yaw_w: float = 1.0) -> PoseStamped:
    pose = PoseStamped()
    pose.header.frame_id = 'map'
    pose.header.stamp = nav.get_clock().now().to_msg()
    pose.pose.position.x = x
    pose.pose.position.y = y
    pose.pose.orientation.z = yaw_z
    pose.pose.orientation.w = yaw_w
    return pose


def main(args=None):
    rclpy.init(args=args)

    # 1. Start Background Handoff Node
    handoff_node = HandoffNode()
    executor = SingleThreadedExecutor()
    executor.add_node(handoff_node)
    thread = threading.Thread(target=executor.spin, daemon=True)
    thread.start()

    # 2. Initialize Nav2 Navigator
    navigator = BasicNavigator()
    navigator.get_logger().info('Waiting for Nav2 to become active...')
    navigator.waitUntilNav2Active(localizer='slam_toolbox')
    navigator.get_logger().info('Nav2 is active! Waiting 5s for map...')
    time.sleep(5.0)
    navigator.clearAllCostmaps()
    
    # 3. Define Patrol Route
    waypoints_data = [
        (1.5,  0.0,  0.0,   1.0),    
        (1.5,  1.5,  0.707, 0.707),  
        (0.0,  1.5,  1.0,   0.0),    
    ]
    
    patrol_count = 0

    try:
        while rclpy.ok():
            # If in APPROACH state, just wait. The background node handles driving.
            if handoff_node.state == 'APPROACH':
                time.sleep(0.5)
                continue
                
            patrol_count += 1
            navigator.get_logger().info(f'=== Starting patrol loop #{patrol_count} ===')

            for wp_idx, (x, y, z, w) in enumerate(waypoints_data):
                # Extra check in case state changed while preparing
                if handoff_node.state == 'APPROACH':
                    break
                    
                goal = make_pose(navigator, x, y, z, w)
                navigator.get_logger().info(f'Navigating to Waypoint {wp_idx + 1}: ({x:.1f}, {y:.1f})')
                
                accepted = navigator.goToPose(goal)
                if not accepted:
                    navigator.get_logger().warn('Goal rejected. Skipping...')
                    continue

                # Poll Nav2 Task
                while not navigator.isTaskComplete():
                    # HANDOFF CHECK: Did the YOLO node detect a target?
                    if handoff_node.handoff_triggered:
                        navigator.get_logger().warn('>>> Handoff triggered! Canceling Nav2 task! <<<')
                        navigator.cancelTask()
                        handoff_node.handoff_triggered = False
                        break 
                        
                    time.sleep(0.1)
                
                # If we broke out due to handoff, break the waypoint loop too
                if handoff_node.state == 'APPROACH':
                    break

                # Otherwise, log waypoint success/failure
                if navigator.getResult() == TaskResult.SUCCEEDED:
                    navigator.get_logger().info(f'  ✓ Waypoint {wp_idx + 1} reached.')
                elif navigator.getResult() == TaskResult.FAILED:
                    navigator.get_logger().warn(f'  ✗ Waypoint {wp_idx + 1} failed.')
                    navigator.clearAllCostmaps()
            
            # If we completed the waypoints normally, reverse route.
            # If we are in COOLDOWN, we don't reverse route, we just loop back and resume the next waypoints!
            if handoff_node.state == 'PATROL':
                navigator.get_logger().info('Route complete. Reversing patrol direction...')
                waypoints_data.reverse()

    except KeyboardInterrupt:
        navigator.get_logger().info('Interrupted by user.')
    finally:
        handoff_node.stop_robot()
        executor.shutdown()
        handoff_node.destroy_node()
        navigator.destroyNode()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
