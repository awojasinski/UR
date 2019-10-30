# TODO
#   - color2=Noneges of colors in separated in different file
#   - create function colorDetect(rgb_pixel_value) return string color

import cv2 as cv
import imutils
import numpy as np
import math
from matplotlib import pyplot as plt

colors = {
    'red': np.array([85, 0, 0]),
    'blue': np.array([0, 0, 85]),
    'orange': np.array([255, 128, 0]),
    'magenta': np.array([255, 0, 255]),
    'green': np.array([0, 85, 0]),
    'yellow': np.array([170, 170, 0]),
    'cyan': np.array([0, 255, 255]),
}

def colorRecognition(pixelRGB):
    newDict = dict()
    for (name, rbg) in colors.items():
        if pixelRGB[0] > rbg[0] and pixelRGB[1] > rbg[1] and pixelRGB[2] > rbg[2]:
            newDict[name] = rbg
    print(newDict)
    return


img = cv.imread('img/shapes_and_colors.jpg')
gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
blurred = cv.GaussianBlur(gray, (5, 5), 0)
thresh = cv.threshold(blurred, 70, 255, cv.THRESH_BINARY)[1]

cnts = cv.findContours(thresh.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

points = np.empty(shape=(0, 3))

for c in cnts:
    M = cv.moments(c)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    points = np.append(points, [[cX, cY, img[cX, cY]]], axis=0)

    cv.drawContours(img, [c], -1, (0, 0, 255), 2, cv.LINE_AA)
    cv.circle(img, (cX, cY), 4, (255, 255, 255), -1)

#for c in range(len(points)):
 #   cv.putText(img, str(c+1)+'.'+points[c][3], tuple([points[c][0], points[c][1]]), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv.LINE_AA)

for i in range(len(points)):
    print(str(points[i]))
    colorRecognition(points[i][2])

plt.imshow(cv.cvtColor(img, cv.COLOR_BGR2RGB))
plt.show()
cv.waitKey(0)
cv.destroyAllWindows()
