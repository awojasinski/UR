import cv2 as cv
import numpy as np
import imutils
from cvision.configRead import *


def contoursDetection(image, drawContours=False):

    config, order, mtx, dist, T, distRatio, thresholdValue = configRead('config.json')

    # Preprocessing obrazu
    hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    h, s, v = cv.split(hsv)
    blurred = cv.GaussianBlur(v, (5, 5), 0)
    thresh = cv.threshold(blurred, 195, 255, cv.THRESH_BINARY)[1] # Pobierane z pliku konfiguracyjnego
    #thresh = cv.adaptiveThreshold(blurred, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11, 2)
    cv.imshow('thresh', thresh)
    # Wykrywanie konturów na obrazie
    cnts = cv.findContours(thresh.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    # Inicjalizacja tablicy centroidów
    center_points = np.empty(shape=(0, 2), dtype=int)

    for c in cnts:
        m = cv.moments(c)  # Obliczenie momentów geometrycznych
        if m["m00"] != 0:
            x = int(m["m10"] / m["m00"])    # Obliczenie współrzędnej X
            y = int(m["m01"] / m["m00"])    # Obliczenie współrzędnej Y
        else:
            x = 0
            y = 0
        center_points = np.append(center_points, [[y, x]], axis=0)  # Dodanie nowych współrzędnych do tablicy

        if drawContours:
            cv.drawContours(image, [c], -1, (0, 0, 255), 2)

    return cnts, center_points
