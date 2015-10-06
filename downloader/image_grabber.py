import urllib
import urllib2
import simplejson
import cStringIO
import time
import numpy
from PIL import Image


import numpy as np
import matplotlib.pyplot as plt

fetcher = urllib2.build_opener()
searchTerm = 'stapler'
for i in range(20):
	print i
	try:
		searchUrl = "http://ajax.googleapis.com/ajax/services/search/images?v=1.0&q=" + searchTerm + "&start=" + str(i)
		f = fetcher.open(searchUrl)
		deserialized_output = simplejson.load(f)

		imageUrl = deserialized_output['responseData']['results'][0]['unescapedUrl']
		file = cStringIO.StringIO(urllib.urlopen(imageUrl).read())
		img = Image.open(file)

		file_name = "ims/thumbnail" + str(i)
		img.save(file_name, "JPEG")
	
		#delay = numpy.random.uniform(10,30)
		#time.sleep(delay)
		
	except Exception as e:
		print('didnt get picture')
		

  
