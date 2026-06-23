import cv2
import torch
import time
import numpy as np
from transformers import pipeline
from PIL import Image

print("Loading Depth Anything V2 (Base)...")
# Automatically use your NVIDIA GPU if PyTorch is configured for it
device = 0 if torch.cuda.is_available() else -1

# Load the pipeline
pipe = pipeline(task="depth-estimation",
                model="depth-anything/Depth-Anything-V2-Base-hf", device=device)

print("Capturing sample image from webcam...")
cap = cv2.VideoCapture(0)
# Warm up the camera
for _ in range(5):
    cap.read()
ret, frame = cap.read()
cap.release()

if not ret:
    print("Failed to grab webcam frame. Please check camera permissions.")
    exit()

# Convert BGR (OpenCV) to RGB (PIL)
image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
pil_image = Image.fromarray(image_rgb)

print("Running inference benchmark...")
# Run once to warm up the GPU/CPU
_ = pipe(pil_image)

# Actual benchmark run
start_time = time.time()
depth_output = pipe(pil_image)
end_time = time.time()

# Extract and process the depth map
depth_map = np.array(depth_output["depth"])

# Normalize to 0-255 for visualization
depth_normalized = cv2.normalize(
    depth_map, None, 0, 255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
# Apply a heatmap color scheme (Inferno looks great for depth)
depth_colormap = cv2.applyColorMap(depth_normalized, cv2.COLORMAP_INFERNO)

inference_time = end_time - start_time
print("\n" + "="*40)
print(f"Benchmark Complete!")
print(f"Inference Time: {inference_time:.4f} seconds")
print(f"Estimated FPS: {1.0 / inference_time:.2f} FPS")
print("="*40 + "\n")

# Stack the original image and depth map side-by-side
combined = np.hstack((frame, depth_colormap))
cv2.imwrite("depth_test_output.jpg", combined)
print("Saved visualization to '~/depth_test_output.jpg'. Open it in your file explorer!")
