import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from ultralytics import YOLO


class YoloDetector(Node):
    def __init__(self):
        super().__init__('yolo_detector')

        # Initialize YOLOv8 model
        self.get_logger().info("Loading YOLOv8 model...")
        self.model = YOLO('yolov8n.pt')
        self.get_logger().info("Model loaded successfully.")

        # Subscribe to raw camera feed
        self.subscription = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10
        )

        # Publisher for annotated debug image
        self.publisher = self.create_publisher(
            Image,
            '/camera/yolo/debug_image',
            10
        )

        self.br = CvBridge()
        self.get_logger().info("YOLO Detector Node has been started.")

    def image_callback(self, data):
        try:
            # 1. Convert ROS Image message to OpenCV image
            current_frame = self.br.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            self.get_logger().error(f"Failed to convert image: {e}")
            return

        # 2. Run YOLOv8 inference
        results = self.model.predict(
            source=current_frame, conf=0.15, verbose=False)

        # 3. Process results
        if len(results) > 0:
            result = results[0]

            # Log detected classes and confidences
            for box in result.boxes:
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                cls_name = self.model.names[cls_id]
                self.get_logger().info(
                    f"Detected: {cls_name} with confidence: {conf:.2f}")

            # 4. Annotate image using Ultralytics plot()
            annotated_frame = result.plot()
        else:
            annotated_frame = current_frame

        try:
            # 5. Convert OpenCV image back to ROS Image message
            img_msg = self.br.cv2_to_imgmsg(annotated_frame, "bgr8")
            img_msg.header = data.header  # Preserve original timestamp and frame_id

            # 6. Republish annotated frame
            self.publisher.publish(img_msg)
        except CvBridgeError as e:
            self.get_logger().error(
                f"Failed to convert back to ROS message: {e}")


def main(args=None):
    rclpy.init(args=args)
    yolo_detector = YoloDetector()
    try:
        rclpy.spin(yolo_detector)
    except KeyboardInterrupt:
        pass
    finally:
        yolo_detector.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
