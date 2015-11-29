#!/usr/bin/env python

import sys
import rospy
#from sound_play.msg import SoundRequest
from sound_play.libsoundplay import SoundClient
from std_msgs.msg import String

class DemoVoiceCommand:
    """docstring for demo_voice_command"""
    def __init__(self):
        rospy.init_node('demo_voice_command', anonymous = True)
        self.soundhandle = SoundClient()
        rospy.sleep(1)

        #voice = 'voice_kal_diphone'
        #voice = 'voice_cmu_us_clb_arctic_clunits'
        #voice = 'voice_cmu_us_slt_arctic_clunits'
        self.voice = 'voice_cmu_us_rms_arctic_clunits'

        self.volume = 1.0

        openup_string = "Hello world"

        print 'Saying: %s' % openup_string
        print 'Voice: %s' % self.voice
        print 'Volume: %s' % self.volume

        self.soundhandle.say(openup_string, self.voice, self.volume)
        rospy.sleep(1)
        self.soundhandle.stopAll()


        rospy.Subscriber('/recognizer/output',String,self.receive_speech_callback)

    def receive_speech_callback(self,msg):
        # print what it recognized
        rospy.loginfo(msg.data)
        
        # speak what it recognized
        self.soundhandle.say(msg.data,self.voice)


if __name__=="__main__":
    try:
        DemoVoiceCommand()
        rospy.spin()
    except rospy.ROSInterruptException:
        rospy.loginfo("Voice command finished")