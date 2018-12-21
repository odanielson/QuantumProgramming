
import itertools
import numpy as np
import warnings


def dagger(m):
    return np.transpose(np.conjugate(m))


def proj(m1, m2):
    return m1 * dagger(m2)


def density_operator(v):
    """Return density operator for a pure state v."""
    return proj(v, v)


def tensor(l):
    """Tensor product of elements in the list l."""

    assert len(l) > 0
    if len(l) == 1:
        return l[0]
    else:
        return np.kron(l[0], tensor(l[1:]))


def rough_complex(x):
    re = np.real(x)
    im = np.imag(x)
    if np.isclose(re, 0) and np.isclose(im, 0):
        return '0'
    elif np.isclose(re, 0):
        return 'i%.2f' % im
    elif np.isclose(im, 0):
        return '%.2f' % re
    else:
        return '%.2f+i%.2f' % (re, im)


def rough_np_array(arr):
    elements = [rough_complex(x) for x in arr]
    return ' '.join(elements)


def basis_states_str(n):
    """Return generator of n-dim basis vectors as strings. E.g. for n=2
    you get ['|00>', '|01>', '|10>', '|11>'] when you iterate."""

    str_vectors = itertools.imap(''.join, itertools.product('01', repeat=n))
    return ('|%s>' % v for v in str_vectors)


def basis_density_states(n):
    """Returns list of density state operator for standard basis states."""
    zero = np.array([[1], [0]])
    one = np.array([[0], [1]])

    basis_vectors = map(tensor, itertools.product([zero, one], repeat=n))
    return [density_operator(bv) for bv in basis_vectors]


def print_density_summary(rho):
    """Given a density matrix rho, present it's mixture with probability
    for each pure state, the pure state itself (probability _wave_) and
    finally probability distribution for (potentially) mixed states."""

    assert len(rho.shape) == 2
    M, N = rho.shape
    assert M == N
    n = int(np.log2(N))

    evalues, evectors = np.linalg.eigh(rho)

    for i, l in enumerate(evalues):
        if np.isclose(l, 0):
            continue
        print 'P=%.3f: %s' % (l, rough_np_array(evectors[:, i]))

    warnings.simplefilter('ignore', np.ComplexWarning)

    str_basis_vectors = basis_states_str(n)

    for bs in basis_density_states(n):
        p = np.trace(rho * bs)
        print 'P(%s) = %.4f' % (next(str_basis_vectors), p)


def partial_trace(rho, n_A, n_B):
    # View N dim Hilbert space as composed of one 2^n_A-dim and one 2^n_B-dim space.
    reshaped = rho.reshape((2**n_A, 2**n_B, 2**n_A, 2**n_B))
    #print 'Reshaped:\n%s' % reshaped

    reduced = np.einsum('jiki->jk', reshaped)
    #print 'Reduced density operator for first qubit:\n%s' % reduced

    return reduced


def print_subsystem_dist(v, n_A, n_B):
    """Given an n-dimensional pure state vector v, print the probability
    distribution for subsystem A. It is assumed v belongs to a vector
    space considered as composed by two subsystem A and B, where A has
    n_A bits and B has n_B bits."""

    n = np.log2(len(v))
    assert n_A + n_B == n
    N = 2**n

    #print 'Sum(v^2) = %0.2f. Squared v:\n%s' % (sum(v**2), v**2)
    rho = density_operator(v)
    rho_A = partial_trace(rho, n_A, n_B)
    print_density_summary(rho_A)


if __name__ == "__main__":
    np.set_printoptions(precision=2)  # Two decimals
    np.set_printoptions(suppress=True)  # Round small numbers to zero

    r = np.sqrt
    N = 2**7
    v = np.ones((N, 1)) / r(N)

    # Skew probabilities a bit to see a difference after partial trace.
    # Hint: 5^2 + 12^2 = 13^2.
    v[0][0] = 5/(r(N/2)*13)
    v[N-1][0] = 12/(r(N/2)*13)

    print_subsystem_dist(v, 4, 3)
