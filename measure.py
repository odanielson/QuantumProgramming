
import numpy as np

from gates import ToZero, ToOne, Identity


def get_bit(i, k, n):
    """Return value of bit `i` for `n` qubit state `k`."""
    return (k >> (n-1-i)) & 0x1


def trim_probabilities(p):
    """Small and negative(!) probabilities will be set to exactly zero."""
    e = np.finfo(dtype=np.complex256).eps  # Smallest number s.t. 1.0+e != 1.0
    return [x if x > 2*e else 0 for x in p]


def measure(qubits, i):
    """Measure qubit `i` in `qubits` and return 0 or 1. Index `i` from 0."""
    assert i < qubits.n, (
        "qubit %d can not be measured in %d-qubit state" % (i, qubits.n))
    distribution = qubits.distribution()
    p = np.squeeze(np.asarray(distribution, dtype=np.float64))
    p = trim_probabilities(p)
    index = np.random.choice(np.arange(2**qubits.n), p=p)
    result = get_bit(i, index, qubits.n)
    projection = ToZero if result == 0 else ToOne
    transform = (Identity ** i) * projection * (Identity ** (qubits.n-i-1))
    transform | qubits
    qubits.normalize()

    return result
