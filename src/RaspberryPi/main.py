import cv2 as cv
import socket
import sys
from picamera.array import PiRGBArray
from picamera import PiCamera
from time import sleep
import cvision as cvis

# Adres IP servera (RespberryPi) oraz port
HOST = '192.168.0.110'
PORT = 10000

# Pobranie danych o kamerze, macierzy homografii oraz kolejności podawania elementów
# z pliku konfiguracyjnego, ustawienie wskaźnika element na pierwszą wartość
config, order, mtx, dist, T, distRatio, thresholdValue, objectHeight = cvis.configRead('config.json')
element = 0

# Początkowe ustawienia kamery
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 30
rawCapture = PiRGBArray(camera, size=(640, 480))
# Zatrzymanie programu aby kamera mogła się uruchomić
sleep(0.1)
photo = 0

print('Computer vision system')
print('----------------------')
print('Server | host %s | port %d |' %(HOST, PORT))
print('----------------------')
print('Objects order:')
for obj in order:
    print(obj)
print('----------------------')

# Utworzenia gniazda do komunikacji TCP/IP pomiędzy RaspberryPi 4 a robotem UR5
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)

print('Waiting for connection')

connection, client_addr = s.accept()    # Zaakceptowanie próby nawiązania połączenia z serwerem

print('Connection from: ', client_addr)

for frame in camera.capture_continuous(rawCapture, format='bgr', use_video_port=True):

    # Trójwymiarowa macierz o wymiarach szerokość, wysokość i kanał koloru
    img = frame.array   # Zapisanie akutalnego kadru do zmiennej

    img = cv.undistort(img, mtx, dist)  # Usunięcie zniekształceń obrazu

    cv.imshow("Live", img)      # Wyświetlenie okna z podglądem obrazu
   
    shapes_info = cvis.objectsRecognition(img, False)   # Wyszukiwanie obiektów na obrazie

    print('---------------------')
    print(shapes_info)
    print('---------------------\n')

    ret, index = cvis.findElement(order[element], shapes_info)  # Sprawdzenie czy w wykrytych obiektach znajuduje się szukany obiekt

    if not ret:
        print("Object not found")

    if ret:
        print('Sending coordinates of shape:\n', shapes_info[index])
        pos = cvis.transformPosition(shapes_info[index][0], T)  # Obliczenie połorzenia obiektu w przestrzeni robota z macierzy homografii
        print('Robot position %f X %f Y' % (pos[0], pos[1]))
        # Wysłanie do robota UR5 współrzędnych punktu w którym znajduje się obiekt
        connection.sendall(("(" + str(round(pos[0], 5)) + ', ' + str(round(pos[1], 5)) + ", " + str(objectHeight) + ", " + str(shapes_info[index][1]) + ", 3.14, 0)").encode('ascii'))
        cv.imwrite('camera_images/main'+str(photo)+'.png', img)
        photo += 1
        print('Waiting for response')
        data = connection.recv(1024).decode('ascii')  # Odebranie informacji od robota
        if data == 'OK':
            element += 1  # Inkrementacja wskaźnika
            if element == len(order):
                element = 0
        elif data == 'q':
            print('Closing server')
            s.close()
            cv.destroyAllWindows()
            sys.exit()

    rawCapture.truncate(0)  # Wyczyszczenie strumienia, aby przygotować go na kolejną klatkę
