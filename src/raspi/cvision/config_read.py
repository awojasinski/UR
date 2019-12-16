import json
import numpy as np


def configRead(filename):
    with open(filename, 'r') as config_file:
        data = config_file.read()

    config = json.loads(data)
    if len(config.keys()) < 3:
        print("There is missing values in configuration file")

    order = np.asarray(config['objects_order'])
    mtx = np.asarray(config['cam_calibration']['mtx'])
    dist = np.asarray(config['cam_calibration']['dist'])
    T = np.asarray(config_file['poc_calibration']['T'])
    areaRatio = config_file['pos_calibration']['areaRatio']

    if len(order) == 0:
        print("There is no objects in list")

    return config, order, mtx, dist, T, areaRatio

