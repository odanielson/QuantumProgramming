
import numpy as np


class Qubits(object):

    def __init__(self, n=1, state=None):

        if state is not None:
            assert len(state) == 2**n, "invalid state %s for n=%d" % (s, n)
            self.n = n
            self.state = state

        else:
            self.n = n
            self.state = (Zero ** n).state

    def __mul__(self, b):
        return Qubits(n=self.n + b.n, state=np.kron(self.state, b.state))

    def __pow__(self, n):
        if n == 1:
            return self
        elif n > 1:
            return self * (self ** (n-1))

        raise AssertionError("Qubits ** %d not supported" % n)

    def __str__(self):
        return 'Qubits(%d)' % self.n


Zero = Qubits(state=np.array([1.0, 0.0], dtype=np.complex256))
One = Qubits(state=np.array([0.0, 1.0], dtype=np.complex256))
