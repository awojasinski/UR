import cv2 as cv
import cvision as cvis
from picamera.array import PiRGBArray
from picamera import PiCamera
from time import sleep
from matplotlib import pyplot as plt
import numpy as np
import json

def nothing(x):
    pass        

config, order, mtx, dist, T, distRatio, thresholdValue = cvis.configRead('config.json')

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 30
rawCapture = PiRGBArray(camera, size=(640, 480))
sleep(0.1)

scale = 40
width = int(camera.resolution[0] * scale / 100 )
height = int(camera.resolution[1] * scale / 100)
dim = (width, 3*height)

fig = plt.figure()

cv.namedWindow("Threshold Setup")
cv.createTrackbar("Próg binaryzacji", "Threshold Setup", thresholdValue, 255, nothing)
cv.createTrackbar("0:OFF\n1:ON", "Threshold Setup", 0, 1, nothing)

for frame in camera.capture_continuous(rawCapture, format='bgr', use_video_port=True):

    img = frame.array
    thresholdValue = cv.getTrackbarPos('Próg binaryzacji', "Threshold Setup")
    
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    h, s, v = cv.split(hsv)
    blurred = cv.GaussianBlur(v, (5, 5), 0)
    thresh = cv.threshold(blurred, thresholdValue, 255, cv.THRESH_BINARY)[1]
    thresh = cv.cvtColor(thresh, cv.COLOR_GRAY2BGR)
    
    hist = cv.calcHist([v],[0],None,[256],[0,256])
    plt.clf()
    plt.plot(hist)
    plt.xlim([0, 255])
    fig.canvas.draw()
    hist_img = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8,sep='')
    hist_img = hist_img.reshape(fig.canvas.get_width_height()[::-1]+(3,))
    hist_img = cv.cvtColor(hist_img, cv.COLOR_RGB2BGR)
    
    vertical_img = np.vstack((img, hist_img, thresh))
    vertical_img = cv.resize(vertical_img, dim, interpolation = cv.INTER_AREA)
    
    cv.imshow("Threshold Setup", vertical_img)
    
    key = cv.waitKey(1) & 0xFF
    if key == 13:
        config['cam_calibration']['thresholdValue'] = thresholdValue
        with open('config.json', 'w') as config_file:
            json.dump(config, config_file, sort_keys=True, indent=4)
        cv.destroyAllWindows()
        break
    
    rawCapture.truncate(0)
