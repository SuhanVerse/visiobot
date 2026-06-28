#!/usr/bin/env python3
# =============================================================================
# Day 28: Waypoint Patrol with Nav2 Simple Commander
# VisioBot Vision Package
#
# Architecture:
#   - BasicNavigator is used STANDALONE as its own node in the main thread.
#   - A separate ROS 2 node handles YOLO subscriptions in a background thread.
#   - goToPose() is used PER WAYPOINT (not goThroughPoses) for reliable
#     sequential waypoint navigation.
#
# API: Installed Jazzy version (OLD API):
#   - goToPose() returns True/False
#   - isTaskComplete() takes no arguments
#   - getFeedback() takes no arguments
# =============================================================================

import csv
import datetime
import os
import threading
import time
from copy import deepcopy

import rclpy
from rclpy.executors import SingleThreadedExecutor
from rclpy.node import Node

from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
from vision_msgs.msg import Detection2DArray
import tf2_ros


# ---------------------------------------------------------------------------
# YOLO Listener Node — subscribes to detections and logs them with robot pose
# ---------------------------------------------------------------------------
class YoloListener(Node):
    """
    A lightweight ROS 2 node that only listens to YOLO detections.
    It uses a TF buffer to look up the robot's pose in the map frame.
    Runs inside a SingleThreadedExecutor on a background thread.
    """

    def __init__(self):
        super().__init__('day28_yolo_listener')
        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)

        # Cooldown: only log once every 2 seconds to avoid log spam
        self._last_log_time = 0.0
        self._log_cooldown = 2.0

        # CSV log file setup
        log_dir = os.path.expanduser('~/.ros/day28_detections')
        os.makedirs(log_dir, exist_ok=True)
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        log_path = os.path.join(log_dir, f'detections_{timestamp}.csv')
        self._csv_file = open(log_path, 'w', newline='')
        self._csv_writer = csv.writer(self._csv_file)
        self._csv_writer.writerow(['timestamp', 'class_id', 'score', 'map_x', 'map_y'])
        self.get_logger().info(f'Detection log file: {log_path}')

        # Subscribe to YOLO detections
        self.create_subscription(
            Detection2DArray,
            '/yolo/detections',
            self._yolo_callback,
            10
        )
        self.get_logger().info('YOLO Listener ready — watching for detections...')

    def _yolo_callback(self, msg: Detection2DArray):
        """Called whenever YOLO publishes detections."""
        if not msg.detections:
            return

        # Enforce cooldown
        now = time.time()
        if now - self._last_log_time < self._log_cooldown:
            return
        self._last_log_time = now

        try:
            # Get robot's current position in the map frame
            transform = self.tf_buffer.lookup_transform(
                'map',
                'base_footprint',
                rclpy.time.Time()
            )
            map_x = transform.transform.translation.x
            map_y = transform.transform.translation.y
        except tf2_ros.TransformException as ex:
            self.get_logger().warn(f'TF lookup failed: {ex}')
            return

        # Log every detection in the current frame
        for detection in msg.detections:
            if not detection.results:
                continue
            hypothesis = detection.results[0].hypothesis
            class_id = hypothesis.class_id
            score = hypothesis.score
            ts = datetime.datetime.now().isoformat()

            self.get_logger().info(
                f'*** ALERT: [{class_id}] (conf={score:.2f}) at '
                f'map coords X={map_x:.2f}m, Y={map_y:.2f}m ***'
            )
            self._csv_writer.writerow([ts, class_id, f'{score:.3f}', f'{map_x:.3f}', f'{map_y:.3f}'])
            self._csv_file.flush()

    def destroy_node(self):
        self._csv_file.close()
        super().destroy_node()


