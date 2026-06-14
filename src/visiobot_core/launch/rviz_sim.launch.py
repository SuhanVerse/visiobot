#!/usr/bin/env python3
"""Launch RViz2 with the visiobot_sim.rviz config.

This is a lightweight launch that ONLY starts RViz2.
Robot state publisher and joint state publisher are expected
to already be running (e.g. from sim.launch.py).
"""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    pkg_share = get_package_share_directory('visiobot_core')
    rviz_config = os.path.join(pkg_share, 'rviz', 'visiobot_sim.rviz')

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config],
        parameters=[{'use_sim_time': True}],
        output='screen',
    )

    return LaunchDescription([rviz_node])
