import json
import numpy as np


def configRead(file):
    with open('config.json', 'r') as config_file:
        data = config_file.read()

    config = json.loads(data)
    mode = config['cvision']['type']

    order = np.empty(shape=(0, len(config['cvision']['order'][0])))

    for object in config['cvision']['order']:
        order = np.append(order, [object], axis=0)

    return config, mode, order

