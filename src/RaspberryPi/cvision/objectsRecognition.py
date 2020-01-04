import numpy as np
import cv2 as cv
from cvision.contoursDetection import *
from cvision.colorRecognition import *
from cvision.configRead import *


def objectsRecognition(image, draw=False):
    config, order, mtx, dist, T, distRatio, thresholdValue, objectHeight = configRead('config.json')  # Odczytanie parametrów z pliku konfiguracyjnego

    cnts, points = contoursDetection(image, draw)     # Wykrywanie konturów na obrazie przekazanym jako argument

    shapes_info = np.empty(shape=(0, 4))        # Inicjalizacja tablicy przechowywującej dane o znalezionych obiektach

    # Pętla dla każdego wykrytego obiektu
    for point, cnt in zip(points, cnts):
        color = colorRecognition(image, cnt)    # Wykrycie koloru danego konturu
        # Zapis informacji do talblicy [[X, Y, theta], kolor, pole powierzchnii]
        shapes_info = np.append(shapes_info, [[[point[0], point[1]], point[2], color, cv.contourArea(cnt)*(distRatio**2)]], axis=0)
        # Funkcje rysujące do przedstawienia informacji o obiektach
    
    if draw:
        return shapes_info, image
    else:
        return shapes_info
