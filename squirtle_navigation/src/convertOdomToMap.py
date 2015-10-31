#!/usr/bin/env python

import rospy
import roslib
from nav_msgs import Odometry
from geometry_msgs.msg import *
import tf

class convertOdomToMap:
    def __init__(self):
    	sub = rospy.Subscriber('/odom', Odometry, odomcallback)

    def odomcallback():
    	self.curPosPub = rospy.Publisher('curPosInMap', Pose, queue_size=10)
    	curMapPos = Pose()
    	while not rospy.is_shutdown():
	    	try:
	    		(trans,rot) = listener.lookupTransform('/odom', '/map', rospy.Time())

	    		curMapPos.position.x = data.pose.pose.position.x + trans[0]
    			curMapPos.position.y = data.pose.pose.position.y + trans[1]
			    curMapPos.position.z = data.pose.pose.position.z + trans[2]
			    curMapPos.orientation.w = data.pose.pose.orientation.w + rot[0]
			    curMapPos.orientation.x = data.pose.pose.orientation.x + rot[1]
			    curMapPos.orientation.y = data.pose.pose.orientation.y + rot[2]
			    curMapPos.orientation.z = data.pose.pose.orientation.z + rot[3]
			    self.curPosPub.publish(curMapPos)

	    	except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
	    		continue
			rate.sleep()
		rospy.spin()

if __name__ == '__main__':
    try:
        convertOdomToMap()
    except rospy.ROSInterruptException:
        pass