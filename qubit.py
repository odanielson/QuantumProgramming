
import numpy as np


class Qubits(object):

    def __init__(self, n=1, state=None):

        if state is not None:
            assert state.shape == (2**n, 1), "invalid state %s for n=%d" % (state, n)
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

    def measure(self):
        """
        Compute the discrete probability distribution for measuring
        one of the states of the entire quantum computer. Then return
        one random state sampled from the distribution.
        """
        def abs_square(x):
            return np.real(x * np.conjugate(x))

        states = xrange(0, 2**self.n)
        print "states = %r" % states
        coefficients = np.squeeze(np.asarray(self.state))
        print "coefficients = %r" % coefficients
        prob_dist = [abs_square(x) for x in coefficients]
        print "prob_dist = %r" % prob_dist
        return np.random.choice(states, p=prob_dist)

Zero = Qubits(state=np.array([[1.0], [0.0]], dtype=np.complex256))
One = Qubits(state=np.array([[0.0], [1.0]], dtype=np.complex256))
