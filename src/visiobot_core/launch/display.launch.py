import os
import xacro
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    # Locate the .xacro file
    xacro_file = os.path.join(
        get_package_share_directory('visiobot_core'),
        'urdf',
        'visiobot.urdf.xacro'
    )

    # Compile the Xacro file into a standard URDF string format on the fly
    robot_description_raw = xacro.process_file(xacro_file).toxml()

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        parameters=[{'robot_description': robot_description_raw, 'use_sim_time': False}]
    )

    joint_state_publisher_gui_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui'
    )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', os.path.join(get_package_share_directory('visiobot_core'), 'rviz', 'visiobot_sim.rviz')]
    )

    return LaunchDescription([
        robot_state_publisher_node,
        joint_state_publisher_gui_node,
        rviz_node
    ])
