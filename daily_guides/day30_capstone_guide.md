# Day 30: Phase 2 Capstone — Find and Approach

**Phase 2 | Day 30 | 4/4 tasks**

> Deliverable: A recorded demo of VisioBot finding, tracking, and approaching a visual target.

---

## 📋 Daily Tasks (All Complete)

- [x] **Task 1:** Populate Gazebo with a target object (textured "Person" model from resource spawner)
- [x] **Task 2:** Launch the full perception stack with annotated image output (`/camera/yolo/overlay_image`)
- [x] **Task 3:** Patrol waypoints until the target appears
- [x] **Task 4:** Approach and stop near the target, then write a phase report

---

## 🏗️ Final Architecture

```
Gazebo (Harmonic)
  ├── VisioBot Robot (URDF)
  ├── async_slam_toolbox → /map (dynamic, no pre-saved map)
  └── ros_gz_bridge → /scan, /odom, /tf, /cmd_vel, /camera/image_raw

Nav2 Navigation Stack
  ├── controller_server  (DWB local planner)
  ├── planner_server     (NavFn global planner)
  ├── bt_navigator       (Behavior Tree orchestrator)
  └── Rolling-window global costmap (day28_nav2_params.yaml)

Perception Stack
  ├── yolo_detector      (YOLOv8n.pt → /yolo/detections)
  └── image_overlay_node (draws bboxes → /camera/yolo/overlay_image)

day30_capstone_node  [The Brain]
  ├── Background Thread: HandoffNode (YOLO sub + IBVS servo_timer)
  └── Main Thread: BasicNavigator patrol (goToPose per waypoint)
```

---

## 🧠 State Machine

| State | Controller | Trigger to Next |
|-------|-----------|----------------|
| `PATROL` | Nav2 `goToPose()` | YOLO detects object with conf > 0.60 |
| `APPROACH` | IBVS via `/cmd_vel` | BBox height ≥ 120px (target reached) OR 3s timeout |
| `COOLDOWN` | Nav2 resumes | 10 seconds elapsed (camera re-enabled) |

### Why 120px target height?
Stopping at 120px means the robot is ~1–2m from the target. This gives Nav2's local costmap enough free space to plan a smooth exit path when COOLDOWN ends, preventing the infamous "Nav2 spinning in recovery" behavior.

---

## 🚀 How to Run

### Terminal 1 — Launch everything
```bash
cd ~/visiobot
source install/setup.bash
ros2 launch visiobot_vision day30_capstone.launch.py
```

### Terminal 2 — View annotated YOLO camera feed
```bash
cd ~/visiobot && source install/setup.bash
ros2 run rqt_image_view rqt_image_view /camera/yolo/overlay_image
```

### Terminal 3 — RViz2 (time-synced)
```bash
cd ~/visiobot && source install/setup.bash
rviz2 -d /opt/ros/jazzy/share/nav2_bringup/rviz/nav2_default_view.rviz \
      --ros-args -p use_sim_time:=true
```

> **Spawn a target:** In Gazebo, use the Resource Spawner and search for **"Rescue Squad Person"** or **"Walking Person"** — textured models that YOLOv8 can detect. Untextured grey shapes will not be detected.

---

## 📺 Expected Terminal Output

```
[day30_capstone_node] === Patrol loop #1 ===
[day30_capstone_node] Heading to Waypoint 1/3: (1.5, 0.0)
[bt_navigator]        Begin navigating from current location (-0.00, -0.00) to (1.50, 0.00)
[day30_capstone_node]   ✓ Waypoint 1 reached.
[day30_capstone_node] Heading to Waypoint 2/3: (1.5, 1.5)
...

[day30_capstone_node] >>> TARGET DETECTED: [person_1] (conf=0.87) — Triggering Handoff! <<<
[day30_capstone_node] >>> Handoff triggered! Canceling Nav2 task! <<<
... (robot visually servos toward person)
[day30_capstone_node] >>> TARGET REACHED! Final alignment complete. Robot stopped. <<<
[day30_capstone_node] COOLDOWN: Ignoring camera for 10.0s to allow Nav2 to safely drive away...
... (10 seconds pass)
[day30_capstone_node] COOLDOWN FINISHED. Camera memory cleared. Resuming active patrol!
[day30_capstone_node] === Patrol loop #2 ===
```

---

## 🐛 Bugs Fixed During Phase 2

| # | Bug | Root Cause | Fix Applied |
|---|-----|-----------|-------------|
| 1 | `isTaskComplete()` TypeError | Jazzy API mismatch | Removed `task=` keyword arg |
| 2 | "Malformed map" error | Static layer rejected SLAM's dynamic map | Rolling window global costmap |
| 3 | "Robot out of bounds" | Rolling costmap origin not at robot | Rolling window = always robot-centered |
| 4 | Patrol loop #1 instant success | Last waypoint `(0,0)` = starting position | Removed origin from waypoint list |
| 5 | `Failed to make progress` | `goThroughPoses` confused near-origin | Switched to sequential `goToPose()` |
| 6 | "Goldfish memory" / target fixation loop | No state memory after APPROACH | Added `COOLDOWN` state (10s blind period) |
| 7 | Nav2 spinning in recovery after approach | Robot too close to obstacle (300px) | Reduced `target_height` to 120px |
| 8 | RViz2 robot teleporting | RViz2 using real clock, Nav2 on sim clock | Added `--ros-args -p use_sim_time:=true` |

---

## 📂 Files

| File | Purpose |
|------|---------|
| `visiobot_vision/day30_capstone_node.py` | Phase 2 Capstone brain |
| `launch/day30_capstone.launch.py` | Master launch file |
| `config/day28_nav2_params.yaml` | Rolling-window Nav2 config |
| `visiobot_vision/yolo_detector.py` | YOLOv8 + SORT tracker |
| `visiobot_vision/image_overlay_node.py` | Annotated image publisher |

---

## 📝 Phase 2 Report

**Phase 2: Vision + Control (Days 18–30)** demonstrated the full pipeline from raw sensor data to autonomous behavior decisions.

Key milestones:
- **Days 18–22**: Camera calibration, YOLO detection, SORT multi-object tracking, ArUco marker pose estimation, event-driven perception
- **Days 23–25**: Depth estimation (monocular), camera-LiDAR fusion, PointCloud2 filtering
- **Days 26–27**: Visual servoing theory (IBVS) and implementation
- **Days 28–29**: Waypoint patrol with Nav2, YOLO-to-Nav2 target handoff
- **Day 30**: Phase 2 Capstone — fully integrated Find and Approach system

The capstone demonstrates that VisioBot can now:
1. Navigate autonomously using a dynamically-built SLAM map
2. Detect and track objects using computer vision
3. Make intelligent decisions to interrupt its mission, approach a target, and safely resume patrol

*Next: **Phase 3 — Edge AI + micro-ROS** (Days 31–45)*
