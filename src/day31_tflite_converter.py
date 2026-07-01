import os
import tensorflow as tf

def main():
    print("Day 31: LiteRT/TFLite Edge AI Conversion")
    print(f"TensorFlow Version: {tf.__version__}")
    print("-" * 50)
    
    model = tf.keras.Sequential([
        tf.keras.layers.InputLayer(input_shape=(128, 6)),
        tf.keras.layers.Conv1D(8, kernel_size=3, activation='relu'),
        tf.keras.layers.MaxPooling1D(pool_size=2),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(16, activation='relu'),
        tf.keras.layers.Dense(4, activation='softmax') # E.g., 4 gesture classes
    ])
    
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    model.summary()

    os.makedirs('models', exist_ok=True)
    keras_model_path = 'models/tiny_imu_model.keras'
    model.save(keras_model_path)
    
    # Get original model size
    keras_size_kb = os.path.getsize(keras_model_path) / 1024
    print(f"\n** Saved original Keras model: {keras_size_kb:.2f} KB")

    # 2. Convert the Model to TFLite (LiteRT Flatbuffer)
    print("\n Converting to TFLite (LiteRT Flatbuffer)...")
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    
    # Optional: Apply optimizations (Quantization) to make it even smaller for ESP32
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    
    tflite_model = converter.convert()
    
    # Save the TFLite flatbuffer
    tflite_model_path = 'models/tiny_imu_model.tflite'
    with open(tflite_model_path, 'wb') as f:
        f.write(tflite_model)
        
    tflite_size_kb = os.path.getsize(tflite_model_path) / 1024
    print(f" Saved converted TFLite model: {tflite_size_kb:.2f} KB")
    print(f" Compression Ratio: {(1 - (tflite_size_kb/keras_size_kb)) * 100:.1f}% reduction in size!")

    # 3. Output C-Array for Microcontrollers (Bonus Step for ESP32)
    # Microcontrollers need the flatbuffer compiled directly into flash memory as a C array.
    c_array_path = 'models/tiny_imu_model.cc'
    with open(c_array_path, 'w') as f:
        f.write("const unsigned char g_model[] = {\n")
        hex_array = [f"0x{b:02x}" for b in tflite_model]
        
        # Write 12 hex bytes per line
        for i in range(0, len(hex_array), 12):
            f.write("  " + ", ".join(hex_array[i:i+12]) + ",\n")
            
        f.write("};\n")
        f.write(f"const int g_model_len = {len(tflite_model)};\n")
        
    print(f" Generated C-array for ESP32 flash memory: {c_array_path}")

if __name__ == '__main__':
    main()
