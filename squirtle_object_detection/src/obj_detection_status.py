#!/usr/bin/env python

'''
Node to send object detection status to the robot state
by Siddharth Srivatsa

Publishes - /current_subroutine_status
Subscribes - 

'''

import roslib
import rospy
import os


class subsroutinestatus:

	def __init__(self, argument):
		self.subRoutineStatus = 0
		# Setup the publishers and subscribers
		rospy.init_node("objectDetectStatus", anonymous=True)
		self.SubRoutineStatusPub = rospy.Publisher('current_subroutine_status', String, queue_size=10)
		
		os.system('rosrun opencv_files tabletop_detector')
		rospy.Timer(rospy.Duration(10), object_callback)
		while not rospy.is_shutdown():
			# do nothing
			pass
		rospy.spin()
			

	def object_callback():
		os.system('/home/squirtle/catkin_ws/src/CIS700_Squirtle/squirtle_object_detection/include/kill_tabletop_detector.sh')
		for (dirpath, dirnames, filenames) in walk("/home/squirtle/images"):
			f.extend(filenames)
			break

		for filename in f:
			obj = os.system('python ~/Documents/caffe/python/workingTest.py ' + filename)
			if(obj == argument):
				print "Identified object is " + obj

		os.system('rosrun opencv_files tabletop_detector')
		return


if __name__=="__main__":
    if len(sys.argv) != 4:
        print("usage: my_node.py arg1")
    else:
        subsroutinestatus(sys.argv[1])