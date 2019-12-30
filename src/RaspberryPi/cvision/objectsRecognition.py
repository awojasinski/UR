import numpy as np
import cv2 as cv
from cvision.contoursDetection import *
from cvision.colorRecognition import *
from cvision.configRead import *


def objectRecognition(image, draw=True):
    dir = ""    # Zainicjalizowanie zmiennej przechowywującej ścieżkę do katalogu
    path = os.getcwd()  # Odczytanie scieżki w której znajduje się skrypt
    if '/' in path:
        path = path.split('/')
        path.pop()
        for p in path:
            dir = dir + p + '/'
    if '\\' in path:
        path = path.split('\\')
        path.pop()
        for p in path:
            dir = dir + p + '\\'
            
    config, order, mtx, dist, T, distRatio, thresholdValue = configRead(dir+'config.json')  # Odczytanie parametrów z pliku konfiguracyjnego

    cnts, points = contoursDetection(image)     # Wykrywanie konturów na obrazie przekazanym jako argument

    shapes_info = np.empty(shape=(0, 3))        # Inicjalizacja tablicy przechowywującej dane o znalezionych obiektach

    # Pętla dla każdego wykrytego obiektu
    for point, cnt in zip(points, cnts):
        color = colorRecognition(image, cnt)    # Wykrycie koloru danego konturu
        # Zapis informacji do talblicy [[X, Y], kolor, pole powierzchnii]
        shapes_info = np.append(shapes_info, [[point, color, cv.contourArea(cnt)*(distRatio**2)]], axis=0)
        # Funkcje rysujące do przedstawienia informacji o obiektach
        if draw:
            cv.drawContours(image, [cnt], -1, (255, 255, 255), 2)
            cv.putText(image, color, (point[1], point[0]), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))

    return shapes_info
