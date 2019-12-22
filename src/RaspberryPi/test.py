import cv2 as cv
import cvision as cvis
from picamera.array import PiRGBArray
from picamera import PiCamera
from time import sleep
import json
import numpy as np
import sys

config, order, mtx, dist, T, areaRatio = cvis.configRead('config.json')

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 30
rawCapture = PiRGBArray(camera, size=(640, 480))
sleep(0.1)

i = 0

for frame in camera.capture_continuous(rawCapture, format='bgr', use_video_port=True):
    img = frame.array
    height, width = img.shape[:2]
    newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (width, height), 1, (width, height))

    img = cv.undistort(img, mtx, dist, None, newcameramtx)

    x, y, w, h = roi
    img = img[y:y + h, x:x + w]

    cv.imshow("Live", img)
    key = cv.waitKey(1) & 0xFF
    
    if key == 13:
        cv.imwrite(str(i)+'.png', img)
        i = i +1
        
    if key == ord('q'):
         cv.destroyAllWindows()
         break
        
    rawCapture.truncate(0)

        
        
        

