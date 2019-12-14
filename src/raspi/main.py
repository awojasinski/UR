import cv2 as cv
import numpy as np
import imutils
import socket
from picamera.array import PiRGBArray
from picamera import PiCamera
from time import sleep
import cvision as cvis

HOST = '192.168.1.113'
PORT = 10000

_, order = cvis.config_read('config.json')

camera = PiCamera()
camera.resolution = (1920, 1080)
camera.framerate = 30
rawCapture = PiRGBArray(camera, size=(1920, 1080))
sleep(0.1)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)

    for frame in camera.capture_continuous(rawCapture, format='bgr', use_video_port=True):

        img = frame.array
        #img = cv.resize(img, (800, 450))


        cv.imshow("Live", img)
        key = cv.waitKey(1) & 0xFF

        rawCapture.truncate(0)

        if key == ord("q"):
            break

