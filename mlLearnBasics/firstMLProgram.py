import matplotlib.pyplot as plt 

from sklearn import datasets
from sklearn import svm

digits = datasets.load_digits()

clf = svm.SVC(gamma=0.001, C=100)

x,y = digits.data[:-1], digits.target[:-1]
clf.fit(x,y)

numToPredict =1
print('Prediction:', clf.predict(digits.data[-numToPredict].reshape(1,-1)))

plt.imshow(digits.images[-numToPredict], cmap=plt.cm.gray_r, interpolation="nearest")
plt.show()
