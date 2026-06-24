import rclpy
from rclpy.node import Node
import time

# Import the ArUco interface from the package you built yesterday
from ros2_aruco_interfaces.msg import ArucoMarkers
# Assuming standard vision_msgs for YOLO, adjust if you use a custom message!
from vision_msgs.msg import Detection2DArray


class PerceptionEventNode(Node):
    def __init__(self):
        super().__init__('perception_event_node')

        # 1. Subscribe to YOLO and ArUco outputs
        self.aruco_sub = self.create_subscription(
            ArucoMarkers,
            '/aruco_markers',
            self.aruco_callback,
            10)

        self.yolo_sub = self.create_subscription(
            Detection2DArray,
            '/yolo/detections',
            self.yolo_callback,
            10)

        self.last_announced_time = {}
        self.debounce_cooldown = 3.0 

        self.get_logger().info("Perception Event Node initialized. Waiting for targets...")

    def aruco_callback(self, msg):
        # 2. Trigger events for marker ID
        for marker_id in msg.marker_ids:
            event_name = f"aruco_marker_{marker_id}"

            # Check the debounce timer
            current_time = time.time()
            if event_name not in self.last_announced_time or \
               (current_time - self.last_announced_time[event_name]) > self.debounce_cooldown:

                # 3. Log announcement
                self.get_logger().info(
                    f"🎯 EVENT TRIGGERED: ArUco Box #{marker_id} detected in the delivery zone!")

                # Update the cooldown timer
                self.last_announced_time[event_name] = current_time

    def yolo_callback(self, msg):
        # 2. Trigger events for target class
        for detection in msg.detections:
            for hypothesis in detection.results:
                class_id = hypothesis.hypothesis.class_id
                confidence = hypothesis.hypothesis.score

                # Only trigger if it meets a confidence threshold
                if confidence > 0.75:
                    event_name = f"yolo_object_{class_id}"

                    # Check the debounce timer
                    current_time = time.time()
                    if event_name not in self.last_announced_time or \
                       (current_time - self.last_announced_time[event_name]) > self.debounce_cooldown:

                        # 3. Log announcement
                        self.get_logger().info(
                            f"🚨 EVENT TRIGGERED: High-confidence YOLO target '{class_id}' spotted (Confidence: {confidence:.2f})")

                        # Update the cooldown timer
                        self.last_announced_time[event_name] = current_time


def main(args=None):
    rclpy.init(args=args)
    node = PerceptionEventNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
