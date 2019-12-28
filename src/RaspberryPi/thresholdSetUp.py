import cv2 as cv
import cvision as cvis
from picamera.array import PiRGBArray
from picamera import PiCamera
from time import sleep
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider, Button
import json

config, order, mtx, dist, T, distRatio, thresholdValue = cvis.configRead('config.json')

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 30
rawCapture = PiRGBArray(camera, size=(640, 480))
sleep(0.1)

for frame in camera.capture_continuous(rawCapture, format='bgr', use_video_port=True):

    img = frame.array
    cv.imshow("Camera", img)
    cv.createButton("Zapisz")
    cv.createTrackbar("Próg binaryzacji", "Camera", thresholdValue, 255)

    key = cv.waitKey(1) & 0xFF
    if key == 13:
        cv.destroyAllWindows()
        break
'''
config['cam_calibration']['thresholdValue'] = thresholdValue

with open('config.json', 'w') as config_file:
    json.dump(config, config_file, sort_keys=True, indent=4)
'''