import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, CameraInfo, PointCloud2
from sensor_msgs_py import point_cloud2
from cv_bridge import CvBridge
import numpy as np

class DepthToPointCloudNode(Node):
    def __init__(self):
        super().__init__('depth_to_pointcloud_node')
        self.bridge = CvBridge()
        self.camera_info = None

        # Subscriptions
        self.info_sub = self.create_subscription(CameraInfo, '/camera/camera_info', self.info_callback, 10)
        self.depth_sub = self.create_subscription(Image, '/camera/depth/image_raw', self.depth_callback, 10)
        
        # Publisher
        self.pc_pub = self.create_publisher(PointCloud2, '/camera/depth/points', 10)

        self.get_logger().info("Depth to PointCloud2 Node Initialized.")

    def info_callback(self, msg):
        self.camera_info = msg

    def depth_callback(self, msg):
        if self.camera_info is None:
            return

        # 1. Convert ROS Image to NumPy array
        depth_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough')
        height, width = depth_image.shape

        # 2. Downsample (The "Simple Stride Filter")
        # Skipping pixels makes the math 16x faster!
        stride = 4  
        downsampled_depth = depth_image[::stride, ::stride]
        
        # Extract Intrinsics
        fx = self.camera_info.k[0]
        cx = self.camera_info.k[2]
        fy = self.camera_info.k[4]
        cy = self.camera_info.k[5]

        # 3. Project 2D to 3D
        # Create a grid of U, V pixel coordinates
        u = np.arange(0, width, stride)
        v = np.arange(0, height, stride)
        uu, vv = np.meshgrid(u, v)

        # 1. Invert the relative depth (255 - depth) so Close = Low Z, Far = High Z
        inverted_depth = 255.0 - downsampled_depth.astype(np.float32)
        
        # 2. Normalize (0 to 1) and scale. 
        # Using 10.0 stretches the cloud out slightly more for a clearer view
        Z = (inverted_depth / 255.0) * 10.0 
        
        # 3. Prevent Z from being exactly 0 (which causes divide-by-zero projection errors)
        Z = np.clip(Z, 0.1, 10.0)
        
        # Pinhole projection math
        X = (uu - cx) * Z / fx
        Y = (vv - cy) * Z / fy

        # Flatten into an N x 3 array of points
        points = np.column_stack((X.flatten(), Y.flatten(), Z.flatten()))

        # 4. Create and Publish PointCloud2 Message
        header = msg.header
        pc2_msg = point_cloud2.create_cloud_xyz32(header, points)
        self.pc_pub.publish(pc2_msg)

def main(args=None):
    rclpy.init(args=args)
    node = DepthToPointCloudNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
