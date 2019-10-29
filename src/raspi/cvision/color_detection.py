# TODO:
#   - define ranges of specific colors (dictionary)
#   - ranges of colors in separated in different file
#   - create function colorDetect(img, cX, cY) return string color

import cv2
import imutils
import numpy as np

#colors = {
    #'red' : np.array((), ()),
    #'blue' : np.array((), ()),
    #'orange' : np.array((), ()),
    #'pink' : np.array((), ()),
    #'white' : np.array((), ()),
    #'green' : np.array((), ()),
    #'yellow' : np.array((), ()),
    #'violet' : np.array((), ()),
#}

img = cv2.imread('img/shapes_and_colors.jpg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
blurred = cv2.GaussianBlur(gray, (5,5), 0)
thresh = cv2.threshold(blurred, 70, 255, cv2.THRESH_BINARY)[1]

cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

i = 0
for c in cnts:
    M = cv2.moments(c)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    pos[i][0] = cX
    pos[i][1] = cY
    i = i + 1

    cv2.drawContours(img, [c], -1, (0, 0, 255), 2, cv2.LINE_AA)
    cv2.circle(img, (cX, cY), 4, (255, 255, 255), -1)

cv2.imshow("Image thresh", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
