import cv2 as cv
from picamera.array import PiRGBArray
from picamera import PiCamera
from time import sleep

# Początkowe ustawienia kamery
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 30
rawCapture = PiRGBArray(camera, size=(640, 480))
# Zatrzymanie programu aby kamera mogła się uruchomić
sleep(0.1)

i = 0   # Zmienna do numerowania uchwyconych zdjęć szachownicy

heigth = int(input("Podaj ilość narożników szachownicy w pionie na szukanej tablicy kalibracyjnej: "))
width = int(input("Podaj ilość narożników szachownicy w poziomie na szukanej tablicy kalibracyjnej: "))
dim = (heigth, width)

for frame in camera.capture_continuous(rawCapture, format='bgr', use_video_port=True):

    # Trójwymiarowa macierz o wymiarach szerokość, wysokość i kanał koloru
    img = frame.array   # Zapisanie akutalnego kadru do zmiennej
    # Dwuwymiarowa macierz szerokość na wysokość wartości od 0 do 255
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)  # Zamiana przestrzeni barw na skale szarości

    cv.imshow('Camera', img)    # Wyświetlenie okna z podglądem obrazu

    ret, corners = cv.findChessboardCorners(gray, dim, None)     # Szukanie szachownicy

    if ret:  # Jeśli wykryto w kadrze szachownicę
        print('Wykonano zdjęcie nr:', i)    # Wyświetlenie informacji o wykonaniu zdjęcia
        cv.imwrite('cam_correction_photos\\'+str(i)+'.png')     # Zapisanie zdjęcia do folderu
        i += 1      # Inkrementacja numeracji zdjęć

    # Oczekiwanie na wciśnięcie klawisza przez użytkownika, klatka wyświetlana jest przez 1ms
    # Operator logiczny AND sprawia że ważny jest tylko pierwszy bajt zwracany przez funkcję
    # dzięki temu nie ma znaczenia czy klwaisz został wciśnięty z włączonym CapsLock czy nie
    key = cv.waitKey(1) & 0xFF

    if key == ord('q'):     # Jeśli wciśnięty klawisz to 'q' zamknij okno i zakończ program
        cv.destroyAllWindows()
        break

    rawCapture.truncate(0)  # Wyczyszczenie strumienia, aby przygotować go na kolejną klatkę
