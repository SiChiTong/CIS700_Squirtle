#!/usr/bin/env python

'''
Node to send navigation status to the robot state
by Siddharth Srivatsa

uint8 status
uint8 PENDING            # The goal has yet to be processed by the action server
uint8 ACTIVE             # The goal is currently being processed by the action server
uint8 PREEMPTED          # The goal received a cancel request after it started executing
                         #   and has since completed its execution (Terminal State)
uint8 SUCCEEDED          # The goal was achieved successfully by the action server (Terminal State)
uint8 ABORTED            # The goal was aborted during execution by the action server due
                         #    to some failure (Terminal State)
uint8 REJECTED           # The goal was rejected by the action server without being processed,
                         #    because the goal was unattainable or invalid (Terminal State)
uint8 PREEMPTING         # The goal received a cancel request after it started executing
                         #    and has not yet completed execution
uint8 RECALLING          # The goal received a cancel request before it started executing,
                         #    but the action server has not yet confirmed that the goal is canceled
uint8 RECALLED           # The goal received a cancel request before it started executing
                         #    and was successfully cancelled (Terminal State)
uint8 LOST               # An action client can determine that a goal is LOST. This should not be
                         #    sent over the wire by an action server

'''

import rospy
import roslib
import rospy
import os
import time
from std_msgs.msg import String
from std_msgs.msg import Bool
from actionlib_msgs import GoalStatusArray

class subsroutinestatus {
	self.subRoutineStatus = None

	self.status = {
		'PENDING' : 'in progress' 
		'ACTIVE' : 'in progress'
		'SUCCEEDED' : 'complete'
		'PREEMPTED' : 'fail'
		'ABORTED' : 'fail'
		'REJECTED' : 'fail'
		'PREEMPTING' : 'fail'
		'RECALLING' : 'fail'
		'RECALLED' : 'fail'
		'LOST' : 'fail'
	}
	
	def __init__(self):
		# Setup the publishers and subscribers
		rospy.init_node("subsroutinestatus", anonymous=True)	
		self.SubRoutineStatusPub = rospy.Publisher('current_subroutine_status', String, queue_size=10)
		self.SubRoutineStatusSub = rospy.subscriber('\status_list', GoalStatusArray, SubRoutineStatusCallBack)
		rate = rospy.Rate(10) # Publish at 10hz
		
		while not rospy.is_shutdown():
			SubRoutineStatusPub.publish(status(subRoutineStatus))
			rate.sleep()

		rospy.spin();


	def SubRoutineStatusCallBack(data data):
		subRoutineStatus = data.text

}