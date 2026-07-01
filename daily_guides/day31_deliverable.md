# Day 31: LiteRT/TFLite Conversion Basics

## Model Overview
* **Original Model Type:** Simple 1D Convolutional Neural Network (CNN) for IMU time-series data
* **Target Hardware:** ESP32 (Microcontroller)

## Conversion Metrics
* **Input Shape:** `(1, 128, 6)` (representing 128 samples of 6-axis MPU6050 data)
* **Supported Ops:** `CONV_2D` (mapped from 1D), `MAX_POOL_2D`, `FULLY_CONNECTED`
* **Original Model Size (.keras):** 58.24 KB
* **Converted Flatbuffer Size (.tflite):** 13.31 KB (77.1% compression!)

## Memory & Operator Constraints (Notes)
* Microcontrollers lack powerful floating-point units (FPUs) and have extremely limited SRAM (usually <500KB).
* The `.tflite` flatbuffer avoids loading the entire model into RAM; instead, the microcontroller runtime maps the weights directly from read-only flash memory using a C-byte array (`.cc` file).
* Not all standard TensorFlow operators are supported on LiteRT (Micro). If an unsupported op is used, the conversion or on-device inference will fail. Keep the model architecture extremely simple (basic dense and convolutional layers).

## Hardware Required for Phase 3
Based on the `LSPPDAY60` project roadmap, the following physical electronics are mandatory:
1. **ESP32 CAM (or standard ESP32):** The edge brain running the TFLite inference.
2. **MPU6050 IMU (6-axis):** The primary sensor used to capture gesture motions.
3. **Physical Actuator:** A basic LED, a micro servo (SG90), or a motor driver to act as a physical output bridging ROS 2 to reality.
4. **Data-Capable USB Cable:** Essential for compiling/flashing the `micro-ROS` firmware over PlatformIO.
