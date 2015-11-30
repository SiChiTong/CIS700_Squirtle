#!/usr/bin/env python

# THis node as a whole is a Finite-State-Machine with states listed below
# 1. Busy   -- means the robot is currently busy at other task
#              when busy, it can response(only) to summoning phrase and flip state to "wait for command"
#              if it was assigned new task it will ask if it should cancel current one
# 2. Free   -- means the robot is not doing anything
#              when free it can response(only) to summoning phrase and flip state to "wait for command"         
# 3. Wait for command (wfc)
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
        #self.voice = 'voice_kal_diphone'
        #self.voice = 'voice_cmu_us_clb_arctic_clunits'
        self.voice = 'voice_cmu_us_slt_arctic_clunits'
        #self.voice = 'voice_cmu_us_rms_arctic_clunits'
        self.soundhandle = SoundClient()
        rospy.sleep(1)


        self.soundhandle.say("Voice initialize complete", self.voice, 1.0)
        rospy.sleep(3)
        self.soundhandle.stopAll()


        self.current_state = "free"
        self.last_state = "free"

        # dictionary indicating phrases to command map
        self.phrases_to_command = {'summoning': ['turtlebot', 'squirtle'],
                                    'forward':['move forward','go forward'],
                                    'backward':['move backward','go backward'],
                                    'move left':['move left', 'step left'],
                                    'move right':['move right', 'step right'],
                                    'turn left': ['turn left'],
                                    'turn right': ['turn right'],
                                    'spin': ['spin'],
                                    'start mimic': ['start mimic','begin mimic'],
                                    'stop mimic': ['stop mimic'],
                                    'check busy': ['are you busy','doing anything']
                                    }





        rospy.Subscriber('/recognizer/output',String,self.receive_speech_callback)

    def receive_speech_callback(self,msg):
        # print what it recognized
        rospy.loginfo(msg.data)
        command = self.parse_command(msg.data,"contain")


        if self.current_state == "free":
            # free state
            if command == "summoning":
                # only summoning can activate turtlebot in this state
                self.soundhandle.say("yes, sir, i'm waiting for your command",self.voice)
                rospy.sleep(4)
                self.current_state = "wfc"
                self.last_state = "free"

        elif self.current_state == "busy":
            # busy state
            if command == "summoning":
                # only summoning can activate turtlebot in this state
                self.soundhandle.say("yes, sir, i'm busy now, what's your command",self.voice)
                rospy.sleep(5)
                self.current_state = "wfc"
                self.last_state = "busy"


        elif self.current_state == "wfc":
            # state of waiting for command, accepting command in this state
            if command == "forward":
                self.soundhandle.say("ok, sir, preparing to move forward",self.voice)
                rospy.sleep(4)
                self.soundhandle.say("action complete, sir, return to free state",self.voice)
                rospy.sleep(4)
                self.current_state = "free"
            elif command == 'start mimic':
                self.soundhandle.say("yes, sir, entering debugging mode, i will repeat what you say",self.voice)
                rospy.sleep(5)
                self.soundhandle.say("note that i will only say what i think i hear, sir",self.voice)
                rospy.sleep(4)
                self.current_state = "mimic"
            else:
                self.soundhandle.say("sorry, i can't recognize any command", self.voice)
                rospy.sleep(3)
                self.current_state = self.last_state

        elif self.current_state == "mimic":
            # mimic state for debugging voice, will repeat what it hear
            if command == "stop mimic":
                self.soundhandle.say("yes, sir, exiting mimic state, now i'm at free state",self.voice)
                rospy.sleep(3)
                self.current_state = "free"
            else:
                self.soundhandle.say(msg.data,self.voice)
                rospy.sleep(3)


        else:
            self.soundhandle.say("sir, my state is encountering an error, please check your code",self.voice)
            rospy.sleep(4)
          






    def parse_command(self,input_phrase,match_method):
        # this method is to convert an input string and output a command
        # has two method, 'exact' for matching exactly, 'contain' for containing phrases(loose) 
        # returned command type:
        # "error" -- indicating error
        # "no command" -- indicating no command found
        # other command -- check the keys of self.phrases_to_command 
        if match_method == "exact":
            for (command, keywords) in self.phrases_to_command.iteritems():
                for word in keywords:
                    if input_phrase == word:
                        return command

        elif match_method == "contain":
            for (command, keywords) in self.phrases_to_command.iteritems():
                for word in keywords:
                    if input_phrase.find(word) > -1:
                        return command
        else:
            self.soundhandle.say("sir, command parser is encountering error, invalid matching method",self.voice)
            rospy.sleep(4)
            return "error"

        return "no command"

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