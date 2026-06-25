import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'visiobot_vision'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='xlegion',
    maintainer_email='khsuhan100@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'camera_processor = visiobot_vision.camera_processor:main',
            'yolo_detector = visiobot_vision.yolo_detector:main',
            'image_overlay_node = visiobot_vision.image_overlay_node:main',
            'aruco_detector = visiobot_vision.aruco_detector:main',
            'perception_event_node = visiobot_vision.perception_event_node:main',
            'depth_estimator_node = visiobot_vision.depth_estimator_node:main',
            'depth_to_pointcloud_node = visiobot_vision.depth_to_pointcloud_node:main',
        ],
    },
)
