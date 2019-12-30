import json
import numpy as np


def configRead(filename):
    # Odczytanie pliku konfiguracyjnego
    with open(filename, 'r') as config_file:
        data = config_file.read()

    config = json.loads(data)   # Konwersja pliku, aby był możliwy do edycji i odczytu wartości
    # Sprawdzenie czy plik posiada wszystkie wartości
    if len(config.keys()) < 3:
        print("Plik konfiguracyjny nie zawiera wszystkich potrzebnych wartości")

    # Przypisanie wartości z pliku konfiguracyjnego do zmiennych
    order = np.asarray(config['objects_order'])
    mtx = np.asarray(config['cam_calibration']['mtx'])
    dist = np.asarray(config['cam_calibration']['dist'])
    thresholdValue = config['cam_calibration']['thresholdValue']
    T = np.asarray(config['pos_calibration']['T'])
    distRatio = config['pos_calibration']['distRatio']

    # Sprawdzenie ilości elementów w tablicy z kolejnością obiektów do rozpoznania
    if len(order) == 0:
        print("Brak obiektów w tablicy elementów do rozpoznania")

    return config, order, mtx, dist, T, distRatio, thresholdValue
