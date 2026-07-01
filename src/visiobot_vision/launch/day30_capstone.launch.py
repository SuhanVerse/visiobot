"""
Day 30: Phase 2 Capstone — Find and Approach (Final YOLO Launch File)

Architecture:
  1. sim_empty.launch.py   → Gazebo + robot_state_publisher + SLAM Toolbox + bridges
  2. yolo_detector         → Reads /camera/image_raw, detects person,
                             publishes /yolo_detections
  3. navigation_launch.py  → Nav2 (rolling window, no static map) with day28_nav2_params
  4. day30_capstone_node   → Patrol + YOLO servo state machine (25s delayed)
"""

import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction, LogInfo
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    visiobot_core_share   = get_package_share_directory('visiobot_core')
    visiobot_vision_share = get_package_share_directory('visiobot_vision')
    nav2_bringup_share    = get_package_share_directory('nav2_bringup')

    nav2_params_file = os.path.join(
        visiobot_vision_share, 'config', 'day28_nav2_params.yaml'
    )

    # ── 1. Gazebo + SLAM + ros_gz_bridge ─────────────────────────────────────
    gazebo_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(visiobot_core_share, 'launch', 'sim_empty.launch.py')
        )
    )

    # ── 2. YOLOv8 Detector ───────────────────────────────────────────────────
    yolo_detector = Node(
        package='visiobot_vision',
        executable='yolo_detector',
        name='yolo_detector',
        output='screen',
        parameters=[{'use_sim_time': True}]
    )

    # ── 3. Nav2 Navigation Stack (delayed 15s for SLAM) ──────────────────────
    nav2_stack = TimerAction(
        period=15.0,
        actions=[
            LogInfo(msg='[Day30] Starting Nav2 navigation stack...'),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    os.path.join(nav2_bringup_share, 'launch', 'navigation_launch.py')
                ),
                launch_arguments={
                    'use_sim_time': 'True',
                    'params_file':  nav2_params_file,
                }.items()
            ),
        ]
    )

    # ── 4. Day 30 Capstone Node (delayed 25s for Nav2) ───────────────────────
    capstone_node = TimerAction(
        period=25.0,
        actions=[
            LogInfo(msg='[Day30] Starting YOLO Phase 2 Capstone Node!'),
            Node(
                package='visiobot_vision',
                executable='day30_capstone_node',
                name='day30_capstone_node',
                output='screen',
                parameters=[{'use_sim_time': True}]
            )
        ]
    )

    return LaunchDescription([
        gazebo_sim,
        yolo_detector,
        nav2_stack,
        capstone_node,
    ])
