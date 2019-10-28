import cv2 as cv
import numpy as np
import imutils
from picamera.array import PiRGBArray
from picamera import PiCamera
from time import sleep


camera = PiCamera()
camera.resolution = (1000, 600)
camera.framerate = 30
rawCapture = PiRGBArray(camera, size=(1000, 600))
sleep(0.1)

for frame in camera.capture_continuous(rawCapture, format='bgr', use_video_port=True):

    img = frame.array
    gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
    blurred = cv.GaussianBlur(gray, (5,5), 0)
    #thresh = cv.threshold(blurred, 50, 255, cv.THRESH_BINARY)[1]
    canny = cv.Canny(blurred, 90, 190)
    
    cnts = cv.findContours(canny.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    for c in cnts:
        #M = cv.moments(c)
        #cX = int(M["m10"] / M["m00"])
        #cY = int(M["m01"] / M["m00"])

        cv.drawContours(img, [c], -1, (0, 0, 255), 2)
        #cv.circle(img, (cX, cY), 4, (255, 255, 255), -1)
	
    cv.imshow("Live", img)
    key = cv.waitKey(1) & 0xFF
	
    rawCapture.truncate(0)
	
    if key == ord("q"):
    	break
	

