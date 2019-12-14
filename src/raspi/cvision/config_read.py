import json
import numpy as np


def configRead(filename):
    with open(filename, 'r') as config_file:
        data = config_file.read()

    config = json.loads(data)

    for object in config['order']:
        order = np.append(order, [object], axis=0)

    return config, order

