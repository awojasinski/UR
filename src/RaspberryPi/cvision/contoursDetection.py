import cv2 as cv
import numpy as np
import imutils
import math
import os
from cvision.configRead import *


def contoursDetection(image, drawContours=False):
    config, order, mtx, dist, T, distRatio, thresholdValue, objectHeight = configRead('config.json')  # Odczytanie parametrów z pliku konfiguracyjnego

    # Preprocessing obrazu
    hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)  # Zmiana przestrzenii barw obrazu
    h, s, v = cv.split(hsv)     # Rozdzielenie kanałów obrazu na osobne zmienne
    blurred = cv.GaussianBlur(v, (5, 5), 0)     # Rozmycie obrazu
    thresh = cv.threshold(blurred, thresholdValue, 255, cv.THRESH_BINARY)[1]    # Binaryzacja obrazu przy użyciu zmiennej z pliku kalibracyjnego
    cv.imshow('thresh', thresh)
    # Wykrywanie konturów na obrazie
    cnts = cv.findContours(thresh.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    # Inicjalizacja tablicy dla punktów centralnych
    center_points = np.empty(shape=(0, 3), dtype=int)

    for c in cnts:
        m = cv.moments(c)  # Obliczenie momentów geometrycznych
        if m["m00"] != 0:
            x = m["m10"] / m["m00"]    # Obliczenie współrzędnej X
            y = m["m01"] / m["m00"]    # Obliczenie współrzędnej Y
            u20 = m['m20'] / m['m00'] - x*x
            u02 = m['m02'] / m['m00'] - y*y
            u11 = m['m11'] / m['m00'] - x*y
            if (u20-u02)!=0:
                theta = 0.5 * math.atan2(2*u11, (u20 - u02))
            else:
                theta = 0
        else:
            x = 0
            y = 0
        center_points = np.append(center_points, [[x, y, theta]], axis=0)  # Dodanie nowych współrzędnych do tablicy

        if drawContours:
            cv.drawContours(image, [c], -1, (0, 0, 255), 2)     # Rysowanie konturów na obrazie
            return cnts, center_points, image
        else:
            return cnts, center_points
