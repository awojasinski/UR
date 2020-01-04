import numpy as np
import cv2 as cv
import glob
import json

# Ustawienie kryteriów zakończenia obliczeń
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Macierze przechowywujące współrzędne punktów obiektu i współrzędne pikseli na obrazie
objpoints = [] # trójwymiarowe współrzędne obiektu
imgpoints = [] # dwuwymiarowe współrzędne punktu na obrazie

images = glob.glob('camera_correction_photos/*.png')  # Utworzenie listy obiektów o rozszeżeniu .png znajdujących się w katalogu cam_correction_photos
heigth = int(input("Podaj ilość narożników szachownicy w pionie na szukanej tablicy kalibracyjnej: "))
width = int(input("Podaj ilość narożników szachownicy w poziomie na szukanej tablicy kalibracyjnej: "))
dim = (heigth, width)

# Przygotowanie współrzędnych punktów na planszy kalibracyjnej
objp = np.zeros((heigth*width, 3), np.float32)
objp[:, :2] = np.mgrid[0:heigth, 0:width].T.reshape(-1, 2)

# Pętla wykonywana dla każdego zdjęcia znalezionego w powyższym katalogu
for fname in images:
    img = cv.imread(fname)  # Odczytanie obrazu
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)  # Konwersja BGR na skalę szarości

    ret, corners = cv.findChessboardCorners(gray, dim, None)     # Wyszukanie wzoru szachownicy na zdjęciu

    if ret == True:
        objpoints.append(objp)
        corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)     # Funkcja zwiększająca dokładność współrzędnych wykrytych narożników
        imgpoints.append(corners)

# Funkcja zwracająca parametry wewnętrzne kamery, wektor zniekształceń oraz wektory rotacji i translacji
ret, mtx_old, dist_old, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

mean_error = 0      # Zainicjalizowanie zmiennej przechowywująceś średni błąd reprojekcji
camConfigRaport = np.empty(shape=(0, 4))    # Zainicjalizowanie tablicy zawierającej [nazwa obrazu, wektor rotacji, wektor translacji, błąd reprojekcji]

# Zapisanie do pliku zewnętrznego wektorów rotacji, translacji i błędu reprojekcji
for rv, tv, fname, objpnt, imgpnt in zip(rvecs, tvecs, images, objpoints, imgpoints):
    if '/' in fname:
        fname = fname.split('/')
        fname = fname[1]
    if '\\' in fname:
        fname = fname.split('\\')
        fname = fname[1]
    imgpoints2, _ = cv.projectPoints(objpnt, rv, tv, mtx_old, dist_old)
    error = cv.norm(imgpnt, imgpoints2, cv.NORM_L2)/len(imgpoints2)
    camConfigRaport = np.append(camConfigRaport, [[fname, rv, tv, error]], axis=0)
    mean_error += error

mean_error = mean_error / len(objpoints)
with open('camera_correction_photos/raport.txt', "w") as f:
    for x in camConfigRaport:
        s = '\n\nfile: ' + x[0] + ',\nrotation vector:\n' + str(x[1]) + ',\ntranslation vector:\n' + str(x[2]) + ',\nreprojection error: ' + str(x[3])
        f.write(s)

print('Średnia wartość błędu reprojekcji wynosi: ', mean_error)
error = float(input('Podaj wartość błędu dla którego zostanie ponownie skalibrowana kamera: '))

# Macierze przechowywujące współrzędne punktów obiektu i współrzędne pikseli na obrazie
objpoints = [] # trójwymiarowe współrzędne obiektu
imgpoints = [] # dwuwymiarowe współrzędne punktu na obrazie

good_img = 0

for i, fname in enumerate(images):
    img = cv.imread(fname)  # Odczytanie obrazu
    if '/' in fname:
        fname = fname.split('/')
        fname = fname[1]
    if '\\' in fname:
        fname = fname.split('\\')
        fname = fname[1]
    if camConfigRaport[i][3] <= error:
        good_img += 1
        print(fname)
        cv.imwrite('camera_correction_photos/second_run/'+fname, img)
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)  # Konwersja BGR na skalę szarości

        ret, corners = cv.findChessboardCorners(gray, dim, None)  # Wyszukanie wzoru szachownicy na zdjęciu

        if ret == True:
            objpoints.append(objp)
            corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)  # Funkcja zwiększająca dokładność współrzędnych wykrytych narożników
            imgpoints.append(corners)

ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

for rv, tv, fname, objpnt, imgpnt in zip(rvecs, tvecs, images, objpoints, imgpoints):
    imgpoints2, _ = cv.projectPoints(objpnt, rv, tv, mtx_old, dist_old)
    error = cv.norm(imgpnt, imgpoints2, cv.NORM_L2) / len(imgpoints2)
    mean_error += error

mean_error = mean_error / len(objpoints)
print("Odrzucono %d zdjęć z %d" % (len(images)-good_img, len(images)))
print("Nowy średni błąd reprojekcji: ", mean_error)


print("\nPierwotna macierz parametrów wewnętrznych:\n", mtx_old)
print('Nowa macierz parametrów wewnętrznych:\n', mtx)

print("\nPierwotny wektor zniekształceń:\n", dist_old)
print("Nowy wektor zniekształceń:\n", dist)

# Odczytanie pliku konfiguracyjnego
with open('config.json') as config_file:
    config = json.load(config_file)

# Przypisanie wyznaczonych wartości do zmiennych w pliku konfiguracyjnym
config['cam_calibration']['mtx'] = mtx.tolist()
config['cam_calibration']['dist'] = dist.tolist()

# Zapisanie powyższych wartości do pliku konfiguracyjnego
with open('config.json', 'w') as config_file:
    json.dump(config, config_file, sort_keys=True, indent=4)

# Usunięcie zniekształceń z obrazów kalibracyjnych
images = glob.glob('camera_correction_photos/*.png')

for fname in images:
    img = cv.imread(fname)
    if '/' in fname:
        fname = fname.split('/')
        fname = fname[1]
    if '\\' in fname:
        fname = fname.split('\\')
        fname = fname[1]
    dst = cv.undistort(img, mtx, dist)
    cv.imwrite('camera_correction_photos/undistored_images/' + fname, dst)
    
