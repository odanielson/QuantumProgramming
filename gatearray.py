"""A gatearray is a list of gates representing a quantum program.

Important notes:

  - qubit index start at 0

"""

from collections import namedtuple


CNOT = namedtuple('CNOT', 'ctrl target')
H = namedtuple('H', 'i')
I = namedtuple('I', 'i')
START = namedtuple('START', 'n')
SWAP = namedtuple('SWAP', 'a b')
X = namedtuple('X', 'i')
T = namedtuple('T', 'i')
Td = namedtuple('Td', 'i')

str_to_gate = {
    'CNOT': CNOT,
    'H': H,
    'I': I,
    'SWAP': SWAP,
    'X': X,
    'T': T,
    'Td': Td
}
