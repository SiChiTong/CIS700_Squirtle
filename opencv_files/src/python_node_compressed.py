#!/usr/bin/env python

import sys, time
import numpy as np
from scipy.ndimage import filters
import cv2
import roslib
import rospy
from sensor_msgs.msg import CompressedImage
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
# We do not use cv_bridge it does not support CompressedImage in python
# from cv_bridge import CvBridge, CvBridgeError

class image_feature:

	def __init__(self):
		# topic where we publish
		self.image_pub = rospy.Publisher("/output/image_raw/compressed", CompressedImage,queue_size = 1)
		# self.bridge = CvBridge()

		# subscribed Topic
		#self.subscriber = rospy.Subscriber("/image_converter/output_video/compressed",Image, self.callback,  queue_size = 1)
		self.subscriber = rospy.Subscriber("/image_converter/output_video/compressed",CompressedImage, self.callback,  queue_size = 1)
		#self.subscriber = rospy.Subscriber("/camera/rgb/image_color/compressed", CompressedImage, self.callback,  queue_size = 1)

	def callback(self, ros_data):
		'''Callback function of subscribed topic.'''

		np_arr = np.fromstring(ros_data.data, np.uint8)
		#image_np = cv2.imdecode(np_arr, cv2.CV_LOAD_IMAGE_GRAYSCALE)
		image_np = cv2.imdecode(np_arr, cv2.CV_LOAD_IMAGE_COLOR)

		# convert np image to grayscale
		#cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY))

		print image_np.shape
		#cv2.imshow('cv_img', image_np)
		#cv2.waitKey(2)

		#### Create CompressedIamge ####
		msg = CompressedImage()
		msg.header.stamp = rospy.Time.now()
		msg.format = "jpeg"
		msg.data = np.array(cv2.imencode('.jpg', image_np)[1]).tostring()
		# Publish new image
		self.image_pub.publish(msg)

		#self.subscriber.unregister()

def main(args):

	ic = image_feature()
	rospy.init_node('image_feature', anonymous=True)
	try:
		rospy.spin()
	except KeyboardInterrupt:
		print "Shutting down ROS Image feature detector module"
	cv2.destroyAllWindows()

if __name__ == '__main__':
	main(sys.argv)