const PHASES = [
  { id: "all", label: "All days", range: "1-60", color: "#0f766e" },
  { id: "1", label: "ROS2 + Simulation", range: "1-15", color: "#0f766e" },
  { id: "2", label: "Vision + Control", range: "16-30", color: "#2563a7" },
  { id: "3", label: "Edge AI + micro-ROS", range: "31-45", color: "#b66b16" },
  { id: "4", label: "Capstone + Portfolio", range: "46-60", color: "#b34a4a" }
];

const LINKS = {
  rosInstall: ["Official docs", "ROS 2 Jazzy Ubuntu install", "https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html"],
  rosTutorials: ["Official docs", "ROS 2 Jazzy tutorials", "https://docs.ros.org/en/jazzy/Tutorials.html"],
  rosWorkspace: ["Official docs", "Creating a ROS 2 workspace", "https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Creating-A-Workspace/Creating-A-Workspace.html"],
  rosPackage: ["Official docs", "Creating a ROS 2 package", "https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Creating-Your-First-ROS2-Package.html"],
  rosTopicsPy: ["Official docs", "Publisher and subscriber in Python", "https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Py-Publisher-And-Subscriber.html"],
  rosTopicsCpp: ["Official docs", "Publisher and subscriber in C++", "https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Cpp-Publisher-And-Subscriber.html"],
  rosTopicsCli: ["Official docs", "Understanding ROS 2 topics", "https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Topics/Understanding-ROS2-Topics.html"],
  rosServicesPy: ["Official docs", "Services and clients in Python", "https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Py-Service-And-Client.html"],
  rosInterfaces: ["Official docs", "Custom messages and services", "https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Custom-ROS2-Interfaces.html"],
  rosActions: ["Official docs", "Creating and using ROS 2 actions", "https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Creating-an-Action.html"],
  rosTf2: ["Official docs", "TF2 introduction", "https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Tf2/Introduction-To-Tf2.html"],
  rosTf2Broadcaster: ["Official docs", "Writing a TF2 broadcaster", "https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Tf2/Writing-A-Tf2-Broadcaster-Py.html"],
  rosLaunch: ["Official docs", "Creating launch files", "https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Launch/Creating-Launch-Files.html"],
  rosParams: ["Official docs", "Using parameters in Python", "https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Using-Parameters-In-A-Class-Python.html"],
  rosUrdf: ["Official docs", "URDF tutorials", "https://docs.ros.org/en/jazzy/Tutorials/Intermediate/URDF/URDF-Main.html"],
  robotStatePublisher: ["Official docs", "URDF with robot_state_publisher", "https://docs.ros.org/en/jazzy/Tutorials/Intermediate/URDF/Using-URDF-with-Robot-State-Publisher-py.html"],
  gazeboInstall: ["Official docs", "Gazebo Harmonic with ROS 2", "https://gazebosim.org/docs/harmonic/ros_installation"],
  gazeboRos2: ["Official docs", "ROS 2 and Gazebo integration", "https://gazebosim.org/docs/harmonic/ros2_integration/"],
  rosGz: ["ROS Index", "ros_gz bridge overview", "https://index.ros.org/r/ros_gz/"],
  slamToolbox: ["Official docs", "SLAM Toolbox Jazzy docs", "https://docs.ros.org/en/ros2_packages/jazzy/api/slam_toolbox/"],
  slamGithub: ["GitHub", "SteveMacenski/slam_toolbox", "https://github.com/SteveMacenski/slam_toolbox"],
  nav2Start: ["Official docs", "Nav2 getting started", "https://docs.nav2.org/getting_started/index.html"],
  nav2Tutorials: ["Official docs", "Nav2 tutorials", "https://docs.nav2.org/tutorials/index.html"],
  nav2Commander: ["Official docs", "Nav2 Simple Commander API", "https://docs.nav2.org/commander_api/index.html"],
  v4l2Camera: ["Official docs", "v4l2_camera for ROS 2 Jazzy", "https://docs.ros.org/en/jazzy/p/v4l2_camera/"],
  cvBridge: ["ROS Index", "cv_bridge package", "https://index.ros.org/p/cv_bridge/"],
  opencvAruco: ["Official docs", "OpenCV ArUco detection", "https://docs.opencv.org/4.x/d5/dae/tutorial_aruco_detection.html"],
  ultralyticsQuick: ["Official docs", "Install Ultralytics YOLO", "https://docs.ultralytics.com/quickstart/"],
  ultralyticsPython: ["Official docs", "Ultralytics Python usage", "https://docs.ultralytics.com/usage/python/"],
  sortGithub: ["GitHub", "SORT tracker reference", "https://github.com/abewley/sort"],
  ros2Aruco: ["GitHub", "ros2_aruco wrapper", "https://github.com/JMU-ROBOTICS-VIVA/ros2_aruco"],
  depthAnything: ["GitHub", "Depth Anything V2", "https://github.com/DepthAnything/Depth-Anything-V2"],
  pointCloud: ["Official docs", "sensor_msgs/PointCloud2", "https://docs.ros.org/en/jazzy/p/sensor_msgs/msg/PointCloud2.html"],
  pclDocs: ["Official docs", "Point Cloud Library docs", "https://pointclouds.org/documentation/"],
  liteRtMicro: ["Official docs", "Google LiteRT for Microcontrollers", "https://ai.google.dev/edge/litert/microcontrollers"],
  liteRtStart: ["Official docs", "LiteRT Micro get started", "https://ai.google.dev/edge/litert/microcontrollers/get_started"],
  onnxRuntime: ["Official docs", "ONNX Runtime docs", "https://onnxruntime.ai/docs/"],
  onnxQuant: ["Official docs", "ONNX Runtime quantization", "https://onnxruntime.ai/docs/performance/model-optimizations/quantization.html"],
  edgeImpulseEsp32: ["Official docs", "Edge Impulse ESP32 docs", "https://docs.edgeimpulse.com/hardware/boards/espressif-esp32"],
  edgeImpulseStudio: ["Platform", "Edge Impulse Studio", "https://studio.edgeimpulse.com/"],
  platformioEsp32: ["Official docs", "PlatformIO Espressif 32", "https://docs.platformio.org/en/latest/platforms/espressif32.html"],
  tfliteEsp32Repo: ["GitHub", "atomic14/tensorflow-lite-esp32", "https://github.com/atomic14/tensorflow-lite-esp32"],
  microRosOverview: ["Official docs", "micro-ROS tutorials", "https://micro.ros.org/docs/tutorials/core/overview/"],
  microRosSetup: ["GitHub", "micro_ros_setup", "https://github.com/micro-ROS/micro_ros_setup"],
  microRosArduino: ["GitHub", "micro_ros_arduino", "https://github.com/micro-ROS/micro_ros_arduino"],
  mpu6050: ["GitHub", "MPU6050 ROS IMU example", "https://github.com/luckydipper/mpu6050_imu"],
  rosbag: ["Official docs", "Recording ROS 2 bags", "https://docs.ros.org/en/jazzy/Tutorials/Advanced/Recording-A-Bag-From-Your-Own-Node-Py.html"],
  rqtConsole: ["Official docs", "Using rqt_console", "https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Using-Rqt-Console/Using-Rqt-Console.html"],
  githubReadme: ["Guide", "GitHub README guide", "https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes"],
  drawio: ["Tool", "Draw.io diagrams", "https://app.diagrams.net/"],
  courseRosBeginners: ["Course", "Udemy: ROS 2 for Beginners (ROS Jazzy - 2026)", "https://www.udemy.com/course/ros2-for-beginners/"],
  courseRosComplete: ["Course", "Udemy: ROS 2 Jazzy Complete Robotics Developer", "https://www.udemy.com/course/ros-2-jazzy-complete-robotics-developer-course/"],
  courseRosLevel2: ["Course", "Udemy: ROS 2 Level 2 - TF, URDF, RViz, Gazebo", "https://www.udemy.com/course/ros2-tf-urdf-rviz-gazebo/"],
  courseNav2: ["Course", "Udemy: ROS 2 Nav2 Stack", "https://www.udemy.com/course/ros2-nav2-stack/"],
  courseConstruct: ["Course", "The Construct: ROS 2 Jazzy Learning Week", "https://app.theconstruct.ai/ros2-jazzy-learning-week/"],
  courseTinyML: ["Course", "Udemy: Practical Guide to Edge AI and TinyML", "https://www.udemy.com/course/practical-guide-to-edge-ai-and-tinyml-for-smarter-devices/"],
  ytConstruct: ["YouTube", "The Construct ROS2 Jazzy Crash Course", "https://www.youtube.com/watch?v=Se5pvRlTX8s"],
  ytBeginnerAdvanced: ["YouTube", "Learn ROS 2: Beginner to Advanced", "https://www.youtube.com/watch?v=HJAE5Pk8Nyw"],
  ytLaunch: ["YouTube", "ROS2 Launch File Tutorial", "https://www.youtube.com/watch?v=T8KJH47aZ8w"],
  ytUrdf: ["YouTube", "ROS2 URDF Tutorial", "https://www.youtube.com/watch?v=LsKL8N5Iwkw"],
  ytRviz: ["YouTube", "ROS2 RViz2 Tutorial", "https://www.youtube.com/watch?v=qWoGkPDg4N8"],
  ytGazebo: ["YouTube", "Install Gazebo Harmonic with ROS2 Jazzy", "https://www.youtube.com/watch?v=dY8JxldcuqA"],
  ytSlam: ["YouTube", "ROS2 SLAM Toolbox Tutorial", "https://www.youtube.com/watch?v=0G6LDuslqmA"],
  ytNav2: ["YouTube", "ROS2 Nav2 Mobile Robot Simulation", "https://www.youtube.com/watch?v=Xbij9Tst-WA"],
  ytOpenCvCamera: ["YouTube", "OpenCV basics for robotics with ROS", "https://www.youtube.com/watch?v=nKu8w3gT6s8"],
  ytYoloRos: ["YouTube", "How to Use YOLOv8 with ROS2", "https://www.youtube.com/watch?v=XqibXP4lwgA"],
  ytYoloAlt: ["YouTube", "YOLOv8 with ROS2 search", "https://www.youtube.com/results?search_query=YOLOv8+ROS2+Jazzy+tutorial"],
  ytAruco: ["YouTube", "ArUco pose estimation with OpenCV", "https://www.youtube.com/watch?v=bS00Vs09Upw"],
  ytVisualServo: ["YouTube", "Autonomous driving robot visual servoing", "https://www.youtube.com/watch?v=uhzCxFm0sko"],
  ytTfliteEsp32: ["YouTube", "TensorFlow Lite with PlatformIO and ESP32", "https://www.youtube.com/watch?v=kZdIO82059E"],
  ytMicroRos: ["YouTube", "micro-ROS Jazzy Arduino ESP32 S3", "https://www.youtube.com/watch?v=tRtfpnu4LjE"],
  ytMicroRosPlatform: ["YouTube", "micro-ROS Jazzy PlatformIO ESP32 S3", "https://www.youtube.com/watch?v=tL7swYonY8w"],
  ytSearchDepth: ["YouTube", "ROS2 monocular depth search", "https://www.youtube.com/results?search_query=ROS2+monocular+depth+estimation+Depth+Anything"],
  ytSearchPointCloud: ["YouTube", "ROS2 PointCloud2 PCL search", "https://www.youtube.com/results?search_query=ROS2+PointCloud2+PCL+tutorial"],
  ytSearchDemo: ["YouTube", "Robotics demo video guide search", "https://www.youtube.com/results?search_query=robotics+project+demo+video+ROS2+RViz+Gazebo"]
};

