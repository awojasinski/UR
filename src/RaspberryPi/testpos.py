import cv2 as cv
import cvision as cvis
import math
from time import sleep
import json
import numpy as np
import sys


def distance(pointA, pointB):
    dist = math.sqrt((pointA[0]-pointB[0])**2 + (pointA[1]-pointB[1])**2)
    return dist

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)  # Zamiana przestrzenii barw BGR na skalę szarości
ret, corners = cv.findChessboardCorners(gray, dim, None)    # Wykrycie planszy kalibracyjnej na obrazie
    if ret:
    # Przypisanie do macierzy skrajnych punktów planszy kaliracyjnej
        U[0] = corners[np.where(corners[0:len(corners), 0] == max(corners[0:len(corners), 0, 0]))[0]]
        U[1] = corners[np.where(corners[0:len(corners), 0] == max(corners[0:len(corners), 0, 1]))[0]]
        U[2] = corners[np.where(corners[0:len(corners), 0] == min(corners[0:len(corners), 0, 0]))[0]]
        U[3] = corners[np.where(corners[0:len(corners), 0] == min(corners[0:len(corners), 0, 1]))[0]]
        # Narysowanie na obrazie położeń oraz numerów poszczególnych punktów kalibracyjnych
        for num, cnt in enumerate(U):
            cv.circle(img, (int(cnt[0]), int(cnt[1])), 5, (0, 0, 255), 3)
            cv.putText(img, str(num + 1), (int(cnt[0]) + 10, int(cnt[1]) - 10), cv.FONT_HERSHEY_SCRIPT_SIMPLEX, 1, (0, 0, 255), 1)
            cv.imshow('Position Calibration', img)
           # Pętla przypisująca współrzędne punktów w przestrzenii robota
        for num, point in enumerate(X):
            point[0] = float(input('Współrzędna X punktu nr ' + str(num + 1) + ':')) / 1000
            point[1] = float(input('Współrzędna Y punktu nr ' + str(num + 1) + ':')) / 1000

            T = cv.findHomography(U, X) # Obliczenie macierzy homografii kamera -> robot
            distRatio = float(distance(X[0], X[2]) / distance(U[0], U[2]))  # Obliczenie współczynnika proporcjonalności długości
            print("Macierz homografii:\n", T[0])
            # Zapisanie obliczonych wartości do pliku konfiguracyjnego
            config['pos_calibration']['T'] = T[0].tolist()
            config['pos_calibration']['distRatio'] = distRatio
            with open('config.json', 'w') as config_file:
                json.dump(config, config_file, sort_keys=True, indent=4)
            cv.destroyAllWindows()
            sys.exit()