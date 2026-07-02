import os
import warnings

# Suppress TensorFlow logging MUST happen before tf is imported
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
warnings.filterwarnings('ignore')

import time
import numpy as np
import tensorflow as tf

# Suppress absl warnings
import logging
logging.getLogger('absl').setLevel(logging.ERROR)

def benchmark_keras_model(model_path, input_shape, iterations=100):
    print(f"Loading Keras model: {model_path}")
    model = tf.keras.models.load_model(model_path)
    
    # Generate dummy IMU data
    dummy_input = np.random.random(input_shape).astype(np.float32)
    
    # Warmup (first inference is always slow)
    model.predict(dummy_input, verbose=0)
    
    print(f"Running {iterations} inferences...")
    latencies = []
    for _ in range(iterations):
        start_time = time.perf_counter()
        model.predict(dummy_input, verbose=0)
        latencies.append((time.perf_counter() - start_time) * 1000) # Convert to ms
        
    avg_latency = np.mean(latencies)
    return avg_latency, os.path.getsize(model_path) / 1024 # Size in KB

def benchmark_tflite_model(model_path, input_shape, iterations=100):
    print(f"Loading TFLite model: {model_path}")
    interpreter = tf.lite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()
    
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    
    # Generate dummy IMU data
    dummy_input = np.random.random(input_shape).astype(np.float32)
    
    # Warmup
    interpreter.set_tensor(input_details[0]['index'], dummy_input)
    interpreter.invoke()
    
    print(f"Running {iterations} inferences...")
    latencies = []
    for _ in range(iterations):
        start_time = time.perf_counter()
        interpreter.set_tensor(input_details[0]['index'], dummy_input)
        interpreter.invoke()
        _ = interpreter.get_tensor(output_details[0]['index'])
        latencies.append((time.perf_counter() - start_time) * 1000) # Convert to ms
        
    avg_latency = np.mean(latencies)
    return avg_latency, os.path.getsize(model_path) / 1024 # Size in KB

def main():
    keras_model_path = 'models/tiny_imu_model.keras'
    tflite_model_path = 'models/tiny_imu_model.tflite'
    
    # Standard resolution shape from Day 31
    standard_shape = (1, 128, 6) 
    
    # 1. Benchmark Standard Keras (FP32)
    keras_latency, keras_size = benchmark_keras_model(keras_model_path, standard_shape)
    
    # 2. Benchmark Standard TFLite (FP32)
    tflite_latency, tflite_size = benchmark_tflite_model(tflite_model_path, standard_shape)
    
    print("\n--------------------------------------------------------------")
    print(" PERFORMANCE BENCHMARK REPORT ")
    print("--------------------------------------------------------------")
    print(f"| {'Format':<15} | {'Input Res':<12} | {'Size (KB)':<10} | {'Avg Latency (ms)':<15} |")
    print("--------------------------------------------------------------")
    print(f"| {'Keras (FP32)':<15} | {'128 x 6':<12} | {keras_size:<10.2f} | {keras_latency:<15.2f} |")
    print(f"| {'TFLite (FP32)':<15} | {'128 x 6':<12} | {tflite_size:<10.2f} | {tflite_latency:<15.2f} |")
    print("--------------------------------------------------------------\n")

if __name__ == "__main__":
    main()
