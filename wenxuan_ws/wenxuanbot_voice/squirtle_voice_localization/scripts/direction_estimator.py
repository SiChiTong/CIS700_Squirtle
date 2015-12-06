#!/usr/bin/env python

import sys
import rospy
from sound_play.libsoundplay import SoundClient
from std_msgs.msg import String
import std_srvs.srv
import random
import threading
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Vector3
from squirtle_voice_localization.msg import DirectionScore
from squirtle_voice_localization.srv import *




class Direction_estimator:
    """This class to for estimating voice angle using microphone array strength"""
    def __init__(self):

        rospy.init_node('direction_estimator')
        rospy.on_shutdown(self.cleanup)

        # publish to turtlebot's velocity teleop topic
        self.ang_pub = rospy.Publisher("~estimated_direction",DirectionScore,queue_size = 10)

        # subcribe to speech recognizer from pocketsphinx
        rospy.Subscriber('/arduino_collector/mic_array_strength',Vector3,self.receive_mic_callback,queue_size = 10)

        rospy.Service('~get_direction_score', GetDirectionScore, self.direction_score_provider)
        
        rospy.Service('start_mic_calibration', StartCalibration, self.calibration_process)


    def receive_mic_callback(self,msg):
        # handle mic data when receive 
        msg_pub = DirectionScore()
        msg_pub.direction = msg.x
        msg_pub.score = msg.y
        self.ang_pub.publish(msg_pub)
        rospy.loginfo(msg_pub)

    def direction_score_provider(self,req):
        # service call back 
        ret_val = GetDirectionScoreResponse()
        ret_val.direction = 180
        ret_val.score = 10
        
        return ret_val

    def calibration_process(self,req):
        rospy.loginfo("Starting Calibration Process...")
        rospy.sleep(10)
        return


    def cleanup(self):
        # cleanup to ensure a decent shutdown
        rospy.loginfo("Shutting down Direction_estimator node...")

if __name__=="__main__":
    try:
        Direction_estimator()
        rospy.spin()
    except rospy.ROSInterruptException:
        rospy.loginfo("Direction_estimator finished")



