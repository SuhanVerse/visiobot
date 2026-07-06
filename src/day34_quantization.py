import os
import warnings

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'  
warnings.filterwarnings('ignore')

import time
import numpy as np
import tensorflow as tf
import logging

logging.getLogger('absl').setLevel(logging.ERROR)

def quantize_model(keras_model_path, quantized_tflite_path):
    print(f"Applying Post-Training INT8 Quantization...")
    model = tf.keras.models.load_model(keras_model_path)
    
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    
    # Force full INT8 representation (requires a representative dataset)
    # For this simple IMU test, we generate a small batch of random data
    def representative_dataset():
        for _ in range(100):
            data = np.random.rand(1, 128, 6).astype(np.float32)
            yield [data]
            
    converter.representative_dataset = representative_dataset
    
    # Restrict operations to INT8
    converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
    converter.inference_input_type = tf.int8
    converter.inference_output_type = tf.int8

    tflite_quant_model = converter.convert()

    with open(quantized_tflite_path, 'wb') as f:
        f.write(tflite_quant_model)
        
    print(f"Quantized model saved to: {quantized_tflite_path}")
    return os.path.getsize(quantized_tflite_path) / 1024 # KB

def benchmark_tflite(model_path, input_shape, is_int8=False, iterations=100):
    interpreter = tf.lite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    
    dtype = np.int8 if is_int8 else np.float32
    # Adjust random data range for INT8 [-128, 127] if needed, else float [0, 1)
    if is_int8:
         dummy_input = np.random.randint(-128, 127, size=input_shape, dtype=dtype)
    else:
         dummy_input = np.random.random(input_shape).astype(dtype)
    
    # Warmup
    interpreter.set_tensor(input_details[0]['index'], dummy_input)
    interpreter.invoke()
    
    latencies = []
    for _ in range(iterations):
        start_time = time.perf_counter()
        interpreter.set_tensor(input_details[0]['index'], dummy_input)
        interpreter.invoke()
        _ = interpreter.get_tensor(output_details[0]['index'])
        latencies.append((time.perf_counter() - start_time) * 1000)
        
    return np.mean(latencies)

def main():
    keras_path = 'models/tiny_imu_model.keras'
    fp32_tflite_path = 'models/tiny_imu_model.tflite'
    int8_tflite_path = 'models/tiny_imu_model_int8.tflite'
    
    standard_shape = (1, 128, 6) 
    
    # 1. Quantize the model
    int8_size = quantize_model(keras_path, int8_tflite_path)
    fp32_size = os.path.getsize(fp32_tflite_path) / 1024
    
    # 2. Benchmark Both
    print("\nRunning benchmarks...")
    fp32_latency = benchmark_tflite(fp32_tflite_path, standard_shape, is_int8=False)
    int8_latency = benchmark_tflite(int8_tflite_path, standard_shape, is_int8=True)
    
    print("\n" + "="*60)
    print(" DAY 34: INT8 QUANTIZATION BENCHMARK ")
    print("="*60)
    print(f"| {'Format':<15} | {'Data Type':<10} | {'Size (KB)':<10} | {'Avg Latency (ms)':<15} |")
    print("-" * 60)
    print(f"| {'TFLite (Base)':<15} | {'FP32':<10} | {fp32_size:<10.2f} | {fp32_latency:<15.2f} |")
    print(f"| {'TFLite (Quant)':<15} | {'INT8':<10} | {int8_size:<10.2f} | {int8_latency:<15.2f} |")
    print("="*60)

if __name__ == "__main__":
    main()
