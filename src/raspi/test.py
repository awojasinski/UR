import cv2 as cv
import numpy as np
import json
from matplotlib import pyplot as plt
from matplotlib import pylab
import cvision as cvis
#from picamera.array import PiRGBArray
#from picamera import PiCamera
#from time import sleep

config, order, mtx, dist, T, areaRatio = cvis.configRead('config.json')
element = 0

img = cv.imread('C:\\Users\\njcp6k\\Desktop\\testing.png')
shapes_info = cvis.objectRecognition(img, draw=False)
ret, index = cvis.findElement(order[element], shapes_info)
if ret:
    pos = cvis.transformPos(shapes_info[index][0], T)
    cvis.drawElement(shapes_info[index], pos, img)
cv.imshow('Image', img)
cv.waitKey(0)

'''
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 30
rawCapture = PiRGBArray(camera, size=(640, 480))
sleep(0.1)


for frame in camera.capture_continuous(rawCapture, format='bgr', use_video_port=True):

    img = frame.array
    cv.imshow("Live", img)
    height, width = img.shape[:2]
    newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (width, height), 1, (width, height))

    img = cv.undistort(img, mtx, dist, None, newcameramtx)

    x, y, w, h = roi
    img = img[y:y+h, x:x+w]

    img_drawing = img.copy()
    shapes_info = cvis.objectRecognition(img_drawing)
    key = cv.waitKey(1) & 0xFF
    
    rawCapture.truncate(0)
    if key == 13:
        pos = cvis.tranformPos(shapes_info[0][0], T)
        print(pos)
        
    
'''
'''
shapes_info = np.empty(shape=(0, 3))
img = cv.imread('C:\\Users\\njcp6k\\Desktop\\test1.png')
shapes_info = np.append(shapes_info, cvis.objectRecognition(img),axis=0)
img = cv.imread('C:\\Users\\njcp6k\\Desktop\\test2.png')
shapes_info = np.append(shapes_info, cvis.objectRecognition(img),axis=0)
img = cv.imread('C:\\Users\\njcp6k\\Desktop\\test3.png')
shapes_info = np.append(shapes_info, cvis.objectRecognition(img),axis=0)
img = cv.imread('C:\\Users\\njcp6k\\Desktop\\test4.png')
shapes_info = np.append(shapes_info, cvis.objectRecognition(img),axis=0)


U = np.empty(shape=(0, 2))
for point in shapes_info:
    U = np.append(U, np.array([[point[0][1], point[0][0]]]), axis=0)

X = np.array([[60., 73.], [60., 20.], [20., 20.], [20., 73.]])
print(X.shape[0])
print(U)
print(X)

T = cv.findHomography(U, X)
print(T[0])

P = np.array([320., 240., 1.])

Robot = T[0]@P

pixelArea = cv.contourArea(U.astype(int))
realArea = cv.contourArea(X.astype(int))

print(pixelArea)
print(realArea)

print(Robot[:2])


U = np.insert(U, 2, 1, axis=1)
print(U)
'''

config, order, mtx, dist, T, areaRatio = cvis.configRead('config.json')

'''
img = cv.imread('C:\\Users\\Adam\\Desktop\\CV_test_img\\11.jpg')

with open('config.json', 'r') as config_file:
    data = config_file.read()

config = json.loads(data)
order = np.asarray(config['objects_order'])

print(len(order))
for num, key in enumerate(order[0].keys()):
    print(num)
    print(key)

config, order = cvis.configRead('config.json')
print(config)
print(order)

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
img = cv.cvtColor(img, cv.COLOR_BGR2HSV)
h, s, v = cv.split(img)

img_hsv = np.zeros(img.shape, dtype=img.dtype)
img_hsv[:, :, 1] = 0
img_hsv[:, :, 2] = v
img_hsv[:, :, 0] = 0

img_hsv = cv.cvtColor(img_hsv, cv.COLOR_HSV2BGR)

#gray = cv.GaussianBlur(gray, (7, 7), 0)

histhsv = cv.calcHist([v], [0], None, [256], [0, 255])
histgray = cv.calcHist([gray], [0], None, [256], [0, 255])

cv.imshow('Value', v)
cv.imwrite('value11.jpg', v)
cv.imshow('Gray', gray)
cv.imwrite('gray11.jpg', gray)
plt.plot(histhsv)
plt.xlabel('Intensywność')
plt.ylabel('Ilość pikseli')
plt.title('Histogram HSV')
plt.savefig('histogramHSV11.png')
plt.show()

plt.plot(histgray)
plt.xlabel('Intensywność')
plt.ylabel('Ilość pikseli')
plt.title('Histogram GRAY')
plt.savefig('histogramGRAY11.png')
plt.show()


threshhsv = cv.threshold(v, 150, 255, cv.THRESH_BINARY)[1]
cv.imshow('threshold HSV', threshhsv)
cv.imwrite('thresholdhsv11.jpg', threshhsv)

threshgray = cv.threshold(gray, 150, 255, cv.THRESH_BINARY)[1]
cv.imshow('threshold GRAY', threshgray)
cv.imwrite('thresholdgray11.jpg', threshgray)


img = cv.imread('C:\\Users\\Adam\\Desktop\\CV_test_img\\14.jpg')
img = cv.cvtColor(img, cv.COLOR_BGR2HSV)
h, s, v = cv.split(img)

cv.imshow('Value', v)

hist = cv.calcHist([v], [0], None, [256], [0, 255])
plt.plot(hist)
plt.xlabel('Intensywność', fontsize=10)
plt.ylabel('Ilość pikseli', fontsize=10)
plt.title('Histogram', fontsize=10)
plt.show()

#img_channel = np.zeros(img.shape, dtype=img.dtype)
#img_channel[:, :, 2] = r

#gray = ((0.20*b + 0.15*g + 0.65*r))
#gray = r/3 + g/3 + b/3

#cv.imshow('HSV-v', img_hsv)
#cv.imwrite('hsv-v.jpg', img_hsv)

#img = cv.merge((b, g, r))
#cv.imshow('img', img)

#cv.imshow('green', img_channel)
#cv.imwrite('red.jpg', img_channel)
cv.waitKey()


#plt.imshow(img)
#plt.show()
'''
