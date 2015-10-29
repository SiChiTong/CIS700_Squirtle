#!/usr/bin/env python
'''
    Node to get the destination for the robot to travel to
    Convert it to x and y co-ordinates and send it move base
    through the action server
    Author: Siddharth Srivatsa
'''

import rospy
from nav_msgs.msg import Odometry
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import *
import actionlib
import move_base_msgs

def odomcallback(data):
    MoveBaseClient = actionlib.SimpleActionClient('move_base', move_base_msgs.msg.MoveBaseAction)
    MoveBaseClient.wait_for_server()
    goal = MoveBaseGoal()

  # we'll send a goal to the robot to move 1 meter forward
    goal.target_pose.header.frame_id = "map";
    goal.target_pose.header.stamp = rospy.Time.now()

    goal.target_pose.pose.position.x = data.position.x
    goal.target_pose.pose.position.y = data.position.y
    goal.target_pose.pose.position.z = data.position.z
    goal.target_pose.pose.orientation.w = data.orientation.w
    goal.target_pose.pose.orientation.x = data.orientation.x
    goal.target_pose.pose.orientation.y = data.orientation.y
    goal.target_pose.pose.orientation.z = data.orientation.z

    MoveBaseClient.send_goal(goal)
    MoveBaseClient.wait_for_result()

    sub_once.unregister()
    
def destinationPoint():
    rospy.init_node('destinationPoint', anonymous=True)
    global sub_once
    sub_once = rospy.Subscriber('/goToPoint', Pose, odomcallback)

    rospy.spin()

if __name__ == '__main__':
    destinationPoint()
