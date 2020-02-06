import cv2 as cv
from time import sleep
import cvision as cvis
import socket

# Pobranie danych o kamerze, macierzy homografii oraz kolejności podawania elementów
# z pliku konfiguracyjnego, ustawienie wskaźnika element na pierwszą wartość
config, order, mtx, dist, T, distRatio, thresholdValue, objectHeight = cvis.configRead('config.json')
element = 0
i = 0

# Początkowe ustawienia kamery
camera = cv.VideoCapture(0)
camera.set(cv.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv.CAP_PROP_FRAME_HEIGHT, 480)
camera.set(cv.CAP_PROP_FPS, 30)
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


while True:

    # Trójwymiarowa macierz o wymiarach szerokość, wysokość i kanał koloru
    ret, img = camera.read()   # Zapisanie akutalnego kadru do zmiennej

    img = cv.undistort(img, mtx, dist)  # Usunięcie zniekształceń obrazu

    cv.imshow("Live", img)      # Wyświetlenie okna z podglądem obrazu

    # Oczekiwanie na wciśnięcie klawisza przez użytkownika, klatka wyświetlana jest przez 1ms
    # Operator logiczny AND sprawia że ważny jest tylko pierwszy bajt zwracany przez funkcję
    # dzięki temu nie ma znaczenia czy klwaisz został wciśnięty z włączonym CapsLock czy nie
    key = cv.waitKey(1) & 0xFF

    if key == ord('q'):     # Jeśli wciśnięty klawisz to 'q' zamknij okno i zakończ program
        print('Zakończenie działania programu')
        cv.destroyAllWindows()
        cv.VideoCapture(0).release()
        break
    elif key == 13:     # Jeśli wciśnięty klawisz to 'Enter' zostanie zapisany obraz
        s = input('Nazwa zdjęcia: ')
        cv.imwrite(s+'.png', img)
    elif key == ord('c'):   # Jeśli wciśnięty klawisz to 'c' rozpocznie się wyszukiwanie obiektu
        
        shapes_info = cvis.objectsRecognition(img, False)   # Funkcja zwraca tablicę z informacjami o znalezioncyh obiektach
        print('---------------------')
        print(shapes_info)
        print('---------------------\n')
        ret, index = cvis.findElement(order[element], shapes_info) # Funkcja zwraca indeks obiektu w drugiej tablicy, informacje o obiekcie podawane są jako pierwszy argument
        print('---------------------')
        print("ret value: ", ret)
        print('index: ', index)

        if ret:
            print('object info: ', shapes_info[index])
            pos = cvis.transformPosition(shapes_info[index][0], T)   # Obliczenie połorzenia obiektu w przestrzeni robota z macierzy homografii
            print('Robot position', pos)
            cv.imwrite('camera_images/homographyTest'+str(i)+'.png', img)
            i += 1
            # Wysłanie do robota UR5 współrzędnych punktu w którym znajduje się obiekt
            connection.send(('('+str(pos[0])+', '+str(pos[1])+', '+str(objectHeight)+', ' + str(shapes_info[index][1]) + ', 3.14, 0)').encode('ascii'))
            data = connection.recv(1024).decode('ascii')    # Odebranie informacji od robota
            if data == 'OK':
                element += 1  # Inkrementacja wskaźnika
            if element == len(order):
                element = 0
