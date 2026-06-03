from setuptools import find_packages, setup

package_name = 'visiobot_core'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
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
        ],
    },
)
