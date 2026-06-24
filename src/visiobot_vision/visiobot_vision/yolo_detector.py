import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from ultralytics import YOLO
import numpy as np
from visiobot_vision.sort import Sort


from vision_msgs.msg import Detection2DArray, Detection2D, ObjectHypothesisWithPose

import os
from ament_index_python.packages import get_package_share_directory

class YoloDetector(Node):
    def __init__(self):
        super().__init__('yolo_detector')

        # Initialize YOLOv8 model
        self.get_logger().info("Loading YOLOv8 model...")
        self.model = YOLO('yolov8n.pt')
        self.get_logger().info("Model loaded successfully.")
        
        # Initialize SORT trackers dictionary (one per class)
        self.trackers = {}

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

        # 2. Run normal YOLOv8 inference
        results = self.model.predict(
            source=current_frame, conf=0.5, verbose=False)

        # 3. Create Detection2DArray
        det_array = Detection2DArray()
        det_array.header = data.header

        # Group detections by class name
        class_detections = {}
        if len(results) > 0:
            result = results[0]
            for box in result.boxes:
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                conf = float(box.conf[0])
                cls_id = int(box.cls[0])
                cls_name = self.model.names[cls_id]

                if cls_name not in class_detections:
                    class_detections[cls_name] = []
                class_detections[cls_name].append([x1, y1, x2, y2, conf])

        # 4. Update trackers and populate message
        # Combine existing tracker keys and new detection keys to ensure we update all
        all_classes = set(self.trackers.keys()).union(set(class_detections.keys()))
        
        for cls_name in all_classes:
            if cls_name not in self.trackers:
                self.trackers[cls_name] = Sort(max_age=120, min_hits=1, iou_threshold=0.05)
                
            if cls_name in class_detections:
                dets = np.array(class_detections[cls_name])
            else:
                dets = np.empty((0, 5))
                
            tracked_objects = self.trackers[cls_name].update(dets)
            
            for trk in tracked_objects:
                x1, y1, x2, y2, obj_id = trk
                
                det = Detection2D()
                det.header = data.header
                
                det.bbox.center.position.x = float((x1 + x2) / 2)
                det.bbox.center.position.y = float((y1 + y2) / 2)
                det.bbox.size_x = float(x2 - x1)
                det.bbox.size_y = float(y2 - y1)
                
                class_id_str = f"{cls_name}_{int(obj_id)}"
                
                hyp = ObjectHypothesisWithPose()
                hyp.hypothesis.class_id = class_id_str
                hyp.hypothesis.score = 1.0  # SORT doesn't track confidence, using 1.0 as placeholder
                
                det.results.append(hyp)
                det_array.detections.append(det)
                
                self.get_logger().info(f"Detected: {class_id_str}")

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
