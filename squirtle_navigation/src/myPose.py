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
		self.taskStatusSub = rospy.Subscriber("/current_subroutine_status", String, self.SubroutineStatusMessageCallback)
		self.pub = rospy.Publisher('initialpose', PoseWithCovarianceStamped, queue_size = 10)
		self.pub1 = rospy.Publisher('send_goal', String, queue_size = 10)
		self.newTask = 0
		self.updatePos = 1
		self.lastTask = ""
		self.myPosition = PoseWithCovarianceStamped()
		self.myPosition.pose.pose.position.x = 2.20424320025
		self.myPosition.pose.pose.position.y = 1.33934123128
		self.myPosition.pose.pose.position.z = 0.0
		self.myPosition.pose.pose.orientation.x = 0.0
		self.myPosition.pose.pose.orientation.y = 0.0
		self.myPosition.pose.pose.orientation.z = 0.99947076813
		self.myPosition.pose.pose.orientation.w = 0.0325297349128

		rate = rospy.Rate(10);
		while not rospy.is_shutdown():
			if self.newTask == 1:
				rospy.sleep(7.)
				self.myPosition.header.frame_id = "map"
				self.myPosition.header.stamp = rospy.Time.now()
				print self.myPosition
				self.pub.publish(self.myPosition)
				self.lastTask = self.currentTask
				self.newTask = 0
				self.updatePos = 1
				self.pub1.publish("true")
#			else:
#				print myPosition
			rate.sleep
		rospy.spin()

	def amclCallback(self, data):
		if self.updatePos == 1:
			self.myPosition.pose.pose.position.x = data.pose.pose.position.x
			self.myPosition.pose.pose.position.y = data.pose.pose.position.y
			self.myPosition.pose.pose.position.z = data.pose.pose.position.z
			self.myPosition.pose.pose.orientation.x = data.pose.pose.orientation.x
			self.myPosition.pose.pose.orientation.y = data.pose.pose.orientation.y
			self.myPosition.pose.pose.orientation.z = data.pose.pose.orientation.z
			self.myPosition.pose.pose.orientation.w = data.pose.pose.orientation.w
		#else :
			#continue


	def taskCallback(self, data):
		self.currentTask = data.data
		if (self.currentTask != self.lastTask):
			self.newTask = 1
		else:
			self.newTask = 0

	def SubroutineStatusMessageCallback(self, data):
		if (data.data == "complete"):
			self.updatePos = 0
if __name__ == '__main__':
	myPose()