const DAYS = [
  day(1, 1, "ROS2 Jazzy environment setup", "Install and verify the robotics software foundation on Ubuntu 24.04.", ["Configure UTF-8 locale, apt sources, and ROS repository keys.", "Install ros-jazzy-desktop and developer tools.", "Source /opt/ros/jazzy/setup.bash from the shell profile.", "Verify with ros2 doctor, turtlesim, and a clean terminal restart."], "ROS2 Jazzy desktop is installed, sourced, and verified with a screenshot or terminal log.", ["rosInstall", "rosTutorials"], ["courseRosBeginners", "courseConstruct"], ["ytConstruct"]),
  day(2, 1, "Workspaces, colcon, and package layout", "Build a clean VisioBot workspace that can grow for 60 days.", ["Create ~/visiobot_ws/src and document the folder convention.", "Install and run colcon build --symlink-install.", "Create a Python package with rclpy and console_scripts entry points.", "Add a README section for build, source, and run commands."], "A versioned workspace with one runnable Python package and reproducible setup notes.", ["rosWorkspace", "rosPackage"], ["courseRosBeginners", "courseRosComplete"], ["ytConstruct"]),
  day(3, 1, "Python publishers, subscribers, and QoS", "Send telemetry through topics and inspect the live ROS graph.", ["Write a telemetry publisher node with a timer callback.", "Write a subscriber node that logs and validates messages.", "Use ros2 topic list, echo, hz, and info for inspection.", "Compare reliable and best-effort QoS at a conceptual level."], "A Python pub/sub pair that runs from launchable package entry points.", ["rosTopicsPy", "rosTopicsCli"], ["courseRosBeginners", "courseConstruct"], ["ytConstruct"]),
  day(4, 1, "C++ nodes with rclcpp", "Translate the core topic pattern into C++ for performance-critical robotics code.", ["Create ament_cmake package scaffolding for C++ nodes.", "Implement publisher and subscriber equivalents with rclcpp.", "Practice shared pointers, callbacks, and executor basics.", "Compare build and run workflow with the Python package."], "A C++ talker/listener package with notes on Python vs C++ tradeoffs.", ["rosTopicsCpp", "rosTopicsCli"], ["courseRosComplete", "courseRosBeginners"], ["ytBeginnerAdvanced"]),
  day(5, 1, "Custom interfaces, services, and clients", "Define structured robot messages and synchronous request-response flows.", ["Create a custom msg for VisioBot target or telemetry state.", "Configure rosidl_generate_interfaces correctly.", "Build a Python service and client around a simple calibration request.", "Inspect service types and call the service from the CLI."], "A custom interface package plus one working service/client pair.", ["rosInterfaces", "rosServicesPy"], ["courseRosBeginners", "courseRosComplete"], ["ytConstruct"]),
  day(6, 1, "Actions for long-running robot goals", "Use preemptible goals for tasks such as navigation, docking, and scanning.", ["Read the action model: goal, feedback, result, cancel.", "Build or adapt a Fibonacci action server/client.", "Send goals from the command line and observe feedback.", "Write a note mapping actions to future Nav2 behavior."], "A working action server/client and a short design note for VisioBot actions.", ["rosActions", "rosTutorials"], ["courseRosComplete", "courseRosBeginners"], ["ytBeginnerAdvanced"]),
  day(7, 1, "TF2 transforms and RViz frame sanity", "Make robot coordinate frames visible and debuggable.", ["Create static transforms for base_link, camera_link, and laser_link.", "Create a dynamic broadcaster example for a moving frame.", "Inspect the transform tree with rqt_tf_tree or RViz.", "Document the frame names you will keep for the full project."], "A clean TF tree screenshot and a frame naming convention for VisioBot.", ["rosTf2", "rosTf2Broadcaster"], ["courseRosLevel2", "courseRosComplete"], ["ytRviz", "ytUrdf"]),
  day(8, 1, "Launch files and YAML parameters", "Run multi-node systems without terminal chaos.", ["Create a Python launch file that starts multiple nodes.", "Add arguments for namespace, topic remaps, and use_sim_time.", "Load YAML parameters into at least one node.", "Make a single command that starts the week-one system."], "A reusable launch file plus YAML config committed to the workspace.", ["rosLaunch", "rosParams"], ["courseRosBeginners", "courseRosComplete"], ["ytLaunch"]),
  day(9, 1, "URDF kinematic model", "Describe the first VisioBot differential chassis.", ["Define base, wheel, caster, camera, and lidar links.", "Add continuous wheel joints and fixed sensor joints.", "Visualize the model with robot_state_publisher in RViz2.", "Check axes, origins, and frame names against your TF convention."], "A URDF robot model that renders correctly in RViz2.", ["rosUrdf", "robotStatePublisher"], ["courseRosLevel2", "courseRosComplete"], ["ytUrdf", "ytRviz"]),
  day(10, 1, "Xacro, collision, and inertia", "Turn the robot description into something a physics engine can trust.", ["Convert repeated geometry into Xacro macros.", "Add collision geometry for every moving or sensor link.", "Add realistic inertial values for chassis and wheels.", "Generate the final URDF and validate that it still renders."], "A Xacro-based robot description with visual, collision, and inertial tags.", ["rosUrdf", "robotStatePublisher"], ["courseRosLevel2", "courseRosComplete"], ["ytUrdf"]),
  day(11, 1, "Gazebo Harmonic and robot spawning", "Move from static visualization into simulated physics.", ["Install ros-jazzy-ros-gz for the Jazzy/Harmonic pairing.", "Launch a clean Gazebo Harmonic world.", "Spawn the VisioBot model into the world.", "Confirm transforms, odometry, and simulation time are consistent."], "A spawned VisioBot model in Gazebo Harmonic with notes on any plugin fixes.", ["gazeboInstall", "gazeboRos2", "rosGz"], ["courseRosLevel2", "courseRosComplete"], ["ytGazebo"]),
  day(12, 1, "Sensors and ros_gz bridge", "Attach simulated lidar and camera streams to the ROS graph.", ["Add lidar and RGB camera plugins to the robot model.", "Bridge Gazebo topics into ROS2 messages with ros_gz_bridge.", "Inspect LaserScan and Image topics from the CLI.", "Open RViz2 with robot, scan, and camera displays."], "A Gazebo robot publishing sensor topics that RViz2 can visualize.", ["gazeboRos2", "rosGz", "v4l2Camera"], ["courseRosLevel2", "courseRosComplete"], ["ytGazebo", "ytRviz"]),
  day(13, 1, "SLAM Toolbox mapping", "Build a 2D map from simulated lidar and odometry.", ["Install and launch slam_toolbox for online async mapping.", "Teleoperate the robot through a simple room or maze.", "Tune basic parameters when map quality drifts.", "Save the map and serialized pose graph for later navigation."], "A saved occupancy map plus RViz screenshot of mapping progress.", ["slamToolbox", "slamGithub"], ["courseNav2", "courseRosComplete"], ["ytSlam"]),
  day(14, 1, "Nav2 configuration", "Give the simulated robot autonomous point-to-point navigation.", ["Install Nav2 and study the lifecycle nodes.", "Configure map server, AMCL, planner, controller, and costmaps.", "Send a goal from RViz2 and observe behavior tree execution.", "Record parameter changes that improve path stability."], "A Nav2 launch/config setup that navigates to at least three RViz goals.", ["nav2Start", "nav2Tutorials"], ["courseNav2", "courseRosComplete"], ["ytNav2"]),
  day(15, 1, "Phase 1 capstone: map and navigate", "Prove the ROS2, Gazebo, SLAM, and Nav2 foundation works together.", ["Run Gazebo, robot_state_publisher, SLAM, and Nav2 as one workflow.", "Map an unknown environment, save it, then switch to localization.", "Navigate to multiple goals while monitoring TF, map, path, and scan.", "Write a concise phase report with commands and screenshots."], "A documented simulation demo: VisioBot maps a room and navigates autonomously.", ["slamToolbox", "nav2Tutorials", "gazeboRos2"], ["courseNav2", "courseRosComplete"], ["ytSlam", "ytNav2"]),

  day(16, 2, "Camera drivers and CvBridge", "Convert ROS image streams into OpenCV matrices.", ["Run v4l2_camera or the Gazebo camera topic.", "Subscribe to sensor_msgs/Image from a Python node.", "Use CvBridge to convert to OpenCV BGR/RGB arrays.", "Republish a processed image and inspect latency."], "A ROS2 image conversion node that displays or republishes camera frames.", ["v4l2Camera", "cvBridge"], ["courseRosComplete", "courseRosBeginners"], ["ytOpenCvCamera"]),
  day(17, 2, "OpenCV preprocessing in ROS2", "Prepare camera frames for detection and tracking.", ["Add resize, color conversion, blur, and threshold utilities.", "Publish debug images for each processing stage.", "Measure frame rate before adding neural inference.", "Write clean helper functions for image callbacks."], "A preprocessing node with measurable FPS and debug image topics.", ["cvBridge", "v4l2Camera"], ["courseRosComplete", "courseRosLevel2"], ["ytOpenCvCamera"]),
  day(18, 2, "YOLOv8 detection node", "Run semantic object detection from a ROS2 image topic.", ["Install Ultralytics and load a small pretrained YOLO model.", "Pass CvBridge frames into model inference.", "Extract boxes, labels, confidence, and timestamps.", "Publish detections in a structured format."], "A ROS2 YOLO node that detects objects from webcam or Gazebo camera input.", ["ultralyticsQuick", "ultralyticsPython"], ["courseRosComplete", "courseRosBeginners"], ["ytYoloRos", "ytYoloAlt"]),
  day(19, 2, "Detection messages and overlays", "Make perception outputs usable by other robot nodes.", ["Define or choose a detection message schema.", "Publish bounding boxes and class IDs on /yolo/detections.", "Create an overlay node that draws boxes on the original image.", "Visualize the annotated stream in RViz2 or rqt_image_view."], "Detection and overlay topics that downstream control nodes can consume.", ["rosInterfaces", "ultralyticsPython", "cvBridge"], ["courseRosComplete", "courseRosBeginners"], ["ytYoloRos"]),
  day(20, 2, "SORT object tracking", "Track objects across frames instead of treating detections as isolated events.", ["Study Kalman prediction and Hungarian matching at a high level.", "Feed YOLO detections into SORT or a lightweight tracker.", "Publish persistent track IDs with each object.", "Test brief occlusion and missed detections."], "A tracking topic with stable object IDs for at least one target class.", ["sortGithub", "ultralyticsPython"], ["courseRosComplete"], ["ytYoloRos", "ytYoloAlt"]),
  day(21, 2, "ArUco marker pose estimation", "Use fiducials for metric pose estimation and docking practice.", ["Generate and print an ArUco marker dictionary target.", "Detect corners and IDs from the camera image.", "Use camera calibration and solvePnP for marker pose.", "Publish PoseStamped or PoseArray messages for detected markers."], "A marker detector that publishes 6D pose and an RViz visualization.", ["opencvAruco", "ros2Aruco"], ["courseRosComplete", "courseRosLevel2"], ["ytAruco"]),
  day(22, 2, "Event-driven perception logic", "Turn perception into robot-readable events.", ["Subscribe to YOLO and ArUco outputs in a state node.", "Trigger events for target class, marker ID, or confidence threshold.", "Add simple text-to-speech or log announcements.", "Debounce repeated detections so the robot does not spam events."], "A perception event node that announces or logs target detections cleanly.", ["rosTopicsPy", "ros2Aruco", "ultralyticsPython"], ["courseRosBeginners", "courseRosComplete"], ["ytYoloRos", "ytAruco"]),
  day(23, 2, "Monocular depth estimation", "Estimate scene structure from a single camera.", ["Install and run Depth Anything V2 or MiDaS on sample images.", "Understand relative depth versus metric depth.", "Benchmark small and base models on your machine.", "Decide which model can run acceptably with ROS2 callbacks."], "A depth model test notebook or script with sample outputs and timing.", ["depthAnything", "ultralyticsPython"], ["courseRosComplete"], ["ytSearchDepth"]),
  day(24, 2, "Depth node and camera calibration", "Publish depth maps alongside RGB frames.", ["Wrap the depth model in a ROS2 node.", "Normalize and publish a depth image topic.", "Read camera intrinsic parameters and image geometry.", "Document latency and practical frame-size tradeoffs."], "A ROS2 depth image publisher with calibration notes and FPS results.", ["depthAnything", "cvBridge", "v4l2Camera"], ["courseRosComplete"], ["ytSearchDepth"]),
  day(25, 2, "PointCloud2 projection and filtering", "Project depth into 3D and clean the point cloud.", ["Convert depth pixels into XYZ points using intrinsics.", "Publish sensor_msgs/PointCloud2.", "Downsample with voxel filtering or a simple stride filter.", "Visualize the cloud in RViz2 and note scale issues."], "A visible PointCloud2 stream in RViz2 from simulated or inferred depth.", ["pointCloud", "pclDocs"], ["courseRosComplete", "courseRosLevel2"], ["ytSearchPointCloud"]),
  day(26, 2, "Visual servoing theory and PID", "Use camera error as a control signal.", ["Define image center, target center, and pixel error.", "Map horizontal error to angular velocity.", "Map bounding-box area or depth to linear velocity.", "Tune proportional gains in a dry-run script before robot motion."], "A documented control equation and gain table for target centering.", ["nav2Tutorials", "ultralyticsPython"], ["courseNav2", "courseRosComplete"], ["ytVisualServo"]),
  day(27, 2, "Visual servoing implementation", "Make the robot rotate and approach a detected target.", ["Subscribe to tracked detections or selected YOLO boxes.", "Publish geometry_msgs/Twist on /cmd_vel.", "Add safety stops for lost target and near-distance threshold.", "Test in Gazebo with a fixed target object."], "A visual servo node that centers and approaches a target without Nav2.", ["rosTopicsPy", "nav2Tutorials", "ultralyticsPython"], ["courseNav2", "courseRosComplete"], ["ytVisualServo", "ytYoloRos"]),
  day(28, 2, "Waypoint patrol with Nav2", "Patrol while the camera continuously searches for targets.", ["Create a small waypoint list in map coordinates.", "Use Nav2 Simple Commander or RViz goals for patrol.", "Run YOLO in parallel with navigation.", "Log detections with robot pose and timestamp."], "A patrol demo that records target sightings while Nav2 moves the robot.", ["nav2Commander", "nav2Tutorials"], ["courseNav2", "courseRosComplete"], ["ytNav2"]),
  day(29, 2, "YOLO-to-Nav2 target handoff", "Preempt patrol and navigate near a detected target.", ["Convert selected detections into a target approach behavior.", "Stop or pause Nav2 patrol when confidence threshold is met.", "Switch control to visual servoing for final alignment.", "Handle target lost, reacquired, and timeout states."], "A hybrid behavior where Nav2 patrol hands control to vision alignment.", ["nav2Commander", "ultralyticsPython", "rosActions"], ["courseNav2", "courseRosComplete"], ["ytNav2", "ytYoloRos"]),
  day(30, 2, "Phase 2 capstone: find and approach", "Unify camera, YOLO, tracking, Nav2, and visual servoing.", ["Populate Gazebo with a target object or marker.", "Launch the full perception stack with annotated image output.", "Patrol waypoints until the target appears.", "Approach and stop near the target, then write a phase report."], "A recorded demo of VisioBot finding, tracking, and approaching a visual target.", ["ultralyticsPython", "nav2Tutorials", "depthAnything"], ["courseNav2", "courseRosComplete"], ["ytYoloRos", "ytVisualServo"]),

  day(31, 3, "LiteRT/TFLite conversion basics", "Start moving models toward constrained devices.", ["Study the microcontroller inference workflow.", "Train or download a tiny baseline model.", "Convert the model to a .tflite or LiteRT flatbuffer.", "Record model size, input shape, and supported ops."], "A converted tiny model plus notes on memory and operator constraints.", ["liteRtMicro", "liteRtStart"], ["courseTinyML"], ["ytTfliteEsp32"]),
  day(32, 3, "Desktop benchmark for small models", "Measure before deploying to the microcontroller.", ["Run the model locally with a small inference script.", "Measure latency over 100 inferences.", "Compare FP32 and smaller input resolutions.", "Save a CSV or markdown table of timing results."], "A benchmark report showing size and latency before optimization.", ["liteRtStart", "onnxRuntime"], ["courseTinyML"], ["ytTfliteEsp32"]),
  day(33, 3, "ONNX export and runtime comparison", "Keep model deployment framework-agnostic.", ["Export a PyTorch or Ultralytics model to ONNX.", "Load it with ONNX Runtime in Python.", "Compare output parity and latency with the TFLite version.", "Document which runtime fits desktop, edge Linux, and MCU targets."], "An ONNX inference script with comparison notes.", ["onnxRuntime", "ultralyticsPython"], ["courseTinyML"], ["ytTfliteEsp32"]),
  day(34, 3, "INT8 quantization", "Compress models for low-power inference.", ["Apply dynamic or post-training quantization where supported.", "Compare FP32 versus INT8 file size.", "Run a small accuracy sanity check.", "Write down model size, speed, and quality tradeoffs."], "A quantized model and a clear before/after benchmark table.", ["onnxQuant", "liteRtMicro"], ["courseTinyML"], ["ytTfliteEsp32"]),
  day(35, 3, "Edge Impulse dataset collection", "Create a TinyML dataset for gestures or sensor states.", ["Create an Edge Impulse project.", "Collect IMU, accelerometer, or simple sensor samples.", "Label at least three classes with balanced examples.", "Split training and test data in the studio."], "A labeled Edge Impulse dataset ready for training.", ["edgeImpulseEsp32", "edgeImpulseStudio"], ["courseTinyML"], ["ytTfliteEsp32"]),
  day(36, 3, "Edge Impulse model deployment", "Train and export an ESP32-ready classifier.", ["Design an impulse with preprocessing and a classifier block.", "Train and inspect confusion matrix results.", "Export an Arduino or C++ library for ESP32.", "Flash and test the classifier on board if hardware is ready."], "An Edge Impulse classifier exported for ESP32 with test accuracy notes.", ["edgeImpulseEsp32", "edgeImpulseStudio"], ["courseTinyML"], ["ytTfliteEsp32"]),
  day(37, 3, "TFLite Micro with PlatformIO", "Compile a tiny inference project for ESP32.", ["Create a PlatformIO Espressif32 project.", "Add TFLite Micro or an example library dependency.", "Convert a model to a C byte array.", "Build and flash a hello-world inference loop."], "An ESP32 firmware project that compiles and runs a tiny model.", ["platformioEsp32", "tfliteEsp32Repo", "liteRtMicro"], ["courseTinyML"], ["ytTfliteEsp32"]),
  day(38, 3, "ESP32 sensor inference loop", "Connect sensor readings to local classification.", ["Wire or simulate an IMU/ultrasonic input.", "Sample at a stable interval with buffering.", "Feed features into the local model.", "Print class, confidence, and timing over serial."], "A firmware loop that reads data and produces local classification output.", ["platformioEsp32", "edgeImpulseEsp32", "mpu6050"], ["courseTinyML"], ["ytTfliteEsp32"]),
  day(39, 3, "micro-ROS agent setup", "Bridge a microcontroller into the ROS2 ecosystem.", ["Install or build micro-ROS agent on the Ubuntu host.", "Study XRCE-DDS and agent/client roles.", "Run the agent over serial first if possible.", "Document firewall and port assumptions for Wi-Fi mode."], "A host-side micro-ROS agent command that starts cleanly.", ["microRosOverview", "microRosSetup"], ["courseRosComplete", "courseTinyML"], ["ytMicroRos"]),
  day(40, 3, "ESP32 micro-ROS Wi-Fi publisher", "Publish from ESP32 into the desktop ROS graph.", ["Set up micro_ros_arduino or PlatformIO support.", "Configure Wi-Fi SSID, agent IP, and UDP transport.", "Flash a basic publisher example.", "Verify the topic with ros2 topic echo on the host."], "An ESP32 that publishes a message to ROS2 over Wi-Fi or serial.", ["microRosArduino", "microRosOverview"], ["courseTinyML", "courseRosComplete"], ["ytMicroRos", "ytMicroRosPlatform"]),
  day(41, 3, "IMU sensor publishing", "Turn physical sensor data into standard ROS2 messages.", ["Wire MPU6050 or an available IMU to ESP32.", "Read accelerometer and gyro data through I2C.", "Pack readings into sensor_msgs/Imu where practical.", "View the IMU topic on the host and note sampling rate."], "A ROS2-visible IMU topic coming from ESP32 firmware.", ["mpu6050", "microRosArduino"], ["courseTinyML", "courseRosComplete"], ["ytMicroRos"]),
  day(42, 3, "ROS2-to-ESP32 actuator subscriber", "Send commands from the ROS graph to physical outputs.", ["Add an LED, servo, or motor-safe mock actuator.", "Create a micro-ROS subscriber topic such as /led_cmd.", "Publish commands from desktop ROS2 CLI.", "Add guardrails for invalid command values."], "A bidirectional bridge where ROS2 controls an ESP32 output.", ["microRosArduino", "microRosOverview"], ["courseRosComplete", "courseTinyML"], ["ytMicroRosPlatform", "ytMicroRos"]),
  day(43, 3, "Bridge reliability and diagnostics", "Make the edge link debuggable under real network conditions.", ["Test agent restart, ESP32 restart, and Wi-Fi reconnect behavior.", "Log heartbeat or status messages from firmware.", "Measure message rate and dropped messages.", "Write a troubleshooting checklist for UDP and serial modes."], "A reliability checklist plus stable publish/subscribe behavior after restarts.", ["microRosSetup", "microRosArduino", "rqtConsole"], ["courseRosComplete", "courseTinyML"], ["ytMicroRosPlatform"]),
  day(44, 3, "Gesture classifier to ROS2", "Expose TinyML classification results as robot commands.", ["Run the gesture classifier on ESP32.", "Publish class label and confidence to ROS2.", "Map labels to safe robot intents such as stop, forward, search.", "Add host-side validation before commands reach /cmd_vel."], "A ROS2 topic carrying ESP32 gesture classifications.", ["edgeImpulseEsp32", "microRosArduino", "liteRtMicro"], ["courseTinyML", "courseRosComplete"], ["ytMicroRos", "ytTfliteEsp32"]),
  day(45, 3, "Phase 3 capstone: gesture controls simulation", "Use edge inference to influence the Gazebo robot.", ["Run Gazebo and Nav2 with the micro-ROS bridge online.", "Publish ESP32 gestures into a command arbitration node.", "Make the simulated robot react safely to gestures.", "Record a split demo of hardware, terminal, and RViz/Gazebo."], "A demo where ESP32 TinyML gestures control or influence VisioBot in simulation.", ["microRosArduino", "edgeImpulseEsp32", "nav2Tutorials"], ["courseTinyML", "courseNav2"], ["ytMicroRos", "ytSearchDemo"]),

  day(46, 4, "Final architecture design", "Lock the system boundaries before the final build sprint.", ["Draw the ROS graph: perception, navigation, micro-ROS, command arbitration.", "List topics, message types, actions, and launch files.", "Define package names and ownership boundaries.", "Decide the final demo scenario and success criteria."], "A complete architecture diagram and final demo checklist.", ["drawio", "rosTutorials", "nav2Tutorials"], ["courseRosComplete"], ["ytSearchDemo"]),
  day(47, 4, "Repository and package structure", "Make the portfolio repo easy to understand.", ["Create packages such as visiobot_description, navigation, perception, edge_bridge.", "Add README files per package with purpose and launch commands.", "Add .gitignore, LICENSE, and requirements/setup notes.", "Open issues or a project board for remaining work."], "A clean monorepo structure that a reviewer can navigate quickly.", ["githubReadme", "rosPackage"], ["courseRosComplete"], ["ytBeginnerAdvanced"]),
  day(48, 4, "Interfaces, launch map, and configs", "Stabilize the contracts between nodes.", ["Finalize custom messages for detections, gestures, and mode state.", "Create top-level launch files for sim, perception, edge, and full demo.", "Move tunables into YAML files.", "Run each launch path from a clean terminal."], "A reliable launch/config layer for every major subsystem.", ["rosInterfaces", "rosLaunch", "rosParams"], ["courseRosComplete", "courseRosBeginners"], ["ytLaunch"]),
  day(49, 4, "Perception package integration", "Prepare the vision stack for the final demo.", ["Move camera, YOLO, tracking, ArUco, and depth nodes into packages.", "Standardize topic names and frame IDs.", "Add launch arguments for webcam versus Gazebo camera.", "Test annotated image and detection topics in one launch."], "A perception launch that starts the full camera-to-detection pipeline.", ["ultralyticsPython", "cvBridge", "opencvAruco"], ["courseRosComplete"], ["ytYoloRos", "ytAruco"]),
  day(50, 4, "Navigation package integration", "Make mapping, localization, and goal execution reusable.", ["Collect Nav2, SLAM, AMCL, and map configs into the navigation package.", "Test saved-map localization mode.", "Add waypoint patrol and target approach helpers.", "Document map generation and reuse workflow."], "A navigation package that can map, localize, patrol, and accept goals.", ["nav2Tutorials", "slamToolbox", "nav2Commander"], ["courseNav2", "courseRosComplete"], ["ytSlam", "ytNav2"]),
  day(51, 4, "Edge bridge integration", "Connect physical ESP32 signals to final robot behavior.", ["Package the micro-ROS agent launch or run command.", "Create a host-side edge bridge node for gesture validation.", "Map physical classifications to robot-safe command intents.", "Test with hardware disconnected and connected."], "An edge bridge that safely translates ESP32 data into robot intents.", ["microRosArduino", "microRosSetup", "edgeImpulseEsp32"], ["courseTinyML", "courseRosComplete"], ["ytMicroRos"]),
  day(52, 4, "Full Gazebo integration test", "Run all subsystems together and find real integration bugs.", ["Launch Gazebo, robot description, Nav2, perception, and edge bridge.", "Run a scripted scenario from startup to target approach.", "Log all errors, topic mismatches, and timing bottlenecks.", "Fix the highest-impact blockers first."], "A full-system run log with blockers fixed or tracked.", ["gazeboRos2", "nav2Tutorials", "rosbag"], ["courseNav2", "courseRosComplete"], ["ytNav2", "ytSearchDemo"]),
  day(53, 4, "Scenario tests and rosbag evidence", "Turn the demo into repeatable proof.", ["Define at least five test scenarios: target visible, target hidden, gesture stop, lost target, restart.", "Record ROS bags for key topics.", "Replay and inspect perception/navigation behavior.", "Create a test results table."], "A repeatable scenario test report with ROS bag evidence.", ["rosbag", "rqtConsole", "nav2Tutorials"], ["courseRosComplete", "courseNav2"], ["ytSearchDemo"]),
  day(54, 4, "Performance profiling", "Measure FPS, latency, and navigation responsiveness.", ["Measure camera FPS and YOLO inference time.", "Measure gesture message rate from ESP32 to ROS2.", "Check CPU/GPU/RAM usage during full demo.", "Reduce image size, model size, or frequency where needed."], "A performance table with before/after optimization notes.", ["ultralyticsPython", "onnxRuntime", "liteRtMicro"], ["courseTinyML", "courseRosComplete"], ["ytTfliteEsp32", "ytYoloRos"]),
  day(55, 4, "Reliability and parameter tuning", "Smooth the system so the demo feels intentional.", ["Tune Nav2 costmaps and controller parameters.", "Tune visual servoing gains and safety stop thresholds.", "Add node restart notes and launch failure messages.", "Run three clean demos back-to-back."], "Three consecutive successful full-system runs and a final parameter set.", ["nav2Tutorials", "rosParams", "rqtConsole"], ["courseNav2", "courseRosComplete"], ["ytNav2", "ytVisualServo"]),
  day(56, 4, "Demo storyboard and capture", "Record the project in a way recruiters can understand quickly.", ["Write a 90-120 second demo storyboard.", "Capture Gazebo, RViz2, terminal, and ESP32 footage.", "Show the cause-effect chain: perception, navigation, edge command.", "Keep failed takes and note lessons for the write-up."], "Raw demo footage and a selected storyboard for the final video.", ["githubReadme", "drawio"], ["courseRosComplete"], ["ytSearchDemo"]),
  day(57, 4, "Documentation and setup guide", "Make the project runnable by someone else.", ["Write the main README with architecture, install, launch, and demo steps.", "Add diagrams, screenshots, and known limitations.", "Create a hardware checklist and software version table.", "Verify commands from a clean terminal where possible."], "A portfolio-grade README with diagrams, screenshots, and exact commands.", ["githubReadme", "rosInstall", "gazeboInstall"], ["courseRosBeginners", "courseRosComplete"], ["ytConstruct"]),
  day(58, 4, "Portfolio article and learning story", "Convert 60 days of work into a clear professional narrative.", ["Draft a LinkedIn article or blog post about the project arc.", "Explain why simulation-first and hardware-light was the right choice.", "Show architecture and key tradeoffs, not only screenshots.", "Link to the repo, demo video, and daily progress thread."], "A polished long-form write-up that frames VisioBot as AI-robotics engineering.", ["githubReadme", "drawio"], ["courseRosComplete"], ["ytSearchDemo"]),
  day(59, 4, "GitHub polish and release prep", "Make the repository feel finished.", ["Clean branches, issues, and stale experiment files.", "Add example commands, screenshots, and sample outputs.", "Tag a v1.0 or final-challenge release if appropriate.", "Ask a peer to follow the README and note confusing parts."], "A tidy release-ready GitHub repo with final docs and demo links.", ["githubReadme", "rosTutorials"], ["courseRosComplete"], ["ytSearchDemo"]),
  day(60, 4, "Final showcase post", "Publish the final outcome and make the work discoverable.", ["Post the demo video and repo link.", "Write a concise thread covering ROS2, Gazebo, YOLO, micro-ROS, and TinyML.", "Mention concrete metrics: FPS, map success, gesture latency, final package count.", "Archive lessons learned and next steps for the next project."], "A final public showcase package: video, repo, article, and summary post.", ["githubReadme", "drawio", "nav2Tutorials"], ["courseRosComplete", "courseTinyML"], ["ytSearchDemo"])
];

