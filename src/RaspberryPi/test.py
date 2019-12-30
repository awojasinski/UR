import cv2 as cv
import cvision as cvis
import math
from matplotlib import pyplot as plt
from picamera.array import PiRGBArray
from picamera import PiCamera
from time import sleep
import json
import numpy as np
import sys

config, order, mtx, dist, T, distRatio, ratio = cvis.configRead('config.json')
'''
U = [155, 307]
X = cvis.transformPos(U, T)

print(X)


U = [[386.95010376, 232.99201965],
 [318.58337402, 333.4888916 ],
 [158.52075195, 225.41828918],
 [226.28141785, 125.30464172]]

X = np.empty(shape=(0,2))
for i in U:
    X = np.append(X, [cvis.transformPos(i, T)], axis=0)
print(X)

T_n = np.linalg.inv(T)

print(T_n)
U = np.empty(shape=(0,2))
for i in X:
    U = np.append(U, [cvis.transformPos(i, T_n)], axis=0)

print(U)
'''
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 30
rawCapture = PiRGBArray(camera, size=(640, 480))
# Zatrzymanie programu aby kamera mogła się uruchomić
sleep(0.1)

for frame in camera.capture_continuous(rawCapture, format='bgr', use_video_port=True):

    img = frame.array   # Zapisanie akutalnego kadru do zmiennej

    height, width = img.shape[:2]   # Przypisanie do zmiennych rozdzielczości obrazu
    # Obliczenie nowej rozdzielczości obrazu po usunięciu zniekształceń
    newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (width, height), 1, (width, height))

    img = cv.undistort(img, mtx, dist, None, newcameramtx)  # Usunięcie zniekształceń obrazu

    x, y, w, h = roi
    img = img[y:y+h, x:x+w]
    cv.imshow('cam', img)
    
    key = cv.waitKey(1) & 0xFF
    
    if key == 13:
        cv.imwrite('test.png', img)
        shape_info = cvis.objectRecognition(img)
        print(shape_info)
        print(shape_info[0][0])
        pos = cvis.transformPos(shape_info[0][0], T)
        print(pos)
        cv.destroyAllWindows()
        break
        
    rawCapture.truncate(0)  # Wyczyszczenie strumienia, aby przygotować go na kolejną klatkę
