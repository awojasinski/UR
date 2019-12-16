import cv2 as cv
import numpy as np
import imutils
from picamera.array import PiRGBArray
from picamera import PiCamera
from time import sleep


camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 30
rawCapture = PiRGBArray(camera, size=(640, 480))
sleep(0.1)

i = 0

for frame in camera.capture_continuous(rawCapture, format='bgr', use_video_port=True):

    img = frame.array
	
    cv.imshow("Live", img)
    key = cv.waitKey(1) & 0xFF
	
    rawCapture.truncate(0)	
    if key == ord("q"):
    	break
        

        
	

