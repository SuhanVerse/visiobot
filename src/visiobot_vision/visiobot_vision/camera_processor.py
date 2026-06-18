import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
import numpy as np
import time

class CameraProcessor(Node):
    def __init__(self):
        super().__init__('camera_processor')
        
        # Subscribe to the raw camera feed
        self.subscription = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10
        )
        
        # Publishers for debug stages
        self.pub_resized = self.create_publisher(Image, '/camera/debug/resized', 10)
        self.pub_blurred = self.create_publisher(Image, '/camera/debug/blurred', 10)
        self.pub_threshold = self.create_publisher(Image, '/camera/debug/threshold', 10)
        
        # Publisher for the processed image (final output)
        self.publisher = self.create_publisher(Image, '/camera/image_processed', 10)
        
        self.br = CvBridge()
        self.last_time = time.time()
        self.get_logger().info("Camera Processor Node has been started.")

    def apply_resize(self, frame):
        # Resize to 50% for faster processing
        height, width = frame.shape[:2]
        return cv2.resize(frame, (width // 2, height // 2))

    def apply_blur(self, frame):
        # Apply Gaussian Blur to reduce noise
        return cv2.GaussianBlur(frame, (5, 5), 0)

    def apply_color_conversion(self, frame):
        # Convert to HSV color space
        return cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    def apply_threshold(self, hsv_frame):
        # Create a binary mask isolating a bright area / specific color
        lower_bound = np.array([0, 0, 200]) # High Value (brightness)
        upper_bound = np.array([180, 255, 255])
        mask = cv2.inRange(hsv_frame, lower_bound, upper_bound)
        return mask

    def image_callback(self, data):
        # FPS Tracking
        current_time = time.time()
        fps = 1.0 / (current_time - self.last_time) if (current_time - self.last_time) > 0 else 0.0
        self.last_time = current_time
        self.get_logger().info(f"FPS: {fps:.2f}")

        try:
            # 1. Convert ROS Image message to OpenCV image
            current_frame = self.br.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            self.get_logger().error(f"Failed to convert image: {e}")
            return
            
        # 2. Process image sequentially through helper functions
        # Stage 1: Resize
        resized_frame = self.apply_resize(current_frame)
        
        # Stage 2: Blur
        blurred_frame = self.apply_blur(resized_frame)
        
        # Stage 3: Color Conversion (HSV)
        hsv_frame = self.apply_color_conversion(blurred_frame)
        
        # Stage 4: Thresholding
        threshold_mask = self.apply_threshold(hsv_frame)
        
        # Prepare final output (draw targeting circle on the resized frame)
        final_frame = resized_frame.copy()
        height, width = final_frame.shape[:2]
        center = (width // 2, height // 2)
        radius = 25 # Scaled down for resized image
        color = (0, 255, 0) # Green in BGR
        thickness = 2
        cv2.circle(final_frame, center, radius, color, thickness)
        
        try:
            # 3. Publish Debug Stages
            msg_resized = self.br.cv2_to_imgmsg(resized_frame, "bgr8")
            msg_resized.header = data.header
            self.pub_resized.publish(msg_resized)
            
            msg_blurred = self.br.cv2_to_imgmsg(blurred_frame, "bgr8")
            msg_blurred.header = data.header
            self.pub_blurred.publish(msg_blurred)
            
            msg_threshold = self.br.cv2_to_imgmsg(threshold_mask, "mono8")
            msg_threshold.header = data.header
            self.pub_threshold.publish(msg_threshold)

            # Publish Final Image
            img_msg = self.br.cv2_to_imgmsg(final_frame, "bgr8")
            img_msg.header = data.header
            self.publisher.publish(img_msg)
            
        except CvBridgeError as e:
            self.get_logger().error(f"Failed to convert back to ROS message: {e}")

def main(args=None):
    rclpy.init(args=args)
    camera_processor = CameraProcessor()
    try:
        rclpy.spin(camera_processor)
    except KeyboardInterrupt:
        pass
    finally:
        camera_processor.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
