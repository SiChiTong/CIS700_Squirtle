#!/usr/bin/env python

'''
Squirtle gives a Shake hand
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
import moveit_msgs.msg
from geometry_msgs.msg import Pose
from std_msgs.msg import Float64
from arbotix_msgs.srv import Relax
from arbotix_python.joints import *

class squirtleShakeHand():

	def stateCallback(self, data):
		self.newPose = data

		targetLocation = Pose()
		startTime = rospy.get_time()
		i = 0


		print 'Initial Arm Position'
		targetLocation.position.x = 0.112902936164
		targetLocation.position.y = -0.0852755716372
		targetLocation.position.z = 0.691366645316
		targetLocation.orientation.x = 0.631222650833
		targetLocation.orientation.y = -0.564510156689
		targetLocation.orientation.z = 0.396455862883
		targetLocation.orientation.w = 0.354554645796
		self.group.set_pose_target(targetLocation)
		# Compute plan and visualize if successful
		newPlan = self.group.plan()
		# Perform plan on Robot
		self.group.go(wait=True)
		rospy.sleep(2)

		for x in range(0, 3):
			print 'Down'
			targetLocation.position.x = 0.0873635029374
			targetLocation.position.y = 0.133321298119
			targetLocation.position.z = 0.764699668327
			targetLocation.orientation.x = 0.23896280041
			targetLocation.orientation.y = -0.211518629674
			targetLocation.orientation.z = 0.709643998206
			targetLocation.orientation.w = 0.628141739682
			self.group.set_pose_target(targetLocation)
			# Compute plan and visualize if successful
			newPlan = self.group.plan()
			# Perform plan on Robot
			self.group.go(wait=True)
			#rospy.sleep(2)
			print 'Up'
			targetLocation.position.x = 0.112902936164
			targetLocation.position.y = -0.0852755716372
			targetLocation.position.z = 0.691366645316
			targetLocation.orientation.x = 0.631222650833
			targetLocation.orientation.y = -0.564510156689
			targetLocation.orientation.z = 0.396455862883
			targetLocation.orientation.w = 0.354554645796
			#os.system("rosrun squirtle_arm_kinematics armPlanning.py");

			self.group.set_pose_target(targetLocation)
			# Compute plan and visualize if successful
			newPlan = self.group.plan()
			# Perform plan on Robot
			self.group.go(wait=True)
			#rospy.sleep(2)

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
		self.sub = rospy.Subscriber("/targetLocation",  Pose, self.stateCallback)
		self.gr = rospy.Publisher('/gripper_joint/command',Float64, queue_size=1)
		self.pos_gr = Float64()
		self.pos_gr = 1.57
		rospy.sleep(3)

		# Relaxing the dynamixel servos (adapted from ControllerGUI.py, vanadium labs)
		dynamixels = rospy.get_param('/arbotix/dynamixels', dict())
		self.servos = list()
		self.relaxers = list()
		joints = rospy.get_param('/arbotix/joints', dict())
		# create sliders and publishers
		for name in sorted(joints.keys()):
			if rospy.get_param('/arbotix/joints/'+name+'/type','dynamixel') == 'dynamixel':
				self.relaxers.append(rospy.ServiceProxy(name+'/relax', Relax))
			else:
				self.relaxers.append(None)	

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
		rospy.init_node('squirtleShakeHand', anonymous=True)#, queue_size=1)
		self.Subfunc()

if __name__ == '__main__':
	try:
		squirtleShakeHand()
	except rospy.ROSInterruptException:
		rospy.loginfo("exception")