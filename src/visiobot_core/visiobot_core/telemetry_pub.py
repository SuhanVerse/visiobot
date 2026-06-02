import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class TelemetryPublisher(Node):
    def __init__(self):
        
        # Name of the node in the ROS2 graph
        super().__init__('telemetry_pub')
        
        self.publisher_ = self.create_publisher(String, 'visiobot_status', 10)
        
        timer_period = 1.0  
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = f'VisioBot Systems Normal(Planned). Runtime cycle: {self.i}'
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: "{msg.data}"')
        self.i += 1

def main(args=None):
    rclpy.init(args=args)
    telemetry_publisher = TelemetryPublisher()
    
    # Keep the node running
    rclpy.spin(telemetry_publisher)
    
    # Cleanup when killed
    telemetry_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()