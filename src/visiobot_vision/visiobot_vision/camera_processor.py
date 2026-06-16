import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2

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
        
        # Publisher for the processed image
        self.publisher = self.create_publisher(
            Image, 
            '/camera/image_processed', 
            10
        )
        
        self.br = CvBridge()
        self.get_logger().info("Camera Processor Node has been started.")

    def image_callback(self, data):
        try:
            # 1. Convert ROS Image message to OpenCV image
            current_frame = self.br.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            self.get_logger().error(f"Failed to convert image: {e}")
            return
            
        # 2. Process image
        # Convert to Grayscale
        gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
        
        # Convert back to BGR to draw colored overlays
        processed_frame = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        
        # Draw a bright green targeting circle in the center
        height, width = processed_frame.shape[:2]
        center = (width // 2, height // 2)
        radius = 50
        color = (0, 255, 0) # Green in BGR
        thickness = 2
        cv2.circle(processed_frame, center, radius, color, thickness)
        
        try:
            # 3. Convert OpenCV image back to ROS Image message
            img_msg = self.br.cv2_to_imgmsg(processed_frame, "bgr8")
            img_msg.header = data.header # Preserve original timestamp and frame_id
            
            # 4. Republish the processed frame
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
