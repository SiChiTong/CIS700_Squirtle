#!/usr/bin/env python

'''
Node to keep track of Robot state 
by Siddharth Srivatsa

publishes - /RobotState
subscribes - /current_task, /current_subroutine_status

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
		rospy.Subscriber("/current_task", String, self.TaskListMessageCallback)
		rospy.Subscriber("/current_subroutine_status", String, self.SubroutineStatusMessageCallback)
		self.StatePub = rospy.Publisher('RobotState', String, queue_size=10)
		
		rate = rospy.Rate(10) # Publish at 10hz
		while not rospy.is_shutdown():
			# Monitor the status of the current subroutine constantly and act accordingly
			if (self.subroutineStatus == "complete"):
				subRoutineToKill = self.currentTask.split()
				subRoutineToKill = subRoutineToKill[0]
				os.system(self.killSubroutines[subRoutineToKill])
				self.taskStatus = "success"
				self.StatePub.publish(self.taskStatus + " " + str(self.currentTask))
				# If python uses pointers, fix this
				self.lastTask = self.currentTask
				self.subroutineStatus = "idle"
				self.taskStatus = "task_not_started"

			elif (self.subroutineStatus == "error"):
				os.system(self.killSubroutines(self.currentSubroutine))
				# Nodes may get reset, you will lose data
				self.taskStatus = "fail"
				#os.system("Find Why you failed and act accordingly?")
				# Shaky ground here, not sure how the three different fail modes are handled
				self.StatePub.publish(self.taskStatus + " " + str(self.currentTask))

			elif (self.subroutineStatus == "going_on"):
				self.taskStatus = "in_progress"
				self.StatePub.publish(self.taskStatus + " " + str(self.currentTask))
				
			elif (self.subroutineStatus == 'idle'):
				self.taskStatus = "task_not_started"
				self.StatePub.publish(self.taskStatus + " " + str(self.currentTask))
			rate.sleep()
		print(self.taskStatus)
		print(self.subroutineStatus)
		rospy.spin();


	# Start a new subroutine you receive a new message from the TaskList
	def TaskListMessageCallback(self, data):
		self.currentTask = data.data
		taskWithParam = self.currentTask.split()
		self.currentSubroutine = self.subroutines[taskWithParam[0]]
		parameterString = ""
		for i in range(1,len(taskWithParam)):
			parameterString = parameterString + "P" + str(i) + ":=" + taskWithParam[i] + " "			# For each paramter convert it to a string to make it a system call
		if (self.taskStatus != "in_progress" and self.lastTask != self.currentTask):
			os.system(self.currentSubroutine + " " + parameterString)
			print(self.currentSubroutine + " " + parameterString)
			self.taskStatus = "in_progress"
			rate = rospy.Rate(10)
			rate.sleep()

	# Get the status of the subRoutine
	def SubroutineStatusMessageCallback(self, data):
		self.subroutineStatus = data.data

	def __init__(self):
		self.currentTask = None
		self.subroutineStatus = "idle"
		self.taskStatus = "task_not_started"
		self.currentSubroutine = None
		self.lastTask = ""

		# Maintain a list of subroutines to be called for each sub task the TaskList sends
		self.subroutines = {
			'go_to_room' : 'roslaunch squirtle_navigation SquirtleNavigation.launch',
			'retrieve_object' : 'roslaunch squirtle_speech squirtle_speech.launch',
			'deliver_object' : 'roslaunch squirtle_speech squirtle_speech.launch',
			'find_person' : 'roslaunch squirtle_speech squirtle_speech.launch',
			# 'follow_person' : '/home/siddharth/catkin_ws/src/CIS700_Squirtle/squirtle_navigation/launch/SquirtleNavigation.launch',
			# 'retrieve_message' : '/home/siddharth/catkin_ws/src/CIS700_Squirtle/squirtle_navigation/launch/SquirtleNavigation.launch',
			# 'deliver_message' : '/home/siddharth/catkin_ws/src/CIS700_Squirtle/squirtle_navigation/launch/SquirtleNavigation.launch',
		}

		self.killSubroutines = {
			'go_to_room' : '~/catkin_ws/src/CIS700_Squirtle/squirtle_navigation/include/NavigationKillNodes.sh',
			'retrieve_object' : '~/catkin_ws/src/CIS700_Squirtle/squirtle_speech/include/killSpeechNodes.sh',
			'deliver_object' : '~/catkin_ws/src/CIS700_Squirtle/squirtle_speech/include/killSpeechNodes.sh',
			'find_person' : '~/catkin_ws/src/CIS700_Squirtle/squirtle_speech/include/killSpeechNodes.sh',
			# 'follow_person' : '/home/siddharth/catkin_ws/src/CIS700_Squirtle/squirtle_navigation/include/NavigationKillNodes.sh',
			# 'retrieve_message' : '/home/siddharth/catkin_ws/src/CIS700_Squirtle/squirtle_navigation/include/NavigationKillNodes.sh',
			# 'deliver_message' : '/home/siddharth/catkin_ws/src/CIS700_Squirtle/squirtle_navigation/include/NavigationKillNodes.sh',
		}
		self.robotState()

if __name__ == '__main__':
	try:
		robotStateNode()
	except rospy.ROSInterruptException:
		rospy.loginfo("Exception in robotStateNode")
