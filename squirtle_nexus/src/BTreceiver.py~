#!/usr/bin/env python

'''
Node to establish ROS link with Nexus 
by Mayumi Mohan

# App should preferrably be turned on before running the node... 8 second delay to establish connection if not
# Subscribes to: /current_task 
# Publishes: 
'''

import roslib
import rospy
import os
import time
import serial
from std_msgs.msg import String
from std_msgs.msg import Bool

class BTreceiver():

  def stateCallback(self, data):
    self.state = data.data;

  def __init__(self):
    self.state = ""
    # setup
    rospy.init_node("BTreceiver") 
    #publisher
    self.pub = rospy.Publisher('nexusMessage', String, queue_size=1)
    #self.debugpub = rospy.Publisher('BTdebug', String, queue_size=1)
    #subscriber
    self.sub = rospy.Subscriber("/current_task", String, self.stateCallback)
    rate = rospy.Rate(10)

    # Setup Bluetooth 
    os.system("sudo sdptool add --channel=16 SP");
    os.system("sudo rfcomm listen /dev/rfcomm6 16 &");
    print("YOU HAVE 10 SECONDS TO CONNECT THE APP!!!!!!!!!")
    time.sleep(10) ## 

    # Serial port setup
    ser = serial.Serial()
    ser.port = "/dev/rfcomm6" # may be called something different
    ser.baudrate = 9600 # may be different
    ser.timeout = 0 # may be different
    
    ser.open()

    rate = rospy.Rate(8) # 10hz
    android_data = ""
    oldData = ""
    #self.debugpub.publish('line 50:')
    while(ser.isOpen()):  
      if oldData != self.state:     
        ser.write(self.state)
        oldData = self.state

      if ser.inWaiting>0:
        btMessage = ser.read()
        #self.debugpub.publish(btMessage)
        self.pub.publish(self.state)
        if btMessage == "$":
          self.pub.publish(android_data)
          android_data = "";
        else:
          android_data = android_data+btMessage;
      rate.sleep()
    btMessage = "Lost Bluetooth Connection!! HELP!!"
    self.pub.publish(btMessage)
    rospy.spin();

if __name__ == '__main__':
  try:
    BTreceiver()
  except rospy.ROSInterruptException:
    rospy.loginfo("exception")

