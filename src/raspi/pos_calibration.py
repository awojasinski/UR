import cv2 as cv
import cvision as cvis
from picamera.array import PiRGBArray
from picamera import PiCamera
from time import sleep
import numpy as np
import sys

def calculateTransform(U, X, config_file)

    with open(config_file) as f:
        config = json.load(f)

    config['pos_calibration']['T'] = T.tolist()

    with open(config_file, 'w') as f:
        json.dump(config, f, sort_keys=True, indent=4)

    return T

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

        print("Podaj współrzędną X: ")
        print("Podaj współrzędną Y: ")

        if U.size[1] == 4 and X.size[1] == 4:
            print("Macierz transformacji:\n", calculateTransform(U, X, 'config.json'))
            cv.destroyAllWindows()
            sys.exit()


    elif key == ord('q') or key == 27:
        print("Przerwanie procesu kalibracji kamery z robotem")
        break

cv.destroyAllWindows()

