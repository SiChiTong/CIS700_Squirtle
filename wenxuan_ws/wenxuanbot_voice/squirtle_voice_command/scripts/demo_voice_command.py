#!/usr/bin/env python

# THis node as a whole is a Finite-State-Machine with states listed below
# 1. Busy   -- means the robot is currently busy at other task
#              when busy, it can response(only) to summoning phrase and flip state to "wait for command"
#              if it was assigned new task it will ask if it should cancel current one
# 2. Free   -- means the robot is not doing anything
#              when free it can response(only) to summoning phrase and flip state to "wait for command"         
# 3. Wait for command
#           -- means the robot is summoned, it will listen for command
#              when wait for command, if the command is not recognizable
#              state will return back to previous state(busy or free)  
# 4. mimic  -- means the robot is in mimic state which is a debugging state
#              in this state it will say anything it hears
#              terminate if it hears mimic mode termination phrase
#
#
# For voice command it has four different levels of recognition (from loose to strict)
# 1. Contains -- will recognize if the desired phrases is contained in input phrase
# 2. Exact    -- Will recognize only if the input phrase is exactly the same as desired one
# 3. Ask for confirmation
#             -- will ask for confirmation once recognized, for safety
# 4. Refuse   -- refuse such command and give a reason
# 
#
# Use multi thread to open up a action, track its state, once finished flip the state from busy to free
#
# TODO: upload a finite-state-machine graph to illustrate

import sys
import rospy
#from sound_play.msg import SoundRequest
from sound_play.libsoundplay import SoundClient
from std_msgs.msg import String

class Demo_voice_command:
    """This script is for demo of voice command of Team4 squirtle"""
    def __init__(self):

        rospy.init_node('demo_voice_command')
        rospy.on_shutdown(self.cleanup)

        #create soundhandle for sound playing
        self.soundhandle = SoundClient()
        rospy.sleep(1)

        #self.voice = 'voice_kal_diphone'
        #self.voice = 'voice_cmu_us_clb_arctic_clunits'
        self.voice = 'voice_cmu_us_slt_arctic_clunits'
        #self.voice = 'voice_cmu_us_rms_arctic_clunits'

        self.soundhandle.say("Hello world", self.voice, 1.0)
        rospy.sleep(2)
        self.soundhandle.stopAll()

 
        rospy.Subscriber('/recognizer/output',String,self.receive_speech_callback)


    def receive_speech_callback(self,msg):
        # print what it recognized
        rospy.loginfo(msg.data)
        
        # speak what it recognized
        self.soundhandle.say(msg.data,self.voice)
        rospy.sleep(3)

    def cleanup(self):
        # cleanup to ensure a decent shutdown
        self.soundhandle.stopAll()
        rospy.loginfo("Shutting down Demo_voice_command node...")

if __name__=="__main__":
    try:
        Demo_voice_command()
        rospy.spin()
    except rospy.ROSInterruptException:
        rospy.loginfo("Voice command finished")