#!/usr/bin/env python

'''
Node to send navigation status to the robot state
by Siddharth Srivatsa

uint8 PENDING           0 # The goal has yet to be processed by the action server
uint8 ACTIVE            1 # The goal is currently being processed by the action server
uint8 PREEMPTED         2 # The goal received a cancel request after it started executing
                          #   and has since completed its execution (Terminal State)
uint8 SUCCEEDED         3 # The goal was achieved successfully by the action server (Terminal State)
uint8 ABORTED           4 # The goal was aborted during execution by the action server due
                          #    to some failure (Terminal State)
uint8 REJECTED          5 # The goal was rejected by the action server without being processed,
                          #    because the goal was unattainable or invalid (Terminal State)
uint8 PREEMPTING        6 # The goal received a cancel request after it started executing
                          #    and has not yet completed execution
uint8 RECALLING         7 # The goal received a cancel request before it started executing,
                          #    but the action server has not yet confirmed that the goal is canceled
uint8 RECALLED          8 # The goal received a cancel request before it started executing
                          #    and was successfully cancelled (Terminal State)
uint8 LOST              9 # An action client can determine that a goal is LOST. This should not be
                          #    sent over the wire by an action server

'''

import rospy
import roslib
import rospy
import os
import tf
import time
import sys
from std_msgs.msg import String
from std_msgs.msg import Bool
from geometry_msgs.msg import *
from actionlib_msgs.msg import GoalStatusArray

class subsroutinestatus:

	def __init__(self, argument):
		self.subRoutineStatus = 'Not Initialized'
		self.subRoutineStatus = 0
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
		
	   	self.roomToGoal = {
		'GRASP_Lab' : [2.66051835131, 1.814285866, 0.0, 0.996794512902, 0.0, 0.0, -0.0800043689302],
		'vending_machine' : [23.6841973344, -13.0116452665, 0.0, 0.927753744615, 0.0, 0.0, 0.373192965305],
		# 'bump_space' : [-14.9074779785, 15.5285880624, 0.0, 1, 0, 0, 0],
		'Charity_Office' : [-27.1387192384, 1.62747479075, 0.0, 0.0546438511255, 0.0, 0.0, 0.998505908613]
		}
		
		self.subroutine(argument)

	def subroutine(self, argument):
		# Setup the publishers and subscribers
		rospy.init_node("subsroutinestatus", anonymous=True)
		self.SubRoutineStatusPub = rospy.Publisher('current_subroutine_status', String, queue_size=10)
		self.goalPub = rospy.Publisher('goToPoint', Pose, queue_size=10)

		self.SubRoutineStatusSub = rospy.Subscriber('/move_base/status', GoalStatusArray, self.SubRoutineStatusCallBack)
		#self.SubRoutineStatusSub = rospy.Subscriber("/statusList", String, self.SubRoutineStatusCallBack)
		listener = tf.TransformListener()

		rate = rospy.Rate(10) # Publish at 10hz
		goal = Pose()
		print("OK")
		while not rospy.is_shutdown():
			try:
				now = rospy.Time.now()
				(trans,rot) = listener.lookupTransform('/odom', '/map', now)
				GoalPos = self.roomToGoal[argument]
				goal.position.x = GoalPos[0] + trans[0]
				goal.position.y = GoalPos[1] + trans[1]
				goal.position.z = GoalPos[2] + trans[2]
				goal.orientation.w = GoalPos[3] + rot[0]
				goal.orientation.x = GoalPos[4] + rot[1]
				goal.orientation.y = GoalPos[5] + rot[2]
				goal.orientation.z = GoalPos[6] + rot[3]
				self.goalPub.publish(goal)
				self.SubRoutineStatusPub.publish(self.status[self.subRoutineStatus])
			except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
				# GoalPos = self.roomToGoal[argument]
				# goal.position.x = GoalPos[0] + trans[0]
				# goal.position.y = GoalPos[1] + trans[1]
				# goal.position.z = GoalPos[2] + trans[2]
				# goal.orientation.w = GoalPos[3] + rot[0]
				# goal.orientation.x = GoalPos[4] + rot[1]
				# goal.orientation.y = GoalPos[5] + rot[2]
				# goal.orientation.z = GoalPos[6] + rot[3]
				# self.goalPub.publish(goal)
				# self.SubRoutineStatusPub.publish(self.status[self.subRoutineStatus])
				continue
				
			except RuntimeError as e:
				print ("Ok now I know who the culprit is")
				ROS_ERROR("Exception: [%s]", e.what());
			rate.sleep()
		rospy.spin()

	def SubRoutineStatusCallBack(self, data):
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
