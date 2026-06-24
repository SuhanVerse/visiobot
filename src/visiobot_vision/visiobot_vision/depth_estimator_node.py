import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, CameraInfo
from cv_bridge import CvBridge
import cv2
import torch
import time
import numpy as np
from transformers import pipeline
from PIL import Image as PILImage

class DepthEstimatorNode(Node):
    def __init__(self):
        super().__init__('depth_estimator_node')
        self.bridge = CvBridge()

        # Load the Small model chosen from yesterday's benchmark
        self.get_logger().info("Loading Depth Anything V2 (Small)...")
        device = 0 if torch.cuda.is_available() else -1
        self.pipe = pipeline(task="depth-estimation", model="depth-anything/Depth-Anything-V2-Small-hf", device=device)
        self.get_logger().info("Model loaded successfully! Waiting for camera frames...")

        # Subscriptions
        self.image_sub = self.create_subscription(Image, '/camera/image_raw', self.image_callback, 10)
        self.info_sub = self.create_subscription(CameraInfo, '/camera/camera_info', self.info_callback, 10)

        # Publishers (One raw for processing, one color for human viewing)
        self.depth_pub = self.create_publisher(Image, '/camera/depth/image_raw', 10)
        self.depth_vis_pub = self.create_publisher(Image, '/camera/depth/image_color', 10)

        self.camera_info = None

    def info_callback(self, msg):
        # Task 3: Read camera intrinsic parameters
        # We store this matrix here so it is ready for Day 25's PointCloud projection
        self.camera_info = msg

    def image_callback(self, msg):
        start_time = time.time()

        # 1. Convert ROS Image to OpenCV, then to PIL for the AI
        cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        rgb_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        
        # Task 4: Frame-Size Tradeoffs. 
        # (Optional: Resizing 'rgb_image' here to 640x480 before converting to PIL 
        # can drastically reduce latency if your original camera feed is 1080p+).
        pil_image = PILImage.fromarray(rgb_image)

        # 2. Run Inference
        depth_output = self.pipe(pil_image)
        depth_map = np.array(depth_output["depth"])

        # 3. Normalize for ROS publishing
        # Normalize to 0-255 grayscale (mono8) for computation
        depth_normalized = cv2.normalize(depth_map, None, 0, 255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        # Apply Inferno colormap (bgr8) for RViz debugging
        depth_colormap = cv2.applyColorMap(depth_normalized, cv2.COLORMAP_INFERNO)

        # 4. Publish Depth Images
        depth_msg = self.bridge.cv2_to_imgmsg(depth_normalized, encoding='mono8')
        depth_msg.header = msg.header # CRITICAL: Keep same timestamp and frame_id!
        self.depth_pub.publish(depth_msg)

        color_msg = self.bridge.cv2_to_imgmsg(depth_colormap, encoding='bgr8')
        color_msg.header = msg.header
        self.depth_vis_pub.publish(color_msg)

        # Log FPS results
        latency = time.time() - start_time
        self.get_logger().info(f"Depth published at {1.0/latency:.1f} FPS (Latency: {latency:.3f}s)")

def main(args=None):
    rclpy.init(args=args)
    node = DepthEstimatorNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
