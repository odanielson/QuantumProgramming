
from gates import Hadamard, Identity
from qubit import Qubits


def simple_test():

    print "Hadamard on 1 qubit: H | (1|0> + 0|1>)"
    qubits = Qubits(1)
    (Hadamard) | qubits
    print qubits.state
    print ""

    print "Hadamard and Idenity on 2 qubits: H*I | (1|00> + 0|01> + 0|10> + 0|11>)"
    qubits = Qubits(2)
    (Hadamard * Identity) | qubits
    print qubits.state
    print ""


if __name__ == "__main__":

    simple_test()
