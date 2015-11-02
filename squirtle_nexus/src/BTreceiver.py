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
  def __init__(self):
    # setup
    rospy.init_node("BTreceiver") 
    self.pub = rospy.Publisher('nexusMessage', String, queue_size=10)

    # Setup Bluetooth 
    os.system("sudo sdptool add --channel=22 SP");
    os.system("sudo rfcomm listen /dev/rfcomm0 22 &");
    print("YOU HAVE 8 SECONDS TO CONNECT THE APP!!!!!!!!!")
    time.sleep(8) ## 

    # Serial port setup
    ser = serial.Serial()
    ser.port = "/dev/rfcomm0" # may be called something different
    ser.baudrate = 9600 # may be different
    ser.open()

    rate = rospy.Rate(10) # 10hz
    while(ser.isOpen()): #ser.write("hello")
      btMessage = ser.read()
      self.pub.publish(btMessage)
    btMessage = "Lost Bluetooth Connection!! HELP!!"
    rospy.spin();

if __name__ == '__main__':
  try:
    BTreceiver()
  except rospy.ROSInterruptException:
    rospy.loginfo("exception")

