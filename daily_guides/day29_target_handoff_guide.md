# Day 29 — YOLO-to-Nav2 Target Handoff

**Goal:** Implement a hybrid behavior where the robot performs a waypoint patrol using Nav2, but dynamically hands off control to vision-based alignment (Visual Servoing) when a target is detected with high confidence.

---

## 📋 Daily Tasks (from Roadmap)

- [x] **Task 1:** Convert selected detections into a target approach behavior.
- [x] **Task 2:** Stop or pause Nav2 patrol when confidence threshold is met.
- [x] **Task 3:** Switch control to visual servoing for final alignment.
- [x] **Task 4:** Handle target lost, reacquired, and timeout states.

---

## 🏗️ Architecture

We created a custom `day29_target_handoff_node.py` which cleverly uses threading to manage two paradigms simultaneously:

1. **Main Thread (Nav2 Patrol):** Runs the `BasicNavigator` in a sequential `goToPose()` loop. It continuously polls `isTaskComplete()`.
2. **Background Thread (Vision Node):** Runs a standard ROS 2 Node (`HandoffNode`) that subscribes to YOLO detections and publishes to `/cmd_vel` using a `0.1s` timer loop.

### State Machine Logic

- **State: `PATROL`** 
  - Nav2 drives the robot. 
  - `HandoffNode` silently monitors YOLO detections.
  - If detection `score > 0.60`, it flags `handoff_triggered = True` and transitions to `APPROACH`.
  
- **State Transition: `PATROL` ➔ `APPROACH`**
  - Main thread detects the `handoff_triggered` flag.
  - Main thread executes `navigator.cancelTask()` to preempt Nav2.
  - Main thread goes into a sleep loop.
  
- **State: `APPROACH`**
  - `HandoffNode` uses Image-Based Visual Servoing (IBVS) with Proportional Gains to compute `Twist` messages (align target in center, move forward until bounding box is 300px tall).
  - Drives robot directly via `/cmd_vel`.
  
- **State Transition: `APPROACH` ➔ `PATROL` (Timeout)**
  - If no detection is seen for > 3.0 seconds, `HandoffNode` transitions back to `PATROL`.
  - Main thread wakes up, requests a new `goToPose()` waypoint, and Nav2 resumes the patrol!

---

## 📂 Files Created/Modified

| File | Purpose |
|------|---------|
| `src/visiobot_vision/visiobot_vision/day29_target_handoff_node.py` | Implementation of the hybrid state machine |
| `src/visiobot_vision/launch/day29_handoff.launch.py` | Day 29 launch file (uses Day 28 Nav2 params) |
| `src/visiobot_vision/setup.py` | Registered the new executable |

---

## 🚀 Step-by-Step Execution

### Step 1 — Run the Simulation and Hybrid Node

```bash
cd ~/visiobot
source install/setup.bash
ros2 launch visiobot_vision day29_handoff.launch.py
```

### Step 2 — Monitor Execution (RViz and Terminal)

```bash
# In a new terminal:
cd ~/visiobot && source install/setup.bash
rviz2 -d /opt/ros/jazzy/share/nav2_bringup/rviz/nav2_default_view.rviz
```

### Expected Behavior

1. The robot starts navigating from Waypoint A ➔ B ➔ C.
2. If an object appears in front of the camera, you will see a console warning:
   `[WARN] >>> Target [airplane_1] spotted (conf=0.98)! Triggering Handoff! <<<`
3. Nav2 will instantly halt (the task is preempted).
4. The robot will smoothly turn to center the object in its camera frame and drive towards it until the object fills the screen (Bounding Box Height = 300px).
5. If the object disappears (or you move the robot away using Gazebo's translation tool), the system will wait 3 seconds and print:
   `[WARN] >>> Target lost for 3s. Returning to PATROL! <<<`
6. Nav2 resumes and calculates a new path to its next waypoint!
