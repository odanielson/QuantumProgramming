import itertools
import numpy as np
from gates import Identity, Hadamard, X, Y, Z, S, T, Td, CNOT


CT = np.matrix([[1.0, 0.0, 0.0, 0.0],
                [0.0, 1.0, 0.0, 0.0],
                [0.0, 0.0, 1.0, 0.0],
                [0.0, 0.0, 0.0, np.exp(1j*np.pi/4)]], dtype=np.complex64)

CS = np.matrix([[1.0, 0.0, 0.0, 0.0],
                [0.0, 1.0, 0.0, 0.0],
                [0.0, 0.0, 1.0, 0.0],
                [0.0, 0.0, 0.0, 1.0j]], dtype=np.complex64)

CZ = np.matrix([[1.0, 0.0, 0.0, 0.0],
                [0.0, 1.0, 0.0, 0.0],
                [0.0, 0.0, 1.0, 0.0],
                [0.0, 0.0, 0.0, -1.0]], dtype=np.complex64)


one_dim_gates = [Identity, Hadamard, X, Y, Z, S, T, Td]

# Form all pair of matrices that we will then combine to find the
# matrix we are looking for. CNOT is already a 2-qbit matrix so
# adjoin it after.
pairs = [np.kron(x.matrix, y.matrix) for (x, y) in itertools.product(one_dim_gates, one_dim_gates)]
pairs.append(CNOT.matrix)
pairs.append(CS)
pairs.append(CZ)

pairs_name = ["%s %s" % (x.name, y.name) for (x, y) in itertools.product(one_dim_gates, one_dim_gates)]
pairs_name.append('CNOT')
pairs_name.append('CS')
pairs_name.append('CZ')

def product(l):
    """Product of elements in the list l."""
    assert len(l) > 0
    if len(l) == 1:
        return l[0]
    else:
        return l[0] * product(l[1:])


def equals(x, y):
    return np.allclose(x, y, rtol=0.001, atol=0.001)


def display(pair):
    for i, p in enumerate(pairs):
        if equals(p, pair):
            return pairs_name[i]
            break


def num_comb(pairs, n):
    return len(pairs)**n

def find(pairs, x, n):
    # Generator for all n-tuples of 2-bit matrix operators
    tuples = itertools.product(*[pairs for _ in range(n)])

    k = 0
    for i in tuples:
        if equals(product(i), x):
            print map(display, i)
        if k % 1000000 == 0:
            print 'Searched %d products (%f%%)' % (k, float(k)/num_comb(pairs, n))
        k += 1
    print 'Finished after searching %d million combinations.' % (k/1000000)


print num_comb(pairs, 4)

find(pairs, CS, 4)