const SOURCE_GROUPS = [
  {
    title: "Local docs analyzed",
    links: [
      ["Gemini research roadmap V2", "docs/Gemini_Reasearch_Roadmap_V2.md"],
      ["Deep research report", "docs/deep-research-report.md"],
      ["Existing VisioBot interactive roadmap", "docs/visiobot_60_day_interactive_roadmap.html"],
      ["60-Day Learning Challenge PDF", "docs/60-Day%20Learning%20Challenge%20Roadmap.pdf"]
    ]
  },
  {
    title: "Official web references",
    links: [
      ["ROS 2 Jazzy docs", LINKS.rosTutorials[2]],
      ["Gazebo Harmonic ROS install", LINKS.gazeboInstall[2]],
      ["Nav2 tutorials", LINKS.nav2Tutorials[2]],
      ["Ultralytics Python docs", LINKS.ultralyticsPython[2]],
      ["Google LiteRT Micro", LINKS.liteRtMicro[2]],
      ["Edge Impulse ESP32", LINKS.edgeImpulseEsp32[2]],
      ["micro-ROS Arduino", LINKS.microRosArduino[2]]
    ]
  },
  {
    title: "Courses and video anchors",
    links: [
      ["ROS 2 for Beginners - Udemy", LINKS.courseRosBeginners[2]],
      ["ROS 2 Jazzy Complete Robotics Developer - Udemy", LINKS.courseRosComplete[2]],
      ["The Construct Jazzy Learning Week", LINKS.courseConstruct[2]],
      ["Practical Edge AI and TinyML - Udemy", LINKS.courseTinyML[2]],
      ["The Construct ROS2 Jazzy Crash Course", LINKS.ytConstruct[2]],
      ["micro-ROS Jazzy Arduino ESP32 S3", LINKS.ytMicroRos[2]]
    ]
  }
];

