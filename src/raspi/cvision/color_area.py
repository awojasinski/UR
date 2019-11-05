import numpy as np
import cv2 as cv
from cvision.edge_detection import *
from cvision.color_detection import *


def color_areaRecognition(image):
    cnts, points = contoursDetection(image)

    shapes_info = np.empty(shape=(0, 3))
    for point, cnt in zip(points, cnts):
        shapes_info = np.append(shapes_info, [[point, colorRecognition(image, point), cv.contourArea(cnt)]], axis=0)

    return shapes_info
