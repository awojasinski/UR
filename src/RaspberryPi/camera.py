import cv2 as cv
from time import sleep

# Początkowe ustawienia kamery
camera = cv.VideoCapture(0)
camera.set(cv.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv.CAP_PROP_FRAME_HEIGHT, 480)
camera.set(cv.CAP_PROP_FPS, 30)
# Zatrzymanie programu aby kamera mogła się uruchomić
sleep(0.1)

i = 1   # Zmienna do numerowania uchwyconych zdjęć szachownicy

heigth = int(input("Podaj ilość narożników szachownicy w pionie na szukanej tablicy kalibracyjnej: "))
width = int(input("Podaj ilość narożników szachownicy w poziomie na szukanej tablicy kalibracyjnej: "))
dim = (heigth, width)

while True:
    
    # Trójwymiarowa macierz o wymiarach szerokość, wysokość i kanał koloru
    ret, img = camera.read()   # Zapisanie akutalnego kadru do zmiennej
    
    cv.imshow('Camera', img)    # Wyświetlenie okna z podglądem obrazu

    # Oczekiwanie na wciśnięcie klawisza przez użytkownika, klatka wyświetlana jest przez 1ms
    # Operator logiczny AND sprawia że ważny jest tylko pierwszy bajt zwracany przez funkcję
    # dzięki temu nie ma znaczenia czy klwaisz został wciśnięty z włączonym CapsLock czy nie
    key = cv.waitKey(1) & 0xFF
    
    if key == ord('q'):     # Jeśli wciśnięty klawisz to 'q' zamknij okno i zakończ program
        cv.destroyAllWindows()
        cv.VideoCapture(0).release()
        break
    elif key == 13:
        ret, corners = cv.findChessboardCorners(gray, dim, None)     # Szukanie szachownicy

        if ret:  # Jeśli wykryto w kadrze szachownicę
            print('Wykonano zdjęcie nr:', i)    # Wyświetlenie informacji o wykonaniu zdjęcia
            cv.imwrite('camera_correction_photos/'+str(i)+'.png', img)     # Zapisanie zdjęcia do folderu
            i += 1      # Inkrementacja numeracji zdjęć
        else:
            print('Brak tablicy kalibracyjnej')
