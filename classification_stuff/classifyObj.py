#!/usr/bin/env python
"""
classify.py is an out-of-the-box image classifer callable from the command line.

By default it configures and runs the Caffe reference ImageNet model.
"""
import numpy as np
import os
import roslib
import rospy
import sys
import time
import caffe
import scipy.io
from sklearn.linear_model import lasso_path, LassoCV
from sklearn import svm
import pickle
from sklearn.externals import joblib
from std_msgs.msg import *

def classify_obj(input_file):
#def classify_obj():
	# Initialize the ros node
	rospy.init_node("classify_object", anonymous=True)

	# Define the parameters for the caffe model
	gpu = 0
	pycaffe_dir = os.path.dirname(__file__)
	model_def = os.path.join(pycaffe_dir, "../models/bvlc_reference_caffenet/deploy_nohead.prototxt")
	pretrained_model = os.path.join(pycaffe_dir, "../models/bvlc_reference_caffenet/bvlc_reference_caffenet.caffemodel")
	image_dims = [256, 256]
	input_scale = 1
	raw_scale = 255.0
	center_only = True
	mean, channel_swap = None, None
	ans = []

	# Define the subscribers and the publishers
	pub = rospy.Publisher('classified_object', String, queue_size=10)
	
	# Load pretrained SVM model
	clf = joblib.load('svmModel_classifier.pkl')

	if gpu:
		caffe.set_mode_gpu()
	else:
		caffe.set_mode_cpu()

	# Make classifier.
	classifier = caffe.Classifier(model_def, pretrained_model, image_dims=image_dims, mean=mean, input_scale=input_scale, raw_scale=raw_scale, channel_swap=channel_swap)

	# Load numpy array (.npy), directory glob (*.jpg), or image file.
	if input_file.endswith('npy'):
		inputs = np.load(input_file)
	elif os.path.isdir(input_file):
		inputs =[caffe.io.load_image(im_f) for im_f in glob.glob(input_file)]
	else:
		inputs = [caffe.io.load_image(input_file)]

	# Classify.
	start = time.time()
	predictions = classifier.predict(inputs, not center_only)
	output = clf.predict(predictions)

# SVM test (classification by default)
	objectClass = np.load("objectClass.npy")
	print objectClass[output[0]]
	print type(objectClass[output[0]])
	pub.publish(str(objectClass[output[0]]))

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print("usage: my_node.py arg1")
	else:
		classify_obj(sys.argv[1])
#	classify_obj()
