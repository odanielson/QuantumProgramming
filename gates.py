
import qmath
import numpy as np


class Gate(object):
    """Gate represent a Quantum gate.

    Supported operations:

        Gate * Gate   => Tensor product between gate and gate
        Gate | qubits => Gate applied on qubits state
        Gate | Gate   => Matrix product between gate and gate
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

    def __or__(self, target):
        """Multiply gates or Apply gate on `qubits`."""
        if isinstance(target, Gate):
            return Gate('Custom', self.matrix * target.matrix)

        # target is qubits
        target.apply_operator(self.matrix)

    def __str__(self):
        return self.name


Hadamard = Gate('Hadamard',
                np.matrix([[1.0, 1.0], [1.0, -1.0]],
                          dtype=np.complex64) / np.sqrt(2))
Identity = Gate('Identity',
                np.matrix([[1.0, 0.0], [0.0, 1.0]], dtype=np.complex64))

ToZero = Gate('ZeroProjection',
              np.matrix([[1.0, 0.0], [0.0, 0.0]], dtype=np.complex64))

ToOne = Gate('OneProjection',
             np.matrix([[0.0, 0.0], [0.0, 1.0]], dtype=np.complex64))

X = Gate('X', np.matrix([[0.0, 1.0], [1.0, 0.0]], dtype=np.complex64))

Y = Gate('Y', np.matrix([[0.0, 0-1j], [0+1j, 0.0]], dtype=np.complex64))

Z = Hadamard | X | Hadamard

S = Gate('S', np.matrix([[1.0, 0.0], [0.0, 0.0+1j]], dtype=np.complex64))

T = Gate('T', np.matrix([[1.0, 0.0], [0.0, (1+1j)/np.sqrt(2)]], dtype=np.complex64))

Td = T | Z | S

CNOT = Gate('CNOT',
            np.matrix([[1.0, 0.0, 0.0, 0.0],
                       [0.0, 1.0, 0.0, 0.0],
                       [0.0, 0.0, 0.0, 1.0],
                       [0.0, 0.0, 1.0, 0.0]], dtype=np.complex64))

# The swap operator swaps 2 qubits.
# The four states should be mapped as 00->00, 01->10, 10->01 and 11->11.
# This is realized by the following operator identity.
SWAP = CNOT | Hadamard**2 | CNOT | Hadamard**2 | CNOT
