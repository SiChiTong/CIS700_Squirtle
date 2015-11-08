#!/usr/bin/env python

'''
Node to send speech status to the robot state
by Siddharth Srivatsa

Publishes - /current_subroutine_status
Subscribes - /nexusMessage, /current_task
'''


import roslib
import rospy
import os
import sys
from std_msgs.msg import *
from geometry_msgs.msg import *

class myPose():

	def __init__(self):
		rospy.init_node("myPose", anonymous = True)
		self.Posesub = rospy.Subscriber('/amcl_pose', PoseWithCovarianceStamped, self.amclCallback)
		self.taskSub = rospy.Subscriber('/current_task', String, self.taskCallback)
		self.pub = rospy.Publisher('initialpose', PoseWithCovarianceStamped, queue_size = 10)
		self.newTask = 0
		self.lastTask = ""
		myPosition = PoseWithCovarianceStamped()

		rate = rospy.Rate(10);
		while not rospy.is_shutdown():
			if self.newTask == 1:
				print "I published, Yay!"
				self.pub.publish(myPosition)
				self.lastTask = self.currentTask
				self.newTask = 0
			else:
				continue
			rate.sleep
		rospy.spin()

	def amclCallback(self, data):
		myPosition.pose.position.x = data.pose.pose.position.x
		myPosition.pose.position.y = data.pose.pose.position.y
		myPosition.pose.position.z = data.pose.pose.position.z
		myPosition.pose.orientation.x = data.pose.pose.orientation.x
		myPosition.pose.orientation.y = data.pose.pose.orientation.y
		myPosition.pose.orientation.z = data.pose.pose.orientation.z
		myPosition.pose.orientation.w = data.pose.pose.orientation.w


	def taskCallback(self, data):
		self.currentTask = data.data
		if (self.currentTask != self.lastTask):
			self.newTask = 1
		else:
			self.newTask = 0


if __name__ == '__main__':
	myPose()
