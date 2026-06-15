#!/usr/bin/env python3

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    # Locate the params and launch files
    visiobot_core_share = get_package_share_directory('visiobot_core')
    nav2_params_file = os.path.join(
        visiobot_core_share, 'config', 'nav2_params.yaml')

    nav2_bringup_dir = get_package_share_directory('nav2_bringup')
    nav2_bringup_launch = os.path.join(
        nav2_bringup_dir, 'launch', 'navigation_launch.py')

    # Declare arguments
    use_sim_time_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='True',
        description='Use simulation clock'
    )

    # Standardized list of tuples for launch_arguments!
    nav2_bringup = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(nav2_bringup_launch),
        launch_arguments=[
            ('use_sim_time', 'True'),
            ('params_file', nav2_params_file),
            ('autostart', 'True'),
            ('use_collision_monitor', 'False')
        ]
    )

    return LaunchDescription([
        use_sim_time_arg,
        nav2_bringup
    ])
