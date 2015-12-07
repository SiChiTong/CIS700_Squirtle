#!/usr/bin/env python

import sys
import rospy
#from sound_play.msg import SoundRequest
from sound_play.libsoundplay import SoundClient
from std_msgs.msg import String


class Mouth_talker:
    def __init__(self):
        rospy.init_node('mouth_talker')

        rospy.Subscriber("string_to_say", String, self.callback)
        #create soundhandle for sound playing
        self.soundhandle = SoundClient()
        rospy.sleep(1)  

        #self.voice = 'voice_kal_diphone'
        #self.voice = 'voice_cmu_us_clb_arctic_clunits'
        #self.voice = 'voice_cmu_us_slt_arctic_clunits'
        self.voice = 'voice_cmu_us_rms_arctic_clunits'
        rospy.loginfo("Mouth initialize complete.")

    def callback(self,msg):
        rospy.loginfo(rospy.get_caller_id() + ": I received %s", msg.data)

        self.soundhandle.say(msg.data, self.voice, 1.0)
        


if __name__ == '__main__':
    Mouth_talker()
    rospy.spin()

