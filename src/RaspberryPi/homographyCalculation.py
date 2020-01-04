import cv2 as cv
import cvision as cvis
import math
from picamera.array import PiRGBArray
from picamera import PiCamera
from time import sleep
import json
import numpy as np
import sys

# Funkcja obliczająca odległość pomiędzy dwoma punktami
def distance(pointA, pointB):
    dist = math.sqrt((pointA[0]-pointB[0])**2 + (pointA[1]-pointB[1])**2)
    return dist

# Pobranie danych o kamerze, macierzy homografii oraz kolejności podawania elementów
# z pliku konfiguracyjnego, ustawienie wskaźnika element na pierwszą wartość
config, order, mtx, dist, T, distRatio, thresholdValue, objectHeight = cvis.configRead('config.json')

# Początkowe ustawienia kamery
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 30
rawCapture = PiRGBArray(camera, size=(640, 480))
# Zatrzymanie programu aby kamera mogła się uruchomić
sleep(0.1)

# Inicjalizacja tablic do przechowywania współrzędnych punktów na obrazie i w przestrzeni robota
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

chess_heigth = int(input("Podaj ilość narożników szachownicy w pionie na szukanej tablicy kalibracyjnej: "))
chess_width = int(input("Podaj ilość narożników szachownicy w poziomie na szukanej tablicy kalibracyjnej: "))
dim = (chess_heigth, chess_width)

for frame in camera.capture_continuous(rawCapture, format='bgr', use_video_port=True):

    # Trójwymiarowa macierz o wymiarach szerokość, wysokość i kanał koloru
    img = frame.array   # Zapisanie akutalnego kadru do zmiennej
    
    img = cv.undistort(img, mtx, dist)  # Usunięcie zniekształceń obrazu

    cv.imshow("Homography Calculation", img)      # Wyświetlenie okna z podglądem obrazu

    # Oczekiwanie na wciśnięcie klawisza przez użytkownika, klatka wyświetlana jest przez 1ms
    # Operator logiczny AND sprawia że ważny jest tylko pierwszy bajt zwracany przez funkcję
    # dzięki temu nie ma znaczenia czy klwaisz został wciśnięty z włączonym CapsLock czy nie
    key = cv.waitKey(1) & 0xFF
    
    if key == 13:
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)  # Zamiana przestrzenii barw BGR na skalę szarości
        ret, corners = cv.findChessboardCorners(gray, dim, None)    # Wykrycie planszy kalibracyjnej na obrazie
        if ret:
            cv.imwrite('homography_calculation.png', img)
            # Przypisanie do macierzy skrajnych punktów planszy kaliracyjnej
            U[0] = corners[np.where(corners[0:len(corners), 0] == max(corners[0:len(corners), 0, 0]))[0]]
            U[1] = corners[np.where(corners[0:len(corners), 0] == max(corners[0:len(corners), 0, 1]))[0]]
            U[2] = corners[np.where(corners[0:len(corners), 0] == min(corners[0:len(corners), 0, 0]))[0]]
            U[3] = corners[np.where(corners[0:len(corners), 0] == min(corners[0:len(corners), 0, 1]))[0]]
            print(U)
            # Narysowanie na obrazie położeń oraz numerów poszczególnych punktów kalibracyjnych
            for num, cnt in enumerate(U):
                cv.circle(img, (int(cnt[0]), int(cnt[1])), 5, (0, 0, 255), 3)
                cv.putText(img, str(num + 1), (int(cnt[0]) + 10, int(cnt[1]) - 10), cv.FONT_HERSHEY_SCRIPT_SIMPLEX, 1, (0, 0, 255), 1)
            cv.imshow('Position Calibration', img)
            cv.imwrite('homography_calculation_points.png', img)
            # Pętla przypisująca współrzędne punktów w przestrzenii robota
            for num, point in enumerate(X):
                point[0] = float(input('Współrzędna X punktu nr ' + str(num + 1) + ':')) / 1000
                point[1] = float(input('Współrzędna Y punktu nr ' + str(num + 1) + ':')) / 1000

            T = cv.findHomography(U, X)# Obliczenie macierzy homografii kamera -> robot
            print(X)
            distRatio = float(distance(X[0], X[2]) / distance(U[0], U[2]))  # Obliczenie współczynnika proporcjonalności długości
            print("Macierz homografii:\n", T[0])
            # Zapisanie obliczonych wartości do pliku konfiguracyjnego
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

