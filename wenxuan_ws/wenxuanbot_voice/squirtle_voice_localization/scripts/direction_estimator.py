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
import tf
from tf.transformations import euler_from_quaternion
import math

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
        self.est_angle = 0.0
        self.est_score = 0.01

        # get the parameters, should set these in launch files 
        # also, self.<parameter> will be modified during calibration
        # offset is with respect of each microphone reading(which implies that if you changed arduino data collection rate it will change), 
        # and offset is always negative
        self.offset_mic_x = rospy.get_param('~offset_mic_x', 0)
        self.offset_mic_y = rospy.get_param('~offset_mic_y', 0)
        self.offset_mic_z = rospy.get_param('~offset_mic_z', 0)
        self.scale_mic_x = rospy.get_param('~scale_mic_x', 1.0)
        self.scale_mic_y = rospy.get_param('~scale_mic_y', 1.0)
        self.scale_mic_z = rospy.get_param('~scale_mic_z', 1.0)

        # publish to turtlebot's velocity teleop topic
        self.cmd_vel_pub = rospy.Publisher("/cmd_vel_mux/input/teleop",Twist,queue_size = 10)
        self.cmd_vel = Twist()

        self.tf_listener = tf.TransformListener()
        

    def update_buffer(self,mic_x,mic_y,mic_z):
        # update self.mic_data_buffer
        # append three mic data into buffer, it will automatically delete old data to keep it at a fixed size
        self.mic_data_buffer_x.append(mic_x)
        self.mic_data_buffer_y.append(mic_y)
        self.mic_data_buffer_z.append(mic_z)

    def estimate_direction(self):
        # estimate direction according to mic_data_buffers, with calibrated parameters
        sum_x = (sum(self.mic_data_buffer_x) + self.window_size * self.offset_mic_x) * self.scale_mic_x
        sum_y = (sum(self.mic_data_buffer_y) + self.window_size * self.offset_mic_y) * self.scale_mic_y
        sum_z = (sum(self.mic_data_buffer_z) + self.window_size * self.offset_mic_z) * self.scale_mic_z

        # strength_sum should always be positive
        if sum_x < 0:
            sum_x = 0
        if sum_y < 0:
            sum_y = 0              
        if sum_z < 0:
            sum_z = 0
        rospy.loginfo('')
        rospy.loginfo('sum_x: '+str(sum_x))
        rospy.loginfo('sum_y: '+str(sum_y))
        rospy.loginfo('sum_z: '+str(sum_z))
        try:
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
            self.est_score = (max([sum_x,sum_y,sum_z]) - min([sum_x,sum_y,sum_z])) / max([sum_x,sum_y,sum_z]) 
      
        except Exception, e:
            self.est_angle = 0 
            self.est_score = 0

         
        return (self.est_angle , self.est_score)

    def receive_mic_callback(self,msg):
        # handle mic data when arrive

        # update buffer queue 
        self.update_buffer(msg.x, msg.y, msg.z)
        self.estimate_direction()

        # for publishing
        msg_pub = DirectionScore()
        msg_pub.direction = self.est_angle
        msg_pub.score = self.est_score
        
        # log to debug
        #rospy.loginfo('Angle: ' + str(self.est_angle))
        #rospy.loginfo('Score: ' + str(self.score))

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

    def wait_for_certain_message(self,msg_str):
        
        received_msg = None
        while received_msg is None or received_msg.data != msg_str:
            try:
                received_msg = rospy.wait_for_message("/recognizer/output",String)
            except Exception, e:
                received_msg = None
        
        

    def calibration_process(self,req):
        # calibration needs recognizer, recognizer output topic, sound_play
        rospy.loginfo("Starting Calibration Process...")
        say_pub = rospy.Publisher('/mouth/string_to_say', String, queue_size=10)
        move_pub = rospy.Publisher('/cmd_vel_mux/input/teleop', String, queue_size=10) 
        tf_listener = tf.TransformListener()
        rospy.sleep(2)

        say_pub.publish("Calibration initialize complete, should we begin?")

        self.wait_for_certain_message("let's begin")
        

        say_pub.publish("Begin offset calibration, Please be quite for several seconds")
        rospy.sleep(5)
        rospy.sleep(4)
        #self.offset_mic_x = - sum(self.mic_data_buffer_x)/self.window_size
        #self.offset_mic_y = - sum(self.mic_data_buffer_y)/self.window_size
        #self.offset_mic_z = - sum(self.mic_data_buffer_z)/self.window_size
        rospy.loginfo("calibrated offset_mic_x: " + str(self.offset_mic_x));
        rospy.loginfo("calibrated offset_mic_y: " + str(self.offset_mic_y));
        rospy.loginfo("calibrated offset_mic_z: " + str(self.offset_mic_z));

        say_pub.publish("Thanks, offset calibration complete, begin scale calibration")

        say_pub.publish("Please stand in front of me and call me")
        
        self.wait_for_certain_message("i'm here")
        # doesn't really do anything except for making the person in front :)
        
        say_pub.publish("Thanks, please stay in position, rotating...")
        # here turtlebot will rotate to let you speak to his left side
        try:
            self.rotater(60)
        except Exception, e:
            rospy.loginfo('rotate failed, turtlebot maybe offline')
            pass
  
        say_pub.publish("OK, please call me like you did before")
        self.wait_for_certain_message("i'm here")
        # calibrate left side mic
        rospy.sleep(0.2)
        self.scale_mic_x = 1.0 # constant x

        sum_x = (sum(self.mic_data_buffer_x) + self.window_size * self.offset_mic_x)
        sum_z = (sum(self.mic_data_buffer_z) + self.window_size * self.offset_mic_z)

        try:
            self.scale_mic_z = float(sum_x) / float(sum_z)
        except Exception, e:
            pass
        
        rospy.loginfo("calibrated scale_mic_z: " + str(self.scale_mic_z));

        say_pub.publish("Thanks, stay in position, there is one last step...")
        try:
            self.rotater(-120)
        except Exception, e:
            rospy.loginfo('rotate failed, turtlebot maybe offline')
            pass
        
        say_pub.publish("OK, please call me")
        self.wait_for_certain_message("i'm here")
        # calibrate right side mic
        rospy.sleep(0.2)
        self.scale_mic_x = 1.0 # constant x
        sum_x = (sum(self.mic_data_buffer_x) + self.window_size * self.offset_mic_x)
        sum_y = (sum(self.mic_data_buffer_y) + self.window_size * self.offset_mic_y)

        try:
            self.scale_mic_y = float(sum_x) / float(sum_y)
        except Exception, e:
            pass   
        rospy.loginfo("calibrated scale_mic_y: " + str(self.scale_mic_y));


        say_pub.publish("Scale calibration complete.")
        say_pub.publish("Calibration successful, now I can know where you are.")
        say_pub.publish("har har har har")
        say_pub.publish("ha ha ha ha")

        rospy.set_param('~offset_mic_x',self.offset_mic_x)
        rospy.set_param('~offset_mic_y',self.offset_mic_y)
        rospy.set_param('~offset_mic_z',self.offset_mic_z)
        rospy.set_param('~scale_mic_x',self.scale_mic_x)
        rospy.set_param('~scale_mic_y',self.scale_mic_y)
        rospy.set_param('~scale_mic_z',self.scale_mic_z)

        rospy.wait_for_message("/recognizer/output",String)
        sleep(2)
        return StartCalibrationResponse()

    def rotater(self,goal_voice_direction):
        current_angle = self.get_current_angle()
        rospy.loginfo(current_angle)
        goal_angle = current_angle - goal_voice_direction 
        if goal_angle > 180:
            goal_angle = goal_angle - 360
        elif goal_angle <-180:
            goal_angle = goal_angle + 360    

        rospy.loginfo(goal_angle)
        if goal_voice_direction < 0:
            rot_speed = 1
        if goal_voice_direction > 0:
            rot_speed = -1

        while abs(self.get_current_angle() - goal_angle) > 5 :
            rot_cmd = Twist()
            rot_cmd.angular.z = rot_speed
            self.cmd_vel_pub.publish(rot_cmd)
            rospy.sleep(0.1)
        rot_cmd = Twist()
        self.cmd_vel_pub.publish(rot_cmd)
  
    def get_current_angle(self):
        try:
            (trans,quat) = self.tf_listener.lookupTransform("/odom","/base_link",rospy.Time(0))
            angles =  euler_from_quaternion(quat)

            return math.degrees(angles[2])

        except Exception, e:
            rospy.loginfo("getting odom failed")
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



