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

## Day 5
**Goal:** Custom interfaces, services, and clients
**Progress:** ...