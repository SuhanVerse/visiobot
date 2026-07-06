# Day 33: ONNX Export and Runtime Comparison

## 🎯 Goal
Keep model deployment framework-agnostic by converting a Keras model to ONNX and comparing its runtime engine against TFLite.

## ⏱️ Benchmark Results

| Format          | Size (KB)    | Avg Latency (ms) |
|-----------------|--------------|------------------|
| ONNX (CPU)      | 34.90        | 0.04             |
| TFLite (CPU)    | 13.31        | 0.01             |

## 🧠 Deployment Strategy (Which runtime fits where?)

* **Desktop / High-End Edge Linux (e.g., Jetson Nano, Raspberry Pi 5):** **ONNX** is king here. It is highly optimized for CPUs/GPUs and is the standard for taking heavy PyTorch models (like YOLO) and running them blisteringly fast on desktop hardware.
* **Microcontrollers (MCU) (e.g., ESP32, Arduino):** **TFLite / LiteRT** is required. ONNX Runtime is generally too heavy for constrained embedded devices with kilobytes of RAM (as seen by ONNX taking up roughly 2.5x more storage space than the TFLite flatbuffer). TFLite Micro excels at converting models into raw C-byte arrays that flash directly to read-only memory.
