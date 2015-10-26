#!/usr/bin/env python

'''
Node to keep track of Robot state 
by Siddharth Srivatsa

# Flags to send to the Task List - "in progress",  "success", "fail"
# Status messages to receive from the individual subroutines "complete", "error"
# Function to call individual subroutines (Takes in name of the subroutine as as argument and calls the corresponfing launch file)
'''

import rospy
import roslib
import rospy
import os
import time
from std_msgs.msg import String
from std_msgs.msg import Bool


class robotStateNode():
	def robotState(self):
		# Setup the publishers and subscribers
		rospy.init_node("robotStateNode", anonymous=True)
		print(self.taskStatus)
		print(self.subroutineStatus)
		rospy.Subscriber("/current_task",String,self.TaskListMessageCallback)
		rospy.Subscriber("/current_subroutine_status",String,self.SubroutineStatusMessageCallback)
		self.StatePub = rospy.Publisher('RobotState', String, queue_size=10)
		
		rate = rospy.Rate(10) # Publish at 10hz
		while not rospy.is_shutdown():
			# Monitor the status of the current subroutine constantly and act accordingly
			if (self.subroutineStatus == "complete"):
				# os.system(self.killSubroutines(currentSubroutine))
				self.taskStatus = "success"
				self.StatePub.publish(self.taskStatus)

			elif (self.subroutineStatus == "error"):
				os.system(self.killSubroutines(currentSubroutine))
				# Nodes may get reset, you will lose data
				self.taskStatus = "fail"
				os.system("Find Why you failed and act accordingly?")
				# Shaky ground here, not sure how the three different fail modes are handled
				self.StatePub.publish(self.taskStatus)

			elif (self.subroutineStatus == "going_on"):
				self.taskStatus = "in progress"
				self.StatePub.publish(self.taskStatus)
			rate.sleep()
		print(self.taskStatus)
		print(self.subroutineStatus)
		rospy.spin();


	# Start a new subroutine you receive a new message from the TaskList
	def TaskListMessageCallback(self, data):
		self.currentTask = data.data
		self.currentTask = self.currentTask.split()
		self.currentSubroutine = self.subroutines[self.currentTask[0]]
		parameterString = ""
		for i in range(1,len(self.currentTask)):
			parameterString = parameterString + "P" + str(i) + ":=" + self.currentTask[i] + " "			# For each paramter convert it to a string to make it a system call
		print(parameterString + " ")
		print(self.taskStatus)
		if (self.taskStatus != "in progress"):
			os.system(self.currentSubroutine + " " + parameterString)
			print(self.currentSubroutine + " " + parameterString)
			self.taskStatus = "in progress"
			rate = rospy.Rate(10)
			rate.sleep()

	# Get the status of the subRoutine
	def SubroutineStatusMessageCallback(self, data):
		self.subroutineStatus = data.data

	def __init__(self):
		self.currentTask = None
		self.subroutineStatus = "comeplete"
		self.taskStatus = "success"
		self.currentSubroutine = None

		# Maintain a list of subroutines to be called for each sub task the TaskList sends
		self.subroutines = {
			'go_to_room' : 'roslaunch squirtle_navigation SquirtleNavigation.launch',
			'retrieve_object' : 'python ~/catkin_ws/src/CIS700_Squirtle/squirtle_utils/src/speech_retrieve_object.py',
			'deliver_object' : 'python ~/catkin_ws/src/CIS700_Squirtle/squirtle_utils/src/speech_deliver_object.py',
			'find_person' : 'python ~/catkin_ws/src/CIS700_Squirtle/squirtle_utils/src/speech_find_peron.py',
			# 'follow_person' : '/home/siddharth/catkin_ws/src/CIS700_Squirtle/squirtle_navigation/launch/SquirtleNavigation.launch',
			# 'retrieve_message' : '/home/siddharth/catkin_ws/src/CIS700_Squirtle/squirtle_navigation/launch/SquirtleNavigation.launch',
			# 'deliver_message' : '/home/siddharth/catkin_ws/src/CIS700_Squirtle/squirtle_navigation/launch/SquirtleNavigation.launch',
		}

		# self.killSubroutines = {
			# 'go_to_room' : '/home/siddharth/catkin_ws/src/CIS700_Squirtle/squirtle_navigation/include/NavigationKillNodes.sh',
			# 'retrieve_object' : '/home/siddharth/catkin_ws/src/CIS700_Squirtle/squirtle_navigation/include/NavigationKillNodes.sh',
			# 'deliver_object' : '/home/siddharth/catkin_ws/src/CIS700_Squirtle/squirtle_navigation/include/NavigationKillNodes.sh',
			# 'find_person' : '/home/siddharth/catkin_ws/src/CIS700_Squirtle/squirtle_navigation/include/NavigationKillNodes.sh',
			# 'follow_person' : '/home/siddharth/catkin_ws/src/CIS700_Squirtle/squirtle_navigation/include/NavigationKillNodes.sh',
			# 'retrieve_message' : '/home/siddharth/catkin_ws/src/CIS700_Squirtle/squirtle_navigation/include/NavigationKillNodes.sh',
			# 'deliver_message' : '/home/siddharth/catkin_ws/src/CIS700_Squirtle/squirtle_navigation/include/NavigationKillNodes.sh',
		# }
		self.robotState()

if __name__ == '__main__':
	try:
		robotStateNode()
	except rospy.ROSInterruptException:
		rospy.loginfo("Exception in robotStateNode")
