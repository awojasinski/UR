import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import pylab
import cvision as cvis

img = cv.imread('C:\\Users\\Adam\\Desktop\\CV_test_img\\11.jpg')
'''
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
img = cv.cvtColor(img, cv.COLOR_BGR2HSV)
h, s, v = cv.split(img)

img_hsv = np.zeros(img.shape, dtype=img.dtype)
img_hsv[:, :, 1] = 0
img_hsv[:, :, 2] = v
img_hsv[:, :, 0] = 0

img_hsv = cv.cvtColor(img_hsv, cv.COLOR_HSV2BGR)

#gray = cv.GaussianBlur(gray, (7, 7), 0)

histhsv = cv.calcHist([v], [0], None, [256], [0, 255])
histgray = cv.calcHist([gray], [0], None, [256], [0, 255])

cv.imshow('Value', v)
cv.imwrite('value11.jpg', v)
cv.imshow('Gray', gray)
cv.imwrite('gray11.jpg', gray)
plt.plot(histhsv)
plt.xlabel('Intensywność')
plt.ylabel('Ilość pikseli')
plt.title('Histogram HSV')
plt.savefig('histogramHSV11.png')
plt.show()

plt.plot(histgray)
plt.xlabel('Intensywność')
plt.ylabel('Ilość pikseli')
plt.title('Histogram GRAY')
plt.savefig('histogramGRAY11.png')
plt.show()


threshhsv = cv.threshold(v, 150, 255, cv.THRESH_BINARY)[1]
cv.imshow('threshold HSV', threshhsv)
cv.imwrite('thresholdhsv11.jpg', threshhsv)

threshgray = cv.threshold(gray, 150, 255, cv.THRESH_BINARY)[1]
cv.imshow('threshold GRAY', threshgray)
cv.imwrite('thresholdgray11.jpg', threshgray)
'''

img = cv.imread('C:\\Users\\Adam\\Desktop\\CV_test_img\\14.jpg')
img = cv.cvtColor(img, cv.COLOR_BGR2HSV)
h, s, v = cv.split(img)

cv.imshow('Value', v)

hist = cv.calcHist([v], [0], None, [256], [0, 255])
plt.plot(hist)
plt.xlabel('Intensywność', fontsize=10)
plt.ylabel('Ilość pikseli', fontsize=10)
plt.title('Histogram', fontsize=10)
plt.
plt.show()

#img_channel = np.zeros(img.shape, dtype=img.dtype)
#img_channel[:, :, 2] = r

#gray = ((0.20*b + 0.15*g + 0.65*r))
#gray = r/3 + g/3 + b/3

#cv.imshow('HSV-v', img_hsv)
#cv.imwrite('hsv-v.jpg', img_hsv)

#img = cv.merge((b, g, r))
#cv.imshow('img', img)

#cv.imshow('green', img_channel)
#cv.imwrite('red.jpg', img_channel)
cv.waitKey()


#plt.imshow(img)
#plt.show()

