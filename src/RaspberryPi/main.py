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
config, order, mtx, dist, T, distRatio, thresholdValue = cvis.configRead('config.json')
element = 0
objectHeight = 0.204

# Początkowe ustawienia kamery
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 30
rawCapture = PiRGBArray(camera, size=(640, 480))
# Zatrzymanie programu aby kamera mogła się uruchomić
sleep(0.1)

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

    height, width = img.shape[:2]   # Przypisanie do zmiennych rozdzielczości obrazu
    # Obliczenie nowej rozdzielczości obrazu po usunięciu zniekształceń
    newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (width, height), 1, (width, height))

    img = cv.undistort(img, mtx, dist, None, newcameramtx)  # Usunięcie zniekształceń obrazu

    x, y, w, h = roi
    img = img[y:y+h, x:x+w]     # Utworzenie nowego obrazu o zmniejsze rozdzielczości niż początkowa
    cv.imshow("Live", img)      # Wyświetlenie okna z podglądem obrazu
    img_drawing = img.copy()    # Utworzenie kopii obrazu
    shapes_info = cvis.objectRecognition(img_drawing)   # Wyszukiwanie obiektów na obrazie

    print('---------------------')
    print(shapes_info)
    print('---------------------\n')

    ret, index = cvis.findElement(order[element], shapes_info)  # Sprawdzenie czy w wykrytych obiektach znajuduje się szukany obiekt

    if not ret:
        print("Object not found")

    if ret:
        print('Sending coordinates of shape:', shapes_info[index])
        pos = cvis.transformPos(shapes_info[index][0], T)  # Obliczenie połorzenia obiektu w przestrzeni robota z macierzy homografii
        # Wysłanie do robota UR5 współrzędnych punktu w którym znajduje się obiekt
        connection.sendall(("(" + str(round(pos[0], 3)) + ', ' + str(round(pos[1], 3)) + ", " + str(objectHeight) + ", " + shapes_info[index][1] + ", 3.14, 0)").encode('ascii'))
        img_drawing = cvis.drawElement(shapes_info[index], pos, img_drawing)    # Zapisanie na obrazie informacji o wykrytym obiekcie
        cv.imshow("Found element", img_drawing)
        cv.imwrite(str(element)+'.png', img_drawing)    # Zapisanie obrazu
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
