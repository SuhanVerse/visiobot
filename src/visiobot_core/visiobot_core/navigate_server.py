import time
import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node
from visiobot_interfaces.action import Navigate

class NavigateActionServer(Node):
    def __init__(self):
        super().__init__('navigate_action_server')
        self._action_server = ActionServer(
            self,
            Navigate,
            'navigate',
            self.execute_callback)
        self.get_logger().info('VisioBot Navigate Action Server is online.')

    def execute_callback(self, goal_handle):
        self.get_logger().info(f'Navigating to X: {goal_handle.request.target_x}, Y: {goal_handle.request.target_y}')
        
        feedback_msg = Navigate.Feedback()
        
        # Simulate driving to the goal over 5 seconds
        for i in range(1, 6):
            feedback_msg.distance_remaining = 5.0 - float(i)
            self.get_logger().info(f'Feedback: {feedback_msg.distance_remaining} meters remaining.')
            goal_handle.publish_feedback(feedback_msg)
            time.sleep(1.0)
            
        goal_handle.succeed()
        
        # Send the final result
        result = Navigate.Result()
        result.elapsed_time = 5.0
        self.get_logger().info('Goal reached successfully!')
        return result

def main(args=None):
    rclpy.init(args=args)
    node = NavigateActionServer()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()