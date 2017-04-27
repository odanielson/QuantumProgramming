"""A gatearray is a list of gates representing a quantum program.

Important notes:

  - qubit index start at 0

"""

from collections import namedtuple


START = namedtuple('START', 'n')
X = namedtuple('X', 'i')
CNOT = namedtuple('CNOT', 'ctrl target')
H = namedtuple('H', 'i')
M = namedtuple('M', 'i')
I = namedtuple('I', 'i')


str_to_gate = {
    'X': X,
    'CNOT': CNOT,
    'H': H,
    'M': M
}
