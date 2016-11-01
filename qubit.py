
import numpy as np


class Qubits(object):

    def __init__(self, n=1):

        self.n = n
        self.state = np.zeros(2**n, dtype=np.complex256)
        self.state[0] = 1.0

    def __str__(self):
        return 'Qubits(%d)' % self.n
