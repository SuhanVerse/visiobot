import rclpy
from rclpy.node import Node
# Import your custom interface!
from visiobot_interfaces.srv import SetMode


class ModeService(Node):
    def __init__(self):
        super().__init__('mode_service')
        self.srv = self.create_service(
            SetMode, 'set_mode', self.set_mode_callback)
        self.get_logger().info('VisioBot Mode Service is ready to receive commands.')

    def set_mode_callback(self, request, response):
        self.get_logger().info(
            f'Incoming request to set mode: "{request.mode}"')

        if request.mode in ['patrol', 'standby', 'search']:
            response.success = True
            response.message = f'VisioBot successfully switched to {request.mode} mode.'
        else:
            response.success = False
            response.message = 'Error: Unknown mode requested!'

        return response


def main(args=None):
    rclpy.init(args=args)
    node = ModeService()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
