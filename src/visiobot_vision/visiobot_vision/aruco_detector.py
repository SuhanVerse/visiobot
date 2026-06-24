import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, CameraInfo
from geometry_msgs.msg import PoseArray, Pose
from cv_bridge import CvBridge, CvBridgeError
import cv2
import numpy as np

def rmat_to_quat(rmat):
    trace = np.trace(rmat)
    if trace > 0:
        s = 0.5 / np.sqrt(trace + 1.0)
        qw = 0.25 / s
        qx = (rmat[2, 1] - rmat[1, 2]) * s
        qy = (rmat[0, 2] - rmat[2, 0]) * s
        qz = (rmat[1, 0] - rmat[0, 1]) * s
    else:
        if rmat[0, 0] > rmat[1, 1] and rmat[0, 0] > rmat[2, 2]:
            s = 2.0 * np.sqrt(1.0 + rmat[0, 0] - rmat[1, 1] - rmat[2, 2])
            qw = (rmat[2, 1] - rmat[1, 2]) / s
            qx = 0.25 * s
            qy = (rmat[0, 1] + rmat[1, 0]) / s
            qz = (rmat[0, 2] + rmat[2, 0]) / s
        elif rmat[1, 1] > rmat[2, 2]:
            s = 2.0 * np.sqrt(1.0 + rmat[1, 1] - rmat[0, 0] - rmat[2, 2])
            qw = (rmat[0, 2] - rmat[2, 0]) / s
            qx = (rmat[0, 1] + rmat[1, 0]) / s
            qy = 0.25 * s
            qz = (rmat[1, 2] + rmat[2, 1]) / s
        else:
            s = 2.0 * np.sqrt(1.0 + rmat[2, 2] - rmat[0, 0] - rmat[1, 1])
            qw = (rmat[1, 0] - rmat[0, 1]) / s
            qx = (rmat[0, 2] + rmat[2, 0]) / s
            qy = (rmat[1, 2] + rmat[2, 1]) / s
            qz = 0.25 * s
    return qx, qy, qz, qw

class ArucoDetector(Node):
    def __init__(self):
        super().__init__('aruco_detector')
        
        self.br = CvBridge()
        
        # Subscriptions
        self.img_sub = self.create_subscription(
            Image, '/camera/image_raw', self.image_callback, 10)
        self.info_sub = self.create_subscription(
            CameraInfo, '/camera/camera_info', self.info_callback, 10)
            
        # Publishers
        self.pose_pub = self.create_publisher(
            PoseArray, '/camera/aruco/poses', 10)
        self.overlay_pub = self.create_publisher(
            Image, '/camera/aruco/overlay', 10)
            
        # Camera intrinsics
        self.K = None
        self.D = None
        
        # ArUco setup
        self.aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
        self.aruco_params = cv2.aruco.DetectorParameters()
        self.detector = cv2.aruco.ArucoDetector(self.aruco_dict, self.aruco_params)
        
        # 0.2m marker -> corner points in 3D (assuming Z=0 plane, standard CCW top-left first)
        s = 0.2 / 2.0
        self.obj_points = np.array([
            [-s,  s, 0],
            [ s,  s, 0],
            [ s, -s, 0],
            [-s, -s, 0]
        ], dtype=np.float32)

    def info_callback(self, msg):
        self.K = np.array(msg.k).reshape((3, 3))
        self.D = np.array(msg.d)

    def image_callback(self, msg):
        if self.K is None or self.D is None:
            return
            
        try:
            cv_image = self.br.imgmsg_to_cv2(msg, "bgr8")
        except CvBridgeError as e:
            self.get_logger().error(f"Failed to convert image: {e}")
            return
            
        # Detect markers
        corners, ids, rejected = self.detector.detectMarkers(cv_image)
        
        pose_array = PoseArray()
        pose_array.header = msg.header
        
        if ids is not None and len(ids) > 0:
            cv2.aruco.drawDetectedMarkers(cv_image, corners, ids)
            
            for i in range(len(ids)):
                # solvePnP for each marker
                success, rvec, tvec = cv2.solvePnP(
                    self.obj_points, corners[i][0], self.K, self.D, flags=cv2.SOLVEPNP_IPPE_SQUARE)
                
                if success:
                    # Draw axes
                    cv2.drawFrameAxes(cv_image, self.K, self.D, rvec, tvec, 0.1)
                    
                    # Convert to geometry_msgs/Pose
                    rmat, _ = cv2.Rodrigues(rvec)
                    qx, qy, qz, qw = rmat_to_quat(rmat)
                    
                    pose = Pose()
                    pose.position.x = float(tvec[0][0])
                    pose.position.y = float(tvec[1][0])
                    pose.position.z = float(tvec[2][0])
                    pose.orientation.x = float(qx)
                    pose.orientation.y = float(qy)
                    pose.orientation.z = float(qz)
                    pose.orientation.w = float(qw)
                    
                    pose_array.poses.append(pose)
                    
        self.pose_pub.publish(pose_array)
        
        # Publish overlay
        try:
            overlay_msg = self.br.cv2_to_imgmsg(cv_image, encoding="bgr8")
            overlay_msg.header = msg.header
            self.overlay_pub.publish(overlay_msg)
        except CvBridgeError as e:
            self.get_logger().error(f"Failed to publish overlay: {e}")

def main(args=None):
    rclpy.init(args=args)
    node = ArucoDetector()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
