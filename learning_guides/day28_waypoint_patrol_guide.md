# Day 28: Waypoint Patrol with Nav2

Welcome to **Day 28** of your 60-Day Robotics Learning Roadmap! 

## 🎯 Daily Goal
Today, we are giving VisioBot the ability to autonomously patrol an environment. Instead of reacting like a remote-control car, VisioBot will use a "brain" (the ROS 2 Navigation Stack, or **Nav2**) to calculate routes, drive to specific map coordinates, and actively scan for objects using its YOLOv8 camera along the way. Think of it as a robotic security guard!

---

## 📚 Why Learn This?
In previous days, you learned **Reactive Control** (Visual Servoing) where the robot responds to what is directly in front of it. 
Today, you learn **Global Planning**. Real-world logistics robots (like Amazon warehouse robots) don't just chase things; they are given specific destinations on a map. They calculate the best route, avoid obstacles, and execute the path. This is a foundational skill for building any professional autonomous robot.

## 🚀 How It Helps
We are using a tool called `nav2_simple_commander`. This tool takes incredibly complex math (path planning algorithms, costmaps, physical constraints) and simplifies it. 
With just a few lines of Python code, you can say `"Drive to X: 2.0, Y: 2.0"`, and the commander handles all the driving and physics in the background while your code focuses on high-level tasks like checking the camera for objects!

---

## 🛠️ Step-by-Step Execution Guide
Follow these simple instructions to install the required tools, compile the code, and run today's patrol mission!

### Step 1: Install the Brain (Nav2 Commander, Nav2 Bringup, and SLAM Toolbox)
Your system needs the simple commander package, the main Nav2 system, and SLAM Toolbox (so it can map the room while it drives!). Open a terminal and run this exact command (you may need to enter your laptop's password):
```bash
sudo apt update
sudo apt install ros-jazzy-nav2-simple-commander ros-jazzy-nav2-bringup ros-jazzy-slam-toolbox
```

### Step 2: Build the Robot's Workspace
We've added a new Python node (`day28_patrol_log_node.py`) and an updated Launch file (`day28_patrol.launch.py`). We must compile them into the ROS 2 system.
Open your terminal and run:
```bash
cd ~/visiobot
colcon build --symlink-install --packages-select visiobot_vision
```

### Step 3: Run the True Day 28 Patrol Demo!
Our **Launch File** (`day28_patrol.launch.py`) now dynamically maps the room using SLAM and turns on the Nav2 brain simultaneously!

Open one terminal and run:
```bash
cd ~/visiobot
source install/setup.bash
ros2 launch visiobot_vision day28_patrol.launch.py
```
**What will happen?**
1. Gazebo will open the 3D world.
2. The YOLO camera, SLAM Toolbox, and Nav2 will turn on.
3. After a 5-second boot delay, the robot will automatically start driving to coordinate `(2.0, 0.0)`, then to `(2.0, 2.0)`, and finally back to `(0.0, 0.0)`.
4. If you drag an object (like a fire hydrant) in front of the camera, the terminal will print an `*** ALERT: Object spotted! ***` message!

---

## 💻 Code Explanation Guide

Here is a simple breakdown of how `day28_patrol_log_node.py` works:

* **`self.navigator = BasicNavigator()`**
  This creates the "Commander" object. It connects your Python script to the complex Nav2 system running in the background.

* **`def set_waypoint(self, x, y, w):`**
  This function wraps up an X/Y map coordinate into a `PoseStamped` message format that Nav2 can understand. The `w` stands for orientation (which direction the robot should face).

* **`self.navigator.goThroughPoses(waypoints)`**
  This single command is the magic. You feed it a list of coordinates, and it commands the robot to visit every single one in order.

* **Threading (Running Two Things at Once)**
  Driving to a waypoint takes time! If we just ran the driving command, our Python script would freeze and stop checking the camera. By putting the driving command in a `threading.Thread`, the robot can drive in the background while the main script continuously checks the `yolo_callback` for new objects!

---

## 🏁 Daily Progress Report
* **Work Completed:** 
  * Wrote the Patrol Log Python node (`day28_patrol_log_node.py`).
  * Wrote the All-In-One Launch File (`day28_patrol.launch.py`) that properly boots up SLAM and Nav2.
  * Achieved the Deliverable: The robot actually moves along a patrol route while running vision checking.
* **Goal Status:** **SUCCESSFUL** ✅

* **Next Steps for Tomorrow (Day 29):** 
Currently, the YOLO alert just prints "Object spotted". Tomorrow, we will read the robot's physical location on the map using the TF (Transform) tree and log the exact coordinate where the object was found!
