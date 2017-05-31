
import gatearray
from gates import Hadamard, Identity, X, CNOT
from qubit import Qubits, Zero, One
from measure import measure


gate_array_gate_to_simulator_gate_map = {
    gatearray.H: Hadamard,
    gatearray.X: X,
    gatearray.CNOT: CNOT,
    gatearray.I: Identity
}


def pretty_format_distribution(distribution):
    return ", ".join((str(x[0]) for x in list(distribution)))


def expand_single_gate(gate, i, num_qbits):
    left_bits = i
    right_bits = num_qbits - 1 - i

    return (Identity ** left_bits) * gate * (Identity ** right_bits)


def expand_double_gate(gate, i, j, num_qbits):
    assert j == i + 1, "Operation only implemented for j == i + 1"
    left_bits = i
    right_bits = num_qbits - 2 - i

    return (Identity ** left_bits) * gate * (Identity ** right_bits)


def run_gate_array(gate_array):
    start = gate_array.pop(0)
    num_qbits = start.n

    qubits = Qubits(num_qbits)
    print "Initial state:", pretty_format_distribution(qubits.distribution())

    for gate in gate_array:
        simulator_gate = gate_array_gate_to_simulator_gate_map[type(gate)]
        if isinstance(gate, gatearray.CNOT):
            expand_double_gate(simulator_gate, gate.ctrl, gate.target,
                               num_qbits) | qubits

        else:
            expand_single_gate(simulator_gate, gate.i, num_qbits) | qubits

    print "Final state:", pretty_format_distribution(qubits.distribution())
    print "Qubit measure:", ", ".join(
        [str(measure(qubits, i)) for i in xrange(num_qbits)])


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

    print ("Hadamard and Idenity on 2 qubits: "
           "H*I | (1|00> + 0|01> + 0|10> + 0|11>)")
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

    print ("Hadamard and Hadamard on 2 qubits: "
           "H*H | (1|00> + 0|01> + 0|10> + 0|11>)")
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
