# VisioBot Simulation Guide

This guide walks you through building, launching, and verifying the full VisioBot simulation stack — Gazebo Harmonic, SLAM Toolbox, and RViz2 — on ROS 2 Jazzy.

---

## Prerequisites

- ROS 2 Jazzy installed and sourced
- Gazebo Harmonic (`gz-sim` 8.x) installed
- The following ROS packages installed:
  - `ros-jazzy-ros-gz-sim`
  - `ros-jazzy-ros-gz-bridge`
  - `ros-jazzy-ros-gz-image`
  - `ros-jazzy-slam-toolbox`
  - `ros-jazzy-nav2-lifecycle-manager`
  - `ros-jazzy-robot-state-publisher`
  - `ros-jazzy-joint-state-publisher-gui`
  - `ros-jazzy-rviz2`

Install any missing packages:

```bash
sudo apt update
sudo apt install ros-jazzy-ros-gz-sim ros-jazzy-ros-gz-bridge ros-jazzy-ros-gz-image \
  ros-jazzy-slam-toolbox ros-jazzy-nav2-lifecycle-manager \
  ros-jazzy-robot-state-publisher ros-jazzy-joint-state-publisher-gui ros-jazzy-rviz2
```

---

## 1. Build the Workspace

Always build from the workspace root (`/home/xlegion/visiobot`).

```bash
cd ~/visiobot

# Install declared dependencies
rosdep install --from-paths src --ignore-src -y

# Build all packages (interfaces first, then the rest)
colcon build --symlink-install --packages-select visiobot_interfaces
colcon build --symlink-install

# Source the workspace
source install/setup.bash
```

> **Note:** Every time you open a new terminal, run `source ~/visiobot/install/setup.bash` before using any `ros2` commands.

---

## 2. Launch the Full Simulation

```bash
ros2 launch visiobot_core sim.launch.py
```

This single command starts:

| Component | What it does |
|---|---|
| `robot_state_publisher` | Publishes `/robot_description` and the TF tree from the URDF |
| Gazebo Harmonic | Loads `gazebo/visiobot_room.sdf` with the room environment |
| `ros_gz_sim create` | Spawns the VisioBot model at `z=0.15` |
| `ros_gz_bridge` | Bridges `/scan`, `/odom`, `/tf`, `/joint_states`, `/cmd_vel`, `/clock` |
| `ros_gz_image` | Bridges `/camera/image_raw` (high-performance image transport) |
| `slam_toolbox` | Starts async SLAM mapping (delayed 10 s to let Gazebo initialize) |
| `lifecycle_manager_slam` | Activates the SLAM Toolbox lifecycle node automatically |

### Expected startup sequence

1. **0–3 s** — Gazebo window opens, robot appears in the room.
2. **3–10 s** — Bridge nodes connect; `/scan` and `/odom` topics become active.
3. **~10 s** — SLAM Toolbox activates; the `map` frame appears in TF.
4. **~12 s** — RViz (if open) shows the LiDAR scan and a growing map.

---

## 3. Open RViz2

In a **new terminal** (with the workspace sourced):

```bash
ros2 launch visiobot_core display.launch.py
```

Or launch RViz manually with the saved config:

```bash
rviz2 -d ~/visiobot/src/visiobot_core/rviz/visiobot.rviz
```

### Key displays to enable in RViz

| Display | Topic / Frame | Purpose |
|---|---|---|
| **RobotModel** | `/robot_description` | Shows the 3-D robot model |
| **LaserScan** | `/scan` | LiDAR point cloud |
| **Map** | `/map` | SLAM-generated occupancy grid |
| **Camera** | `/camera/image_raw` | RGB camera feed |
| **TF** | — | Full transform tree |

Set **Fixed Frame** to `map` for navigation/SLAM work, or `base_link` for robot-centric inspection.

---

## 4. Verify the Pipeline

Run these checks in separate terminals after launching the simulation.

### 4.1 Confirm active topics

```bash
ros2 topic list
```

Expected topics (among others):

