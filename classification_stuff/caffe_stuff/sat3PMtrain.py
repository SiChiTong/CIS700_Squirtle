#!/usr/bin/env python
"""
classify.py is an out-of-the-box image classifer callable from the command line.

By default it configures and runs the Caffe reference ImageNet model.
"""
import numpy as np
import os
from os import walk
import sys
import argparse
import glob
import time
import caffe
import scipy.io
from sklearn.linear_model import lasso_path, LassoCV
from sklearn import svm

def main(argv):
	gpu = 0
	pycaffe_dir = os.path.dirname(__file__)
	model_def = os.path.join(pycaffe_dir, "../models/bvlc_reference_caffenet/deploy_nohead.prototxt")
	pretrained_model = os.path.join(pycaffe_dir, "../models/bvlc_reference_caffenet/bvlc_reference_caffenet.caffemodel")
	images_dim = '256,256'
	input_scale = 1
	raw_scale = 255.0
	center_only = True
	output_file = "foo1"
	(dirpath, dirnames, filesInFolder) = os.walk("/home/squirtle/objects/subset").next()
	classes = np.zeros(len(filesInFolder))
	finalPred = []
	counter = 0
	objectClass = []

	
	f = []
	for (dirpath, dirnames, filenames) in walk("/home/squirtle/objects/subset"):
	    f.extend(filenames)
	    break
	print f
	
	for filename in f:
	    image_dims = [int(s) for s in images_dim.split(',')]

	    mean, channel_swap = None, None

	    if gpu:
		caffe.set_mode_gpu()
		print("GPU mode")
	    else:
		caffe.set_mode_cpu()
		print("CPU mode")

	    # Make classifier.
	    classifier = caffe.Classifier(model_def, pretrained_model, image_dims=image_dims, mean=mean, input_scale=input_scale, raw_scale=raw_scale, channel_swap=channel_swap)

	    # Load numpy array (.npy), directory glob (*.jpg), or image file.
	    input_file = "/home/squirtle/objects/subset/" + filename
	    if input_file.endswith('npy'):
		print("Loading file: %s" % input_file)
		inputs = np.load(input_file)
	    elif os.path.isdir(input_file):
		print("Loading folder: %s" % input_file)
		inputs =[caffe.io.load_image(im_f)
		         for im_f in glob.glob(input_file)]
	    else:
		print("Loading file: %s" % input_file)
		inputs = [caffe.io.load_image(input_file)]

	    print("Classifying %d inputs." % len(inputs))

	    # Classify.
	    start = time.time()
	    predictions = classifier.predict(inputs, not center_only)
	    print("Done in %.2f s." % (time.time() - start))

	    # Save
	    print("Saving results into %s" % output_file)
	    np.save(output_file, predictions)
	    if counter == 0:
	        finalPred = predictions
	    else:
	        finalPred = np.append(finalPred, predictions, axis=0)
	    #finalPred = np.append(finalPred, predictions, axis=0)
	    classes[counter] = counter
	    counter = counter + 1
	    objectClass.append(filename)
	    
	# SVM train (classification by default)
	print "finalPred"
	print finalPred.size
	np.save("crayy", finalPred)
	clf = svm.SVC()
	clf.fit(finalPred, classes)
	np.save("objectClass", objectClass)
	
	ans = []
	f = []
	for (dirpath, dirnames, filenames) in walk("/home/squirtle/objects/testset"):
	    f.extend(filenames)
	    break
	print f
	
	for filename in f:
	    image_dims = [int(s) for s in images_dim.split(',')]

	    mean, channel_swap = None, None

	    if gpu:
		caffe.set_mode_gpu()
		print("GPU mode")
	    else:
		caffe.set_mode_cpu()
		print("CPU mode")

	    # Make classifier.
	    classifier = caffe.Classifier(model_def, pretrained_model, image_dims=image_dims, mean=mean, input_scale=input_scale, raw_scale=raw_scale, channel_swap=channel_swap)

	    # Load numpy array (.npy), directory glob (*.jpg), or image file.
	    input_file = "/home/squirtle/objects/testset/" + filename
	    if input_file.endswith('npy'):
		print("Loading file: %s" % input_file)
		inputs = np.load(input_file)
	    elif os.path.isdir(input_file):
		print("Loading folder: %s" % input_file)
		inputs =[caffe.io.load_image(im_f)
		         for im_f in glob.glob(input_file)]
	    else:
		print("Loading file: %s" % input_file)
		inputs = [caffe.io.load_image(input_file)]

	    print("Classifying %d inputs." % len(inputs))

	    # Classify.
	    start = time.time()
	    predictions = classifier.predict(inputs, not center_only)
	    print("Done in %.2f s." % (time.time() - start))
	    ans.append(clf.predict(predictions))

	# SVM test (classification by default)
	
	print ans

if __name__ == '__main__':
    main(sys.argv)
