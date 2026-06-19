import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from vision_msgs.msg import Detection2DArray
from cv_bridge import CvBridge, CvBridgeError
import message_filters
import cv2

class ImageOverlayNode(Node):
    def __init__(self):
        super().__init__('image_overlay_node')

        # Synchronize image and detection topics
        self.image_sub = message_filters.Subscriber(self, Image, '/camera/image_raw')
        self.detections_sub = message_filters.Subscriber(self, Detection2DArray, '/yolo/detections')

        # Use ApproximateTimeSynchronizer to match messages with close timestamps
        self.ts = message_filters.ApproximateTimeSynchronizer(
            [self.image_sub, self.detections_sub],
            queue_size=10,
            slop=0.1
        )
        self.ts.registerCallback(self.sync_callback)

        # Publisher for the annotated image
        self.publisher = self.create_publisher(Image, '/camera/yolo/overlay_image', 10)
        self.br = CvBridge()
        
        self.get_logger().info("Image Overlay Node has been started.")

    def sync_callback(self, image_msg, detections_msg):
        try:
            # Convert ROS Image to OpenCV frame
            frame = self.br.imgmsg_to_cv2(image_msg, "bgr8")
        except CvBridgeError as e:
            self.get_logger().error(f"Failed to convert image: {e}")
            return

        # Draw each detection on the frame
        for det in detections_msg.detections:
            center_x = det.bbox.center.position.x
            center_y = det.bbox.center.position.y
            size_x = det.bbox.size_x
            size_y = det.bbox.size_y

            # Calculate top-left and bottom-right corners
            min_x = int(center_x - size_x / 2)
            min_y = int(center_y - size_y / 2)
            max_x = int(center_x + size_x / 2)
            max_y = int(center_y + size_y / 2)

            # Draw bounding box
            cv2.rectangle(frame, (min_x, min_y), (max_x, max_y), (0, 255, 0), 2)

            # Draw class label and score if available
            if len(det.results) > 0:
                hyp = det.results[0]
                class_id = hyp.hypothesis.class_id
                score = hyp.hypothesis.score
                label = f"{class_id}: {score:.2f}"
                
                # Text background
                (text_width, text_height), baseline = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
                cv2.rectangle(frame, (min_x, min_y - text_height - baseline), (min_x + text_width, min_y), (0, 255, 0), cv2.FILLED)
                cv2.putText(frame, label, (min_x, min_y - baseline), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

        try:
            # Convert annotated frame back to ROS Image
            annotated_msg = self.br.cv2_to_imgmsg(frame, "bgr8")
            annotated_msg.header = image_msg.header

            # Publish the overlay image
            self.publisher.publish(annotated_msg)
        except CvBridgeError as e:
            self.get_logger().error(f"Failed to convert annotated image to ROS msg: {e}")

def main(args=None):
    rclpy.init(args=args)
    node = ImageOverlayNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