```
/camera/image_raw
/clock
/cmd_vel
/joint_states
/map
/odom
/robot_description
/scan
/tf
/tf_static
```

### 4.2 Check LiDAR data

```bash
ros2 topic echo /scan --once
```

You should see a `sensor_msgs/msg/LaserScan` message with 360 range values.

### 4.3 Verify scan QoS (required for SLAM Toolbox)

```bash
ros2 topic info /scan --verbose
```

The publisher reliability must show **Reliable** (not Best Effort). If it shows Best Effort, the `qos_overrides` parameter in `sim.launch.py` is not being applied — rebuild and re-source.

### 4.4 Check the TF tree

```bash
ros2 run tf2_tools view_frames
```

This generates `frames.pdf` in the current directory. The expected chain is:

```
map → odom → base_footprint → base_link → laser_link
                                         → camera_link → camera_link_optical
```

- `map → odom` is published by **SLAM Toolbox** (appears ~10 s after launch).
- `odom → base_footprint` is published by the **DiffDrive Gazebo plugin**.
- `base_footprint → base_link` and sensor frames are published by **robot_state_publisher**.

### 4.5 Verify SLAM Toolbox is active

```bash
ros2 lifecycle get /slam_toolbox
```

Expected output: `active [3]`. If it shows `unconfigured`, the lifecycle manager has not activated it yet — wait a few more seconds and retry.

### 4.6 Check the bridge is running

```bash
ros2 node list | grep parameter_bridge
```

Should return `/parameter_bridge`.

---

## 5. Drive the Robot

Send velocity commands to move the robot and build the map:

```bash
# Move forward
ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist \
  "{linear: {x: 0.3, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}"

# Rotate in place
ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist \
  "{linear: {x: 0.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.5}}"

# Stop
ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist \
  "{linear: {x: 0.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}"
```

For interactive keyboard control, install and run `teleop_twist_keyboard`:

