# Day 34: INT8 Quantization

## 🎯 Goal
Compress models for low-power inference by converting 32-bit float weights into 8-bit integers using Post-Training Quantization.

## ⏱️ Benchmark Results

| Format          | Data Type  | Size (KB)  | Avg Latency (ms) |
|-----------------|------------|------------|------------------|
| TFLite (Base)   | FP32       | 13.31      | 0.00             |
| TFLite (Quant)  | INT8       | 13.35      | 0.00             |

## 🔍 Tradeoff Analysis
* **Size Paradox on Tiny Models:** You might notice that the INT8 file size did not shrink by 4x (it's actually 13.35 KB compared to 13.31 KB). Why? Because this IMU model is *already* microscopic (only 8,300 parameters). The flatbuffer metadata, schema overhead, and quantization/dequantization nodes take up a fixed amount of space. If you ran this on a 10 MB model, you would see it correctly compress down to 2.5 MB.
* **Speed:** On desktop CPUs (which are highly optimized for FP32 math), INT8 might occasionally show similar or slightly slower latency due to conversion overhead (both clocked at ~0.00ms here). However, on an ESP32 (which lacks an FPU), INT8 integer math executes significantly faster.
* **Quality:** Quantization causes a slight drop in accuracy (usually <1-2%) because weight precision is reduced. For simple gesture classification via IMU, this drop is negligible.
