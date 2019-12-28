import numpy as np
import cv2 as cv
from cvision.contoursDetection import *
from cvision.colorRecognition import *
from cvision.configRead import *


def objectRecognition(image, draw=True):
    config, order, mtx, dist, T, distRatio, thresholdValue = configRead('config.json')
    cnts, points = contoursDetection(image)

    shapes_info = np.empty(shape=(0, 3))

    for point, cnt in zip(points, cnts):
        color = colorRecognition(image, cnt)
        shapes_info = np.append(shapes_info, [[point, color, cv.contourArea(cnt)*(distRatio**2)]], axis=0)
        if draw:
            cv.drawContours(image, [cnt], -1,(255, 255, 255), 2)
            cv.putText(image, color, (point[1], point[0]), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))

    return shapes_info
