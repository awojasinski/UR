# TODO:
#   - ranges of colors in separated in different file
#   - create function colorDetect(rgb_pixel_value) return string color

import cv2 as cv
import imutils
import numpy as np

colors = {
    'red': np.array([255, 100, 100]),
    'blue': np.array([100, 100, 255]),
    'orange': np.array([255, 183, 101]),
    'magenta': np.array([255, 100, 255]),
    'grey': np.array([178, 178, 178]),
    'green': np.array([100, 255, 100]),
    'yellow': np.array([255, 255, 100]),
    'cyan': np.array([192, 255, 255]),
}

img = cv.imread('img/shapes_and_colors.jpg')
gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
blurred = cv.GaussianBlur(gray, (5, 5), 0)
thresh = cv.threshold(blurred, 70, 255, cv.THRESH_BINARY)[1]

cnts = cv.findContours(thresh.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

points = np.empty(shape = (0,3))

for c in cnts:
    M = cv.moments(c)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    points = np.append(points, [[cX, cY, img[cX, cY]]], axis=0)

    cv.drawContours(img, [c], -1, (0, 0, 255), 2, cv.LINE_AA)
    cv.circle(img, (cX, cY), 4, (255, 255, 255), -1)

cv.imshow("Image thresh", img)
cv.waitKey(0)
cv.destroyAllWindows()
