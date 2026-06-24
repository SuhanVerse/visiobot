import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'visiobot_core'

models_files = []
for root, dirs, files in os.walk('models'):
    install_dir = os.path.join('share', package_name, root)
    models_files.append((install_dir, [os.path.join(root, f) for f in files]))

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
        (os.path.join('share', package_name, 'urdf'), glob('urdf/*.urdf')),
        (os.path.join('share', package_name, 'urdf'), glob('urdf/*.xacro')),
        (os.path.join('share', package_name, 'gazebo'), glob('gazebo/*.sdf')),
        (os.path.join('share', package_name, 'rviz'), glob('rviz/*.rviz')),
    ] + models_files,
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='xlegion',
    maintainer_email='khsuhan100@gmail.com',
    description='TODO: Package description',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'telemetry_pub = visiobot_core.telemetry_pub:main',
            'telemetry_sub = visiobot_core.telemetry_sub:main',
            'mode_service = visiobot_core.mode_service:main',
            'navigate_server = visiobot_core.navigate_server:main',
            'tf_broadcaster = visiobot_core.tf_broadcaster:main',
            'dynamic_tf_broadcaster = visiobot_core.dynamic_tf_broadcaster:main',
        ],
    },
)
