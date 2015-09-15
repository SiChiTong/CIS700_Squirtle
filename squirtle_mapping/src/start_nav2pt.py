#!/usr/bin/env python

'''
Listen for SLAM to complete. "SLAM_complete"
Call necessary commands to close SLAM nodes and start up go-to-point nodes

'''

import rospy
import os
from std_msgs.msg import String

def callback(data):
    #rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    
    # save map
    #os.system("rosrun map_server map_saver -f mymap")
    
    # close SLAM nodes
    #os.system("rosnode kill BLAH")
    
    # open navigation stuff
    os.system("roslaunch turtlebot_gazebo amcl_demo.launch map_file:=/path/to/map/mymap.yaml")
    os.system("roslaunch turtlebot_rviz_launchers view_navigation.launch")
    
    
def start_nav2pt():

    rospy.init_node('start_nav2pt', anonymous=True)

    rospy.Subscriber("SLAM_complete", String, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    start_nav2pt()

