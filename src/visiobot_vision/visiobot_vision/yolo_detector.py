import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from ultralytics import YOLO


from vision_msgs.msg import Detection2DArray, Detection2D, ObjectHypothesisWithPose

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

        # Publisher for clean detection data
        self.publisher = self.create_publisher(
            Detection2DArray,
            '/yolo/detections',
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

        # 3. Create Detection2DArray
        det_array = Detection2DArray()
        det_array.header = data.header

        # 4. Process results and populate message
        if len(results) > 0:
            result = results[0]

            for box in result.boxes:
                det = Detection2D()
                det.header = data.header

                # YOLO box.xywh returns [center_x, center_y, width, height]
                xywh = box.xywh[0]
                det.bbox.center.position.x = float(xywh[0])
                det.bbox.center.position.y = float(xywh[1])
                det.bbox.size_x = float(xywh[2])
                det.bbox.size_y = float(xywh[3])

                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                cls_name = self.model.names[cls_id]

                hyp = ObjectHypothesisWithPose()
                hyp.hypothesis.class_id = cls_name
                hyp.hypothesis.score = conf
                
                det.results.append(hyp)
                det_array.detections.append(det)

                self.get_logger().info(
                    f"Detected: {cls_name} with confidence: {conf:.2f}")

        # 5. Publish the clean data message
        self.publisher.publish(det_array)


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
