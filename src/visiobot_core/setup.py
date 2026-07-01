import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'visiobot_core'

def package_files(data_files, directory_list):
    for directory in directory_list:
        if os.path.exists(directory):
            for path, _, filenames in os.walk(directory):
                for filename in filenames:
                    filepath = os.path.join(path, filename)
                    data_files.append((os.path.join('share', package_name, path), [filepath]))
    return data_files

extra_files = package_files([], ['models', 'worlds'])

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
    ] + extra_files,
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
