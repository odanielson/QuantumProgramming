
from gates import ToZero, ToOne, Identity


def get_bit(self, i, k):
    """Return value of bit `i` for state at index `k`."""
    return (index >> i) & 0x1

def measure(qubits, i):
    """Measure qubit `i` in `qubits` and return 0 or 1. Index `i` from 0."""
    assert i < self.n, (
        "qubit %d can not be measured in %d-qubit state" % (i, self.n))
    distribution = qubits.distribution()
    index = np.random.choice(np.arange(2**qubits.n), p=distribution)
    result = get_bit(i, index)
    projection = ToZero if result == 0 else ToOne
    transform = (Identity ** i) * projection * (Identity ** (n-i-1))
    transform | qubits
    qubits.normalize()

    return result
