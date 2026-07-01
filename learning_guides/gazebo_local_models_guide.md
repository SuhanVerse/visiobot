# Gazebo Local Models Guide

This guide explains how to properly download, extract, and link 3D models into your local Gazebo simulation (Harmonic/Fortress and later).

Often, downloading directly from the Gazebo GUI (using the cloud icon) can fail due to connection issues or missing dependencies. Manually managing your models locally ensures they load instantly every time.

## 1. Downloading a Model from Gazebo Fuel

1. Navigate to the official repository: [app.gazebosim.org/OpenRobotics](https://app.gazebosim.org/OpenRobotics) (or search for specific models like the Fire Hydrant or Rescue Squad Person).
2. On the model's page, click the **Download** button (the zip file icon) located near the top right of the model viewer. 
3. This will download a `.zip` file to your PC (e.g., to `~/Downloads`).

## 2. Directory Structure Setup

Gazebo doesn't automatically know where your zip files are. You need to extract them into a dedicated folder where Gazebo can find them. We use `~/.gz/models` as the standard folder for manually downloaded assets.

```bash
# Create the local models directory if it doesn't exist yet
mkdir -p ~/.gz/models
```

## 3. Extracting the Model Correctly

**Critical Rule:** Gazebo requires a specific directory structure. The `model.sdf` and `model.config` files MUST be directly inside the named folder. They cannot be buried inside subfolders.

```bash
# Unzip the downloaded file directly into a new folder named after the model
unzip ~/Downloads/fire_hydrant.zip -d ~/.gz/models/fire_hydrant
```

If you check the folder using `ls ~/.gz/models/fire_hydrant`, you should immediately see `model.sdf` and `model.config`. 

## 4. Linking Your ROS 2 Workspace Models

In addition to models downloaded from the web, you likely have models built directly into your ROS 2 packages (like your `aruco_id1_box` in `visiobot_core`). Gazebo needs to know about this folder too!

Your ROS 2 models are stored here:
`~/visiobot/src/visiobot_core/models`

## 5. Telling Gazebo Where to Look

To permanently link these folders to Gazebo, we add an environment variable called `GZ_SIM_RESOURCE_PATH` to your `~/.bashrc` file. This tells Gazebo every path it should search when looking for models.

Open your terminal and run:

```bash
echo 'export GZ_SIM_RESOURCE_PATH=$GZ_SIM_RESOURCE_PATH:~/.gz/models:~/visiobot/src/visiobot_core/models' >> ~/.bashrc
```

Apply the changes to your current terminal:
```bash
source ~/.bashrc
```

## 6. Accessing Models in Gazebo

1. Launch your simulation.
2. In the Gazebo UI, open the **Resource Spawner** panel (usually on the left side or accessible via the top-right plugin menu).
3. Click the **Local resources** dropdown.
4. You will now see two new paths listed there:
   - `~/.gz/models` (Containing your web downloads like the fire hydrant)
   - `~/visiobot/src/visiobot_core/models` (Containing `aruco_id1_box`)
5. Expand the paths and you can now drag and drop these models directly into your world instantly, entirely offline!
