# TODO:
#   - convert image from BGR to HSV
#   - define ranges of specific colors (data structure? dictionary or something like that)
#   - ranges of colors in separated in different file
#   - create array with information (shape area, coordinate X, coordinate Y, color, orientation of the shape)

import cv2
import imutils

img = cv2.imread('shapes_and_colors.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
blurred = cv2.GaussianBlur(gray, (5,5), 0)
thresh = cv2.threshold(blurred, 70, 255, cv2.THRESH_BINARY)[1]

cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

for c in cnts:
    M = cv2.moments(c)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])

    cv2.drawContours(img, [c], -1, (0, 0, 255), 2, cv2.LINE_AA)
    cv2.circle(img, (cX, cY), 4, (255, 255, 255), -1)

cv2.imshow("Image thresh", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
