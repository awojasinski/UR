import cv2 as cv
import cvision as cvis
from picamera.array import PiRGBArray
from picamera import PiCamera
from time import sleep
from matplotlib import pyplot as plt
import numpy as np
import json

def nothing(x):
    pass

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

scale = 40  # Zmiejszenie obrazu do 40% oryginalnego
width = int(camera.resolution[0] * scale / 100)
height = int(camera.resolution[1] * scale / 100)
dim = (width, 3*height)     # Nowe wymiary obrazu

fig = plt.figure()  # Inicjalizacja wykresu

# Inicjalizacja okna
cv.namedWindow("Threshold Setup")
cv.createTrackbar("Próg binaryzacji", "Threshold Setup", thresholdValue, 255, nothing)

for frame in camera.capture_continuous(rawCapture, format='bgr', use_video_port=True):

    # Trójwymiarowa macierz o wymiarach szerokość, wysokość i kanał koloru
    img = frame.array   # Zapisanie akutalnego kadru do zmiennej
    thresholdValue = cv.getTrackbarPos('Próg binaryzacji', "Threshold Setup")   # Pobranie wartości z suwaka
    
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)    # Zmiana przestrzeni barw z BGR na HSV
    h, s, v = cv.split(hsv)     # Wydzielenie kanałów HSV obrazu na osobne zmienne
    blurred = cv.GaussianBlur(v, (5, 5), 0)     # Rozmycie obrazu
    thresh = cv.threshold(blurred, thresholdValue, 255, cv.THRESH_BINARY)[1]    # Binaryzacja obrazu
    thresh = cv.cvtColor(thresh, cv.COLOR_GRAY2BGR)     # Zmiana zbinaryzowanego obrazu na 3 kanały
    
    hist = cv.calcHist([v], [0], None, [256], [0, 256])     # Obliczenie histogramu obrazu
    plt.clf()   # Usunięcie poprzedniego wykresu z okna
    plt.plot(hist)  # Utworzenie wykresu histogramu
    plt.xlim([0, 255])      # Ustawienie limitu na osi X
    fig.canvas.draw()   # Narysowanie wykresu
    hist_img = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')     # Zamiana wykresu na rysunek
    hist_img = hist_img.reshape(fig.canvas.get_width_height()[::-1]+(3,))       # Zmiana rozmiaru tablicy
    hist_img = cv.cvtColor(hist_img, cv.COLOR_RGB2BGR)      # Zamiana przestrzeni barw z RGB na BGR
    
    vertical_img = np.vstack((img, hist_img, thresh))   # Połączenie trzech obrazów w pionie
    vertical_img = cv.resize(vertical_img, dim, interpolation=cv.INTER_AREA)    # Zmiana rozdzielczości obrazu
    
    cv.imshow("Threshold Setup", vertical_img)  # Wyświetlenie obrazu

    # Oczekiwanie na wciśnięcie klawisza przez użytkownika, klatka wyświetlana jest przez 1ms
    # Operator logiczny AND sprawia że ważny jest tylko pierwszy bajt zwracany przez funkcję
    # dzięki temu nie ma znaczenia czy klwaisz został wciśnięty z włączonym CapsLock czy nie
    key = cv.waitKey(1) & 0xFF

    if key == 13:
        print('Zapisano w pliku konfiguracyjnym wartość progu binaryzacji')
        print('Wszystkie piksele o wartości poniżej %d będą czarne,\na wszystkie > %d białe' %(thresholdValue, thresholdValue))
        cv.imwrite('threshold_setup.png', vertical_img)
        config['cam_calibration']['thresholdValue'] = thresholdValue    # Zapisanie zmiennej do pliku konfiguracyjnego
        with open('config.json', 'w') as config_file:
            json.dump(config, config_file, sort_keys=True, indent=4)
        cv.destroyAllWindows()
        break
    
    rawCapture.truncate(0)
