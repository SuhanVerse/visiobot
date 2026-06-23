import cv2
import torch
import time
import numpy as np
from transformers import pipeline
from PIL import Image

def process_depth_map(depth_output):
    """Helper function to convert pipeline output to an Inferno colormap"""
    depth_map = np.array(depth_output["depth"])
    depth_normalized = cv2.normalize(
        depth_map, None, 0, 255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    return cv2.applyColorMap(depth_normalized, cv2.COLORMAP_INFERNO)

device = 0 if torch.cuda.is_available() else -1

image_path = "1.png"
print(f"Loading downloaded image: '{image_path}'...")
frame = cv2.imread(image_path)

if frame is None:
    print(
        f"Failed to load image. Make sure you downloaded an image and named it '{image_path}' in this folder!")
    exit()

image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
pil_image = Image.fromarray(image_rgb)


print("\nLoading Depth Anything V2 (Small)...")
pipe_small = pipeline(task="depth-estimation",
                      model="depth-anything/Depth-Anything-V2-Small-hf", device=device)

print("Running Small model inference...")
_ = pipe_small(pil_image)

start_time = time.time()
depth_output_small = pipe_small(pil_image)
small_time = time.time() - start_time
small_fps = 1.0 / small_time


print("\nLoading Depth Anything V2 (Base)...")
pipe_base = pipeline(task="depth-estimation",
                     model="depth-anything/Depth-Anything-V2-Base-hf", device=device)

print("Running Base model inference...")
_ = pipe_base(pil_image)

start_time = time.time()
depth_output_base = pipe_base(pil_image)
base_time = time.time() - start_time
base_fps = 1.0 / base_time


print("\n" + "="*50)
print("** BENCHMARK RESULTS (Same Image) **")
print(f"Small Model : {small_time:.4f} seconds ({small_fps:.2f} FPS)")
print(f"Base Model  : {base_time:.4f} seconds ({base_fps:.2f} FPS)")
print("="*50 + "\n")


colormap_small = process_depth_map(depth_output_small)
colormap_base = process_depth_map(depth_output_base)

max_height = 600
h, w = frame.shape[:2]
if h > max_height:
    scale = max_height / h
    new_w = int(w * scale)
    frame = cv2.resize(frame, (new_w, max_height))
    colormap_small = cv2.resize(colormap_small, (new_w, max_height))
    colormap_base = cv2.resize(colormap_base, (new_w, max_height))

font = cv2.FONT_HERSHEY_SIMPLEX
cv2.putText(frame, "Original", (10, 30), font,
            1, (255, 255, 255), 2, cv2.LINE_AA)
cv2.putText(colormap_small, f"Small ({small_fps:.1f} FPS)",
            (10, 30), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
cv2.putText(colormap_base, f"Base ({base_fps:.1f} FPS)",
            (10, 30), font, 1, (255, 255, 255), 2, cv2.LINE_AA)

combined = np.hstack((frame, colormap_small, colormap_base))

cv2.imwrite("depth_comparison_output.jpg", combined)
print("Saved visualization to 'depth_comparison_output.jpg'. This will look great on your timeline!")
