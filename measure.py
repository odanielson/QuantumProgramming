
import numpy as np

from gates import ToZero, ToOne, Identity


def get_bit(i, k, n):
    """Return value of bit `i` for `n` qubit state `k`."""
    return (k >> (n-1-i)) & 0x1

def measure(qubits, i):
    """Measure qubit `i` in `qubits` and return 0 or 1. Index `i` from 0."""
    assert i < 2**qubits.n, (
        "qubit %d can not be measured in %d-qubit state" % (i, self.n))
    distribution = qubits.distribution()
    p = np.squeeze(np.asarray(distribution, dtype=np.float64))
    index = np.random.choice(np.arange(2**qubits.n), p=p)
    result = get_bit(i, index, qubits.n)
    projection = ToZero if result == 0 else ToOne
    transform = (Identity ** i) * projection * (Identity ** (qubits.n-i-1))
    transform | qubits
    qubits.normalize()

    return result
