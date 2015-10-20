#!/usr/bin/env python


import rospy



'''
Node to keep track of Robot state 
by Siddharth Srivatsa

'''


import roslib
import rospy
import os
import time
from std_msgs.msg import String
from std_msgs.msg import Bool


class robotState():
	
	# Flags to send to the Task List - "in progress",  "success", "fail"
	# Status messages to receive from the individual subroutines "complete", "error"
	# Function to call individual subroutines (Takes in name of the subroutine as as argument and calls the corresponfing launch file)
	self.currentTask = None
	self.subroutineStatus = None
	self.taskStatus = None
	self.currentSubroutine = None

	# Maintain a list of subroutines to be called for each sub task the TaskList sends
	self.subroutines = {
		'go_to_room' : '/home/siddharth/catkin_ws/src/CIS700_Squirtle/squirtle_navigation/launch/SquirtleNavigation.launch'
		'retrieve_object' : '/home/siddharth/catkin_ws/src/CIS700_Squirtle/squirtle_navigation/launch/quirtleNavigation.launch'
		'deliver_object' : '/home/siddharth/catkin_ws/src/CIS700_Squirtle/squirtle_navigation/launch/SquirtleNavigation.launch'
		'find_person' : '/home/siddharth/catkin_ws/src/CIS700_Squirtle/squirtle_navigation/launch/SquirtleNavigation.launch'
		'follow_person' : '/home/siddharth/catkin_ws/src/CIS700_Squirtle/squirtle_navigation/launch/SquirtleNavigation.launch'
		'retrieve_message' : '/home/siddharth/catkin_ws/src/CIS700_Squirtle/squirtle_navigation/launch/SquirtleNavigation.launch'
		'deliver_message' : '/home/siddharth/catkin_ws/src/CIS700_Squirtle/squirtle_navigation/launch/SquirtleNavigation.launch'
	}

	self.killSubroutines = {
		'go_to_room' : '/home/siddharth/catkin_ws/src/CIS700_Squirtle/squirtle_navigation/include/NavigationKillNodes.sh'
		'retrieve_object' : '/home/siddharth/catkin_ws/src/CIS700_Squirtle/squirtle_navigation/include/NavigationKillNodes.sh'
		'deliver_object' : '/home/siddharth/catkin_ws/src/CIS700_Squirtle/squirtle_navigation/include/NavigationKillNodes.sh'
		'find_person' : '/home/siddharth/catkin_ws/src/CIS700_Squirtle/squirtle_navigation/include/NavigationKillNodes.sh'
		'follow_person' : '/home/siddharth/catkin_ws/src/CIS700_Squirtle/squirtle_navigation/include/NavigationKillNodes.sh'
		'retrieve_message' : '/home/siddharth/catkin_ws/src/CIS700_Squirtle/squirtle_navigation/include/NavigationKillNodes.sh'
		'deliver_message' : '/home/siddharth/catkin_ws/src/CIS700_Squirtle/squirtle_navigation/include/NavigationKillNodes.sh'
	}

	def __init__(self):
		# Setup the publishers and subscribers
		rospy.init_node("robotStateNode", anonymous=True)	
		self.StatePub = rospy.Publisher('RobotState', String, queue_size=10)
		self.TaskListSub = rospy.Subscriber("/current_task",String,self.TaskListMessageCallback)
		self.SubroutineStatusSub = rospy.Subscriber("/current_subroutine_status",String,self.SubroutineStatusMessageCallback)

		rate = rospy.Rate(10) # Publish at 10hz
		while not rospy.is_shutdown():

			# Monitor the status of the current subroutine constantly and act accordingly
			if (self.subroutineStatus == "complete"):
				os.system(self.killSubroutines(currentSubroutine))
				taskStatus = "success"
				self.StatePub.publish(taskStatus)
				return

			elif (self.subroutineStatus == "error"):
				os.system(self.killSubroutines(currentSubroutine))
				# Nodes may get reset, you will lose data
				taskStatus = "fail"
				os.system("Find Why you failed and act accordingly?")
				# Shaky ground here, not sure how the three different fail modes are handled
				self.StatePub.publish(taskStatus)

			else
				taskStatus = "in progress"
				self.StatePub.publish(taskStatus)

			rate.sleep()

		rospy.spin();


	# Start a new subroutine you receive a new message from the TaskList
	def TaskListMessageCallback(data data):
		self.currentTask = data.data
		self.currentSubroutine = self.subroutines(currentTask)
		os.system(currentSubroutine)

	# Get the status of the subRoutine
	def SubroutineStatusMessageCallback(data data):
		self.subroutineStatus = data.data


if __name__ == '__main__':
	try:
		tasklist()
	except rospy.ROSInterruptException:
		rospy.loginfo("exception in robotStateNode")
