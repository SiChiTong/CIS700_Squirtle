#!/usr/bin/env python

'''
Listen and Talk
by David Isele

'''

import rospy
import roslib
import rospy
import os
import time
from kobuki_msgs.msg import SensorState
from std_msgs.msg import String
from std_msgs.msg import Bool
from collections import deque

class tasklist():
	
	def __init__(self):
		# setup
		self.history = deque([])
		self.command_queue = deque(["retrieve_object Chips", "go_to_room vending_machine", "deliver_object diet_coke", "go_to_room GRASP_Lab"])
		self.server_list =[]
		rospy.init_node("tasklist")	
		self.pub = rospy.Publisher('current_task', String, queue_size=10)
		# self.sub = rospy.Subscriber("/serverstuff",String,self.ServerMessageCallback)
		# self.sub2 = rospy.Subscriber("/RobotState",String,self.RobotStateCallback)
		rate = rospy.Rate(10) # 10hz
		while not rospy.is_shutdown():
			if len(self.command_queue)>0:
				self.pub.publish(self.command_queue[0])
				rate.sleep()

		# rospy.spin();


	def ServerMessageCallback(self,data):
		if data.data!=self.server_list:
			self.server_list = data.data+[]
			#parse server list
			for command in self.server_list:
				self.command_queue.append(command)

	def RobotStateCallback(self,data):
		if data.data=="in progress":
			pass
		elif data.data=="success":
			# remove the current task from the list
			completed_task = self.command_queue.popleft()
			
			# store the completed task in the history
			self.history.append(completed_task)
			
		#elif data.data=="fail":
		
		else:
			print("The robot state is trying to confuse me")
			
		rospy.loginfo(my_message)
		pub.publish(my_message)
		rate.sleep()

if __name__ == '__main__':
	try:
		tasklist()
	except rospy.ROSInterruptException:
		rospy.loginfo("exception")
