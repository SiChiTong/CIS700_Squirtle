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

from collections import deque #queue for buffering mic data
from numpy import argmax


class Direction_estimator:
    """This class to for estimating voice angle using microphone array strength"""
    def __init__(self):

        rospy.init_node('voice_direction_estimator')
        rospy.on_shutdown(self.cleanup)

        # publish to turtlebot's velocity teleop topic
        self.ang_pub = rospy.Publisher("~estimated_direction",DirectionScore,queue_size = 10)

        # subcribe to arduino microphone data collector
        rospy.Subscriber('/arduino_collector/mic_array_strength',Vector3,self.receive_mic_callback,queue_size = 10)

        # provide service for getting the current estimated direction
        rospy.Service('~get_direction_score', GetDirectionScore, self.direction_score_provider)
        
        # provide service for calibration procedure
        rospy.Service('~start_mic_calibration', StartCalibration, self.calibration_process)


        self.window_size = 8
        self.mic_data_buffer_x = deque(maxlen = self.window_size)
        self.mic_data_buffer_y = deque(maxlen = self.window_size)
        self.mic_data_buffer_z = deque(maxlen = self.window_size)
        self.est_angle = 0
        self.est_score = 0

    def update_buffer(self,mic_x,mic_y,mic_z):
        # update self.mic_data_buffer
        # append three mic data into buffer, it will automatically delete old data to keep it at a fixed size
        self.mic_data_buffer_x.append(mic_x)
        self.mic_data_buffer_y.append(mic_y)
        self.mic_data_buffer_z.append(mic_z)

    def estimate_direction(self):
        #estimate direction according to mic_data_buffers
        sum_x = sum(self.mic_data_buffer_x)
        sum_y = sum(self.mic_data_buffer_y)
        sum_z = sum(self.mic_data_buffer_z)

        if argmax([sum_x,sum_y,sum_z]) == 0:
            # sum_x is the biggest
            main_angle = 0
            adjust_angle = ((sum_x-sum_z)-(sum_x-sum_y))/((sum_x-sum_z)+(sum_x-sum_y))*60
        
        elif argmax([sum_x,sum_y,sum_z]) == 1:
            # sum_y is the biggest
            main_angle = 120
            adjust_angle = ((sum_y-sum_x)-(sum_y-sum_z))/((sum_y-sum_x)+(sum_y-sum_z))*60

        elif argmax([sum_x,sum_y,sum_z]) == 2:    
            # sum_z is the biggest
            main_angle = 240
            adjust_angle = ((sum_z-sum_y)-(sum_z-sum_x))/((sum_z-sum_y)+(sum_z-sum_x))*60

        self.est_angle = self.normalize_angle(main_angle + adjust_angle)  
        self.score = 0
         
        return (self.est_angle , self.score)

    def receive_mic_callback(self,msg):
        # handle mic data when arrive

        # update buffer queue 
        self.update_buffer(msg.x, msg.y, msg.z)
        self.estimate_direction()

        msg_pub = DirectionScore()
        msg_pub.direction = self.est_angle
        msg_pub.score = self.score
       
        rospy.loginfo(self.est_angle)

    def direction_score_provider(self,req):
        # service call back 
        response = GetDirectionScoreResponse()
        response.direction = self.est_angle 
        response.score = self.est_score
        
        return response
    
    def normalize_angle(self,raw_angle):
        # make angle -180 ~ 180 in degree     
        if raw_angle > 180:
            norm_angle = raw_angle - 360
        elif raw_angle < -180:
            norm_angle = raw_angle + 360
        else:
            norm_angle = raw_angle

        return norm_angle

    def calibration_process(self,req):
        rospy.loginfo("Starting Calibration Process...")
        rospy.sleep(10)
        
        return StartCalibrationResponse()


    def cleanup(self):
        # cleanup to ensure a decent shutdown
        rospy.loginfo("Shutting down Direction_estimator node...")

if __name__=="__main__":
    try:
        Direction_estimator()
        rospy.spin()
    except rospy.ROSInterruptException:
        rospy.loginfo("Direction_estimator finished")



