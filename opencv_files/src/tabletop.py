#!/usr/bin/env python
import sys, time
import numpy as np
#from scipy.ndimage import filters
import roslib
import rospy
import cv2
import sys
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import time

class Test:

    def __init__(self):
        self.image_sub = rospy.Subscriber("/camera/depth/image",Image, self.callback, queue_size = 1)
        #self.image_pub = rospy.Publisher("test_image", Image, queue_size = 1)
        self.bridge = CvBridge()
        self.time = time.time()


    def callback(self, image):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(image)
        except CvBridgeError, e:
            print e

        #np_arr = np.fromstring(image.data, np.uint8) #only 1 channel?
        np_arr = np.fromstring(cv_image, np.uint8)
        #print cv_image.shape
        print 'fps: ',1.0/(time.time()-self.time)
        self.time = time.time()
        
        n,m = cv_image.shape
        k = 3
        im = np.reshape(cv_image,(np.size(cv_image),1))
        y,x = np.meshgrid(range(n),range(m))
        triples = (np.reshape(cv_image,(np.size(x),1)), np.reshape(cv_image,(np.size(x),1)), im)
        #tr = np.array(triples) # kills the runtime
        #print np.shape(tr)
        #triples = tr[:,~np.isnan(tr[2,:])]

        #newim = np.reshape(tr[2,:],(n,m))
        
        #print im
        '''
        # computation, making this list is about 4fps
        n = 480
        m = 640
        k = 3
        triples = (m*n,k) #for a mat
        triples = np.zeros(triples)
        #print cv_image[0,0]
        for i in range(m):
            for j in range(n):
                #print i,j,i*n+j
                triples[i*n + j,0] = j
                triples[i*n + j,1] = i
                triples[i*n + j,2] = cv_image[j,i]
        merp = triples[:,2]
        triples = triples[~np.isnan(merp),:]  
        
        # RANSAC   
        it = 10
        one = (3,1)
        one = np.ones(one)
        oness = (triples.shape[0],1)
        oness = np.ones(oness)
        inlier_thresh = .01
        best_coeffs = one
        max_inliers = 0
        for i in range(it):
            r = np.random.randint(triples.shape[0], size=3)         
            coeffs = np.dot(np.linalg.pinv(triples[r,:]),one)
            val = np.dot(triples,coeffs)
            dist = pow(val-oness,2)
            inliers = sum(dist<inlier_thresh)
            if inliers>max_inliers:
                best_coeffs = coeffs
                max_inliers = inliers
        val = np.dot(triples,best_coeffs)
        dist = pow(val-oness,2)
        inliers = dist<inlier_thresh
        print sum(dist<inlier_thresh), inliers.shape, triples.shape
        #print inliers
        triples = triples[inliers[:,0],:]

        rgb_im = cv2.cvtColor(cv_image,cv2.COLOR_GRAY2RGB)
        for i in range(triples.shape[0]):
            rgb_im[triples[i,0],triples[i,1],0] = 255
        '''

        cv2.imshow("Test", cv_image)
        #cv2.imshow("Test", rgb_im)
    
        cv2.waitKey(1)
        

        #test2 = cv2.resize(cv_image,(250,240))
        #print test2.shape 
        #self.image_pub.publish(self.bridge.cv2_to_imgmsg(test2))

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