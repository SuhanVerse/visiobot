# Day 28 — Waypoint Patrol with Nav2

**Goal:** VisioBot patrols a fixed route using Nav2 while YOLO watches for targets. Every sighting is logged with the robot's map coordinates and timestamp.

---

## 📋 Daily Tasks (from Roadmap)

- [x] **Task 1:** Create a small waypoint list in map coordinates
- [x] **Task 2:** Use Nav2 Simple Commander for patrol
- [x] **Task 3:** Run YOLO in parallel with navigation
- [x] **Task 4:** Log detections with robot pose and timestamp

---

## 🏗️ Architecture

```
sim_empty.launch.py
  ├── Gazebo + robot_state_publisher
  ├── ros_gz_bridge → /scan, /odom, /tf, /cmd_vel
  └── async_slam_toolbox → /map (ONLY map source)

navigation_launch.py (Nav2 — NO AMCL, NO map server)
  ├── controller_server (DWB local planner)
  ├── planner_server (NavFn global planner)
  ├── bt_navigator (behavior tree orchestrator)
  └── behavior_server (spin, backup, wait)

day28_patrol_log_node.py
  ├── BasicNavigator (main thread) → goToPose() per waypoint
  └── YoloListener (background thread) → logs detections to CSV
```

---

## 🚀 Step-by-Step Execution

### Step 1 — Build

```bash
cd ~/visiobot
colcon build --symlink-install --packages-select visiobot_vision
source install/setup.bash
```

### Step 2 — Launch

```bash
ros2 launch visiobot_vision day28_patrol.launch.py
```

### What to Expect

| Time | Event |
|------|-------|
| 0s   | Gazebo starts |
| 5s   | Robot spawns |
| 12s  | SLAM activates → `/map` publishing |
| 15s  | Nav2 stack starts |
| 25s  | Patrol node starts |
| ~35s | `Patrol#1 → Waypoint 1/3: (1.5, 0.0)` — robot moves! |

### Expected Console Output

```
[day28_patrol_log_node] Costmaps cleared. Starting patrol!
[day28_patrol_log_node] === Starting patrol loop #1 ===
[day28_patrol_log_node] Patrol#1 → Waypoint 1/3: (1.5, 0.0)
[bt_navigator] Begin navigating to (1.50, 0.00)
[day28_patrol_log_node]   → Distance remaining: 1.32m
[day28_patrol_log_node]   ✓ Waypoint 1 reached!
[day28_patrol_log_node] Patrol#1 → Waypoint 2/3: (1.5, 1.5)
...
```

### Step 3 — Monitor (New Terminal)

```bash
cd ~/visiobot && source install/setup.bash
rviz2 -d /opt/ros/jazzy/share/nav2_bringup/rviz/nav2_default_view.rviz
```

### Step 4 — Check Logs

```bash
cat ~/.ros/day28_detections/*.csv | column -t -s ","
```

---

## 🔧 Bugs Fixed (Complete History)

| # | Error | Root Cause | Fix |
|---|-------|-----------|-----|
| 1 | `TypeError: isTaskComplete() got unexpected keyword argument 'task'` | Tutorial repo has newer API than installed Jazzy | Use old API: no `task=` param |
| 2 | `Received map message is malformed` | `static_layer` can't handle SLAM's dynamic map | Rolling window global costmap |
| 3 | `Robot is out of bounds of the costmap` | Map starts at (0,0) boundary, robot at (0,0) | Rolling window = always centered on robot |
| 4 | Loop #1 instant "success" without moving | Last waypoint (0,0) = robot's start position | Removed origin from waypoints |
| 5 | `Failed to make progress` | `goThroughPoses` confused by near-origin goals | Use `goToPose()` per waypoint (sequential) |

---

## 📂 Files

| File | Purpose |
|------|---------|
| `src/visiobot_vision/visiobot_vision/day28_patrol_log_node.py` | Patrol + YOLO logging |
| `src/visiobot_vision/launch/day28_patrol.launch.py` | Launch file |
| `src/visiobot_vision/config/day28_nav2_params.yaml` | SLAM-friendly Nav2 config |
| `daily_guides/day28_waypoint_patrol_guide.md` | This guide |

---

## 🔗 References

- [Nav2 Simple Commander API](https://docs.nav2.org/commander_api/index.html)
- `~/visiobot/tutorials/navigation2-main/nav2_simple_commander/nav2_simple_commander/demo_security.py`
- `~/visiobot/tutorials/ROS2-Autonomous-Driving-and-Navigation-SLAM-with-TurtleBot3-master/autonomous_tb3/autonomous_tb3/maze_solver.py`

---

*Next: **Day 29** — YOLO-to-Nav2 Target Handoff*
