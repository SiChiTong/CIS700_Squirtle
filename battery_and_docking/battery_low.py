#!/usr/bin/env python

'''
Send a Message if the battery is low
David Isele
based on code by Mark Silliman

'''

# Monitor the kobuki's battery level

import roslib
import rospy
from kobuki_msgs.msg import SensorState
from std_msgs.msg import Bool

class battery_low():

	kobuki_base_max_charge = 160

	def __init__(self):
    # setup
    	rospy.init_node("battery_low")	
    	pub = rospy.Publisher('battery_is_low', Bool, queue_size=10)
    	rospy.Subscriber("/mobile_base/sensors/core",SensorState,self.SensorPowerEventCallback)
    	rate = rospy.Rate(10) # 10hz
	
		rospy.spin();


	def SensorPowerEventCallback(self,data):
		percent_charge = round(float(data.battery) / float(self.kobuki_base_max_charge) * 100)
		is_battery_low = False
		if percent charge<10:
			is_battery_low = True
			
        rospy.loginfo(is_battery_low)
        pub.publish(is_battery_low)
        rate.sleep()
		if(int(data.charger) == 0) :
			rospy.loginfo("Not charging at docking station")
		else:
			rospy.loginfo("Charging at docking station")
	

if __name__ == '__main__':
	try:
		battery_low()
	except rospy.ROSInterruptException:
		rospy.loginfo("exception")
