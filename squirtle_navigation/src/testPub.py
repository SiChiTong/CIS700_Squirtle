#!/usr/bin/env python
# license removed for brevity
'''
    Test script for publishing status messages to check working of the pipeline
'''
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import *
import tf

class example:
    def __init__(self):
        pub = rospy.Publisher('current_subroutine_status', String, queue_size=10)
        rospy.init_node('testPub', anonymous=True)
        rospy.Subscriber("/current_task",String,self.TaskListMessageCallback)
        listener = tf.TransformListener()
        rate = rospy.Rate(10) # 10hz

        while not rospy.is_shutdown():
            hello_str = "going_on"
            pub.publish(hello_str)
            try:
                (trans,rot) = listener.lookupTransform('/base_link', '/odom', rospy.Time())
                print("t = ")
                print(trans)
                print("r = ")
                print(rot)
            except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
                continue
            rate.sleep()
        rospy.spin()

    def TaskListMessageCallback(self, data):
        # print data.data
        x = 1

if __name__ == '__main__':
    try:
        example()
    except rospy.ROSInterruptException:
        pass