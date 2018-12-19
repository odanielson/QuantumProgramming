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
Y = namedtuple('Y', 'i')
Z = namedtuple('Z', 'i')
S = namedtuple('S', 'i')
T = namedtuple('T', 'i')
Td = namedtuple('Td', 'i')

str_to_gate = {
    'CNOT': CNOT,
    'H': H,
    'I': I,
    'SWAP': SWAP,
    'X': X,
    'Y': Y,
    'Z': Z,
    'S': S,
    'T': T,
    'Td': Td
}

gate_names = str_to_gate.keys()
