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
from os import walk
import sys
from std_msgs.msg import *

class subsroutinestatus:

	def __init__(self, argument):
		self.subRoutineStatus = 0
		self.obj_to_detect = argument
		# Setup the publishers and subscribers
		rospy.init_node("objectDetectStatus", anonymous=True)
		self.SubRoutineStatusPub = rospy.Publisher('current_subroutine_status', String, queue_size=10)
		self.objectPub = rospy.Publisher('detected_object', String, queue_size=10)
		os.system('rosrun opencv_files tabletop_detector &')
		
		rospy.Timer(rospy.Duration(10.0), self.object_callback)
		self.SubRoutineStatusPub.publish("While") 
		
		while not rospy.is_shutdown():
			# do nothing
				pass
		rospy.spin()
			

	def object_callback(self, event):
		print "I killed and re-called tabletop"
		os.system('/home/squirtle/catkin_ws/src/CIS700_Squirtle/squirtle_object_detection/include/kill_tabletop_detector.sh')
		f = []
		for (dirpath, dirnames, filenames) in walk("/home/squirtle/images"):
			f.extend(filenames)
			break
			
		print f
		objects = []
		for filename in f:
			obj = os.system('python /home/squirtle/Documents/caffe/python/testSVM.py /home/squirtle/images/' + filename)
			#obj = obj.split('_')[0]
			objects.append(obj)
		if(self.obj_to_detect in objects):
			print "Identified object is " + obj
			self.objectPub(self.obj_to_detect)
		else:
			print " I did not find the object :("	
			self.objectPub("no obj")
		os.system('rosrun opencv_files tabletop_detector &')
		self.SubRoutineStatusPub.publish("Callback") 
		return


if __name__=="__main__":
    if len(sys.argv) != 4:
        print("usage: my_node.py arg1")
    else:
        subsroutinestatus(sys.argv[1])
