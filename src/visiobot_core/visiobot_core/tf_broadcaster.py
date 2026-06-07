import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TransformStamped
from tf2_ros.static_transform_broadcaster import StaticTransformBroadcaster


class VisioBotTfBroadcaster(Node):
    def __init__(self):
        super().__init__('tf_broadcaster')
        self.tf_broadcaster = StaticTransformBroadcaster(self)
        self.publish_static_transform()

    def publish_static_transform(self):

        # Camera Transform
        t_camera = TransformStamped()
        t_camera.header.stamp = self.get_clock().now().to_msg()
        t_camera.header.frame_id = 'base_link'
        t_camera.child_frame_id = 'camera_link'
        t_camera.transform.translation.x = 0.20
        t_camera.transform.translation.z = 0.10
        t_camera.transform.rotation.w = 1.0

        # Laser/Lidar Transform
        t_laser = TransformStamped()
        t_laser.header.stamp = self.get_clock().now().to_msg()
        t_laser.header.frame_id = 'base_link'
        t_laser.child_frame_id = 'laser_link'
        t_laser.transform.translation.z = 0.25
        t_laser.transform.rotation.w = 1.0

        # Broadcast both simultaneously
        self.tf_broadcaster.sendTransform([t_camera, t_laser])
        self.get_logger().info('Broadcasting static transforms: camera_link & laser_link')


def main(args=None):
    rclpy.init(args=args)
    node = VisioBotTfBroadcaster()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
