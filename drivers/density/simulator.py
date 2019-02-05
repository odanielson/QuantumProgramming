
import gatearray
from gates import Hadamard, Identity, X, Y, Z, S, T, Td, CNOT, SWAP
from qubit import Qubits, Zero, One
from measure import measure


gate_array_gate_to_simulator_gate_map = {
    gatearray.H: Hadamard,
    gatearray.X: X,
    gatearray.Y: Y,
    gatearray.Z: Z,
    gatearray.S: S,
    gatearray.T: T,
    gatearray.Td: Td,
    gatearray.CNOT: CNOT,
    gatearray.I: Identity,
    gatearray.SWAP: SWAP
}


def expand_single_gate(gate, i, num_qbits):
    left_bits = i
    right_bits = num_qbits - 1 - i

    return (Identity ** left_bits) * gate * (Identity ** right_bits)


def expand_double_gate(gate, i, j, num_qbits):
    assert i < j, "Operation only implemented for i < j"

    k = j - 1
    left_bits = k
    right_bits = num_qbits - 2 - k

    operator = (Identity ** left_bits) * gate * (Identity ** right_bits)

    # Swap left bit until it is left of right bit before real gate operator
    # and swap it left again after real gate operator
    while k > i:
        swap_operator = expand_double_gate(SWAP, k-1, k, num_qbits)
        operator = swap_operator | operator | swap_operator
        k -= 1

    return operator


def run_gate_array(gate_array, num_measures=1, print_dist=False, print_state=False):
    start = gate_array.pop(0)
    num_qbits = start.n

    qubits = Qubits(num_qbits)

    for gate in gate_array:
        if isinstance(gate, gatearray.MSG):
            print 'state @%s:\n%s' % (gate.label, qubits.state)
            continue

        simulator_gate = gate_array_gate_to_simulator_gate_map[type(gate)]
        if isinstance(gate, gatearray.CNOT):
            expand_double_gate(simulator_gate, gate.ctrl, gate.target,
                               num_qbits) | qubits

        elif isinstance(gate, gatearray.SWAP):
            expand_double_gate(simulator_gate, gate.a, gate.b,
                               num_qbits) | qubits

        else:
            expand_single_gate(simulator_gate, gate.i, num_qbits) | qubits

    if print_dist:
        print "Final distribution:", qubits.distribution()
    if print_state:
        print "Final state:", qubits.state
    for _ in xrange(num_measures):
        measurement = [measure(qubits, i, project=False) for i in xrange(num_qbits)]
        print "Qubit measure:", ", ".join((str(q) for q in measurement))
    return measurement

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
