import os
import warnings

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'  
warnings.filterwarnings('ignore')

import time
import numpy as np
import tensorflow as tf
import tf2onnx
import onnxruntime as ort

def convert_keras_to_onnx(keras_path, onnx_path):
    print(f"Converting {keras_path} to ONNX...")
    model = tf.keras.models.load_model(keras_path)
    
    spec = (tf.TensorSpec((None, 128, 6), tf.float32, name="input"),)
    
    @tf.function
    def inference(inputs):
        return model(inputs)
        
    # Convert and save using from_function
    model_proto, _ = tf2onnx.convert.from_function(
        inference, 
        input_signature=spec, 
        output_path=onnx_path
    )
    print(f"ONNX model saved to: {onnx_path}")
    return os.path.getsize(onnx_path) / 1024 # KB

def benchmark_onnx_model(model_path, input_shape, iterations=100):
    print(f"Loading ONNX model: {model_path}")
    session = ort.InferenceSession(model_path, providers=['CPUExecutionProvider'])
    input_name = session.get_inputs()[0].name
    
    dummy_input = np.random.random(input_shape).astype(np.float32)
    
    # Warmup
    session.run(None, {input_name: dummy_input})
    
    print(f"Running {iterations} ONNX inferences...")
    latencies = []
    for _ in range(iterations):
        start_time = time.perf_counter()
        session.run(None, {input_name: dummy_input})
        latencies.append((time.perf_counter() - start_time) * 1000)
        
    return np.mean(latencies)

def benchmark_tflite_model(model_path, input_shape, iterations=100):
    interpreter = tf.lite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    
    dummy_input = np.random.random(input_shape).astype(np.float32)
    
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
    keras_model_path = 'models/tiny_imu_model.keras'
    tflite_model_path = 'models/tiny_imu_model.tflite'
    onnx_model_path = 'models/tiny_imu_model.onnx'
    
    standard_shape = (1, 128, 6) 
    
    # 1. Convert to ONNX
    onnx_size = convert_keras_to_onnx(keras_model_path, onnx_model_path)
    
    # 2. Benchmark ONNX
    onnx_latency = benchmark_onnx_model(onnx_model_path, standard_shape)
    
    # 3. Benchmark TFLite
    tflite_latency = benchmark_tflite_model(tflite_model_path, standard_shape)
    tflite_size = os.path.getsize(tflite_model_path) / 1024
    
    print("\n" + "="*55)
    print(" DAY 33: RUNTIME COMPARISON (ONNX vs TFLite) ")
    print("="*55)
    print(f"| {'Format':<15} | {'Size (KB)':<12} | {'Avg Latency (ms)':<17} |")
    print("-" * 55)
    print(f"| {'ONNX (CPU)':<15} | {onnx_size:<12.2f} | {onnx_latency:<17.2f} |")
    print(f"| {'TFLite (CPU)':<15} | {tflite_size:<12.2f} | {tflite_latency:<17.2f} |")
    print("="*55)

if __name__ == "__main__":
    main()
