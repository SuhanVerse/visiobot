import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from vision_msgs.msg import Detection2DArray
import time

class VisualServoNode(Node):
    def __init__(self):
        super().__init__('visual_servo_node')

        # 1. IBVS Proportional Gains
        self.k_w = 0.002   # Angular gain
        self.k_v = 0.005   # Linear gain (Tuned for bounding box pixels!)
        
        self.max_w = 0.5
        self.max_v = 1.0
        
        self.image_width = 640
        self.cx = self.image_width / 2.0
        
        # 2. Target Height (IBVS)
        # When the bounding box reaches 300 pixels tall, the robot stops.
        self.target_height = 300.0  

        self.last_target_time = time.time()
        self.target_active = False
        self.latest_error_x = 0.0
        self.latest_error_z = 0.0 # This now represents bounding box size error

        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        
        # NOTE: Depth subscription completely removed. We only need YOLO!
        self.yolo_sub = self.create_subscription(Detection2DArray, '/yolo/detections', self.yolo_callback, 10)

        # Timers
        self.control_timer = self.create_timer(0.1, self.control_loop)
        self.safety_timer = self.create_timer(1.5, self.safety_check) # Relaxed to 1.5s
        
        self.get_logger().info("True IBVS Node Initialized. Waiting for target...")

    def yolo_callback(self, msg):
        if not msg.detections:
            return

        self.last_target_time = time.time()
        self.target_active = True

        detection = msg.detections[0]
        target_x = detection.bbox.center.position.x
        
        # NEW: Get the height of the bounding box
        current_height = detection.bbox.size_y

        # Angular Error
        self.latest_error_x = target_x - self.cx
        
        # Linear Error (Bounding box size)
        error_z = self.target_height - current_height
        
        # Prevent driving backward
        if error_z < 0: 
            error_z = 0.0 
            
        self.latest_error_z = error_z

    def control_loop(self):
        if not self.target_active:
            return

        twist = Twist()

        # Angular Velocity Calculation
        raw_w = -self.k_w * self.latest_error_x
        twist.angular.z = max(min(raw_w, self.max_w), -self.max_w)

        # Linear Velocity Calculation
        raw_v = self.k_v * self.latest_error_z
        twist.linear.x = max(min(raw_v, self.max_v), -self.max_v)

        self.cmd_pub.publish(twist)

    def safety_check(self):
        if self.target_active and (time.time() - self.last_target_time > 1.5):
            self.get_logger().warn("Target lost! Initiating safety stop.")
            self.stop_robot()
            self.target_active = False
            self.latest_error_x = 0.0
            self.latest_error_z = 0.0

    def stop_robot(self):
        twist = Twist() 
        self.cmd_pub.publish(twist)

def main(args=None):
    rclpy.init(args=args)
    node = VisualServoNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.stop_robot()
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()