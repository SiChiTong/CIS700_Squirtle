#!/usr/bin/env python

import sys
import rospy
#from sound_play.msg import SoundRequest

from sound_play.libsoundplay import SoundClient

rospy.init_node('say', anonymous = True)
soundhandle = SoundClient()
rospy.sleep(1)

#voice = 'voice_kal_diphone'
#voice = 'voice_cmu_us_clb_arctic_clunits'
#voice = 'voice_cmu_us_slt_arctic_clunits'
voice = 'voice_cmu_us_rms_arctic_clunits'

volume = 1.0

s = "Hello world"

print 'Saying: %s' % s
print 'Voice: %s' % voice
print 'Volume: %s' % volume

soundhandle.say(s, voice, volume)
rospy.sleep(1)
