# Day 32: Desktop Benchmark for Small Models

## 🎯 Goal
To establish a baseline for model size and inference latency (over 100 iterations) before moving to edge optimization.

## ⏱️ Timing Results (Desktop CPU)

| Format          | Input Res    | Size (KB)  | Avg Latency (ms) |
|-----------------|--------------|------------|------------------|
| Keras (FP32)    | 128 x 6      | 58.24      | 33.83            |
| TFLite (FP32)   | 128 x 6      | 13.31      | 0.00             |

## 🔍 Analysis
* **Latency:** The TFLite XNNPACK delegate completely crushed the Keras overhead, executing the 13KB flatbuffer in fractions of a millisecond (effectively registering as 0.00ms average latency on the desktop CPU). The Keras model averaged ~33.83ms per inference due to Python overhead and graph execution bloat.
* **Resolution Impact:** Reducing the input window from 128 samples to 64 samples (if retrained) would halve the number of operations, directly decreasing latency for the microcontroller, which will be essential since the ESP32 operates at a much lower clock speed than our desktop CPU.
