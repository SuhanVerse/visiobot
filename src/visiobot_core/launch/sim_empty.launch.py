import os
import xacro
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():
    visiobot_core_dir = get_package_share_directory('visiobot_core')
    ros_gz_sim_dir = get_package_share_directory('ros_gz_sim')

    models_dir = os.path.join(visiobot_core_dir, 'models')
    if 'GZ_SIM_RESOURCE_PATH' in os.environ:
        os.environ['GZ_SIM_RESOURCE_PATH'] = f"{models_dir}:{os.environ['GZ_SIM_RESOURCE_PATH']}"
    else:
        os.environ['GZ_SIM_RESOURCE_PATH'] = models_dir

    world_file = os.path.join(visiobot_core_dir, 'gazebo', 'visiobot_empty.sdf')

    xacro_file = os.path.join(visiobot_core_dir, 'urdf', 'visiobot.urdf.xacro')
    robot_description_raw = xacro.process_file(xacro_file).toxml()

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{
            'robot_description': robot_description_raw,
            'use_sim_time': True
        }]
    )

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ros_gz_sim_dir, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={'gz_args': f'{world_file} -r'}.items()
    )

    spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-topic', 'robot_description',
            '-name', 'visiobot',
            '-z', '0.0'
        ],
        output='screen'
    )

    # Standard Bridge (with QoS Overrides and Odom)
    bridge_node = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan',
            '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
            '/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist',
            '/tf@tf2_msgs/msg/TFMessage[gz.msgs.Pose_V',
            '/joint_states@sensor_msgs/msg/JointState[gz.msgs.Model',
            '/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry',
            '/camera/camera_info@sensor_msgs/msg/CameraInfo[gz.msgs.CameraInfo'
        ],
        parameters=[{
            'qos_overrides./scan.publisher.reliability': 'reliable',
            'use_sim_time': True
        }],
        output='screen'
    )

    # High-Performance Bridge exclusively for camera image
    image_bridge_node = Node(
        package='ros_gz_image',
        executable='image_bridge',
        arguments=['/camera/image_raw'],
        output='screen'
    )

    slam_toolbox_node = Node(
        package='slam_toolbox',
        executable='async_slam_toolbox_node',
        name='slam_toolbox',
        parameters=[
            os.path.join(visiobot_core_dir, 'config', 'slam_toolbox_params.yaml'),
            {'use_sim_time': True}
        ],
        output='screen'
    )

    lifecycle_manager_slam = Node(
        package='nav2_lifecycle_manager',
        executable='lifecycle_manager',
        name='lifecycle_manager_slam',
        parameters=[{
            'autostart': True,
            'bond_timeout': 0.0,
            'node_names': ['slam_toolbox'],
            'use_sim_time': True
        }],
        output='screen'
    )

    # Delay spawn until Gazebo is ready
    spawn_timer = TimerAction(
        period=5.0,
        actions=[spawn_entity]
    )

    # Delay bridge until Gazebo topics exist
    bridge_timer = TimerAction(
        period=3.0,
        actions=[bridge_node, image_bridge_node]
    )

    # Delay SLAM until robot is spawned and bridge is up
    slam_timer = TimerAction(
        period=12.0,
        actions=[slam_toolbox_node, lifecycle_manager_slam]
    )

    return LaunchDescription([
        robot_state_publisher_node,
        gazebo,
        spawn_timer,
        bridge_timer,
        slam_timer,
    ])
