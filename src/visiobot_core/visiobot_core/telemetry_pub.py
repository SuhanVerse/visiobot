import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class TelemetryPublisher(Node):
    def __init__(self):
        super().__init__('telemetry_pub')

        self.declare_parameter('robot_name', 'DefaultBot')
        self.robot_name = self.get_parameter('robot_name').get_parameter_value().string_value

        # Set up the publisher and timer
        self.publisher_ = self.create_publisher(String, 'visiobot_status', 10)
        self.timer = self.create_timer(1.0, self.timer_callback)
        
        # Here is the missing counter initialization!
        self.count_ = 0

    def timer_callback(self):
        msg = String()
        # Use the injected YAML parameter for the robot name
        msg.data = f"{self.robot_name} Systems Nominal. Runtime cycle: {self.count_}"
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: "{msg.data}"')
        
        # Increment the counter for the next loop
        self.count_ += 1

def main(args=None):
    rclpy.init(args=args)
    node = TelemetryPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()