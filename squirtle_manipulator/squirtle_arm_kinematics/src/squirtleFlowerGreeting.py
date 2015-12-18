#!/usr/bin/env python

'''
Squirtle Flower Greeting 
by Mayumi Mohan
# 
# Subscribes to: 
# Publishes: /targetLocation
'''

import roslib
import rospy
import sys
import time
import moveit_commander
import os
import moveit_msgs.msg
from geometry_msgs.msg import Pose
from std_msgs.msg import Float64

class squirtleFlowerGreeting():

	def stateCallback(self, data):
		self.newPose = data

		targetLocation = Pose()
		startTime = rospy.get_time()
		i = 0

		os.system("rostopic pub  /gripper_joint/command std_msgs/Float64 -- 1.57 &")
		rospy.sleep(5)

		print 'Move to Flower'
		targetLocation.position.x = 0.0144326423953
		targetLocation.position.y = 0.263114368294
		targetLocation.position.z = 0.554147669158
		targetLocation.orientation.x = -0.15822121316
		targetLocation.orientation.y = 0.110466551696
		targetLocation.orientation.z = 0.804522708772
		targetLocation.orientation.w = 0.561699563586
		self.group.set_pose_target(targetLocation)
		
		
		# Compute plan and visualize if successful
		newPlan = self.group.plan()
		# Perform plan on Robot
		
		self.group.go(wait=True)
		print "Grasp"
		rospy.sleep(5)
		
		
		os.system("rostopic pub  /gripper_joint/command std_msgs/Float64 -- -1.2")
		
		rospy.wait(2)
		rospy.sleep(10)

		print 'Lift flower'
		targetLocation.position.x = 0.152084466078
		targetLocation.position.y = -0.101408893961
		targetLocation.position.z = 0.687939025664
		targetLocation.orientation.x = 0.779572704978
		targetLocation.orientation.y = -0.529587263257
		targetLocation.orientation.z = 0.276585994996
		targetLocation.orientation.w = 0.187893362364
		self.group.set_pose_target(targetLocation)
		# Compute plan and visualize if successful
		newPlan = self.group.plan()
		# Perform plan on Robot
		self.group.go(wait=True)
		rospy.sleep(2)

		print "Release"
		os.system("rostopic pub  /gripper_joint/command std_msgs/Float64 -- 1.57 &")
		rospy.sleep(5)

		# End task
		print 'Rest'
		targetLocation.position.x = 0.0637378729914
		targetLocation.position.y = 0.314422971062
		targetLocation.position.z = 0.585093066776
		targetLocation.orientation.x = -0.0363535046398
		targetLocation.orientation.y = 0.0320124025576
		targetLocation.orientation.z = 0.749608676985
		targetLocation.orientation.w = 0.660106400644
		#os.system("rosrun squirtle_arm_kinematics armPlanning.py");

		self.group.set_pose_target(targetLocation)
		# Compute plan and visualize if successful
		newPlan = self.group.plan()
		# Perform plan on Robot
		self.group.go(wait=True)
		self.group.clear_pose_targets()
		#relax servos
		for servo in self.servos:
			self.relaxers[servo]()
		rospy.sleep(5)
		#print  self.group.get_planning_frame()
		## Adding/Removing Objects and Attaching/Detaching Objects
		## ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
		## First, we will define the collision object message
		collision_object = moveit_msgs.msg.CollisionObject()

		## When finished shut down moveit_commander.
		moveit_commander.roscpp_shutdown()

	def Subfunc(self):
				# Subscriber
		#self.sub = rospy.Subscriber("/targetLocation",  Pose, self.stateCallback)
		#self.gr = rospy.Publisher('/gripper_joint/command',Float64, queue_size=1)
		self.pos_gr = Float64()
		self.pos_gr = 1.57
		rospy.sleep(3)
		
		targetLocation = Pose()
		startTime = rospy.get_time()
		i = 0

		print 'Lift flower'
		targetLocation.position.x = 0.152084466078
		targetLocation.position.y = -0.101408893961
		targetLocation.position.z = 0.687939025664
		targetLocation.orientation.x = 0.779572704978
		targetLocation.orientation.y = -0.529587263257
		targetLocation.orientation.z = 0.276585994996
		targetLocation.orientation.w = 0.187893362364
		self.group.set_pose_target(targetLocation)
		# Compute plan and visualize if successful
		newPlan = self.group.plan()
		# Perform plan on Robot
		self.group.go(wait=True)
		rospy.sleep(2)

		os.system("rostopic pub  /gripper_joint/command std_msgs/Float64 -- 1.57 &")
		rospy.sleep(5)

		print 'Move to Flower'
		targetLocation.position.x = 0.0144326423953
		targetLocation.position.y = 0.263114368294
		targetLocation.position.z = 0.554147669158
		targetLocation.orientation.x = -0.15822121316
		targetLocation.orientation.y = 0.110466551696
		targetLocation.orientation.z = 0.804522708772
		targetLocation.orientation.w = 0.561699563586
		self.group.set_pose_target(targetLocation)
		
		
		# Compute plan and visualize if successful
		newPlan = self.group.plan()
		# Perform plan on Robot
		
		self.group.go(wait=True)
		
		print "Grasp"
		rospy.sleep(5)
		
		os.system("rostopic pub  /gripper_joint/command std_msgs/Float64 -- -1.57 &")
	
		rospy.sleep(5)

		print 'Lift flower'
		targetLocation.position.x = 0.152084466078
		targetLocation.position.y = -0.101408893961
		targetLocation.position.z = 0.687939025664
		targetLocation.orientation.x = 0.779572704978
		targetLocation.orientation.y = -0.529587263257
		targetLocation.orientation.z = 0.276585994996
		targetLocation.orientation.w = 0.187893362364
		self.group.set_pose_target(targetLocation)
		# Compute plan and visualize if successful
		newPlan = self.group.plan()
		# Perform plan on Robot
		self.group.go(wait=True)
		rospy.sleep(2)

		print "Release"
		os.system("rostopic pub  /gripper_joint/command std_msgs/Float64 -- 1.57 &")
		rospy.sleep(5)

		# End task
		print 'Rest'
		targetLocation.position.x = 0.0637378729914
		targetLocation.position.y = 0.314422971062
		targetLocation.position.z = 0.585093066776
		targetLocation.orientation.x = -0.0363535046398
		targetLocation.orientation.y = 0.0320124025576
		targetLocation.orientation.z = 0.749608676985
		targetLocation.orientation.w = 0.660106400644
		#os.system("rosrun squirtle_arm_kinematics armPlanning.py");

		self.group.set_pose_target(targetLocation)
		# Compute plan and visualize if successful
		newPlan = self.group.plan()
		# Perform plan on Robot
		self.group.go(wait=True)
		self.group.clear_pose_targets()
		#relax servos
		for servo in self.servos:
			self.relaxers[servo]()
		rospy.sleep(5)
		#print  self.group.get_planning_frame()
		## Adding/Removing Objects and Attaching/Detaching Objects
		## ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
		## First, we will define the collision object message
		collision_object = moveit_msgs.msg.CollisionObject()

		## When finished shut down moveit_commander.
		moveit_commander.roscpp_shutdown()
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
		rospy.init_node('squirtleFlowerGreeting', anonymous=True)#, queue_size=1)
		self.Subfunc()

if __name__ == '__main__':
	try:
		squirtleFlowerGreeting()
	except rospy.ROSInterruptException:
		rospy.loginfo("exception")