import numpy as np


def transformPosition(U, T):
    U = np.insert(U, 2, 1)
    X = T@U
    X = X / X[2]
    return X[:2]
