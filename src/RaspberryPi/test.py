import cv2 as cv
import cvision as cvis
from matplotlib import pyplot as plt
#from picamera.array import PiRGBArray
#from picamera import PiCamera
from time import sleep
import json
import numpy as np
import sys

for i in range(26):
    img = cv.imread('camera_images\\' + str(i) + '.png')
    gray = cv.imread('camera_images\\' + str(i) + '.png', 0)

    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    h, s, v = cv.split(hsv)
    '''
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
    '''
    shapes_info = cvis.objectRecognition(img, True)

    cv.imshow('recognized', img)
    print(shapes_info)
    cv.waitKey()
