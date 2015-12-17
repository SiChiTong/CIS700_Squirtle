#!/bin/bash          
#
# Script to launch Squirtle Arm Pick and Give Demo
# 
# Written By: Mayumi Mohan

# Start Arm Launcher
roslaunch squirtle_arm squirtle_arm_bringup.launch &
sleep $3

# Start moveIt
roslaunch turtlebot_arm_moveit_config turtlebot_arm_moveit.launch sim:=false --screen &
sleep $7

# Run sendPose... just because
rosrun squirtle_arm_kinematics sendArmPose.py &

# Run the pick and give... not place code
rosrun squirtle_arm_kinematics squirtleFlowerGreeting.py