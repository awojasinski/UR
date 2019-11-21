import cv2 as cv
import numpy as np
import imutils


def contoursDetection(image, drawContours=False):
    # Processing image for better contour recognition
    gray = cv.cvtColor(image, cv.COLOR_RGB2GRAY)
    blurred = cv.GaussianBlur(gray, (5, 5), 0)
    thresh = cv.threshold(blurred, 70, 255, cv.THRESH_BINARY)[1]

    cnts = cv.findContours(thresh.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    center_points = np.empty(shape=(0, 2), dtype=int)

    for c in cnts:
        m = cv.moments(c)
        x = int(m["m10"] / m["m00"])
        y = int(m["m01"] / m["m00"])
        center_points = np.append(center_points, [[y, x]], axis=0)

        if drawContours:
            cv.drawContours(image, [c], -1, (0, 0, 255), 2)

    return cnts, center_points