let selectedPhase = "all";
let selectedDay = 1;
let searchTerm = "";
let progress = loadProgress();

function day(dayNumber, phase, title, focus, tasks, deliverable, resources, courses, videos) {
  return {
    day: dayNumber,
    phase: String(phase),
    title,
    focus,
    tasks,
    deliverable,
    resources,
    courses,
    videos,
    tags: title.toLowerCase().split(/[^a-z0-9+#]+/).filter(Boolean)
  };
}

function loadProgress() {
  try {
    return JSON.parse(localStorage.getItem("visiobot-progress-v1")) || {};
  } catch (_error) {
    return {};
  }
}

function saveProgress() {
  localStorage.setItem("visiobot-progress-v1", JSON.stringify(progress));
}

function taskKey(dayNumber, index) {
  return `d${dayNumber}-t${index}`;
}

function isTaskDone(dayNumber, index) {
  return Boolean(progress[taskKey(dayNumber, index)]);
}

function isDayComplete(item) {
  return item.tasks.every((_task, index) => isTaskDone(item.day, index));
}

function phaseFor(id) {
  return PHASES.find((phase) => phase.id === id) || PHASES[0];
}

function filteredDays() {
  const query = searchTerm.trim().toLowerCase();
  return DAYS.filter((item) => {
    const inPhase = selectedPhase === "all" || item.phase === selectedPhase;
    if (!inPhase) return false;
    if (!query) return true;
    const haystack = [
      item.day,
      item.title,
      item.focus,
      item.deliverable,
      item.tasks.join(" "),
      item.resources.concat(item.courses, item.videos).map((id) => LINKS[id]?.[1] || "").join(" ")
    ].join(" ").toLowerCase();
    return haystack.includes(query);
  });
}

function renderPhaseButtons() {
  const container = document.getElementById("phaseButtons");
  container.innerHTML = PHASES.map((phase) => `
    <button class="phase-button ${phase.id === selectedPhase ? "is-active" : ""}" style="--phase-color:${phase.color}" data-phase="${phase.id}" type="button">
      <span class="phase-dot"></span>
      <span>${phase.label}</span>
      <small>${phase.range}</small>
    </button>
  `).join("");
  container.querySelectorAll("button").forEach((button) => {
    button.addEventListener("click", () => {
      selectedPhase = button.dataset.phase;
      const visible = filteredDays();
      selectedDay = visible[0]?.day || selectedDay;
      renderAll();
    });
  });
}

function renderDayList() {
  const list = document.getElementById("dayList");
  const visible = filteredDays();
  if (!visible.length) {
    list.innerHTML = `<div class="empty-state"><i data-lucide="search-x"></i><p>No matching days found.</p></div>`;
    renderEmptyDetail();
    return;
  }
  if (!visible.some((item) => item.day === selectedDay)) {
    selectedDay = visible[0].day;
  }
  list.innerHTML = visible.map((item) => {
    const phase = phaseFor(item.phase);
    const complete = isDayComplete(item);
    return `
      <button class="day-button ${item.day === selectedDay ? "is-active" : ""} ${complete ? "is-complete" : ""}" style="--phase-color:${phase.color}" data-day="${item.day}" type="button">
        <span class="day-num">${item.day}</span>
        <span>
          <h3>${item.title}</h3>
          <p>${phase.label}</p>
        </span>
        <span class="completion-dot" aria-hidden="true"></span>
      </button>
    `;
  }).join("");
  list.querySelectorAll("button").forEach((button) => {
    button.addEventListener("click", () => {
      selectedDay = Number(button.dataset.day);
      renderDayList();
      renderDetail();
    });
  });
}

function renderDetail() {
  const item = DAYS.find((entry) => entry.day === selectedDay);
  if (!item) {
    renderEmptyDetail();
    return;
  }
  const phase = phaseFor(item.phase);
  const previous = Math.max(1, item.day - 1);
  const next = Math.min(60, item.day + 1);
  const doneCount = item.tasks.filter((_task, index) => isTaskDone(item.day, index)).length;
  document.getElementById("dayDetail").style.setProperty("--phase-color", phase.color);
  document.getElementById("dayDetail").innerHTML = `
    <div class="detail-topline">
      <span class="badge phase"><i data-lucide="route"></i>Phase ${item.phase}</span>
      <span class="badge"><i data-lucide="calendar-days"></i>Day ${item.day}</span>
      <span class="badge"><i data-lucide="check-check"></i>${doneCount}/${item.tasks.length} tasks</span>
    </div>
    <div class="detail-heading">
      <div>
        <h2>${item.title}</h2>
        <p>${item.focus}</p>
      </div>
      <div class="detail-nav">
        <button class="nav-button" type="button" data-go="${previous}" ${item.day === 1 ? "disabled" : ""}><i data-lucide="arrow-left"></i>Prev</button>
        <button class="nav-button" type="button" data-go="${next}" ${item.day === 60 ? "disabled" : ""}>Next<i data-lucide="arrow-right"></i></button>
      </div>
    </div>
    <div class="detail-block">
      <h3>Daily tasks</h3>
      <div class="task-list">
        ${item.tasks.map((task, index) => `
          <label class="task-row ${isTaskDone(item.day, index) ? "is-done" : ""}">
            <input class="task-check" type="checkbox" data-task="${index}" ${isTaskDone(item.day, index) ? "checked" : ""}>
            <span>${task}</span>
          </label>
        `).join("")}
      </div>
    </div>
    <div class="detail-block">
      <h3>Deliverable</h3>
      <p class="deliverable">${item.deliverable}</p>
    </div>
    <div class="detail-block">
      <h3>Resources, courses, and YouTube guidance</h3>
      <div class="link-groups">
        ${renderLinkGroup("Resources", item.resources, "book-open")}
        ${renderLinkGroup("Courses", item.courses, "graduation-cap")}
        ${renderLinkGroup("YouTube", item.videos, "play-circle")}
      </div>
    </div>
    <div class="detail-block">
      <h3>Learning rhythm</h3>
      <div class="mini-plan">
        <div><strong>Study</strong><span>Read/watch the primary resource before coding.</span></div>
        <div><strong>Build</strong><span>Implement the smallest working version first.</span></div>
        <div><strong>Verify</strong><span>Use CLI tools, RViz2, logs, or serial output.</span></div>
        <div><strong>Document</strong><span>Commit code plus one screenshot, note, or metric.</span></div>
      </div>
    </div>
  `;
  document.querySelectorAll(".task-check").forEach((checkbox) => {
    checkbox.addEventListener("change", (event) => {
      const key = taskKey(item.day, Number(event.currentTarget.dataset.task));
      if (event.currentTarget.checked) {
        progress[key] = true;
      } else {
        delete progress[key];
      }
      saveProgress();
      renderAll();
    });
  });
  document.querySelectorAll(".nav-button[data-go]").forEach((button) => {
    button.addEventListener("click", () => {
      selectedDay = Number(button.dataset.go);
      if (selectedPhase !== "all" && DAYS.find((entry) => entry.day === selectedDay)?.phase !== selectedPhase) {
        selectedPhase = "all";
      }
      renderAll();
    });
  });
}

function renderLinkGroup(title, ids, icon) {
  return `
    <div class="link-group">
      <h4>${title}</h4>
      ${ids.map((id) => {
        const link = LINKS[id];
        if (!link) return "";
        return `
          <a class="link-card" href="${link[2]}" target="_blank" rel="noreferrer">
            <i data-lucide="${icon}"></i>
            <span><strong>${link[1]}</strong><span>${link[0]}</span></span>
          </a>
        `;
      }).join("")}
    </div>
  `;
}

function renderEmptyDetail() {
  document.getElementById("dayDetail").innerHTML = `
    <div class="empty-state">
      <i data-lucide="search-x"></i>
      <p>No day selected.</p>
    </div>
  `;
}

function renderProgress() {
  const completed = DAYS.filter(isDayComplete).length;
  const percent = (completed / DAYS.length) * 100;
  document.getElementById("progressFill").style.width = `${percent}%`;
  document.getElementById("progressNote").textContent = `${completed} of ${DAYS.length} days completed`;
}

function renderSources() {
  document.getElementById("sourceGrid").innerHTML = SOURCE_GROUPS.map((group) => `
    <article class="source-card">
      <h3>${group.title}</h3>
      ${group.links.map(([label, url]) => `<a href="${url}" target="_blank" rel="noreferrer">${label}</a>`).join("")}
    </article>
  `).join("");
}

function renderAll() {
  renderPhaseButtons();
  renderDayList();
  renderDetail();
  renderProgress();
  renderSources();
  if (window.lucide) {
    window.lucide.createIcons();
  }
}

document.getElementById("searchInput").addEventListener("input", (event) => {
  searchTerm = event.target.value;
  renderAll();
});

document.getElementById("resetProgress").addEventListener("click", () => {
  progress = {};
  saveProgress();
  renderAll();
});

document.getElementById("themeToggle").addEventListener("click", () => {
  const root = document.documentElement;
  const next = root.dataset.theme === "dark" ? "light" : "dark";
  root.dataset.theme = next;
  localStorage.setItem("visiobot-theme", next);
  document.getElementById("themeToggle").innerHTML = `<i data-lucide="${next === "dark" ? "moon" : "sun"}"></i>`;
  if (window.lucide) {
    window.lucide.createIcons();
  }
});

const savedTheme = localStorage.getItem("visiobot-theme");
if (savedTheme) {
  document.documentElement.dataset.theme = savedTheme;
  document.getElementById("themeToggle").innerHTML = `<i data-lucide="${savedTheme === "dark" ? "moon" : "sun"}"></i>`;
}

renderAll();
