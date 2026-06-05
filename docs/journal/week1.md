# Week 1: Core ROS2 Programming

## Day 1
**Goal:** Install ROS2 Jazzy and create the workspace.
**Progress:** Set up Ubuntu 24.04 environment. Colcon build works.
**Roadblocks:** Encountered a locale issue, fixed it by running the UTF-8 config steps.

## Day 2
**Goal:** Write publisher node in Python.
**Progress:** Set up ROS2 workspace for my VisioBot project. Created a simple publisher node that publishes a string message every second and build this package using `colcon build --symlink-install`.
**Roadblocks:** Had some issues with the ROS2 environment setup, but resolved them by sourcing the setup script correctly and also encountered package license issues (Apache-2.0).

## Day 3
**Goal:** Write Listener node in Python.
**Progress:** Created a subscriber node that listens to the topic published by the publisher node and prints the received messages to the console. Successfully ran both nodes and verified that the communication works as expected.


## Day 4
**Goal:** C++ nodes with rclcpp.
**Progress:** Implemented the same publisher and subscriber nodes in C++ that I have previously implemented in Python. (rclcpp)

## Day 5: Custom Interfaces and Services
**Date:** June 5, 2026
**Objective:** Transition from continuous Topic broadcasts (pub/sub) to synchronous Request-Response calls using ROS2 Services.

**Tasks Completed:**
* **Created a Custom Interface Package:** Generated an `ament_cmake` package named `visiobot_interfaces` strictly for holding `.msg` and `.srv` files.
* **Defined a Custom Service:** Built `SetMode.srv`, configuring the request payload (`string mode`) and the response payload (`bool success`, `string message`).
* **Configured Interface Build Architecture:** Updated `package.xml` and `CMakeLists.txt` using `rosidl_default_generators` to ensure ROS2 properly compiles the custom service into usable C++ and Python headers.
* **Built a Python Service Server:** Authored `mode_service.py` inside `visiobot_core` to act as the server. It listens for requested modes (e.g., patrol, standby) and returns a success boolean and validation string.
* **CLI Verification:** Successfully tested the synchronous loop without building a separate client node by using `ros2 service call /set_mode visiobot_interfaces/srv/SetMode "{mode: 'patrol'}"` directly from the terminal.

**Key Takeaway:**
While Topics are ideal for continuous data streams like sensor telemetry, Services provide a crucial mechanism for triggering specific state changes or actions within the robot's architecture where confirmation of execution is required.



## Day 6
**Goal:** Actions for long-running robot goals
**Progress:** ...