import numpy as np


def transformPos(U, T):
    U = np.insert(U, 2, 1)
    X = T@U

    return X[:2]
