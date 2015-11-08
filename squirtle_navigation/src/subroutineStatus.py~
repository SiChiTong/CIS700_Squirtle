#!/usr/bin/env python

'''
Node to send navigation status to the robot state
by Siddharth Srivatsa

Publishes - /current_subroutine_status
Subscribes - /move_base/status

PENDING           0 # The goal has yet to be processed by the action server
ACTIVE            1 # The goal is currently being processed by the action server
PREEMPTED         2 # The goal received a cancel request after it started executing
                    #   and has since completed its execution (Terminal State)
SUCCEEDED         3 # The goal was achieved successfully by the action server (Terminal State)
ABORTED           4 # The goal was aborted during execution by the action server due
                    #    to some failure (Terminal State)
REJECTED          5 # The goal was rejected by the action server without being processed,
                    #    because the goal was unattainable or invalid (Terminal State)
PREEMPTING        6 # The goal received a cancel request after it started executing
                    #    and has not yet completed execution
RECALLING         7 # The goal received a cancel request before it started executing,
                    #    but the action server has not yet confirmed that the goal is canceled
RECALLED          8 # The goal received a cancel request before it started executing
                    #    and was successfully cancelled (Terminal State)
LOST              9 # An action client can determine that a goal is LOST. This should not be
                    #    sent over the wire by an action server

'''

import roslib
import rospy
import os
import tf
import time
import sys
from std_msgs.msg import *
from geometry_msgs.msg import *
from actionlib_msgs.msg import GoalStatusArray

class subsroutinestatus:

	def __init__(self, argument):
		self.subRoutineStatus = 0

		# Modify the status message got from the navigation stack to the required format
		self.status = {
		0 : 'going_on',
		1 : 'going_on',
		2 : 'complete',
		3 : 'complete',
		4 : 'error',
		5 : 'error',
		6 : 'error',
		7 : 'error',
		8 : 'error',
		9 : 'error',
		100 : 'idle'
		}

		# Coordinates of the desired locations in the map
	   	self.roomToGoal = {
		'GRASP_Lab' : [2.66051835131, 1.814285866, 0.0, 0.996794512902, 0.0, 0.0, -0.0800043689302],
		'vending_machine' : [23.6841973344, -13.0116452665, 0.0, 0.927753744615, 0.0, 0.0, 0.373192965305],
		# 'bump_space' : [-14.9074779785, 15.5285880624, 0.0, 1, 0, 0, 0],
		'Charity_Office' : [-27.1387192384, 1.62747479075, 0.0, 0.0546438511255, 0.0, 0.0, 0.998505908613]
		}
		
		self.subroutine(argument)

	def subroutine(self, argument):
		goal = Pose()
		# Setup the publishers and subscribers
		rospy.init_node("subsroutinestatus", anonymous=True)
		self.SubRoutineStatusPub = rospy.Publisher('current_subroutine_status', String, queue_size=10)
		self.goalPub = rospy.Publisher('goToPoint', Pose, queue_size=10)
		self.SubRoutineStatusSub = rospy.Subscriber('/move_base/status', GoalStatusArray, self.SubRoutineStatusCallBack)
		
		rate = rospy.Rate(10) # Publish at 10hz
		while not rospy.is_shutdown():
			GoalPos = self.roomToGoal[argument]
			# Publish the goal point
			goal.position.x = GoalPos[0]
			goal.position.y = GoalPos[1]
			goal.position.z = GoalPos[2]
			goal.orientation.w = GoalPos[3]
			goal.orientation.x = GoalPos[4]
			goal.orientation.y = GoalPos[5]
			goal.orientation.z = GoalPos[6]
			self.goalPub.publish(goal)
			self.SubRoutineStatusPub.publish(self.status[self.subRoutineStatus])
			rate.sleep()
		rospy.spin()

	def SubRoutineStatusCallBack(self, data):
		# If subroutine hasn't started it's status should be idle, else get the status from move base
		if not data.status_list:
			self.subRoutineStatus = 100
		else:
			self.subRoutineStatus = data.status_list[-1].status
			print data.status_list[-1].status

if __name__=="__main__":
    if len(sys.argv) != 4:
        print("usage: my_node.py arg1")
    else:
        subsroutinestatus(sys.argv[1])
