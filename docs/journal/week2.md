## Day 8
**Goal:** Launch Files and YAML parameters
**Progress:**  Today, I built a ROS2 launch file to start the entire VisioBot system with a single command. Also injected YAML parameters to change node names dynamically without recompiling.
This prevents from the multiple terminal opening problem. 

## Day 9
**Goal:** URDF model
**Progress:** Today, I finally built VisioBot's physical model and wrote its URDF kinematic model from scratch to define the chassis, wheels, and sensor mounts, then rendered the 3D robot in RViz2.


## Day 10
**Goal:** Xmacro model
**Progress:** Today, I turned VisioBot from a 3D hologram into a physics-ready machine. Used Xacro macros to auto-calculate the bot's complex mass and collision boundaries. 

## Day 11
**Goal:** Gazebo Simulation
**Progress:** ## 🎯 Objective
Move the robot from static visualization (RViz) into a full physics engine (Gazebo Harmonic) to simulate gravity, collisions, and differential drive mechanics.

## 🛠️ Tasks Completed
1. **Gazebo Integration:** Installed the `ros-jazzy-ros-gz` bridge packages to pair ROS 2 Jazzy with Gazebo Harmonic.
2. **Gazebo Plugins:** Added `<gazebo>` specific tags to the `visiobot.urdf.xacro` file. 
   - Applied Gazebo-specific material colors (Gazebo ignores standard URDF materials).
   - Attached the `gz::sim::systems::DiffDrive` plugin to simulate wheel joints and generate `odom` (odometry) and `cmd_vel` (velocity command) topics.
3. **Physics Bug Fix (KDL Parser):** Resolved the `Unable to update the pose` crash. Gazebo's physics engine cannot process inertia on the root link. Fixed this by creating a weightless, invisible `base_footprint` dummy link and attaching the heavy `base_link` to it via a fixed joint.
4. **Simulation Launch File:** Wrote `sim.launch.py` to:
   - Compile the Xacro file on the fly.
   - Start the `robot_state_publisher` with `use_sim_time` set to `True`.
   - Launch an empty Gazebo world.
   - Use the `ros_gz_sim create` node to spawn VisioBot 15cm in the air, allowing it to drop cleanly onto the floor using real physics.

## 🚀 Key Takeaways
- **Sim Time is Critical:** When running Gazebo, all ROS 2 nodes (like `robot_state_publisher`) must have the `use_sim_time` parameter set to `True` so they sync with the simulation clock rather than the computer's system clock.
- **Root Links Must Be Weightless:** Always start a URDF with a `base_footprint` link that has no `<inertial>` or `<collision>` tags to anchor the robot safely in the physics engine.


## Day 12
**Goal:** Gazebo Simulation
**Progress:** ...