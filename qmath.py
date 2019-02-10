
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


def print_mixture_summary(rho, evalues, evectors):
    """Summarize pure states making up a mixed state rho by printing
    the probability and the state coefficients. The natural eigenstates
    are used; other mixtures of states may yield the same density
    operator rho. Since eigenvalues and eigenvectors are likley needed
    outside this function, the are passed as parameter although the
    are implicit in rho."""

    for i, l in enumerate(evalues):
        if np.isclose(l, 0):
            continue
        print 'P=%.3f: %s' % (l, rough_np_array(evectors[:, i]))


def entropy(ps):
    """Return entropy for a list of probabilities p."""
    def log2(x):
        if np.isclose(x, 0):
            return 0  # Convention in definition of entropy
        else:
            return np.log2(x)

    return sum(map(lambda p: -p*log2(p), ps))


def print_density_summary(rho):
    """Given a density matrix rho, present it's mixture with probability
    for each pure state, the pure state itself (probability _wave_) and
    finally probability distribution for (potentially) mixed states."""

    assert len(rho.shape) == 2
    M, N = rho.shape
    assert M == N
    n = int(np.log2(N))

    evalues, evectors = np.linalg.eigh(rho)

    print_mixture_summary(rho, evalues, evectors)

    print 'Entropy: %.2f' % entropy(evalues)

    warnings.simplefilter('ignore', np.ComplexWarning)

    str_basis_vectors = basis_states_str(n)

    for bs in basis_density_states(n):
        p = np.trace(rho * bs)
        print 'P(%s) = %.4f' % (next(str_basis_vectors), p)


def partial_trace(rho, n_A, n_B, trace_left=False):
    # View N dim Hilbert space as composed of one 2^n_A-dim and one
    # 2^n_B-dim space.
    reshaped = rho.reshape((2**n_A, 2**n_B, 2**n_A, 2**n_B))
    # print 'Reshaped:\n%s' % reshaped

    if trace_left:
        reduced = np.einsum('ijik->jk', reshaped)
    else:
        reduced = np.einsum('jiki->jk', reshaped)
    # print 'Reduced density operator for first qubit:\n%s' % reduced

    return reduced


def print_subsystem_dist(v, n_A, n_B, right=False):
    """Given an n-dimensional pure state vector v, print the probability
    distribution for subsystem A. It is assumed v belongs to a vector
    space considered as composed by two subsystem A and B, where A has
    n_A bits and B has n_B bits.

    If the parameter `right` is true, the probability distribution for
    subsystem B will be printed instead, tracing out subsystem A.
    """

    n = np.log2(len(v))
    assert n_A + n_B == n

    # print 'Sum(v^2) = %0.2f. Squared v:\n%s' % (sum(v**2), v**2)
    rho = density_operator(v)
    rho_S = partial_trace(rho, n_A, n_B, trace_left=right)
    print_density_summary(rho_S)


if __name__ == "__main__":
    np.set_printoptions(precision=2)  # Two decimals
    np.set_printoptions(suppress=True)  # Round small numbers to zero

    r = np.sqrt
    N = 2**7
    v = np.ones((N, 1)) / r(N)

    # Skew probabilities a bit to see a difference after partial trace.
    # Hint: 9^2 + 40^2 = 41^2. 13^2 + 84^2 = 85^2.
    v[0][0] = 9/(r(N/2)*41)
    v[N-1][0] = 40/(r(N/2)*41)

    v[1][0] = 13/(r(N/2)*85)
    v[N-2][0] = 84/(r(N/2)*85)

    print_subsystem_dist(v, 4, 3)
    print_subsystem_dist(v, 4, 3, right=True)
