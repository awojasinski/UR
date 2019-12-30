import numpy as np
import cv2 as cv
from cvision.colorspaceConversion import rgb2hsv, bgr2hsv


# Słownik zawierający zdefiniowane kolory w przestrzeni barw HSV
colors = {
    'red': np.array([0, 100, 100]),
    'orange': np.array([50, 100, 100]),
    'yellow': np.array([60, 100, 100]),
    'green': np.array([120, 100, 100]),
    'blue': np.array([240, 100, 100]),
    'violet': np.array([260, 100, 100]),
    'pink': np.array([330, 100, 100]),
    'red': np.array([360, 100, 100]),
}

def colorRecognition(image, cnt):
    b, g, r = cv.split(image)   # Wydzielenie kanałów RGB obrazu na osobne zmienne
    mask = np.zeros(b.shape, np.uint8)  # Zdefiniowanie maski o wymiarach obrazu
    cnt = np.array(cnt).reshape((-1, 1, 2)).astype(np.int32)
    cv.drawContours(mask, [cnt], -1, 255, -1)   # Narysowanie konturu na masce
    # Obliczenie średniej wartości każdego kanału przestrzenii barw z nałożoną maską dla konturu
    b = cv.mean(b, mask=mask)
    g = cv.mean(g, mask=mask)
    r = cv.mean(r, mask=mask)

    hsv = bgr2hsv(int(b[0]), int(g[0]), int(r[0]))  # Konwersja przestrzenii barw BGR na HSV
    # Gdy nasycenie barwy jest małe sprawdzenie obrazu pod kątem szarości, bieli i czerni
    if hsv[1] < 10:
        if hsv[2] < 12:
            return 'black'
        elif hsv[2] > 80:
            return 'white'
        else:
            return 'gray'
    else:
        # Zainicjalizowanie tablicy do przechowywania różnicy pomiędzy wartościami barwy z obrazu a wartościami ze słownika
        diff = np.empty(shape=(0, 2), dtype=([('values', np.dtype(int)), ('names', type(colors.keys()))]))
        # Pętla obliczająca różnice
        for name, value in colors.items():
            abs_diff = abs(int(hsv[0]) - int(value[0]))
            diff = np.append(diff, np.array([(abs_diff, name)], dtype=diff.dtype))
        color = np.sort(diff)[0][1]     # Posortowanie tablicy i przypisanie najmniejszej wartości do zwracanej zmiennej
        # Sprawdzenie czy natężenie nie jest zbyt małe
        if hsv[2] < 10:
            return 'black'
        else:
            return color
