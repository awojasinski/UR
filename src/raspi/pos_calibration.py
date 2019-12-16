import cv2 as cv
import cvision as cvis
from picamera.array import PiRGBArray
from picamera import PiCamera
from time import sleep
import numpy as np
import sys

config, order, mtx, dist = cvis.configRead('config.json')

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 30
rawCapture = PiRGBArray(camera, size=(640, 480))
sleep(0.1)

U = np.empty(size=(0, 2))
X = np.empty(size=(0, 2))

print("Kalibracja kamery z robotem")
print("---------------------------")
print("Opis procesu kalibracji:")
print("1.Ustaw chwytak robota w pozycji pionowej")
print("2.Umieść obiekt w polu widzenia kamery")
print("3.Przemieść pozostałe elementy poza obszar aktywny kamery")
print("4.Naciśnij klawisz Enter")
print("5.Przy pomocy panelu operatorskiego zbliż chwytak robota do obiektu")
print("6.Do okna terminala wprowadź współrzędne chwytaka według wyświetlonych w terminalu poleceń")
print("Powyższe kroki powtórzyć dla czterech punktów\nw narożnikach obszaru aktywnego pola widzenia kamery")

for frame in camera.capture_continous(rawCapture, format='bgr', use_video_port=True):
    img = frame.array
    height, width = img.shape[:2]
    newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (width, height), 1, (width, height))

    img = cv.undistort(img, mtx, dist, None, newcameramtx)

    x, y, w, h = roi
    img = img[y:y + h, x:x + w]

    cv.imshow("Live", img)
    key = cv.waitkey(1) & 0xFF

    rawCapture.truncate(0)
    if key == 13:
        shapes_info = cvis.objectRecognition(img, draw=False)
        if len(shapes_info) != 1:
            print("W obszarze aktywnym kamery wykryto więcej niż jeden obiekt!")
            break
        U = np.append(U, [shapes_info[0][0][1], shapes_info[0][0][0]], axis=0)
        x = float(input("Podaj współrzędną X: "))
        y = float(input("Podaj współrzędną Y: "))
        X = np.append(X, [x, y], axis=0)

        if U.shape[0] == 4 and X.shape[0] == 4:
            T = cv.findHomography(U, X)
            areaRatio = cv.contourArea(X.astype(int)) / cv.contourArea(U.astype(int))
            print("Macierz transformacji:\n", T[0])
            config['pos_calibration']['T'] = T[0].tolist()
            config['pos_calibration']['areaRatio'] = areaRatio.tolist()
            with open('config.json', 'w') as config_file:
                json.dump(config, config_file, sort_keys=True, indent=4)
            cv.destroyAllWindows()
            sys.exit()

    elif key == ord('q') or key == 27:
        print("Przerwanie procesu kalibracji kamery z robotem")
        break

cv.destroyAllWindows()

