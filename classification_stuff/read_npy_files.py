import numpy as np
np.set_printoptions(threshold=np.nan)

data = np.load('objectClass.npy')
#data = [1,2,3,4]
print data
#print len(data[0,:])
#print len(data[:0])
print "size"
print data.shape
