
import numpy as np


class Gate(object):
    """Gate represent a Quantum gate.

    Supported operations:

        Gate * Gate   => Tensor product between gate and gate
        Gate | qubits => Gate applied on qubits state

    """

    def __init__(self, name, matrix):
        self.name = name
        self.matrix = matrix

    def __mul__(self, b):
        if isinstance(b, int):
            return Gate('Custom', b*self.matrix)

        if isinstance(b, Gate):
            return Gate('Custom', np.kron(self.matrix, b.matrix))

        raise TypeError("Gate * %s not supported" % type(b))

    def __rmul__(self, b):
        return self.__mul__(b)

    def __pow__(self, n):
        if n == 0:
            return 1

        elif n == 1:
            return self

        elif n > 1:
            return self * (self ** (n-1))

        raise AssertionError("Gate ** %d not supported" % n)

    def __or__(self, qubits):
        """Apply gate on `qubits`."""
        qubits.state = np.asarray(self.matrix * qubits.state)

    def __str__(self):
        return self.name


Hadamard = Gate('Hadamard',
                np.matrix([[1.0, 1.0], [1.0, -1.0]],
                          dtype=np.complex256) / np.sqrt(2))
Identity = Gate('Identity',
                np.matrix([[1.0, 0.0], [0.0, 1.0]], dtype=np.complex256))

ToZero = Gate('ZeroProjection',
              np.matrix([[1.0, 0.0], [0.0, 0.0]], dtype=np.complex256))

ToOne = Gate('OneProjection',
             np.matrix([[0.0, 0.0], [0.0, 1.0]], dtype=np.complex256))

X = Gate('X', np.matrix([[0.0, 1.0], [1.0, 0.0]], dtype=np.complex256))

CNOT = Gate('CNOT',
            np.matrix([[1.0, 0.0, 0.0, 0.0],
                       [0.0, 1.0, 0.0, 0.0],
                       [0.0, 0.0, 0.0, 1.0],
                       [0.0, 0.0, 1.0, 0.0]], dtype=np.complex256))
