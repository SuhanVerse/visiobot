# Day 30 Capstone: Complete Fix Reference Guide

## The 3 Issues Found & Fixed

### Issue 1: Models Not Spawning in Gazebo (Mesh Errors)

**Root Cause:** When models are downloaded from `app.gazebosim.org/OpenRobotics`, the
zip files extract to folders with human-readable names like `"Standing person"`,
`"Fire hydrant"`, `"Ambulance"`, etc. However, the `model.sdf` files inside those
folders reference the model with underscored names like `model://person_standing/...`.
Gazebo's resource resolver does an **exact string match** — it couldn't find `person_standing`
because the directory on disk was named `Standing person`.

**Fix Applied:** Created symlinks in `~/.gz/models`:
```
person_standing → Standing person
person_walking  → Walking person
fire_hydrant    → Fire hydrant
ambulance       → Ambulance
office_chair    → Office Chair
simple_desk     → Simple_desk
suv             → SUV
```

**To re-apply this fix if it gets lost:**
```bash
cd ~/.gz/models
ln -sf "Standing person" person_standing
ln -sf "Walking person"  person_walking
ln -sf "Fire hydrant"    fire_hydrant
ln -sf "Ambulance"       ambulance
ln -sf "Office Chair"    office_chair
```

---

### Issue 2: RViz2 Crash (Segfault + Syntax Error)

**Syntax Error:** The backslash `\` line-continuation doesn't work for `--ros-args`:
```bash
# ❌ WRONG — breaks argument parser
rviz2 -d /path/to/rviz.rviz \
      --ros-args -p use_sim_time:=true

# ✅ CORRECT — all on one line
rviz2 -d /opt/ros/jazzy/share/nav2_bringup/rviz/nav2_default_view.rviz --ros-args -p use_sim_time:=true
```

**Segfault:** Caused by the costmap exploding when YOLO triggered on car/truck models.
RViz2's GPU rendering thread crashed trying to draw the chaotic 1000-particle costmap.
**Fixed by switching from YOLO to ViSP** (ArUco marker detection is mathematically
guaranteed, no false positives from cars/trucks).

---

### Issue 3: Python Node Crash on Ctrl+C

**Error:** `rclpy._rclpy_pybind11.RCLError: Failed to publish: publisher's context is invalid`

**Root Cause:** The background patrol thread called `rclpy.spin()` or `self.cmd_pub.publish()`
after the main thread had already called `rclpy.shutdown()`.

**Fix Applied:** Added `threading.Event()` guard:
```python
self.is_running = threading.Event()
self.is_running.set()

# In shutdown:
node.is_running.clear()    # Signals all threads to stop
patrol_thread.join(timeout=3.0)  # Wait for thread to finish
executor.shutdown(timeout_sec=2.0)
rclpy.shutdown()
```

---

## Why ViSP > YOLO for Day 30

| Feature | YOLO (old) | ViSP visp_auto_tracker (new) |
|---------|-----------|------------------------------|
| Output | 2D bounding box (pixels) | 6D pose (X, Y, Z in **meters**) |
| Distance | Estimated: `target_height = 120px` | Exact: `pose.position.z` in meters |
| False positives | Detects cars, trucks, chairs | Only detects ArUco marker pattern |
| Nav2 spin trigger | Yes (too close → costmap panic) | No (stops at exactly 1.0m) |
| Shutdown safety | Crashed with RCLError | Clean with `threading.Event()` |

---

## How to Run Day 30

### Step 1: Install ViSP + Build
```bash
sudo apt install -y ros-jazzy-visp libdmtx-dev libzbar-dev
cd ~/visiobot
colcon build --symlink-install --packages-select visiobot_vision visp_bridge visp_tracker visp_auto_tracker
source install/setup.bash
```

### Step 2: Launch
```bash
ros2 launch visiobot_vision day30_capstone.launch.py
```

### Step 3: RViz2 (in a new terminal)
```bash
cd ~/visiobot && source install/setup.bash
rviz2 -d /opt/ros/jazzy/share/nav2_bringup/rviz/nav2_default_view.rviz --ros-args -p use_sim_time:=true
```

### Step 4: Spawn Target in Gazebo
1. In Gazebo → Click the **Resource Spawner** (box icon on right panel)
2. Open **Local resources** → expand `~/.gz/models`
3. Drag **`aruco_id1_box`** from `visiobot/src/visiobot_core/models` 
   OR from your `~/.gz/models` path into the scene
4. Watch the terminal — the robot will print:
   ```
   >>> ArUco Marker acquired by ViSP! <<<
   >>> Triggering Nav2 preemption → PBVS APPROACH <<<
   ```

### Step 5: Camera Feed (annotated)
```bash
ros2 run rqt_image_view rqt_image_view /visp_auto_tracker/image_tracked
```

---

## State Machine Reference

```
┌─────────────┐    ViSP detects ArUco     ┌─────────────┐
│   PATROL    │ ─────────────────────────▶ │    SERVO    │
│  Nav2 drives│                            │ PBVS drives │
│  waypoints  │ ◀────────────────────────  │  by /cmd_vel│
└─────────────┘  Target lost (3s timeout)  └──────┬──────┘
       ▲                                          │
       │                                          │ Z < 1.05m
       │                                          ▼
       │                                   ┌─────────────┐
       └────────────── 12s elapsed ──────── │  COOLDOWN   │
                                            │ Camera off  │
                                            └─────────────┘
```
