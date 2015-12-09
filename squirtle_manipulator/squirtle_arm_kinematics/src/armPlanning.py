#!/usr/bin/env python
## tolerance!!
'''
Node for Planning of arm using MoveIt
by Mayumi Mohan

Adapted from: MoveIt Python Tutorials for PR2

# Requires: in following order run
## Squirtle arm launcher: roslaunch squirtle_arm squirtle_arm_bringup.launch
## Moveit: roslaunch turtlebot_arm_moveit_config turtlebot_arm_moveit.launch sim:=false --screen
# Subscribes to: /targetLocation
# Publishes:
'''

import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
from geometry_msgs.msg import Pose

class armPlanning():

	def stateCallback(self, data):
		self.newPose = data
		#newPose = self.group.get_current_pose().pose
		#newPose.position.x = newPose.position.x +0.0005
		#newPose.position.y = newPose.position.y +0.0005
		#newPose.position.z = newPose.position.z +0.0005
		self.group.set_pose_target(self.newPose)

		# Compute plan and visualize if successful
		print self.newPose
		newPlan = self.group.plan()

		# Wait for Rviz to display
		print "Rviz displaying"
		rospy.sleep(5)

		# Perform plan on Robot
		self.group.go(wait=True)

		rospy.sleep(5)
		self.group.clear_pose_targets()
		#print  self.group.get_planning_frame()
		## Adding/Removing Objects and Attaching/Detaching Objects
		## ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
		## First, we will define the collision object message
		collision_object = moveit_msgs.msg.CollisionObject()

		## When finished shut down moveit_commander.
		moveit_commander.roscpp_shutdown()

	def Subfunc(self):
				# Subscriber
		self.sub = rospy.Subscriber("/targetLocation",  Pose, self.stateCallback)
		while not rospy.is_shutdown():
			pass
		rospy.spin()

	def __init__(self):
		
		self.newPose =  Pose()

		# Initializations for plannning with moveit

		# Initialize the MoveIt Commander
		moveit_commander.roscpp_initialize(sys.argv)

		# RobotCommander object is an interface to the robot as a whole
		self.squirtleArm = moveit_commander.RobotCommander()

		# PlanningSceneInterface object is an interface to world surrounding robot
		self.scene = moveit_commander.PlanningSceneInterface()

		# MoveGroupCommander object enables planning and executing motions 
		self.group = moveit_commander.MoveGroupCommander("arm")

		# Initialize this node
		rospy.init_node('armPlanning', anonymous=True)#, queue_size=1)
		self.Subfunc()


if __name__ == '__main__':
  try:
    armPlanning()
  except rospy.ROSInterruptException:
    pass