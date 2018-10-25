
import numpy as np


def dagger(m):
    return np.transpose(np.conjugate(m))


def proj(m1, m2):
    return m1 * dagger(m2)
