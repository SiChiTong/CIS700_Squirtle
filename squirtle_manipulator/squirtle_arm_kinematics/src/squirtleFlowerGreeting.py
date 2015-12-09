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
import moveit_msgs.msg
from geometry_msgs.msg import Pose
from std_msgs.msg import Float64

class squirtleFlowerGreeting():

	def stateCallback(self, data):
		self.newPose = data

		targetLocation = Pose()
		startTime = rospy.get_time()
		i = 0

		while i<5:
			if (rospy.get_time() - startTime)>5:
				i = i+1;
				startTime = rospy.get_time()

			if i == 1:
				# Initial Arm Position
				#os.system("rosnode kill /armPlanning");
				print 'Initial Arm Position'
				targetLocation.position.x = 0.088547521044
				targetLocation.position.y = 0.316993328381
				targetLocation.position.z = 0.512233272363
				targetLocation.orientation.x =  0.0295722736395
				targetLocation.orientation.y = -0.0284165464407
				targetLocation.orientation.z = 0.72045953698
				targetLocation.orientation.w = 0.692283205122
				self.pos_gr = -1.57
				#os.system("rosrun squirtle_arm_kinematics armPlanning.py");
			elif i == 2:
				#Lift:
				#os.system("rosnode kill /armPlanning");
				print 'Lift'
				targetLocation.position.x = 0.101038497391
				targetLocation.position.y = 0.00396533110741
				targetLocation.position.z = 0.781107991419
				targetLocation.orientation.x = 0.525076324286
				targetLocation.orientation.y = -0.504541780718
				targetLocation.orientation.z = 0.494197650205
				targetLocation.orientation.w = 0.47486959022
				#os.system("rosrun squirtle_arm_kinematics armPlanning.py");
			elif i == 3:
				# Pause
				#os.system("rosnode kill /armPlanning");
				self.pos_gr = 1.57
				print 'Pause'
				rospy.sleep(10);
			else:
				# Return
				#os.system("rosnode kill /armPlanning");
				print 'Return'
				targetLocation.position.x = 0.0881870116312
				targetLocation.position.y = 0.326027305883
				targetLocation.position.z = 0.534264838597
				targetLocation.orientation.x = 0.0626843965696
				targetLocation.orientation.y = -0.0602336920208
				targetLocation.orientation.z = 0.718336362869
				targetLocation.orientation.w = 0.690243028615
				#os.system("rosrun squirtle_arm_kinematics armPlanning.py");

			self.group.set_pose_target(targetLocation)

			# Compute plan and visualize if successful
			newPlan = self.group.plan()

			# Wait for Rviz to display
			print "Rviz displaying"

			# Perform plan on Robot
			self.group.go(wait=True)
			self.gr.publish(self.pos_gr)
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
		self.gr = rospy.Publisher('/gripper_joint/command',Float64, queue_size=1)
		self.pos_gr = Float64()
		self.pos_gr = 1.57
		rospy.sleep(3)
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