```bash
sudo apt install ros-jazzy-teleop-twist-keyboard
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

---

## 6. Save the SLAM Map

Once you have driven around the room and the map looks complete:

```bash
mkdir -p ~/visiobot/maps
ros2 run nav2_map_server map_saver_cli -f ~/visiobot/maps/visiobot_room
```

This saves `visiobot_room.pgm` (image) and `visiobot_room.yaml` (metadata) to the `maps/` directory.

---

## 7. Visualize the URDF Only (No Gazebo)

To inspect the robot model and joint positions without launching the full simulation:

```bash
ros2 launch visiobot_core display.launch.py
```

This opens RViz with `joint_state_publisher_gui` sliders to articulate the wheels.

---

## 8. Rebuild After Code Changes

```bash
cd ~/visiobot
colcon build --symlink-install
source install/setup.bash
```

If you only changed `visiobot_interfaces` (`.srv` or `.action` files):

```bash
colcon build --symlink-install --packages-select visiobot_interfaces
colcon build --symlink-install --packages-select visiobot_core visiobot_cpp_core
source install/setup.bash
```

---

## 9. Common Issues

### "Frame [map] does not exist" in RViz

SLAM Toolbox has not activated yet. Wait until ~10 seconds after launch and check:

```bash
ros2 lifecycle get /slam_toolbox
```

If it stays `unconfigured`, check that `slam_toolbox` and `nav2_lifecycle_manager` are listed as `exec_depend` in `src/visiobot_core/package.xml`.

### Robot does not move

- Confirm Gazebo is not paused — the `-r` flag in `sim.launch.py` should auto-play it.
- Check the bridge is running: `ros2 node list | grep parameter_bridge`
- Verify `/cmd_vel` is bridged with `]` (ROS → Gazebo direction).

### Camera image is blank in RViz

- Confirm `ros_gz_image` bridge node is running: `ros2 node list | grep image_bridge`
- Check the `gz_frame_id` in the URDF xacro is set to `camera_link_optical` for the camera sensor.

### SLAM Toolbox drops scan messages

```bash
ros2 topic info /scan --verbose
```

The publisher must show **Reliable** reliability. If it shows Best Effort, the `qos_overrides./scan.publisher.reliability: reliable` parameter in `sim.launch.py` is not applied — rebuild the package and re-source.

### `use_sim_time` mismatch

All nodes must use simulation time when running in Gazebo. The `sim.launch.py` sets `use_sim_time: True` on `robot_state_publisher`, `parameter_bridge`, and `slam_toolbox`. If you launch additional nodes manually, pass `--ros-args -p use_sim_time:=true`.

### Build fails after interface changes

Always rebuild `visiobot_interfaces` first:

```bash
colcon build --symlink-install --packages-select visiobot_interfaces
colcon build --symlink-install --packages-select visiobot_core visiobot_cpp_core
```

---

## 10. Package Overview

| Package | Type | Role |
|---|---|---|
| `visiobot_core` | `ament_python` | URDF/xacro, launch files, SLAM config, Python nodes |
| `visiobot_cpp_core` | `ament_cmake` | C++ telemetry publisher/subscriber |
| `visiobot_interfaces` | `ament_cmake` | Custom `SetMode.srv` and `Navigate.action` definitions |

---

## 11. File Reference

| File | Purpose |
|---|---|
| `src/visiobot_core/urdf/visiobot.urdf.xacro` | Robot description (links, joints, sensors, Gazebo plugins) |
| `src/visiobot_core/launch/sim.launch.py` | Full simulation launch (Gazebo + bridge + SLAM) |
| `src/visiobot_core/launch/display.launch.py` | URDF-only RViz visualization |
| `src/visiobot_core/launch/bringup.launch.py` | Real-robot hardware bringup |
| `src/visiobot_core/config/slam_toolbox_params.yaml` | SLAM Toolbox tuning parameters |
| `src/visiobot_core/config/visiobot_params.yaml` | Telemetry node parameters |
| `gazebo/visiobot_room.sdf` | Simulation world (room with walls and obstacles) |
| `gazebo/visiobot_v1.sdf` | Minimal flat-ground world (available for manual use) |

---

## Day 14: Autonomous Navigation (Nav2)

This section covers running the full Nav2 navigation stack on visiobot inside the Gazebo simulation.

### Prerequisites

Build the workspace after the Day 14 changes:

bash
cd ~/visiobot
colcon build --symlink-install
source install/setup.bash
+
### Terminal 1 — Start the Simulation

Launch Gazebo with the robot, sensor bridges, and `robot_state_publisher`:

bash
ros2 launch visiobot_core sim.launch.py
+
Wait until you see Gazebo open and the robot appear in the scene before proceeding.

### Terminal 2 — Start the Nav2 Stack

In a new terminal (source the workspace first):

bash
source ~/visiobot/install/setup.bash
ros2 launch visiobot_core nav_bringup.launch.py
+
This brings up AMCL, the global and local costmap servers, the planner server, the controller server, and the behavior tree navigator. All nodes use `use_sim_time:=True` so they stay in sync with the Gazebo clock.

> **Note:** `nav_bringup.launch.py` requires a pre-built map. Pass the path to your map file as a launch argument:
> bash
> ros2 launch visiobot_core nav_bringup.launch.py map:=/path/to/your/map.yaml
> +> If you do not yet have a map, run SLAM Toolbox first (`slam.launch.py`) to build one, save it with `ros2 run nav2_map_server map_saver_cli -f ~/my_map`, then relaunch with the saved map.

### Terminal 3 (optional) — Open RViz2

bash
source ~/visiobot/install/setup.bash
ros2 launch visiobot_core rviz_sim.launch.py
+
This is a dedicated RViz-only launch — it does not start `robot_state_publisher` or `joint_state_publisher`, and it loads the `visiobot_sim.rviz` config automatically. Add the following displays in RViz2 if they are not already present:
- **Map** — topic `/map`
- **LaserScan** — topic `/scan`
- **Path** — topic `/plan` (global path)
- **Path** — topic `/local_plan` (local path)
- **Costmap** — topic `/global_costmap/costmap`
- **Costmap** — topic `/local_costmap/costmap`

Set the **Fixed Frame** to `map`.

### Setting the Initial Pose

AMCL does not know where the robot is until you tell it. In RViz2:

1. Click the **"2D Pose Estimate"** button in the toolbar (or press **P**).
2. Click on the map at the robot's actual starting position.
3. Hold and drag in the direction the robot is facing, then release.

AMCL will initialise its particle filter around that estimate. You should see the laser scan align with the map walls within a few seconds. If the scan does not align, repeat the pose estimate closer to the true position.

### Sending a Navigation Goal

Once the initial pose is set and the costmaps have loaded:

1. Click the **"2D Goal Pose"** button in the toolbar (or press **G**).
2. Click on the map at the desired destination.
3. Hold and drag to set the goal heading, then release.

Nav2 will compute a global path, then drive the robot along it using the local controller. The robot stops when it reaches the goal or if it cannot find a valid path.

### Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `map` frame missing in RViz | AMCL not yet localised | Set a 2D Pose Estimate first |
| Robot does not move after goal | Nav2 lifecycle nodes not active | Check `ros2 lifecycle list /bt_navigator` |
| Laser scan does not match map | Wrong initial pose | Re-set the 2D Pose Estimate |
| `use_sim_time` warnings | Node launched without sim time | Ensure `use_sim_time:=True` is passed |
| Goals immediately rejected | No map loaded | Pass `map:=<path>` to `nav_bringup.launch.py` |

---

## Day 14 Troubleshooting

### `collision_monitor` and `opennav_docking` strict parameter parsing quirks

**Symptom:** The `collision_monitor` or `opennav_docking` nodes may crash at startup with exceptions such as `InvalidParameterTypeException`, or warnings about uninitialized/deprecated parameters.
For `collision_monitor`, the logs may indicate:
1. "Numbers at depth other than 2"
2. "max_points parameter was deprecated"
3. "polygon_sub_topic is not initialized"

**Cause:** In ROS 2 Jazzy, parameter parsing for Nav2 components is much stricter.

**Fix for `collision_monitor` (`PolygonStop`):**

1. The `points` string must be a 2D array of coordinate pairs (e.g., `"[[x, y], [x, y]]"`), rather than a flat 1D array.
2. The `max_points` parameter was deprecated and must be renamed to `min_points`.
3. The `polygon_sub_topic` must be explicitly defined.

```yaml
# WRONG — Causes parsing issues and warnings in Jazzy
PolygonStop:
  type: "polygon"
  points: "[0.3, 0.3, 0.3, -0.3, -0.3, -0.3, -0.3, 0.3]"
  action_type: "stop"
  max_points: 4
  visualize: True
  polygon_pub_topic: "polygon_stop"

