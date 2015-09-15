#!/usr/bin/env python

import rospy
import numpy as np
import os
from std_msgs.msg import String
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import time

class GoForward():
	def __init__(self):
		rospy.init_node('GoForward', anonymous=False)

		rospy.loginfo("To stop TurtleBot CTRL + C")  
		rospy.on_shutdown(self.shutdown)
		self.cmd_vel = rospy.Publisher('cmd_vel_mux/input/navi', Twist, queue_size=10)
		rospy.Subscriber('scan', LaserScan, self.laser_callback)
		
		self.r = rospy.Rate(10);
		self.move_cmd = Twist()
		self.move_cmd.linear.x = 0.2
		self.move_cmd.angular.z = 0
		
		while not rospy.is_shutdown():
			self.cmd_vel.publish(self.move_cmd)
			self.r.sleep()
			
	def shutdown(self):
		rospy.loginfo("Stop TurtleBot")
		self.move_cmd.linear.x = 0.0
		self.cmd_vel.publish(self.move_cmd)
		rospy.sleep(1)

	def turn_away(self):
		print "turn away"
		self.move_cmd.angular.z = .3
		self.move_cmd.linear.x = self.move_cmd.linear.x - 0.08
		if self.move_cmd.linear.x<0:
			self.move_cmd.linear.x = 0
			
		
		self.cmd_vel.publish(self.move_cmd)
		#self.turning = 0

	def get_closer(self):

		print "get closer"
		self.move_cmd.angular.z = -.15
		self.move_cmd.linear.x = 0.2
		self.cmd_vel.publish(self.move_cmd)

	def laser_callback(self, scan):
		# Build a depths array to rid ourselves of any nan data inherent in scan.ranges.
		depths = []
		max_scan = 100
		too_close = .95
		too_far = 1.2
		for dist in scan.ranges:
			if np.isnan(dist):
				depths.append(max_scan)
			else:
				depths.append(dist)
		if np.min(depths)<too_close or abs(np.min(depths)-max_scan)<.01:
			self.turn_away()
		elif np.min(depths)>too_far:
			self.get_closer()
		else:
			print "doing great"
			self.move_cmd.linear.x = 0.2
			self.move_cmd.angular.z = 0
			self.cmd_vel.publish(self.move_cmd)
		print np.min(depths)

if __name__ == '__main__':
	try:
		GoForward()
	except:
		rospy.loginfo("GoForward node terminated.")

