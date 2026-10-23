This daily 60-day roadmap provides a structured schedule for the **Leapfrog Technology 60 Days of Learning Challenge 2026 (LSPP2026)**. The curriculum progresses through four cumulative phases, culminating in the integration of the **VisioBot** autonomous docking platform.

---

## Phase 1: ROS2 Foundations and Simulation (Days 1–15)

The objective of this phase is to establish a solid simulation foundation using **ROS2 Jazzy Jalisco**, **Gazebo Harmonic**, and **RViz2** on **Ubuntu 24.04 LTS**.

### Day 1: ROS2 Jazzy Installation on Ubuntu 24.04 LTS

* **Objective**: Configure locales and install the ROS2 desktop package.
* **Technical Tasks**:
1. Verify system locales support UTF-8 .
2. Configure `/etc/apt/sources.list.d/ubuntu.sources` to include `noble-updates` and `noble-backports` .
3. Run `sudo apt install ros-jazzy-desktop` .


* **Primary Resource**:([https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html](https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html)) .
* **YouTube Support**:([https://www.youtube.com/watch?v=Se5pvRlTX8s](https://www.youtube.com/watch?v=Se5pvRlTX8s))  - Complete environment installation and verification guide.



### Day 2: ROS2 Workspaces, Colcon, and Package Structures

* **Objective**: Build a clean directory structure using the Colcon compilation system.
* **Technical Tasks**:
1. Create `~/visiobot_ws/src`.


2. Execute `colcon build --symlink-install` from the workspace root .
3. Create a custom Python package with `rclpy` dependencies.




* **Primary Resource**:([https://docs.ros.org/en/jazzy/Installation/Alternatives/Ubuntu-Development-Setup.html](https://docs.ros.org/en/jazzy/Installation/Alternatives/Ubuntu-Development-Setup.html)) .

### Day 3: Client Library (rclpy): Writing a Telemetry Publisher Node

* **Objective**: Write a basic telemetry publisher node in Python using `rclpy`.


* **Technical Tasks**:
1. Initialize a node instance in a custom Python file.


2. Write a high-rate timer callback publishing string metadata.


3. Configure `setup.py` entry points.




* **Primary Resource**:([https://docs.ros.org/en/jazzy/Tutorials.html](https://docs.ros.org/en/jazzy/Tutorials.html)).


* **YouTube Support**:([https://www.youtube.com/watch?v=Se5pvRlTX8s](https://www.youtube.com/watch?v=Se5pvRlTX8s))  - Deep dive into Python nodes and topic creation.



### Day 4: Creating a ROS2 Subscriber Node and Diagnostic Logging

* **Objective**: Write a Python node to subscribe to data topics and log output in the console.
* **Technical Tasks**:
1. Implement a subscription callback for target topics.


2. Test concurrent execution of the publisher and subscriber using separate terminals.


3. Inspect active topic structures using `ros2 topic info`.




* **Primary Resource**:([https://docs.ros.org/en/jazzy/Tutorials.html](https://docs.ros.org/en/jazzy/Tutorials.html)).


* **YouTube Support**:([https://www.youtube.com/watch?v=Se5pvRlTX8s](https://www.youtube.com/watch?v=Se5pvRlTX8s))  - Verification of subscriptions and message flow.



### Day 5: Defining Custom Interfaces (Messages and Services)

* **Objective**: Write custom `.msg` files representing VisioBot state parameters.
* **Technical Tasks**:
1. Create a subdirectory named `msg` inside a custom package.


2. Define custom coordinates using basic field types .
3. Configure `CMakeLists.txt` with `rosidl_generate_interfaces` and compile the package.




* **Primary Resource**:([https://docs.ros.org/en/jazzy/Tutorials.html](https://docs.ros.org/en/jazzy/Tutorials.html)).



### Day 6: Coordinate Frames and the $tf2$ Transform Tree

* **Objective**: Publish and listen to coordinate transformations in RViz2.
* **Technical Tasks**:
1. Understand the parent-child relationships within coordinate transforms.


2. Publish static transforms using `tf2_ros` .
3. Inspect coordinate alignment using `ros2 run rqt_tf_tree rqt_tf_tree`.




* **Primary Resource**:([https://docs.ros.org/en/jazzy/Tutorials.html](https://docs.ros.org/en/jazzy/Tutorials.html)).



### Day 7: URDF Kinematic Modeling: Links, Joints, and Visual Meshes

* **Objective**: Draft the kinematic tree of the VisioBot differential chassis.


* **Technical Tasks**:
1. Define a visual chassis using primitive shapes.
2. Configure wheel joints and assign coordinates.
3. Launch and verify joint transforms in RViz2.




* **Primary Resource**:([https://github.com/MOGI-ROS/Week-3-4-Gazebo-basics](https://github.com/MOGI-ROS/Week-3-4-Gazebo-basics)).

### Day 8: Collision, Inertial Matrices, and Xacro Macros

* **Objective**: Add collision geometry and inertial parameters to the URDF model.
* **Technical Tasks**:
1. Write a Xacro macro to compute cylinder and box inertia.
2. Assign collision parameters to each link.
3. Compile Xacro into a raw URDF file.




* **Primary Resource**:([https://github.com/MOGI-ROS/Week-3-4-Gazebo-basics](https://github.com/MOGI-ROS/Week-3-4-Gazebo-basics)).

### Day 9: Gazebo Harmonic Installation and Standalone Simulation

* **Objective**: Install Gazebo Harmonic on Ubuntu Noble and run a standalone simulation environment.


* **Technical Tasks**:
1. Verify the default installation package using `sudo apt install ros-jazzy-ros-gz`.


2. Run `gz sim` to verify standalone graphics performance.


3. Explore the standard shapes world interface.


* **Primary Resource**:([https://gazebosim.org/docs/harmonic/tutorials/](https://gazebosim.org/docs/harmonic/tutorials/)).



### Day 10: Bidirectional Bridge: Configuring the `ros_gz_bridge`

* **Objective**: Map communication between Gazebo internal topics and ROS2 topics .
* **Technical Tasks**:
1. Run the parameter bridge command for Twist commands:
```bash
ros2 run ros_gz_bridge parameter_bridge /model/visiobot/cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist

```


2. Verify topic directions (`GZ_TO_ROS` or `ROS_TO_GZ`) .


* **Primary Resource**:([https://github.com/gazebosim/ros_gz](https://github.com/gazebosim/ros_gz)) .

### Day 11: Spawning URDF in Gazebo and Command Remapping

* **Objective**: Spawn the custom VisioBot model into Gazebo and control it with a keyboard node.
* **Technical Tasks**:
1. Write a launch file utilizing the `spawn_entity.py` node.


2. Remap Gazebo internal topics to custom namespaces .
3. Drive the spawned model using the keyboard.


* **Primary Resource**: [ros_gz Integration Guides](https://gazebosim.org/docs/latest/ros2_integration/) .

### Day 12: Diff-Drive Control Setup via `ros2_control`

* **Objective**: Configure a differential-drive velocity controller in ROS2.
* **Technical Tasks**:
1. Define `ros2_control` parameters in a `.yaml` config file.


2. Launch the controller manager with joint state publishers.


3. Drive the simulated robot by publishing to the `/cmd_vel` topic .


* **Primary Resource**:([https://github.com/rlxai/rbot](https://github.com/rlxai/rbot)).

### Day 13: 2D Lidar Integration and SLAM Toolbox Mapping

* **Objective**: Mount a 2D Lidar in the URDF and generate a map of a simulated world.
* **Technical Tasks**:
1. Verify LaserScan publications on the `/scan` topic.
2. Run SLAM Toolbox in asynchronous mapping mode.
3. Drive the robot to map a simulated room.


* **Primary Resource**:([https://github.com/SteveMacenski/slam_toolbox](https://github.com/SteveMacenski/slam_toolbox)).


* **YouTube Support**:([https://www.youtube.com/watch?v=0G6LDuslqmA](https://www.youtube.com/watch?v=0G6LDuslqmA))  - Detailed guide on parameters and map serialization.



### Day 14: Navigation2 (Nav2) Stack Setup and Global Planner Selection

* **Objective**: Configure costmaps and global planning engines in Nav2.
* **Technical Tasks**:
1. Install Nav2 using `sudo apt install ros-jazzy-navigation2` .
2. Configure costmap inflation and obstacle layers.
3. Launch the navigation server with default map parameters.


* **Primary Resource**:([https://docs.nav2.org/getting_started/index.html](https://docs.nav2.org/getting_started/index.html)) .
* **YouTube Support**:([https://www.youtube.com/watch?v=NkOX4zX9XbQ](https://www.youtube.com/watch?v=NkOX4zX9XbQ))  - High-quality walkthrough of Nav2 deployment.



### Day 15: Autonomy Validation and Map Serialization

* **Objective**: Implement autonomous path planning and save the mapped occupancy grid.


* **Technical Tasks**:
1. Send a target coordinate in RViz2 using the "Nav2 Goal" button.
2. Verify dynamic obstacle avoidance.


3. Save the map as `.pgm` and `.yaml` files.


* **Primary Resource**:([https://github.com/SteveMacenski/slam_toolbox](https://github.com/SteveMacenski/slam_toolbox)).


* **YouTube Support**:([https://www.youtube.com/watch?v=NkOX4zX9XbQ](https://www.youtube.com/watch?v=NkOX4zX9XbQ))  - Validation of autonomous navigation.



---

## Phase 2: Computer Vision for Robotics (Days 16–30)

This phase focuses on camera integration, image transformation pipelines, fiducial marker tracking, and semantic deep-learning inference.

### Day 16: Adding Simulated RGB Camera to URDF

* **Objective**: Add a virtual camera link to the URDF and map Gazebo image streams.
* **Technical Tasks**:
1. Define a camera sensor block in the URDF Xacro file.


2. Add a Gazebo sensor plugin publishing raw images.
3. Verify the publication of the `/camera/image_raw` topic .


* **Primary Resource**: [linorobot2 Jazzy Properties Configurations](https://github.com/linorobot/linorobot2/tree/jazzy).



### Day 17: ROS2 Image Topics and `cv_bridge` Conversion

* **Objective**: Stream RGB data and convert raw image packets into OpenCV Matrices.


* **Technical Tasks**:
1. Create a subscriber to monitor incoming image topics.


2. Import `CvBridge` in a custom Python node.


3. Convert the `sensor_msgs/msg/Image` type to a standard BGR image array.




* **Primary Resource**:([https://index.ros.org/p/cv_bridge/](https://index.ros.org/p/cv_bridge/)).


* **YouTube Support**:([https://www.youtube.com/watch?v=WhkiPYPIO9M](https://www.youtube.com/watch?v=WhkiPYPIO9M))  - Complete image publishing and subscription walkthrough.

### Day 18: Processing Image Streams via Custom OpenCV Python Nodes

* **Objective**: Implement real-time color segmentation and contour filtering on camera streams.
* **Technical Tasks**:
1. Write a callback function to process incoming camera frames.


2. Apply threshold segmentation in the HSV color space.


3. Republish the annotated image back to the ROS2 graph.




* **Primary Resource**:([https://automaticaddison.com/getting-started-with-opencv-in-ros-2-foxy-fitzroy-python/](https://automaticaddison.com/getting-started-with-opencv-in-ros-2-foxy-fitzroy-python/)).


* **YouTube Support**:([https://www.youtube.com/watch?v=WhkiPYPIO9M](https://www.youtube.com/watch?v=WhkiPYPIO9M))  - In-depth validation of processed image republishing.

### Day 19: Camera Intrinsics and Spatial Rectification

* **Objective**: Calibrate camera matrices and configure camera metadata nodes.
* **Technical Tasks**:
1. Generate and save a camera matrix and distortion vector.


2. Configure camera information publishers .
3. Map raw image frames to rectify lens distortion .


* **Primary Resource**:([https://github.com/lagadic/vision_visp](https://github.com/lagadic/vision_visp)).



### Day 20: ArUco Marker Generation and Sim Spawn

* **Objective**: Generate ArUco markers and place them as target docking pads in Gazebo.


* **Technical Tasks**:
1. Generate a standard `6x6_250` ArUco marker.


2. Create a simulated visual board in Gazebo containing the marker.
3. Add the visual board near the simulated docking zone.




* **Primary Resource**:([https://github.com/JMU-ROBOTICS-VIVA/ros2_aruco](https://github.com/JMU-ROBOTICS-VIVA/ros2_aruco)) .

### Day 21: Real-Time ArUco Identification and Pose Broadcast

* **Objective**: Detect fiducials, compute rotation vectors, and publish coordinates to $tf2$.


* **Technical Tasks**:
1. Detect ArUco markers in the raw image stream using OpenCV .
2. Compute translation and rotation matrices relative to the camera frame .
3. Broadcast computed transforms to the active coordinate tree.




* **Primary Resource**:([https://github.com/JMU-ROBOTICS-VIVA/ros2_aruco](https://github.com/JMU-ROBOTICS-VIVA/ros2_aruco)) .

### Day 22: Deep Learning Integration: Setting up YOLOv8

* **Objective**: Configure the Python virtual environment and run YOLOv8 object detection on ROS2 image streams.


* **Technical Tasks**:
1. Create an isolated virtual environment.


2. Install Ultralytics dependencies.


3. Run a basic Python detection script using a pre-trained model.




* **Primary Resource**:([https://ibrahimmansur4.medium.com/integrating-opencv-with-ros2-a-comprehensive-guide-to-computer-vision-in-robotics-9b47c4569e57](https://ibrahimmansur4.medium.com/integrating-opencv-with-ros2-a-comprehensive-guide-to-computer-vision-in-robotics-9b47c4569e57)).



### Day 23: Exporting YOLOv8 Models to ONNX Format

* **Objective**: Convert PyTorch weights into the standardized ONNX format.


* **Technical Tasks**:
1. Load the pre-trained weights in Python.


2. Export the model using the command:
```bash
yolo export model=yolov8s.pt format=onnx simplify=True dynamic=False

```


3. Verify the input and output node shapes .


* **Primary Resource**:([https://nvidia-isaac-ros.github.io/repositories_and_packages/isaac_ros_object_detection/isaac_ros_yolov8/index.html](https://nvidia-isaac-ros.github.io/repositories_and_packages/isaac_ros_object_detection/isaac_ros_yolov8/index.html)).



### Day 24: High-Performance ONNX Runtime Inference in ROS2

* **Objective**: Build a custom decoupled ROS2 node utilizing ONNX Runtime for low-latency inference.


* **Technical Tasks**:
1. Initialize an ONNX Runtime inference session.


2. Write preprocessing pipelines using NumPy arrays.


3. Publish detected bounding boxes on custom topics .


* **Primary Resource**:([https://github.com/yacin-hamdi/yolo-raspberrypi](https://github.com/yacin-hamdi/yolo-raspberrypi)).



### Day 25: 3D Projection: Transforming Pixels to Spatial Coordinates

* **Objective**: Map 2D pixel centroids to 3D Cartesian coordinates using depth camera feeds.


* **Technical Tasks**:
1. Synchronize RGB and depth topics using `ApproximateTimeSynchronizer` .
2. Extract depth values at the center pixel of the 2D bounding box .
3. Compute 3D position vectors relative to the camera frame.




* **Primary Resource**:([https://robocloud-dashboard.vercel.app/learn/blog/yolov8-ros2-custom-messages](https://robocloud-dashboard.vercel.app/learn/blog/yolov8-ros2-custom-messages)) .

### Day 26: RGBD Camera URDF Configuration

* **Objective**: Mount an RGBD camera in the URDF and map Gazebo output topics.


* **Technical Tasks**:
1. Define an RGBD sensor block in the URDF Xacro.


2. Configure point cloud generation via `ros_gz_point_cloud` plugins .
3. Verify point cloud data generation.


* **Primary Resource**: [linorobot2 Properties Configurations](https://github.com/linorobot/linorobot2/tree/jazzy).



### Day 27: Point Cloud Processing and NaN Filtering

* **Objective**: Convert depth images into point cloud data.


* **Technical Tasks**:
1. Subscribe to raw depth images and camera information topics.


2. Initialize a point cloud converter node.


3. Filter out invalid depth and NaN values .


* **Primary Resource**:([https://index.ros.org/p/depth_image_proc/](https://index.ros.org/p/depth_image_proc/)) .

### Day 28: Coordinate Transform Alignment ($tf2$ REP-103 standards)

* **Objective**: Resolve coordinate frame misalignments between physical links and visual optical frames.


* **Technical Tasks**:
1. Align the physical chassis frame (Z-axis up) with the camera optical frame (Z-axis forward) .
2. Publish static transforms using `static_transform_publisher` .
3. Verify spatial alignment in RViz2 .


* **Primary Resource**:([https://robotics.stackexchange.com/questions/114231/pointcloud-visualization-issue-with-pointcloudxyz-node-in-depth-image-proc-packa](https://robotics.stackexchange.com/questions/114231/pointcloud-visualization-issue-with-pointcloudxyz-node-in-depth-image-proc-packa)) .

### Day 29: Image-Based Visual Servoing (IBVS) Controller Formulation

* **Objective**: Formulate the image Jacobian matrix mapping pixel errors to physical velocities.


* **Technical Tasks**:
1. Define target feature states $s^*$ and current states $s$.


2. Write a Python controller utilizing proportional gain scaling :



$$e = s - s^*$$


$$v_c = -\lambda L_e^{+} e$$


3. Implement a velocity limits safety threshold.




* **Primary Resource**:([https://robocloud-dashboard.vercel.app/learn/blog/visual-servoing](https://robocloud-dashboard.vercel.app/learn/blog/visual-servoing)) .

### Day 30: Target Centering and Closed-Loop Differential Steering

* **Objective**: Combine the visual feedback loop with the simulated drive system.


* **Technical Tasks**:
1. Verify the visual tracking feedback loop in simulation.


2. Calculate errors relative to the image center.


3. Send steering commands to the `/cmd_vel` topic.




* **Primary Resource**:([https://articulatedrobotics.xyz/tutorials/mobile-robot/applications/objtrack/](https://articulatedrobotics.xyz/tutorials/mobile-robot/applications/objtrack/)).



---

## Phase 3: Edge AI and Embedded Intelligence (Days 31–45)

This phase shifts focus to the physical edge, establishing communication with the **ESP32** via **micro-ROS** and deploying quantized **TinyML** models.

### Day 31: PlatformIO IDE and ESP32 Setup

* **Objective**: Set up PlatformIO and compile a basic firmware for the ESP32.


* **Technical Tasks**:
1. Configure a basic `platformio.ini` environment .
2. Write and compile a basic LED blink script .
3. Flash the firmware to the ESP32 via USB .


* **Primary Resource**: [micro_ros_platformio Configuration](https://github.com/micro-ROS/micro_ros_platformio).
* **YouTube Support**:([https://www.youtube.com/watch?v=tL7swYonY8w](https://www.youtube.com/watch?v=tL7swYonY8w))  - Complete PlatformIO environment setup.

### Day 32: ESP32 Hardware Peripheral Interfacing

* **Objective**: Interface the ESP32 with sensors and actuators using hardware drivers .
* **Technical Tasks**:
1. Implement an I2C communication interface for sensors .
2. Configure PWM signals to simulate actuator control .
3. Verify serial telemetry logging .


* **Primary Resource**:([https://docs.cirkitdesigner.com/component/3b9fd6dd-acf7-4b60-a6b6-812e3a03c2fa/micro-ros-control-board-esp32](https://docs.cirkitdesigner.com/component/3b9fd6dd-acf7-4b60-a6b6-812e3a03c2fa/micro-ros-control-board-esp32)) .

### Day 33: Embedded Concurrency with FreeRTOS

* **Objective**: Build a multi-tasking FreeRTOS firmware to manage timing-critical loops .
* **Technical Tasks**:
1. Implement `xTaskCreate` to handle concurrent tasks .
2. Create separate tasks for sensor reading and motor command execution .
3. Configure task priority to prevent resource conflicts .


* **Primary Resource**:([https://github.com/SEPENGU/mYuMi_micro-ROS/blob/main/ESP32/README.md](https://github.com/SEPENGU/mYuMi_micro-ROS/blob/main/ESP32/README.md)) .
* **YouTube Support**:([https://www.youtube.com/watch?v=tL7swYonY8w](https://www.youtube.com/watch?v=tL7swYonY8w))  - Step-by-step task scheduling on FreeRTOS.

### Day 34: micro-ROS Architecture and Agent Setup

* **Objective**: Install the micro-ROS setup toolchain and build the host agent workspace .
* **Technical Tasks**:
1. Clone `micro_ros_setup` into a dedicated workspace .
2. Create and compile the agent package .
3. Run the agent node to verify DDS bridge connectivity :
```bash
ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyUSB0

```




* **Primary Resource**: [micro_ros_setup GitHub](https://github.com/micro-ROS/micro_ros_setup) .

### Day 35: Flash & Test: Publishing ESP32 Telemetry over micro-ROS

* **Objective**: Flash a micro-ROS publisher to the ESP32 and monitor topics on the host machine .
* **Technical Tasks**:
1. Set up the micro-ROS serial transport layer.
2. Run the host agent and reset the ESP32 .
3. Verify the incoming topic stream using `ros2 topic list` .


* **Primary Resource**:([https://technologiehub.at/project-posts/micro-ros-on-esp32-tutorial/](https://technologiehub.at/project-posts/micro-ros-on-esp32-tutorial/)) .
* **YouTube Support**:([https://www.youtube.com/watch?v=tRtfpnu4LjE](https://www.youtube.com/watch?v=tRtfpnu4LjE))  - Agent launching and client interaction.

### Day 36: Command Subscription: ESP32 Listening to Twist Commands

* **Objective**: Subscribe to velocity commands on the ESP32 and translate inputs to motor signals .
* **Technical Tasks**:
1. Write a subscription callback for `geometry_msgs/msg/Twist` .
2. Initialize the subscription options in the rclc executor .
3. Publish test commands from the host PC using `ros2 topic pub`.




* **Primary Resource**:([https://github.com/DominikN/esp32-microros-husarnet](https://github.com/DominikN/esp32-microros-husarnet)) .

### Day 37: Custom micro-ROS Message Types & Allocators

* **Objective**: Optimize micro-ROS memory allocation and stack size on the ESP32 .
* **Technical Tasks**:
1. Map the default memory allocator to rclc functions .
2. Set custom transport variables to prevent stack overflow .
3. Run memory footprint diagnostics .


* **Primary Resource**:([https://technologiehub.at/project-posts/micro-ros-on-esp32-tutorial/](https://technologiehub.at/project-posts/micro-ros-on-esp32-tutorial/)) .

### Day 38: TinyML Architecture and Core Concepts

* **Objective**: Understand model optimization, quantization, and resource planning for edge hardware.


* **Technical Tasks**:
1. Evaluate constraints: SRAM limits (520KB) vs. Model sizes .
2. Explore INT8 quantization theory .
3. Set up a new project in Edge Impulse Studio.




* **Primary Resource**:([https://docs.edgeimpulse.com/](https://docs.edgeimpulse.com/)) .

### Day 39: Data Acquisition via Mobile and Webcam

* **Objective**: Gather and label image datasets for target detection.


* **Technical Tasks**:
1. Connect your smartphone or webcam to the Edge Impulse project.


2. Capture 50+ images of the target docking pad.


3. Draw bounding boxes and label targets.




* **Primary Resource**:([https://www.makerguides.com/train-an-object-detection-model-with-edge-impulse-for-esp32-cam/](https://www.makerguides.com/train-an-object-detection-model-with-edge-impulse-for-esp32-cam/)).



### Day 40: Training FOMO (Fast Object Detection) Models

* **Objective**: Train a lightweight centroid tracking model in Edge Impulse.


* **Technical Tasks**:
1. Configure processing blocks with raw image parameters .
2. Select FOMO (Fast Object Detection for Microcontrollers).


3. Train the network and evaluate model validation curves .


* **Primary Resource**:([https://www.makerguides.com/train-an-object-detection-model-with-edge-impulse-for-esp32-cam/](https://www.makerguides.com/train-an-object-detection-model-with-edge-impulse-for-esp32-cam/)).



### Day 41: EON Compiler INT8 Optimization

* **Objective**: Use the EON Compiler to optimize model resource usage .
* **Technical Tasks**:
1. Analyze model deployment estimates for RAM and Flash .
2. Enable the EON Compiler optimization pipeline .
3. Verify the estimated latency remains under 30ms .


* **Primary Resource**:([https://docs.edgeimpulse.com/studio/projects/deployment](https://docs.edgeimpulse.com/studio/projects/deployment)) .

### Day 42: Exporting Edge Impulse C++ Code

* **Objective**: Build and download the trained model as an optimized C++ library .
* **Technical Tasks**:
1. Select the "Arduino Library" or "ESP-IDF Component" deployment option .
2. Build and save the compressed library file .
3. Verify the library contents locally .


* **Primary Resource**:([https://docs.edgeimpulse.com/hardware/boards/espressif-esp32](https://docs.edgeimpulse.com/hardware/boards/espressif-esp32)) .

### Day 43: Local FOMO Model Deployment on ESP32-CAM

* **Objective**: Deploy the compiled FOMO model directly to the ESP32-CAM board.


* **Technical Tasks**:
1. Add the downloaded C++ library zip to your workspace.


2. Write firmware to capture frames from the onboard OV2640 sensor .
3. Run local inference and verify real-time centroid detection.




* **Primary Resource**:([https://docs.edgeimpulse.com/hardware/boards/espressif-esp32](https://docs.edgeimpulse.com/hardware/boards/espressif-esp32)) .

### Day 44: Local Telemetry Fusion: Merging FOMO with micro-ROS

* **Objective**: Publish edge AI object coordinates directly to ROS2 topics over micro-ROS.


* **Technical Tasks**:
1. Combine the local FOMO inference code with micro-ROS publisher templates .
2. Publish local centroid coordinates as message packets .
3. Monitor predictions using `ros2 topic echo` on the host PC .


* **Primary Resource**:([https://docs.cirkitdesigner.com/component/3b9fd6dd-acf7-4b60-a6b6-812e3a03c2fa/micro-ros-control-board-esp32](https://docs.cirkitdesigner.com/component/3b9fd6dd-acf7-4b60-a6b6-812e3a03c2fa/micro-ros-control-board-esp32)) .

### Day 45: Phase 3 Verification: Standalone Edge Node Complete Verification

* **Objective**: Test end-to-end edge AI execution and measure connection latency.
* **Technical Tasks**:
1. Run the full edge detection firmware continuously .
2. Log transport connection states and handle network drops .
3. Verify the system operates reliably within memory limits .


* **Primary Resource**:([https://docs.edgeimpulse.com/studio/projects/deployment](https://docs.edgeimpulse.com/studio/projects/deployment)) .

---

## Phase 4: Final Capstone and Portfolio (Days 46–60)

The final phase integrates the system components, profiles performance, and documents the portfolio project.

### Day 4 Capstone Architecture

```
                                 +--------------------------------+
                                 |          Host (ROS2)           |
                                 +--------------------------------+
                                                 |
                       +-------------------------+-------------------------+
                       |                                                   |
                       v                                                   v
        +-----------------------------+                     +-----------------------------+
        |  High-Level Perception      |                     |  Global Navigation (Nav2)   |
        |  - YOLOv8 (ONNX) [19, 11]   |                     |  - Obstacle Avoidance [10]   |
        |  - ArUco Tracking [17]      |                     |  - Path Planning [10]        |
        +-----------------------------+                     +-----------------------------+
                       |                                                   |
                       +-------------------------+-------------------------+
                                                 |
                                                 v
                                 +--------------------------------+
                                 |    Active State Controller     |
                                 |    Image-Based Visual Servoing |
                                 |    (IBVS Control Law) [32]     |
                                 +--------------------------------+
                                                 |
                                                 v
                                 +--------------------------------+
                                 |  Actuator Velocity commands    |
                                 |  (/cmd_vel Topic) [18]         |
                                 +--------------------------------+
                                                 |
                                                 v
                                 +--------------------------------+
                                 |        Gazebo Simulation       |
                                 |        (VisioBot physics)      |
                                 +--------------------------------+
                                                 ^
                                                 | Telemetry over serial
                                 +--------------------------------+
                                 |     Physical ESP32 Edge Node   |
                                 |     (micro-ROS Client) [34]     |
                                 +--------------------------------+

```

### Day 46: Designing VisioBot System Topology

* **Objective**: Document coordinates, topic pathways, and system architecture.


* **Technical Tasks**:
1. Map visual topics and coordinate transformation pipelines.
2. Define ROS2 node interactions and publisher-subscriber paths.


3. Create system design block diagrams.


* **Primary Resource**:([https://www.theconstruct.ai/the-best-way-to-create-your-robotics-portfolio/](https://www.theconstruct.ai/the-best-way-to-create-your-robotics-portfolio/)).



### Day 47: Refactoring Package Configuration Files

* **Objective**: Clean up and optimize package configuration files across the workspace.
* **Technical Tasks**:
1. Configure compiler arguments in `CMakeLists.txt` .
2. Verify dependency declarations in `package.xml`.


3. Ensure modularity and maintainability of package components.




* **Primary Resource**:([https://github.com/MOGI-ROS/Week-7-8-ROS2-Navigation](https://github.com/MOGI-ROS/Week-7-8-ROS2-Navigation)).



### Day 48: ROS2 Node Multi-Threading and Executor Tuning

* **Objective**: Implement multi-threaded executors to resolve latency issues on the host PC .
* **Technical Tasks**:
1. Convert single-threaded executors to `MultiThreadedExecutor`.


2. Assign callbacks to mutually exclusive callback groups .
3. Verify the publisher and subscriber timing states .


* **Primary Resource**:([https://thenewtoncapstone.github.io/blog/posts/issues-with-microros/](https://thenewtoncapstone.github.io/blog/posts/issues-with-microros/)) .

### Day 49: Programming the VisioBot High-Level State Machine

* **Objective**: Implement state machine transitions from global Nav2 to active visual docking.
* **Technical Tasks**:
1. Implement a target detection listener node .
2. Write transitions to switch command velocity topics when a target is detected.


3. Configure automated recovery states.




* **Primary Resource**:([https://robocloud-dashboard.vercel.app/learn/blog/visual-servoing](https://robocloud-dashboard.vercel.app/learn/blog/visual-servoing)) .

### Day 50: Refining Nav2 & SLAM Configurations

* **Objective**: Tune costmaps and SLAM parameters in the simulated environment.


* **Technical Tasks**:
1. Adjust Lidar scanning filters to reduce noise.


2. Tune Nav2 obstacle layer parameters.
3. Test autonomous path planning in Gazebo.




* **Primary Resource**:([https://dilipkumar.medium.com/slam-simultaneous-localization-and-mapping-the-core-of-robotic-autonomy-582048002e64](https://dilipkumar.medium.com/slam-simultaneous-localization-and-mapping-the-core-of-robotic-autonomy-582048002e64)).

### Day 51: Tuning the Proportional Gain in the Jacobian Loop

* **Objective**: Stabilize the visual servoing control loop by adjusting proportional gains.


* **Technical Tasks**:
1. Measure positional errors relative to the target pose .
2. Tune controller gains to prevent overshoot during alignment .
3. Define safe velocity limits to ensure stable execution.




* **Primary Resource**:([https://robocloud-dashboard.vercel.app/learn/blog/visual-servoing](https://robocloud-dashboard.vercel.app/learn/blog/visual-servoing)) .

### Day 52: Hardware-in-the-Loop Simulation Integration

* **Objective**: Connect physical ESP32 sensor telemetry to the simulated Gazebo robot.


* **Technical Tasks**:
1. Bridge raw serial topics from the ESP32 to the host agent .
2. Map incoming hardware signals to Gazebo joint states .
3. Verify bidirectional communication stability .


* **Primary Resource**:([https://github.com/micro-ROS/micro_ros_platformio](https://github.com/micro-ROS/micro_ros_platformio)).

### Day 53: Comprehensive Profiling of Host and Edge Devices

* **Objective**: Profile resource usage on both the host computer and the ESP32.
* **Technical Tasks**:
1. Monitor CPU usage on the host PC using `htop`.
2. Measure neural network inference times under ONNX Runtime.


3. Analyze RAM usage and heap constraints on the ESP32 .


* **Primary Resource**:([https://onnxruntime.ai/docs/](https://onnxruntime.ai/docs/)).



### Day 54: Implementing Safe Failsafes and Dynamic Recovery Layer

* **Objective**: Write failsafe logic to handle target loss or collision risks.


* **Technical Tasks**:
1. Implement an automatic search sweep routine when targets are lost .
2. Configure collision limits within `nav2_collision_monitor`.
3. Verify recovery behaviors in simulation.




* **Primary Resource**:([https://github.com/lagadic/vision_visp](https://github.com/lagadic/vision_visp)).



### Day 55: VisioBot Complete Autonomy Loop Execution

* **Objective**: Validate the complete waypoint navigation, target detection, and visual docking routine.
* **Technical Tasks**:
1. Launch the integrated system using a master launch file.
2. Run Nav2 path planning to reach the docking area .
3. Execute visual servoing to align and complete the docking sequence .


* **Primary Resource**:([https://github.com/SteveMacenski/slam_toolbox](https://github.com/SteveMacenski/slam_toolbox)).



### Day 56: Workspace Cleanup and GitHub Structuring

* **Objective**: Organize the repository structure and remove temporary build artifacts.


* **Technical Tasks**:
1. Clean compiled files using `colcon clean`.


2. Organize code into clear subfolders (`ros2_ws`, `vision_src`, `esp32_firmware`).


3. Configure `.gitignore` files to exclude build caches.




* **Primary Resource**:([https://www.digikey.com/en/maker/tutorials/2025/github-for-robotics-organizing-your-first-project](https://www.digikey.com/en/maker/tutorials/2025/github-for-robotics-organizing-your-first-project)).



### Day 57: Video Demonstration Capture

* **Objective**: Capture and edit a video demonstrating VisioBot's autonomous operation.


* **Technical Tasks**:
1. Record autonomous navigation runs in Gazebo and RViz.


2. Create a split-screen video showing simulation states on the left and topic visualizations on the right.


3. Keep the video under 60 seconds and focus on key autonomous milestones.




* **Primary Resource**:([https://roboticsjobs.co.uk/career-advice/portfolio-projects-that-get-you-hired-for-robotics-jobs-with-real-github-examples-](https://roboticsjobs.co.uk/career-advice/portfolio-projects-that-get-you-hired-for-robotics-jobs-with-real-github-examples-)).



### Day 58: Performance Curve Plotting and System Visualizations

* **Objective**: Generate and export charts illustrating system performance metrics.


* **Technical Tasks**:
1. Log pixel tracking errors during the docking phase .
2. Plot tracking error convergence over time to verify stability .
3. Export charts as high-resolution image files.




* **Primary Resource**:([https://roboticsjobs.co.uk/career-advice/portfolio-projects-that-get-you-hired-for-robotics-jobs-with-real-github-examples-](https://roboticsjobs.co.uk/career-advice/portfolio-projects-that-get-you-hired-for-robotics-jobs-with-real-github-examples-)).



### Day 59: Writing the Ultimate Recruiter-Facing README

* **Objective**: Write a comprehensive, professional README for the VisioBot repository.


* **Technical Tasks**:
1. State project objectives, hardware parameters, and the software stack.


2. Add system architecture schematics.


3. Embed demonstration videos, performance plots, and setup instructions.




* **Primary Resource**:([https://www.digikey.com/en/maker/tutorials/2025/github-for-robotics-organizing-your-first-project](https://www.digikey.com/en/maker/tutorials/2025/github-for-robotics-organizing-your-first-project)).



### Day 60: Public Launch & Portfolio Distribution

* **Objective**: Publish and share your completed project with the robotics community.


* **Technical Tasks**:
1. Push the final, documented codebase to GitHub.


2. Share a summary of the 60-day challenge and the final demo video on professional networks.


3. Verify all links, repository documentation, and contact info are up to date.




* **Primary Resource**:([https://www.theconstruct.ai/the-best-way-to-create-your-robotics-portfolio/](https://www.theconstruct.ai/the-best-way-to-create-your-robotics-portfolio/)).