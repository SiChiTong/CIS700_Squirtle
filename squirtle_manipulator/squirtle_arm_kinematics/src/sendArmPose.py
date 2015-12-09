#!/usr/bin/env python

'''
Node to send a Pose to the arm 
by Mayumi Mohan

# 
# Subscribes to: 
# Publishes: /targetLocation
'''
import roslib
import rospy
import os
import time
from geometry_msgs.msg import Pose
class sendArmPose():

	def stateCallback(self, data):
		self.state = data.data;

	def __init__(self):
		self.state = ""
		# Initialize Node
		rospy.init_node("sendArmPose") 
		#publisher
		self.pub = rospy.Publisher('targetLocation', Pose, queue_size=1)
		targetLocation = Pose()

		while(1):
			targetLocation.position.x = 0.251364568834
			targetLocation.position.y = -0.227889839659
			targetLocation.position.z = -0.522008078422
			targetLocation.orientation.x = -0.861906845189
			targetLocation.orientation.y = 0.493517321703
			targetLocation.orientation.z = 0.10104411357
			targetLocation.orientation.w = 0.0578561190228
			self.pub.publish(targetLocation)

if __name__ == '__main__':
	try:
		sendArmPose()
	except rospy.ROSInterruptException:
		rospy.loginfo("exception")

