
from gates import Hadamard, Identity, X, CNOT
from qubit import Qubits, Zero, One
from measure import measure

def simple_test():

    print "Zero Qubit: 1|0> + 0|1>"
    print Zero.state
    print ""

    print "One Qubit: 0|0> + 1|1>"
    print One.state
    print ""

    print "Hadamard on 1 qubit: H | (1|0> + 0|1>)"
    qubits = Qubits(1)
    (Hadamard) | qubits
    print qubits.state

    print "Non-collapsing peak of probability distribution:"
    print qubits.distribution()
    print ""

    print "Measure first qubit 3 times"
    print measure(qubits, 0), measure(qubits, 0), measure(qubits, 0)
    print ""

    print ""
    print "Hadamard again: H | H | (1|0> + 0|1>)"
    Hadamard | qubits
    print qubits.state
    print ""

    print "Hadamard and Idenity on 2 qubits: H*I | (1|00> + 0|01> + 0|10> + 0|11>)"
    qubits = Qubits(2)
    (Hadamard * Identity) | qubits
    print qubits.state
    print ""

    print "Measure first qubit 3 times"
    print measure(qubits, 0), measure(qubits, 0), measure(qubits, 0)
    print ""

    print "Measure second qubit 3 times"
    print measure(qubits, 1), measure(qubits, 1), measure(qubits, 1)
    print ""

    print "Hadamard and Hadamard on 2 qubits: H*H | (1|00> + 0|01> + 0|10> + 0|11>)"
    qubits = Qubits(2)
    (Hadamard * Hadamard) | qubits
    print ""

    print "Measure first qubit 3 times"
    print measure(qubits, 0), measure(qubits, 0), measure(qubits, 0)
    print ""

    print "Measure second qubit 3 times"
    print measure(qubits, 1), measure(qubits, 1), measure(qubits, 1)
    print ""

    print "CNOT on two qubits |10>, expecting |11>"
    qubits = Qubits(2)
    (X * Identity) | qubits
    CNOT | qubits
    print measure(qubits, 0), measure(qubits, 1)
    print ""


if __name__ == "__main__":

    simple_test()
