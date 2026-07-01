#!/usr/bin/env python3
# =============================================================================
# Day 30: Phase 2 Capstone — Find and Approach (YOLOv8 Edition)
# VisioBot Vision Package
#
# STATE MACHINE:
#   PATROL (Nav2 waypoints) → SERVO (YOLO tracking) → COOLDOWN → PATROL
#
# KEY FIXES:
#   1. Uses threading.Event() for safe shutdown without RCLError.
#   2. Validates 'person' class only to prevent chasing trucks.
#   3. YOLO bounding box approximation for distance. Clamps minimum 1.5m 
#      to prevent driving too close and crashing the Nav2 costmap.
# =============================================================================

import time
import threading
import rclpy
from rclpy.node import Node
from rclpy.executors import SingleThreadedExecutor
from geometry_msgs.msg import PoseStamped, Twist
from vision_msgs.msg import Detection2DArray
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult


class YoloCapstoneNode(Node):
    """Day 30 Capstone Brain Node using YOLOv8."""

    K_ANGULAR = 0.003
    K_LINEAR  = 0.4
    MAX_ANGULAR = 0.5
    MAX_LINEAR  = 0.3
    
    # Distance approximation based on YOLO bounding box height (pixels)
    # The larger the box, the closer the object.
    STOP_HEIGHT_PX = 200.0  
    
    LOST_TIMEOUT_S = 3.0
    COOLDOWN_SECS = 15.0

    def __init__(self):
        super().__init__('day30_capstone_node')
        self.state = 'PATROL'
        
        # Thread safety guard for clean Ctrl+C
        self.is_running = threading.Event()
        self.is_running.set()

        self.handoff_triggered = False

        self._last_detection_time = 0.0
        self._cooldown_start = 0.0
        
        self._cx_error = 0.0
        self._height = 0.0
        
        self.allowed_classes = {'person', 'person_standing', 'human'}

        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.yolo_sub = self.create_subscription(
            Detection2DArray,
            '/yolo/detections',
            self._yolo_callback,
            10
        )
        self.servo_timer = self.create_timer(0.1, self._servo_loop)

        self.get_logger().info('\n[Day30] YOLO Capstone Node initialized. Waiting for Nav2...')

    def _yolo_callback(self, msg: Detection2DArray):
        if not self.is_running.is_set() or self.state == 'COOLDOWN':
            return

        best_det = None
        for det in msg.detections:
            if not det.results: continue
            class_id = det.results[0].hypothesis.class_id.lower()
            score = det.results[0].hypothesis.score
            
            # Check whitelist! (Prevents chasing Cars/Trucks and crashing RViz)
            if class_id in self.allowed_classes and score > 0.60:
                best_det = det
                break

        if best_det:
            self._last_detection_time = time.time()
            # Image center is 320 for a 640x480 image
            self._cx_error = best_det.bbox.center.position.x - 320.0 
            self._height = best_det.bbox.size_y

            if self.state == 'PATROL':
                self.get_logger().warn(
                    f'\n>>> Target acquired! Height={self._height:.1f}px <<<\n'
                    f'>>> Triggering Nav2 preemption → SERVO APPROACH <<<'
                )
                self.state = 'SERVO'
                self.handoff_triggered = True

    def _servo_loop(self):
        if not self.is_running.is_set():
            return

        if self.state == 'SERVO':
            if self._last_detection_time > 0 and time.time() - self._last_detection_time > self.LOST_TIMEOUT_S:
                self.get_logger().warn(f'>>> Target lost for {self.LOST_TIMEOUT_S}s. Returning to PATROL! <<<')
                self.state = 'PATROL'
                self.handoff_triggered = False
                self._stop_robot()
                return

            # If bounding box height > STOP_HEIGHT_PX, we are close enough (approx 1.5m)
            if self._height > self.STOP_HEIGHT_PX and self._last_detection_time > 0:
                self.get_logger().info(
                    f'\n>>> TARGET REACHED! (Box height {self._height:.1f} > {self.STOP_HEIGHT_PX}) <<<\n'
                    f'>>> Entering COOLDOWN for {self.COOLDOWN_SECS}s <<<'
                )
                self._stop_robot()
                self.state = 'COOLDOWN'
                self._cooldown_start = time.time()
                self.handoff_triggered = False
                return

            # Proportional Control
            twist = Twist()
            # Turn toward object
            w = -self.K_ANGULAR * self._cx_error
            twist.angular.z = max(min(w, self.MAX_ANGULAR), -self.MAX_ANGULAR)
            
            # Drive forward (faster when box is small/far, slower when big/close)
            v = self.K_LINEAR * (1.0 - (self._height / self.STOP_HEIGHT_PX))
            twist.linear.x = max(min(v, self.MAX_LINEAR), 0.0)
            
            self.cmd_pub.publish(twist)

        elif self.state == 'COOLDOWN':
            if time.time() - self._cooldown_start > self.COOLDOWN_SECS:
                self.get_logger().info('>>> Cooldown finished. Resuming active hunting. <<<')
                self._last_detection_time = 0.0
                self.state = 'PATROL'

    def _stop_robot(self):
        if self.is_running.is_set():
            self.cmd_pub.publish(Twist())


