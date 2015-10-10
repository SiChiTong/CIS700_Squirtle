#!/usr/bin/env python
import sys, time
import numpy as np
from scipy.ndimage import filters
import roslib
import rospy
import cv2
import sys
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

class Test:

    def __init__(self):
        self.image_sub = rospy.Subscriber("/image_converter/output_video",Image, self.callback, queue_size = 1)
        self.image_pub = rospy.Publisher("test_image", Image, queue_size = 1)
        self.bridge = CvBridge()
        self.counter = 0

    def callback(self, image):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(image, 'bgr8')#mono8')
        except CvBridgeError, e:
            print e

        #print cv_image.shape ### output: (480, 640, 1)

        #np_arr = np.fromstring(image.data, np.uint8) #only 1 channel?
        np_arr = np.fromstring(cv_image, np.uint8)
        #print np_arr.shape
        
        #logfile = open('faces/david.txt', 'a') 
        #logfile.write(str(self.counter)+" ")
        #logfile.write(np_arr)
        #logfile.close() 

        #data = np.arange(200).reshape((4,5,10))
        #with file('test.txt', 'w') as outfile:
        #outfile.write('# Array shape: {0}\n'.format(data.shape))
        #for data_slice in data:
        #np.savetxt(outfile, data_slice, fmt='%-7.2f')
        #outfile.write('# New slice\n')
        #new_data = np.loadtxt('test.txt')
        #print new_data.shape
        #new_data = new_data.reshape((4,5,10))
        #assert np.all(new_data == data)

        cv2.imshow("Test", cv_image)
    
        cv2.waitKey(1)
        title = "faces/im"+str(self.counter)+".png"
        cv2.imwrite(title, cv_image)
        self.counter+=1

        test2 = cv2.resize(cv_image,(250,240))
        #print test2.shape 
        self.image_pub.publish(self.bridge.cv2_to_imgmsg(test2))

def main(args):
    test = Test()
    rospy.init_node('image_converter', anonymous=True)

    try:
        rospy.spin()
    except KeyboardInterrupt:
        print "Shutting down"
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main(sys.argv)