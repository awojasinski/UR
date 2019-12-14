import numpy as np
import cv2 as cv
from cvision.contours_detection import *
from cvision.color_detection import *


def objectRecognition(image):
    cnts, points = contoursDetection(image, drawContours=True)

    shapes_info = np.empty(shape=(0, 3))

    for point, cnt in zip(points, cnts):
        shapes_info = np.append(shapes_info, [[point, colorRecognition(image, point), cv.contourArea(cnt)]], axis=0)
        cv.drawContours(image, [cnt], -1,(255, 255, 255), 2)
        cv.putText(image, colorRecognition(image, point), (point[1], point[0]), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))

    return shapes_info