# ── Waypoint Helper ───────────────────────────────────────────────────────────
def _make_goal(nav: BasicNavigator, x: float, y: float, qz: float=0.0, qw: float=1.0) -> PoseStamped:
    p = PoseStamped()
    p.header.frame_id = 'map'
    p.header.stamp = nav.get_clock().now().to_msg()
    p.pose.position.x = x
    p.pose.position.y = y
    p.pose.orientation.z = qz
    p.pose.orientation.w = qw
    return p


# ── Patrol Thread ─────────────────────────────────────────────────────────────
def _patrol_loop(node: YoloCapstoneNode, navigator: BasicNavigator):
    navigator.get_logger().info('Waiting for Nav2 to become active...')
    navigator.waitUntilNav2Active(localizer='slam_toolbox')
    navigator.clearAllCostmaps()
    time.sleep(3.0)
    navigator.get_logger().info(
        '\n[Day30] === Patrol STARTED ===\n'
        'ACTION REQUIRED: In Gazebo Resource Spawner, spawn the "person_standing"\n'
        'model. The robot will detect and approach it.'
    )

    route_a = [
        _make_goal(navigator, 1.5,  0.0,  0.0,   1.0),
        _make_goal(navigator, 1.5,  1.5,  0.707, 0.707),
        _make_goal(navigator, 0.0,  1.5,  1.0,   0.0),
    ]
    route_b = list(reversed(route_a))
    loop = 0

    while node.is_running.is_set():
        if node.state in ('SERVO', 'COOLDOWN'):
            time.sleep(0.3)
            continue

        loop += 1
        navigator.get_logger().info(f'=== Patrol loop #{loop} ===')
        current_route = route_b if loop % 2 == 0 else route_a

        for idx, goal in enumerate(current_route):
            if not node.is_running.is_set(): return
            if node.state in ('SERVO', 'COOLDOWN'): break

            navigator.get_logger().info(f'→ Waypoint {idx+1}/{len(current_route)}')
            if not navigator.goToPose(goal): continue

            while not navigator.isTaskComplete():
                if not node.is_running.is_set():
                    navigator.cancelTask()
                    return
                if node.handoff_triggered:
                    navigator.get_logger().warn('>>> HANDOFF: Canceling Nav2 task! <<<')
                    navigator.cancelTask()
                    node.handoff_triggered = False
                    break
                time.sleep(0.1)

            if node.state in ('SERVO', 'COOLDOWN'):
                break

            if navigator.getResult() == TaskResult.FAILED:
                navigator.clearAllCostmaps()
                time.sleep(1.0)

# ── Main ──────────────────────────────────────────────────────────────────────
def main(args=None):
    rclpy.init(args=args)
    node = YoloCapstoneNode()
    executor = SingleThreadedExecutor()
    executor.add_node(node)
    spin_thread = threading.Thread(target=executor.spin, daemon=True)
    spin_thread.start()

    navigator = BasicNavigator()
    patrol_thread = threading.Thread(target=_patrol_loop, args=(node, navigator), daemon=True)
    patrol_thread.start()

    try:
        while rclpy.ok():
            time.sleep(0.5)
    except KeyboardInterrupt:
        node.get_logger().info('Shutting down Day 30 Capstone...')
    finally:
        node.is_running.clear()
        node._stop_robot()
        try: navigator.cancelTask()
        except: pass
        patrol_thread.join(timeout=3.0)
        executor.shutdown(timeout_sec=2.0)
        node.destroy_node()
        navigator.destroyNode()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
