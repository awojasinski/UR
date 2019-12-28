import cv2 as cv
from picamera.array import PiRGBArray
from picamera import PiCamera
from time import sleep
import cvision as cvis
import socket

# Pobranie danych o kamerze, macierzy homografii oraz kolejności podawania elementów
# z pliku konfiguracyjnego, ustawienie wskaźnika element na pierwszą wartość
config, order, mtx, dist, T, distRatio, thresholdValue = cvis.configRead('config.json')
element = 0
objectHeight = 0

# Początkowe ustawienia kamery
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 30
rawCapture = PiRGBArray(camera, size=(640, 480))
# Zatrzymanie programu aby kamera mogła się uruchomić
sleep(0.1)

# Adres IP servera (RespberryPi) oraz port
HOST = '192.168.0.110'
PORT = 10000

# Utworzenia gniazda do komunikacji TCP/IP pomiędzy RaspberryPi 4 a robotem UR5
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)

print('Server |%s|%d|' %(HOST, PORT))

connection, client_addr = s.accept()    # Zaakceptowanie próby nawiązania połączenia z serwerem

print('Connection from: ', client_addr)


for frame in camera.capture_continuous(rawCapture, format='bgr', use_video_port=True):

    # Trójwymiarowa macierz o wymiarach szerokość, wysokość i kanał koloru
    img = frame.array   # Zapisanie akutalnego kadru do zmiennej

    height, width = img.shape[:2]   # Przypisanie do zmiennych rozdzielczości obrazu
    # Obliczenie nowej rozdzielczości obrazu po usunięciu zniekształceń
    newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (width, height), 1, (width, height))

    img = cv.undistort(img, mtx, dist, None, newcameramtx)  # Usunięcie zniekształceń obrazu

    x, y, w, h = roi
    img = img[y:y+h, x:x+w]     # Utworzenie nowego obrazu o zmniejsze rozdzielczości niż początkowa
    cv.imshow("Live", img)      # Wyświetlenie okna z podglądem obrazu

    # Oczekiwanie na wciśnięcie klawisza przez użytkownika, klatka wyświetlana jest przez 1ms
    # Operator logiczny AND sprawia że ważny jest tylko pierwszy bajt zwracany przez funkcję
    # dzięki temu nie ma znaczenia czy klwaisz został wciśnięty z włączonym CapsLock czy nie
    key = cv.waitKey(1) & 0xFF

    rawCapture.truncate(0)  # Wyczyszczenie strumienia, aby przygotować go na kolejną klatkę

    if key == ord('q'):     # Jeśli wciśnięty klawisz to 'q' zamknij okno i zakończ program
        cv.destroyAllWindows()
        break
    elif key == 13:     # Jeśli wciśnięty klawisz to 'Enter' zostanie zapisany obraz
        s = input('Nazwa zdjęcia: ')
        cv.imwrite(s+'.png', img)
    elif key == ord('c'):   # Jeśli wciśnięty klawisz to 'c' rozpocznie się wyszukiwanie obiektu
        shapes_info = cvis.objectRecognition(img)   # Funkcja zwraca tablicę z informacjami o znalezioncyh obiektach
        print('---------------------')
        print(shapes_info)
        print('---------------------\n')
        ret, index = cvis.findElement(order[element], shapes_info) # Funkcja zwraca indeks obiektu w drugiej tablicy, informacje o obiekcie podawane są jako pierwszy argument
        print('---------------------')
        print("ret value: ", ret)
        print('index: ', index)

        if ret:
            print('object info: ', shapes_info[index])
            pos = cvis.transformPos(shapes_info[index][0], T)   # Obliczenie połorzenia obiektu w przestrzeni robota z macierzy homografii
            print('Robot position', pos)
            element += 1    # Inkrementacja wskaźnika
            # Wysłanie do robota UR5 współrzędnych punktu w którym znajduje się obiekt
            connection.send(('('+str(round(pos[0], 3))+', '+str(round(pos[1], 3))+', '+str(objectHeight)+', 0, 3.14, 0)').encode('ascii'))
            data = connection.recv(1024).decode('ascii')

            if element == len(order):
                element = 0
