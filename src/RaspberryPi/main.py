import cv2 as cv
import numpy as np
import socket
import sys
from picamera.array import PiRGBArray
from picamera import PiCamera
from time import sleep
import cvision as cvis

HOST = '192.168.1.113'
PORT = 10000

config, order, mtx, dist, T, areaRatio = cvis.configRead('config.json')
element = 0

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 30
rawCapture = PiRGBArray(camera, size=(640, 480))
sleep(0.1)

print('Computer vision system')
print('----------------------')
print('Server | host %s | port %d |' %(HOST, PORT))
print('----------------------')
print('Objects order:')
for obj in order:
    print(obj)
print('----------------------')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)

print('Waiting for connection')

connection, client_addr = s.accept()

print('Connection from: ', client_addr)

for frame in camera.capture_continuous(rawCapture, format='bgr', use_video_port=True):

    img = frame.array

    height, width = img.shape[:2]
    newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (width, height), 1, (width, height))

    img = cv.undistort(img, mtx, dist, None, newcameramtx)

    x, y, w, h = roi
    img = img[y:y+h, x:x+w]
    cv.imshow("Live", img)
    img_drawing = img.copy()
    shapes_info = cvis.objectRecognition(img_drawing)

    print('---------------------')
    print(shapes_info)
    print('---------------------\n')

    ret, index = cvis.findElement(shapes_info, order[element])

    if not ret:
        print("Object not found")

    if ret:
        print('Sending coordinates of shape:', shapes_info[index])
        pos = cvis.tranformPos(shapes_info[index][0], T)
        connection.sendall("(" + pos[0] + ',' + pos[1] + ")")
        img_drawing = cvis.drawElement(shapes_info[index], pos, img_drawing)
        cv.imshow("Found element", img_drawing)
        cv.imwrite(str(element)+'.png', img_drawing)
        print('Waiting for response')
        data = connection.recv(1024)
        if data == 'OK':
            element = element + 1
            if element == len(order):
                element = 0
        elif data == 'q':
            print('Closing server')
            s.close()
            cv.destroyAllWindows()
            sys.exit()

    rawCapture.truncate(0)
