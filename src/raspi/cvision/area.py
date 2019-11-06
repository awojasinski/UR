import numpy as np
import cv2 as cv
from cvision.edge_detection import *


def areaRecognition(image):
    cnts, points = contoursDetection(image)

    shapes_info = np.empty(shape=(0, 2))
    for point, cnt in zip(points, cnts):
        shapes_info = np.append(shapes_info, [[point, cv.contourArea(cnt)]], axis=0)

    return shapes_info
