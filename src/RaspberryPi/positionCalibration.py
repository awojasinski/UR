import cv2 as cv
import cvision as cvis
import math
from picamera.array import PiRGBArray
from picamera import PiCamera
from time import sleep
import json
import numpy as np
import sys


def distance(pointA, pointB):
    dist = math.sqrt((pointA[0]-pointB[0])**2 + (pointA[1]-pointB[1])**2)
    return dist


config, order, mtx, dist, T, distRatio, thresholdValue = cvis.configRead('config.json')

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 30
rawCapture = PiRGBArray(camera, size=(640, 480))
sleep(0.1)

U = np.empty(shape=(4, 2))
X = np.empty(shape=(4, 2))

print("Kalibracja kamery z robotem")
print("---------------------------")
print("Opis procesu kalibracji:")
print("1.Ustaw chwytak robota w pozycji pionowej")
print("2.Umieść tablicę kalibracyjną w polu widzenia kamery")
print("3.Przemieść pozostałe elementy poza obszar aktywny kamery")
print("4.Naciśnij klawisz Enter")
print("5.Wprowadź współrzędne zaznaczonych narożników w odpowiedniej kolejności w mm")

for frame in camera.capture_continuous(rawCapture, format='bgr', use_video_port=True):
    img = frame.array
    height, width = img.shape[:2]
    newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (width, height), 1, (width, height))

    img = cv.undistort(img, mtx, dist, None, newcameramtx)

    x, y, w, h = roi
    img = img[y:y + h, x:x + w] # Zastanowić się czy bez będzie lepiej?

    cv.imshow("chess", img)
    key = cv.waitKey(1) & 0xFF

    
    if key == 13:
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        ret, corners = cv.findChessboardCorners(gray, (9, 6), None) # Wilekość tablicy podawana przez użytkownika
        if ret:
            U[0] = corners[np.where(corners[0:len(corners), 0] == max(corners[0:len(corners), 0, 0]))[0]]
            U[1] = corners[np.where(corners[0:len(corners), 0] == max(corners[0:len(corners), 0, 1]))[0]]
            U[2] = corners[np.where(corners[0:len(corners), 0] == min(corners[0:len(corners), 0, 0]))[0]]
            U[3] = corners[np.where(corners[0:len(corners), 0] == min(corners[0:len(corners), 0, 1]))[0]]
            for num, cnt in enumerate(U):
                cv.circle(img, (int(cnt[0]), int(cnt[1])), 5, (0, 0, 255), 3)
                cv.putText(img, str(num + 1), (int(cnt[0]) + 10, int(cnt[1]) - 10), cv.FONT_HERSHEY_SCRIPT_SIMPLEX, 1, (0, 0, 255), 1)
            cv.imshow('chess', img)
            cv.imwrite('pos_calibration.png', img)
            for num, point in enumerate(X):
                point[0] = float(input('Współrzędna X punktu nr ' + str(num + 1) + ':')) / 1000
                point[1] = float(input('Współrzędna Y punktu nr ' + str(num + 1) + ':')) / 1000

            T = cv.findHomography(U, X)
            distRatio = float(distance(X[0], X[2]) / distance(U[0], U[2]))
            print("Macierz homografii:\n", T[0])
            config['pos_calibration']['T'] = T[0].tolist()
            config['pos_calibration']['distRatio'] = distRatio
            with open('config.json', 'w') as config_file:
                json.dump(config, config_file, sort_keys=True, indent=4)
            cv.destroyAllWindows()
            sys.exit()
        else:
            print("W obszarze aktywnym nie wykryto tablicy kalibracyjnej")

    elif key == ord('q') or key == 27:
        print("Przerwanie procesu kalibracji kamery z robotem")
        break
    
    rawCapture.truncate(0)

cv.destroyAllWindows()