# ---------------------------------------------------------------------------
# Helper — build a PoseStamped in the map frame
# ---------------------------------------------------------------------------
def make_pose(nav: BasicNavigator, x: float, y: float, yaw_z: float = 0.0, yaw_w: float = 1.0) -> PoseStamped:
    """Create a PoseStamped message in the map frame."""
    pose = PoseStamped()
    pose.header.frame_id = 'map'
    pose.header.stamp = nav.get_clock().now().to_msg()
    pose.pose.position.x = x
    pose.pose.position.y = y
    pose.pose.orientation.z = yaw_z
    pose.pose.orientation.w = yaw_w
    return pose


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------
def main(args=None):
    rclpy.init(args=args)

    # ── 1. Create the YOLO listener node and spin it on a background thread ──
    yolo_node = YoloListener()
    yolo_executor = SingleThreadedExecutor()
    yolo_executor.add_node(yolo_node)
    yolo_thread = threading.Thread(target=yolo_executor.spin, daemon=True)
    yolo_thread.start()
    yolo_node.get_logger().info('YOLO listener thread started.')

    # ── 2. Create the BasicNavigator (it is its own ROS 2 node) ──
    navigator = BasicNavigator()

    # ── 3. Wait for Nav2 to be fully active ──
    navigator.get_logger().info('Waiting for Nav2 to become active...')
    navigator.waitUntilNav2Active(localizer='slam_toolbox')
    navigator.get_logger().info('Nav2 is active!')

    # Give SLAM a few more seconds to build a map large enough for planning
    navigator.get_logger().info('Waiting 5s for SLAM map to expand...')
    time.sleep(5.0)

    # Clear any stale costmap data before starting patrol
    navigator.clearAllCostmaps()
    navigator.get_logger().info('Costmaps cleared. Starting patrol!')

    # ── 4. Define the waypoint patrol route ──
    # These are waypoints the robot visits ONE BY ONE using goToPose().
    # Do NOT include the starting position — each waypoint must require movement.
    # The patrol forms a triangle: A → B → C → A → B → C → ...
    waypoints_data = [
        (1.5,  0.0,  0.0,   1.0),   # A: 1.5m forward
        (1.5,  1.5,  0.707, 0.707),  # B: diagonal corner
        (0.0,  1.5,  1.0,   0.0),    # C: left side
    ]

    # ── 5. Patrol loop: visit each waypoint one by one ──
    patrol_count = 0
    while rclpy.ok():
        patrol_count += 1
        navigator.get_logger().info(f'=== Starting patrol loop #{patrol_count} ===')

        for wp_idx, (x, y, z, w) in enumerate(waypoints_data):
            goal = make_pose(navigator, x, y, z, w)
            navigator.get_logger().info(
                f'Patrol#{patrol_count} → Waypoint {wp_idx + 1}/{len(waypoints_data)}: '
                f'({x:.1f}, {y:.1f})'
            )

            # goToPose() returns True/False (OLD Jazzy API)
            accepted = navigator.goToPose(goal)
            if not accepted:
                navigator.get_logger().warn(
                    f'Waypoint ({x:.1f}, {y:.1f}) was REJECTED. Skipping...'
                )
                continue

            # Poll for completion (OLD API — no task= parameter)
            i = 0
            while not navigator.isTaskComplete():
                i += 1
                feedback = navigator.getFeedback()
                if feedback and i % 10 == 0:
                    remaining = feedback.distance_remaining
                    navigator.get_logger().info(
                        f'  → Distance remaining: {remaining:.2f}m'
                    )
                time.sleep(0.2)

            # Check per-waypoint result
            result = navigator.getResult()
            if result == TaskResult.SUCCEEDED:
                navigator.get_logger().info(
                    f'  ✓ Waypoint {wp_idx + 1} reached!'
                )
            elif result == TaskResult.CANCELED:
                navigator.get_logger().info('Patrol was canceled. Exiting.')
                break
            elif result == TaskResult.FAILED:
                navigator.get_logger().warn(
                    f'  ✗ Waypoint {wp_idx + 1} FAILED. Clearing costmaps and continuing...'
                )
                navigator.clearAllCostmaps()
                time.sleep(2.0)
        else:
            # All waypoints visited successfully (no break)
            navigator.get_logger().info(
                f'Patrol loop #{patrol_count} complete! Reversing route...'
            )
            waypoints_data.reverse()
            continue

        # If we broke out of the for loop (canceled), exit the while loop too
        break

    # ── 6. Cleanup ──
    navigator.get_logger().info('Shutting down Day 28 patrol node.')
    yolo_executor.shutdown()
    yolo_node.destroy_node()
    navigator.destroyNode()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
