#!/usr/bin/env python

'''
Node to send speech status to the robot state
by Siddharth Srivatsa

Publishes - /current_subroutine_status
Subscribes - /nexusMessage, /current_task
'''
#!/usr/bin/env python


import roslib
import rospy
import os
import sys
from std_msgs.msg import *
from geometry_msgs.msg import *



os.system("rosrun sound_play say.py 'button presser has been loaded'")
task_type = str(sys.argv[1])
task_arg1 = str(sys.argv[2])

rospy.init_node('speech_button_presser',anonymous=True)
button_press_pub = rospy.Publisher("/nexusMessage", String, queue_size = 10)


# find person task will take one arguments
if task_type == "find_person":

    # load argument
    person_to_find = task_arg1
    person_to_find = person_to_find.replace("_"," ") # replace _ to space

    string_to_say = "'" + "finding person " + person_to_find + "'"
    os.system("rosrun sound_play say.py " + string_to_say)


    # call the person 
    string_to_say = "'" + "hey " + person_to_find + " please come over here" + "'"
    os.system("rosrun sound_play say.py " + string_to_say)
    
    # continuously ask for the person until get the feedback
    received_voice = None
    while received_voice is None or received_voice.data != "i'm here":
        if rospy.is_shutdown():
            os._exit(0)
        try:
            received_voice = rospy.wait_for_message("/recognizer/output",String,timeout=10)
        except Exception, e:
            string_to_say = "'" + person_to_find + " i cant find you, please come over here" + "'"
            os.system("rosrun sound_play say.py " + string_to_say)
            rospy.sleep(5)



# retrieve object task will take one arguments
elif task_type == "retrieve_object":    
    # load argument
    object_to_retrieve = task_arg1
    object_to_retrieve = object_to_retrieve.replace("_"," ") # replace _ to space

    string_to_say = "'" + "retrieving object " + object_to_retrieve + "'"
    os.system("rosrun sound_play say.py " + string_to_say)

    # ask for the object 
    string_to_say = "'" + "hello human, please give me a " + object_to_retrieve + " thanks" + "'"
    os.system("rosrun sound_play say.py " + string_to_say)

    # continuously ask for the person until get the feedback
    received_voice = None
    while received_voice is None or received_voice.data != "you have it":
        if rospy.is_shutdown():
            os._exit(0)
        try:
            received_voice = rospy.wait_for_message("/recognizer/output",String,timeout=10)
        except Exception, e:
            string_to_say = "'" + "anyone here? please give me a " + object_to_retrieve + "'"
            os.system("rosrun sound_play say.py " + string_to_say)
            rospy.sleep(5)



# deliver object task will take two arguments, arg1=object arg2=location
elif task_type == "deliver_object":   
    object_to_deliver = task_arg1
    object_to_deliver = object_to_deliver.replace("_"," ") # replace _ to space

    
    string_to_say = "'" + "delivering object " + object_to_deliver + "'"
    os.system("rosrun sound_play say.py " + string_to_say)
   
    # ask for the object 
    string_to_say = "'" + "hello human, i have a " + object_to_deliver + " for you, please take it" + "'"
    os.system("rosrun sound_play say.py " + string_to_say)

    # continuously ask for the person until get the feedback
    received_voice = None
    while received_voice is None or received_voice.data != "i got it":
        if rospy.is_shutdown():
            os._exit(0)
        try:
            received_voice = rospy.wait_for_message("/recognizer/output",String,timeout=10)
        except Exception, e:
            string_to_say = "'" + "hello? please take the " + object_to_deliver + " it is for you" + "'"
            os.system("rosrun sound_play say.py " + string_to_say)
            rospy.sleep(5)


# deliver object task will take two arguments, arg1=object arg2=location
elif task_type == "deliver_message":   
    message_to_deliver = task_arg1
    message_to_deliver = message_to_deliver.replace("_"," ") # replace _ to space

    
    string_to_say = "'" + "delivering message " + message_to_deliver + "'"
    os.system("rosrun sound_play say.py " + string_to_say)
   
    # ask for the object 
    string_to_say = "'" + "hello human, i have a message for you, someone ask me to say that " + message_to_deliver + "'"
    os.system("rosrun sound_play say.py " + string_to_say)

    # continuously ask for the person until get the feedback
    received_voice = None
    while received_voice is None or received_voice.data != "i got it":
        if rospy.is_shutdown():
            os._exit(0)
        try:
            received_voice = rospy.wait_for_message("/recognizer/output",String,timeout=10)
        except Exception, e:
            string_to_say = "'" + "hello? did you receive the message " + message_to_deliver  + "'"
            os.system("rosrun sound_play say.py " + string_to_say)
            rospy.sleep(5)



else:
    os.system("rosrun sound_play say.py 'error shutting down'")
    os._exit(0)



# received the person's feedback, press the "button" and kill itself(the node)
os.system("rosrun sound_play say.py " + "'thank you, voice feedback received'")
rospy.sleep(2)

button_press_pub.publish("button_pressed") 



