import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist

class ValidatorNode(Node):
    def __init__(self):
        super().__init__('host_safety_validator')
        
        # Listen to the ESP32's intents
        self.subscription = self.create_subscription(
            String, 'gesture_intent', self.listener_callback, 10)
            
        # Talk to the robot's motor controllers
        self.publisher = self.create_publisher(Twist, 'cmd_vel', 10)
        
        self.get_logger().info("Safety Validator Active. Waiting for gestures...")

    def listener_callback(self, msg):
        intent = msg.data.lower()
        twist = Twist()

        # Host-side safety mapping and validation
        if intent == "forward":
            twist.linear.x = 0.5  # Safe forward speed (meters per second)
            twist.angular.z = 0.0
            self.get_logger().info("Valid intent: FORWARD. Sending cmd_vel.")
            
        elif intent == "search":
            twist.linear.x = 0.0
            twist.angular.z = 0.5 # Safe rotation speed (radians per second)
            self.get_logger().info("Valid intent: SEARCH. Sending cmd_vel.")
            
        else:
            # If it hears "stop" or ANY unknown glitch text, it forces a halt.
            twist.linear.x = 0.0  
            twist.angular.z = 0.0
            self.get_logger().warning(f"Stop/Unknown intent: '{intent}'. HALTING.")

        # Publish the safe Twist message to the robot
        self.publisher.publish(twist)

def main(args=None):
    rclpy.init(args=args)
    node = ValidatorNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
