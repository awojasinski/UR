import numpy as np


def transformPos(U, T):
    U = np.insert(U, 2, 1)
    X = T@U
    #print(X)
    X = X / X[2]
    #print(X)
    return X[:2]
