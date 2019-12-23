import numpy as np
import cv2 as cv
from cvision.contoursDetection import *
from cvision.colorRecognition import *


def objectRecognition(image, draw=True):
    cnts, points = contoursDetection(image)

    shapes_info = np.empty(shape=(0, 3))

    for point, cnt in zip(points, cnts):
        color = colorRecognition(image, cnt)
        shapes_info = np.append(shapes_info, [[point, color, cv.contourArea(cnt)]], axis=0)
        if draw:
            cv.drawContours(image, [cnt], -1,(255, 255, 255), 2)
            cv.putText(image, color, (point[1], point[0]), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))

    return shapes_info
