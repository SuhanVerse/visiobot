import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    # 1. Locate the YAML config file
    config_file = os.path.join(
        get_package_share_directory('visiobot_core'),
        'config',
        'visiobot_params.yaml'
    )

    # 2. Declare Launch Arguments
    use_sim_time_arg = DeclareLaunchArgument(
        'use_sim_time', default_value='false', description='Use simulation time'
    )
    namespace_arg = DeclareLaunchArgument(
        'namespace', default_value='', description='Robot namespace for multi-robot setups'
    )

    # 3. Define the Nodes to launch
    telemetry_node = Node(
        package='visiobot_core',
        executable='telemetry_pub',
        name='telemetry_pub',
        namespace=LaunchConfiguration('namespace'),
        parameters=[config_file, {
            'use_sim_time': LaunchConfiguration('use_sim_time')}],
        # Example of a topic remap
        remappings=[('/visiobot_status', '/status_updates')]
    )

    tf_broadcaster_node = Node(
        package='visiobot_core',
        executable='tf_broadcaster',
        name='tf_broadcaster',
        namespace=LaunchConfiguration('namespace'),
        parameters=[{'use_sim_time': LaunchConfiguration('use_sim_time')}]
    )

    # 4. Return the LaunchDescription to start everything
    return LaunchDescription([
        use_sim_time_arg,
        namespace_arg,
        telemetry_node,
        tf_broadcaster_node
    ])
