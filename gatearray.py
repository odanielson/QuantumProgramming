from collections import namedtuple

START = namedtuple('START', 'n')
X = namedtuple('X', 'i')
CNOT = namedtuple('CNOT', 'ctrl target')
H = namedtuple('H', 'i')
M = namedtuple('M', 'i')

str_to_gate = {
    'X': X,
    'CNOT': CNOT,
    'H': H,
    'M': M
}
