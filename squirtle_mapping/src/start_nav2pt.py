#!/usr/bin/env python

'''
Listen for SLAM to complete. "SLAM_complete"
Call necessary commands to close SLAM nodes and start up go-to-point nodes

'''

import rospy
import os
from std_msgs.msg import String
from actionlib_msgs.msg import GoalStatusArray

def callback(data):
    if (data.status_list==4 || data.status_list==5):
        print("Frontier Exploration aborted")
        # save map, Confirm where map is being saved
        os.system("rosrun map_server map_saver -f mymap")
    
        # close SLAM nodes
        os.system("rosnode kill /explore_client")
        os.system("rosnode kill /explore_server")
    
        # open navigation stuff
        os.system("roslaunch turtlebot_navigation amcl_demo.launch map_file:=/path/to/map/mymap.yaml")
        os.system("roslaunch turtlebot_rviz_launchers view_navigation.launch")

    if (data.status_list==3):
        print("Frontier Exploration succeeded")

def start_nav2pt():

    rospy.init_node('start_nav2pt', anonymous=True)

    rospy.Subscriber("explore_server/status", GoalStatusArray, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    start_nav2pt()