# CORRECT — 2D array points string, min_points, and polygon_sub_topic defined
PolygonStop:
  type: "polygon"
  points: "[[0.3, 0.3], [0.3, -0.3], [-0.3, -0.3], [-0.3, 0.3]]"
  action_type: "stop"
  min_points: 4
  visualize: True
  polygon_pub_topic: "polygon_stop"
  polygon_sub_topic: "polygon_stop_sub"
```

**References:**
- [Nav2 Collision Monitor Package](https://docs.ros.org/en/jazzy/p/nav2_collision_monitor/)
- [Using Collision Monitor Tutorial](https://docs.nav2.org/tutorials/docs/using_collision_monitor.html)

These strict type enforcements apply to other similar plugins (like `opennav_docking`). Always verify parameter definitions in the official documentation if a node crashes before fully starting.

---

## Reference Library Integration

The `tutorials/` directory contains reference code from MOGI-ROS (Gazebo basics, sensors, navigation, cognitive robotics) and Automatic Addison's Nav2 setups (`yahboom_rosmaster`). 

Based on these reference repositories, the following major architectural upgrades were applied to VisioBot today:

1. **Gazebo Harmonic Sensor Upgrades (MOGI-ROS)**:
   - Added Gaussian noise models (`<noise>`) to the `gpu_lidar` and `camera` sensor plugins in the URDF for more realistic simulation.
   - Standardized the camera `<camera_info_topic>` and aligned the `<gz_frame_id>` structure to Gazebo Harmonic best practices.

2. **Nav2 Parameter Optimization (Automatic Addison)**:
   - Replaced the string-based `PolygonStop` with a dynamic `FootprintApproach` for the `collision_monitor` to ensure perfect formatting and safe dynamic collision avoidance in ROS 2 Jazzy.
   - Added a `denoise_layer` to the `local_costmap` to improve short-range path planning robustness against sensor noise.
   - Optimized `inflation_layer` parameters in both costmaps (`cost_scaling_factor: 2.58`, `inflation_radius: 1.75`) to encourage smoother trajectories and safer obstacle clearance.

---

## Phase 2: Vision + Control

### Day 16: CvBridge Integration

This section introduces `visiobot_vision`, a new package for handling computer vision pipelines on VisioBot using OpenCV and `cv_bridge`.

#### The `camera_processor` Node

We have added a new node that performs basic image processing on the raw camera feed:

1. Subscribes to the high-performance Gazebo image bridge at `/camera/image_raw`.
2. Uses `cv_bridge` to convert the ROS `sensor_msgs/Image` to an OpenCV image matrix (`bgr8`).
3. Converts the image to grayscale, then back to BGR (so color overlays can be applied).
4. Draws a bright green targeting circle in the center of the frame.
5. Uses `cv_bridge` to convert the OpenCV image back into a ROS message.
6. Publishes the result to `/camera/image_processed`.

#### Running the Vision Pipeline

1. **Build the workspace**

```bash
cd ~/visiobot
colcon build --symlink-install --packages-select visiobot_vision
source install/setup.bash
```

2. **Launch the Simulation**

In terminal 1:
```bash
ros2 launch visiobot_core sim.launch.py
```

3. **Start the Camera Processor Node**

In terminal 2 (source the workspace first):
```bash
ros2 run visiobot_vision camera_processor
```

4. **Verify the Processed Image**

You can inspect the resulting image using RViz2 or `rqt_image_view`.

In terminal 3:
```bash
ros2 run rqt_image_view rqt_image_view
```
Select `/camera/image_processed` from the dropdown menu in rqt_image_view to see the greyscale image with the green targeting circle.

### Day 17: OpenCV Preprocessing

We have upgraded the `camera_processor` node to include standard OpenCV preprocessing techniques and FPS tracking. The node now passes the raw image through a series of stages:

1. **Resize (`apply_resize`)**: Scales the image down to improve processing performance.
2. **Blur (`apply_blur`)**: Applies Gaussian blur to reduce high-frequency noise.
3. **Color Conversion (`apply_color_conversion`)**: Converts the image from BGR to HSV color space.
4. **Thresholding (`apply_threshold`)**: Creates a binary mask isolating specific color ranges or brightness.

#### Debug Topics

To help track the vision pipeline and measure performance, the resulting images from each stage are exposed on separate ROS topics. You can inspect these using `rqt_image_view` or RViz2:

- `/camera/debug/resized`: The scaled-down BGR image.
- `/camera/debug/blurred`: The image after Gaussian blur is applied.
- `/camera/debug/threshold`: The binary mask created from the thresholding stage.
- `/camera/image_processed`: The final output frame with any overlays (like the targeting circle).

Additionally, an FPS counter measures the time elapsed between frames and logs the performance directly to the terminal.

### Day 18: YOLOv8 Detection Node

We have integrated Ultralytics YOLOv8 into the vision pipeline for real-time semantic object detection.

#### Dependencies
To run the YOLO node, ensure you have the `ultralytics` package installed with the correct numpy version for ROS 2 Jazzy:
```bash
pip install ultralytics "numpy<2"
```

#### The `yolo_detector` Node
This new node performs the following tasks:
1. Subscribes to `/camera/image_raw` using `cv_bridge`.
2. Runs `yolov8n.pt` on the incoming frames to extract bounding boxes, classes, and confidence scores.
3. Annotates the frame with the detection results.
4. Republishes the annotated image to `/camera/yolo/debug_image`.
5. Logs all detections to the terminal output.

#### Running the YOLO Pipeline

1. **Build the workspace**
```bash
cd ~/visiobot
colcon build --symlink-install --packages-select visiobot_vision
source install/setup.bash
```

2. **Launch the COCO Simulation**
In terminal 1:
```bash
ros2 launch visiobot_core sim_coco.launch.py
```

3. **Start the YOLO Detector Node**
In terminal 2 (source the workspace first):
```bash
ros2 run visiobot_vision yolo_detector
```

4. **Verify the Processed Image**
In terminal 3:
```bash
ros2 run rqt_image_view rqt_image_view
```
Select `/camera/yolo/debug_image` from the dropdown menu to see the real-time YOLOv8 bounding boxes.

### Day 19: Detection Messages and Overlays

We have decoupled the YOLO vision pipeline into a standard data-publisher and a separate image-overlay visualizer using industry-standard `vision_msgs`.

#### The `yolo_detector` Node (Data Only)
This node now runs YOLOv8 and only publishes clean data:
- Subscribes to `/camera/image_raw`.
- Runs inference.
- Converts the bounding boxes, classes, and confidences into `vision_msgs/Detection2DArray` messages.
- Publishes data to `/yolo/detections` without rendering any images itself.

#### The `image_overlay_node` (Visualization)
This new node synchronizes the image and data streams to render the bounding boxes:
- Uses `message_filters.ApproximateTimeSynchronizer` to sync `/camera/image_raw` and `/yolo/detections`.
- Decodes the `Detection2DArray` message and uses standard `cv2.rectangle` to draw bounding boxes and class names onto the frames.
- Publishes the final annotated image to `/camera/yolo/overlay_image`.

#### Running the Decoupled Pipeline

1. **Build the workspace**
```bash
cd ~/visiobot
colcon build --symlink-install --packages-select visiobot_vision
source install/setup.bash
```

2. **Launch the COCO Simulation**
In terminal 1:
```bash
ros2 launch visiobot_core sim_coco.launch.py
```

3. **Start the YOLO Detector (Data)**
In terminal 2 (source the workspace first):
```bash
ros2 run visiobot_vision yolo_detector
```

4. **Start the Image Overlay (Visualization)**
In terminal 3 (source the workspace first):
```bash
ros2 run visiobot_vision image_overlay_node
```

5. **Verify the Processed Image**
In terminal 4:
```bash
ros2 run rqt_image_view rqt_image_view
```
Select `/camera/yolo/overlay_image` from the dropdown menu to see the real-time YOLOv8 bounding boxes generated by the overlay node.

### Day 20: SORT Object Tracking

We have upgraded our YOLO pipeline to perform object tracking, giving VisioBot temporal memory across frames!

By changing `model.predict()` to `model.track(persist=True, tracker='botsort.yaml')`, YOLOv8 now maintains persistent tracking IDs for each unique object it detects. This prevents the robot from confusing two different people or losing track of a target if it is briefly occluded.

#### The `yolo_detector` Node Update
The node now extracts the tracking ID from the YOLO results (`result.boxes.id`) and prepends it to the `class_id` string inside our `vision_msgs/Detection2DArray` messages.
For example, if the model locks onto a person, it will now publish the `class_id` as `person_1` instead of just `person`.

#### Visualizing the Tracking
Because we decoupled the data and overlay in Day 19, the `image_overlay_node` will automatically draw these new labels without needing any code changes!

1. Build your workspace and source it:
```bash
colcon build --symlink-install --packages-select visiobot_vision
source install/setup.bash
```
2. Launch the COCO environment and nodes exactly as described in Day 19.
3. Open `rqt_image_view` to the `/camera/yolo/overlay_image` topic.

You will now see bounding boxes cleanly labeled with persistent tracking IDs like `person_1: 0.85`!
