"""
Day 29: YOLO-to-Nav2 Target Handoff — Launch File
=================================================
Architecture:
  1. sim_empty.launch.py → Gazebo + robot_state_publisher + ros_gz_bridge +
                           async_slam_toolbox_node (the ONE source of /map)
  2. Nav2 navigation_launch.py → planners, controllers, costmaps, bt_navigator
     Uses day28_nav2_params.yaml which has a ROLLING WINDOW global costmap
  3. YOLOv8 detector node
  4. Day 29 Target Handoff node (delayed 25s to let Gazebo + SLAM + Nav2 fully start)
"""

import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction, LogInfo
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    visiobot_core_share  = get_package_share_directory('visiobot_core')
    visiobot_vision_share = get_package_share_directory('visiobot_vision')
    nav2_bringup_share   = get_package_share_directory('nav2_bringup')

    # Use our Day 28 specific nav2 params (rolling window global costmap)
    nav2_params_file = os.path.join(visiobot_vision_share, 'config', 'day28_nav2_params.yaml')

    # ── 1. Gazebo simulation (includes SLAM toolbox + bridges) ──
    gazebo_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(visiobot_core_share, 'launch', 'sim_empty.launch.py')
        )
    )

    # ── 2. Nav2 stack (navigation only) ──
    nav2_stack = TimerAction(
        period=15.0,
        actions=[
            LogInfo(msg='[Day29] Starting Nav2 navigation stack...'),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    os.path.join(nav2_bringup_share, 'launch', 'navigation_launch.py')
                ),
                launch_arguments={
                    'use_sim_time': 'True',
                    'params_file': nav2_params_file,
                }.items()
            ),
        ]
    )

    # ── 3. YOLOv8 Detector ──
    yolo_detector = Node(
        package='visiobot_vision',
        executable='yolo_detector',
        name='yolo_detector',
        output='screen',
        parameters=[{'use_sim_time': True}]
    )

    # ── 4. Day 29 Handoff Node ──
    handoff_node = TimerAction(
        period=25.0,
        actions=[
            LogInfo(msg='[Day29] Starting target handoff node...'),
            Node(
                package='visiobot_vision',
                executable='day29_target_handoff_node',
                name='day29_handoff_node',
                output='screen',
                parameters=[{'use_sim_time': True}]
            )
        ]
    )

    return LaunchDescription([
        gazebo_sim,
        yolo_detector,
        nav2_stack,
        handoff_node,
    ])
