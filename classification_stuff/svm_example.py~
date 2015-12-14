import scipy.io
import numpy as np
import pylab as pl
from sklearn.linear_model import lasso_path, LassoCV
from sklearn import svm
import matplotlib.pyplot as plt

# create data
numpts = 1000
b = 2+np.random.normal(loc=0.0, scale=1.0, size=[numpts, 2])
c = np.random.normal(loc=0.0, scale=1.0, size=[numpts, 2])

plt.plot(b[:,0],b[:,1],'.r')
plt.plot(c[:,0],c[:,1],'.k')
#plt.show()

x = np.concatenate((b[:,0], c[:,0])) # to append
y = np.concatenate((b[:,1], c[:,1]))
X = np.column_stack((x, y)) #to stack

a = np.ones(numpts)
a2 = np.zeros(numpts)
Y = np.concatenate((a,a2))


# SVM train (classification by default)
clf = svm.SVC()
clf.fit(X, Y)

# SVM classify 
Yhat = clf.predict(X)
error = np.sum(abs(Yhat-Y))
print (numpts-error)/numpts

Yb = Yhat==1
plt.plot(X[Yb,0],X[Yb,1],'or',markersize=10,fillstyle='none')
plt.plot(X[~Yb,0],X[~Yb,1],'ok',markersize=10,fillstyle='none')
plt.plot(b[:,0],b[:,1],'.r')
plt.plot(c[:,0],c[:,1],'.k')
plt.show()

