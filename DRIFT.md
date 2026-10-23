# visiobot

Autonomous differential-drive robot built for the LSPP2026 60-day challenge. ROS 2 Jazzy, Gazebo Harmonic, Nav2, and YOLOv8 integration.

## Identity

- Small differential-drive ground robot (~0.4 × 0.3 m chassis)
- Two driven wheels + front caster; onboard 2D lidar and RGB camera
- Purpose: autonomous navigation with visual perception (SLAM + YOLOv8)
- Target simulator: Gazebo Harmonic (`ros_gz_sim`)

## Stack

- **ROS 2**: Jazzy
- **Simulator**: Gazebo Harmonic (`gz-sim`)
- **Build system**: `ament_cmake` (C++ packages), `ament_python` (Python package)
- **Bridge**: `ros_gz_bridge` (parameter bridge) + `ros_gz_image` (image bridge)

## Packages

| Package | Type | Role |
|---|---|---|
| `visiobot_core` | `ament_python` | Main Python nodes, URDF/xacro, launch files, config |
| `visiobot_cpp_core` | `ament_cmake` | C++ telemetry publisher/subscriber |
| `visiobot_interfaces` | `ament_cmake` | Custom service (`SetMode.srv`) and action (`Navigate.action`) |

## Build & Workflow

Build from the workspace root:

```bash
colcon build --symlink-install
source install/setup.bash
```

Build a single package:

```bash
colcon build --symlink-install --packages-select visiobot_interfaces
# rebuild dependents after interface changes
colcon build --symlink-install --packages-select visiobot_core visiobot_cpp_core
```

`visiobot_interfaces` must be built before any package that uses `SetMode.srv` or `Navigate.action`.

Launch targets:

```bash
# Visualize URDF in RViz with joint_state_publisher_gui
ros2 launch visiobot_core display.launch.py

# Full Gazebo simulation (robot + bridge + image bridge)
ros2 launch visiobot_core sim.launch.py

# Hardware / real-robot bringup (telemetry + TF broadcaster)
ros2 launch visiobot_core bringup.launch.py [use_sim_time:=false] [namespace:=]
```

`sim.launch.py` starts Gazebo with `-r` (auto-play, not paused). The robot is spawned at `z=0.15` to clear the ground plane.

## Robot Description

Entry point: `src/visiobot_core/urdf/visiobot.urdf.xacro`

Key links and their roles:

| Link | Description |
|---|---|
| `base_footprint` | Root link; odometry child frame |
| `base_link` | Chassis (0.4 × 0.3 × 0.1 m, 1.5 kg) |
| `right_wheel` / `left_wheel` | Continuous joints, wheel separation 0.35 m, radius 0.1 m |
| `caster_wheel` | Fixed front caster, sphere r=0.05 m |
| `camera_link` | RGB camera mount (fixed, xyz=0.18 0.0 0.075 from base) |
| `camera_link_optical` | Optical frame with standard camera rotation (rpy=-1.5708 0 -1.5708) |
| `laser_link` | 2D lidar mount (fixed, xyz=0.0 0.0 0.075 from base) |

The xacro defines reusable inertia macros (`box_inertia`, `cylinder_inertia`, `sphere_inertia`) and a `wheel` macro parameterized by `prefix`, `y_reflect`, and `rpy_val`.

Gazebo plugins embedded in the xacro:
- `gz::sim::systems::DiffDrive` — subscribes `/cmd_vel`, publishes `/odom` and `/tf`; `frame_id=odom`, `child_frame_id=base_footprint`
- `gz::sim::systems::JointStatePublisher` — publishes `/joint_states` for `base_to_left_wheel` and `base_to_right_wheel`

## Sensors & Topics

| Topic | Type | Source | Notes |
|---|---|---|---|
| `/scan` | `sensor_msgs/msg/LaserScan` | Gazebo lidar → bridge | 360 samples, ±180°, range 0.12–10.0 m, 10 Hz |
| `/camera/image_raw` | `sensor_msgs/msg/Image` | `ros_gz_image` bridge | 640×480 RGB, 10 Hz, frame `camera_link_optical` |
| `/cmd_vel` | `geometry_msgs/msg/Twist` | ROS → Gazebo | DiffDrive input |
| `/odom` | `nav_msgs/msg/Odometry` | Gazebo → ROS | DiffDrive output |
| `/tf` | `tf2_msgs/msg/TFMessage` | Gazebo → ROS | DiffDrive TF |
| `/joint_states` | `sensor_msgs/msg/JointState` | Gazebo → ROS | Wheel joints |
| `/clock` | `rosgraph_msgs/msg/Clock` | Gazebo → ROS | Sim time |
| `/visiobot_status` | remapped to `/status_updates` | `telemetry_pub` node | See bringup remapping |

## QoS Profiles

The `/scan` bridge publisher is forced to **Reliable** reliability via a QoS override in `sim.launch.py`:

```python
'qos_overrides./scan.publisher.reliability': 'reliable'
```

This is required for SLAM Toolbox compatibility. Without it, the default BestEffort QoS from the Gazebo bridge will cause SLAM Toolbox to drop scan messages.

The `/camera/image_raw` topic uses a separate `ros_gz_image` bridge node for higher-performance image transport.

## Custom Interfaces

Defined in `visiobot_interfaces`:

```
srv/SetMode.srv
action/Navigate.action
```

Both depend on `action_msgs`. Regenerate with `colcon build --packages-select visiobot_interfaces` after any `.srv` or `.action` file change; downstream packages must be rebuilt afterward.

## Configuration

```
src/visiobot_core/config/visiobot_params.yaml
```

```yaml
telemetry_pub:
  ros__parameters:
    robot_name: "VisioBot_Prime"
    publish_rate_hz: 2.0
```

Loaded by `bringup.launch.py` and passed to the `telemetry_pub` node. The `tf_broadcaster` node does not use this config file.

## Worlds

`gazebo/visiobot_v1.sdf` — flat ground-plane world, physics at 1 ms step / 1000 Hz update rate, real-time factor 1.0. The `sim.launch.py` currently loads `empty.sdf` from the `ros_gz_sim` package rather than this file; `visiobot_v1.sdf` is available for manual use or future integration.

## Debugging

- **Gazebo starts paused**: `sim.launch.py` passes `-r` to `gz_args`. If the robot doesn't move, verify this flag is present.
- **SLAM Toolbox drops scans**: Confirm the `/scan` bridge QoS override is active (`ros2 topic info /scan --verbose` should show Reliable).
- **TF tree broken**: The DiffDrive plugin publishes `odom → base_footprint`. The `robot_state_publisher` publishes `base_footprint → base_link` and all fixed/joint transforms. Both must be running.
- **`use_sim_time` mismatch**: `sim.launch.py` hardcodes `use_sim_time: True` in `robot_state_publisher`. Pass `use_sim_time:=true` to any additional nodes or they will use wall clock.
- **Interface not found after edit**: Always rebuild `visiobot_interfaces` first, then rebuild consumer packages.

```bash
# Check TF tree
ros2 run tf2_tools view_frames

# Inspect topic QoS
ros2 topic info /scan --verbose

# Verify bridge is running
ros2 node list | grep parameter_bridge
```