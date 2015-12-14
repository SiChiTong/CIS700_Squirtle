#!/usr/bin/env python

'''
Node to send speech status to the robot state
by Siddharth Srivatsa

Publishes - /current_subroutine_status
Subscribes - /nexusMessage, /current_task
'''


import roslib
import rospy
import os
import sys
from std_msgs.msg import *
from geometry_msgs.msg import *

class speechStatus():
        	
#	Check which button is pressed on the nexus 
    def buttonCallback(self, string_msg):
        # when the button is pressed, self.buttonPress = "button_pressed"
        self.buttonPress = string_msg.data
    

    def __init__(self, argument):
        
        self.subRoutineStatus = 0
        self.buttonPress = "not_init"
#		Map the tasks to the appropriate voice commands
        self.speechCommand = {
            'retrieve_object' : 'rosrun squirtle_speech speech_button_presser.py retrieve_object',
            'deliver_object' : 'rosrun squirtle_speech speech_button_presser.py deliver_object',
            'find_person' : 'rosrun squirtle_speech speech_button_presser.py find_person',
            'deliver_message' : 'rosrun squirtle_speech speech_button_presser.py deliver_message',

        }
        rospy.init_node("speechStatus", anonymous=True)
#		Initialize the publishers and subscribers
        self.SubRoutineStatusPub = rospy.Publisher('current_subroutine_status', String, queue_size=10)
        rospy.Subscriber("/nexusMessage", String, self.buttonCallback)
			
		# load the current task
		# since this node will be brought up and killed dynamically, 
		# it only needs to load current task once
        received_current_task = "not_initialized"
        self.speech_task = "not_initialized"
        
        while received_current_task == 'not_initialized' or self.speechCommand.has_key(self.speech_task) == False:
            # handle shutdown otherwise it's hard to kill
            if rospy.is_shutdown():
                rospy.loginfo("speech status node shut down")
                return

            try:
                received_current_task = rospy.wait_for_message("/current_task",String,timeout=1)
                self.speech_task = received_current_task.data.partition(' ')[0] 

            except Exception, e:
                rospy.loginfo("current_task not received")
                self.SubRoutineStatusPub.publish("Not initialized")
                os.system("rosrun sound_play say.py 'current task not received'")

        # when got here it means the task has been loaded
        # bring up the "speech_button_presser" 
        os.system("rosrun sound_play say.py 'current task has been loaded'")
        rospy.loginfo("current_task loaded: " + self.speech_task + " " + argument)

        # bring up speech_button_presser at backgroud
        os.system(self.speechCommand[self.speech_task] + " " + argument + "&")
       
        rate = rospy.Rate(10) # Publish at 10hz

        while not rospy.is_shutdown():
            # 

            if self.buttonPress == "button_pressed":
                self.SubRoutineStatusPub.publish("complete")
            else:
                self.SubRoutineStatusPub.publish("going_on")
            
            rate.sleep()

        os.system("rosrun sound_play say.py 'current speech task has been competed'")    

if __name__ == '__main__':
	if len(sys.argv) != 4:
		print("usage: my_node.py arg1")
	else:
		speechStatus((sys.argv[1]))
