import cv2 as cv
import cvision as cvis
import math
from matplotlib import pyplot as plt
#from picamera.array import PiRGBArray
#from picamera import PiCamera
from time import sleep
import json
import numpy as np
import sys

config, order, mtx, dist, T, distRatio = cvis.configRead('config.json')

U = [463, 234]
X = cvis.transformPos(U, T)

print(X)

'''
#img = cv.imread()

config, order, mtx, dist, T, distRatio, thresholdValue = cvis.configRead('config.json')
height, width = img.shape[:2]
newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (width, height), 1, (width, height))

img = cv.undistort(img, mtx, dist, None, newcameramtx)

x, y, w, h = roi
img = img[y:y+h, x:x+w]

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
cv.imshow('chess', gray)

ret, corners = cv.findChessboardCorners(gray, (9, 6), None)

U = np.empty(shape=(4, 2))
X = np.empty(shape=(4, 2))

U[0] = corners[np.where(corners[0:len(corners),0] == max(corners[0:len(corners),0,0]))[0]]
U[1] = corners[np.where(corners[0:len(corners),0] == max(corners[0:len(corners),0,1]))[0]]
U[2] = corners[np.where(corners[0:len(corners),0] == min(corners[0:len(corners),0,0]))[0]]
U[3] = corners[np.where(corners[0:len(corners),0] == min(corners[0:len(corners),0,1]))[0]]

print(U)

for num, cnt in enumerate(U):
    cv.circle(img, (int(cnt[0]), int(cnt[1])), 5, (0,0,255), 3)
    cv.putText(img, str(num+1), (int(cnt[0])+10, int(cnt[1])-10), cv.FONT_HERSHEY_SCRIPT_SIMPLEX, 1, (0,0,255), 2)
cv.imshow('chess', img)
D = math.sqrt((U[2][0]-U[0][0])**2 + (U[2][1]-U[0][1])**2)



print(X)
print(D)

cv.waitKey(0)

'''

'''
for i in range(26):
    img = cv.imread('camera_images\\' + str(i) + '.png')
    gray = cv.imread('camera_images\\' + str(i) + '.png', 0)

    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    h, s, v = cv.split(hsv)
   
    cv.imshow('original', img)
    cv.imshow('value', v)

    hist_v = cv.calcHist([v], [0], None, [256], [0, 256])
    plt.plot(hist_v)
    plt.title('value')
    plt.show()

    clahe = cv.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    clv = clahe.apply(v)
    hist_cv = cv.calcHist([clv], [0], None, [256], [0, 256])
    plt.plot(hist_cv)
    plt.title('clahe value')
    plt.show()

    thresh = cv.threshold(v, 190, 255, cv.THRESH_BINARY)[1]
    cv.imshow('thresh', thresh)
    
    shapes_info = cvis.objectRecognition(img, True)

    cv.imshow('recognized', img)
    print(shapes_info)
    cv.waitKey()
'''