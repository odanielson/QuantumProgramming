
from qmath import proj, dagger

import numpy as np


class Qubits(object):

    def __init__(self, n=1, state=None, state_vector=None):

        assert state is None or state_vector is None, (
            "Can not initialize Qubits with both state and state_vector")
        if state is not None:
            assert state.shape == (2**n, 2**n), (
                "invalid state %s for n=%d" % (state, n))
            self.n = n
            self.state = state

        elif state_vector is not None:
            assert state_vector.shape == (2**n, 1), (
                "invalid state %s for n=%d" % (state_vector, n))
            self.n = n
            self.state = proj(state_vector, state_vector)

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

    def normalize(self):
        norm = np.trace(self.state)
        self.state = self.state / norm

    def distribution(self):
        """
        Return the discrete probability distribution for measuring
        one of the states of the entire quantum computer as a list.
        The position of the list indicates the corresponding state.
        """
        return np.diag(self.state).real

    def apply_operator(self, operator):
        self.state = operator * self.state * dagger(operator)


Zero = Qubits(state_vector=np.array([[1.0], [0.0]], dtype=np.complex256))
One = Qubits(state_vector=np.array([[0.0], [1.0]], dtype=np.complex256))


if __name__ == "__main__":
    print Zero.state
    print (One ** 2).state
