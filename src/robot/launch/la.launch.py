import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

import xacro


def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time')

    pkg_path = os.path.join(get_package_share_directory('robot'))
    xacro_file = os.path.join(pkg_path,'urdf','robot.urdf.xacro')
    robot_description_config = xacro.process_file(xacro_file)
    
    params = {'robot_description': robot_description_config.toxml(), 'use_sim_time': use_sim_time}
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[params]
    )

    rviz = Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
        )

    gazebo = IncludeLaunchDescription(
            PythonLaunchDescriptionSource([os.path.join(
                get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]),
         )

    spawn_entity = Node(package='gazebo_ros', 
                        executable='spawn_entity.py',
                        arguments=['-topic', 'robot_description',
                                   '-entity', 'my_bot'],
                        output='screen')

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use sim time if true'),

        robot_state_publisher, 
        rviz,
        gazebo,
        spawn_entity
    ])
