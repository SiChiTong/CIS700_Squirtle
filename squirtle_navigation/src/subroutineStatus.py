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
import time
import sys
from std_msgs.msg import String
from std_msgs.msg import Bool
from geometry_msgs.msg import *
from actionlib_msgs.msg import GoalStatusArray

class subsroutinestatus:

	def __init__(self, argument):
		self.subRoutineStatus = 'Not Initialized'
		self.subRoutineStatus = "0"
		self.status = {
		'0' : 'going_on',
		'1' : 'going_on',
		'2' : 'complete',
		'3' : 'fail',
		'4' : 'fail',
		'5' : 'fail',
		'6' : 'fail',
		'7' : 'fail',
		'8' : 'fail',
		'9' : 'fail'
		}
		
		self.roomToGoal = {
		'GRASP_Lab' : [13.4993789353, 23.6495585172, 0.0],
		'vending_machine' : [-1.39744438739, -0.821078977705, 0.0],
		'bump_space' : [-14.9074779785, 15.5285880624, 0.0],
		'Charity_Office' : [-29.9078956456, 0.3836611574, 0.0]
		}
		
		self.subroutine(argument)

	def subroutine(self, argument):
		position = [0, 0, 0]
		quaternion = [1, 0, 0, 0]
		# Setup the publishers and subscribers
		rospy.init_node("subsroutinestatus", anonymous=True)
		self.SubRoutineStatusPub = rospy.Publisher('current_subroutine_status', String, queue_size=10)
		self.goalPub = rospy.Publisher('goToPoint', Pose, queue_size=10)
#		self.SubRoutineStatusSub = rospy.Subscriber('/move_base/status', GoalStatusArray, self.SubRoutineStatusCallBack)
		#self.SubRoutineStatusSub = rospy.Subscriber("/statusList", String, self.SubRoutineStatusCallBack)
		rate = rospy.Rate(10) # Publish at 10hz
		goal = Pose()
		print("OK")
		while not rospy.is_shutdown():
			currentPos = self.roomToGoal[argument]
			goal.position.x = position[0]
			goal.position.y = position[1]
			goal.position.z = position[2]
			goal.orientation.w = quaternion[0]
			goal.orientation.x = quaternion[1]
			goal.orientation.y = quaternion[2]
			goal.orientation.z = quaternion[3]
			print(goal)
			self.goalPub.publish(goal)
			self.SubRoutineStatusPub.publish(self.status[self.subRoutineStatus])
			rate.sleep()
		rospy.spin()

	def SubRoutineStatusCallBack(self, data):
		self.subRoutineStatus = data.status
		# listener = tf.TransformListener()
		# try:
  #           (position, quaternion) = listener.lookupTransform('/odom', '/map', rospy.Time(0))
  #           quaternion = tf.transformations.quaternion_from_euler(rot[0], rot[1], rot[2])
  #       except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
  #           continue

if __name__=="__main__":
    if len(sys.argv) != 4:
        print("usage: my_node.py arg1")
    else:
        subsroutinestatus(sys.argv[1])
