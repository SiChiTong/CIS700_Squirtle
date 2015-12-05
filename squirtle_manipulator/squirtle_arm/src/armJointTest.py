#!/usr/bin/env python

'''
Node to test ever joint of Turtlebot Arm 
by Mayumi Mohan

# Run: roslaunch squirtle_arm squirtle_arm.launch beforehand
# Publishes: an angle to every joint in order to test...
'''

import roslib
import rospy
import os
import time
from kobuki_msgs.msg import SensorState
from std_msgs.msg import Float64
from std_msgs.msg import Bool

class armJointTest():

	def __init__(self):
		# Initialize the node
		rospy.init_node("armJointTest") 
		self.sh1 = rospy.Publisher('/arm_shoulder_pan_joint/command',Float64, queue_size=1)
		self.sh2 = rospy.Publisher('/arm_shoulder_lift_joint/command',Float64, queue_size=1)
		self.el = rospy.Publisher('/arm_elbow_flex_joint/command',Float64, queue_size=1)
		self.wr = rospy.Publisher('/arm_wrist_flex_joint/command',Float64, queue_size=1)
		self.gr = rospy.Publisher('/gripper_joint/command',Float64, queue_size=1)

		# Variables are of type Float64
		self.pos_sh1 = Float64()
		self.pos_sh2 = Float64()
		self.pos_el = Float64()
		self.pos_wr = Float64()
		self.pos_gr = Float64()

		while(1):
			##########################ENTER REQUIRED ANGLES HERE:#######################
			# Initialize all servos to 0.00
			self.pos_sh1 = 0.00
			self.pos_sh2 = 0.00
			self.pos_el = 0.00
			self.pos_wr = 0.00
			self.pos_gr = 0.00
			###########################################################################

			# Publish the initial position of all the servos
			self.sh1.publish(self.pos_sh1)
			self.sh2.publish(self.pos_sh2)
			self.el.publish(self.pos_el)
			self.wr.publish(self.pos_wr)
			self.gr.publish(self.pos_gr)

			# Wait for arm to respond(10 sec)
			rospy.sleep(5)

if __name__ == '__main__':
	try:
		armJointTest()
	except rospy.ROSInterruptException:
		rospy.loginfo("exception")