from qiskit import QuantumCircuit, execute, Aer

from qp import gatearray
from qp import qmath


gate_array_gate_to_simulator_gate_map = {
    gatearray.H: QuantumCircuit.h,
    gatearray.X: QuantumCircuit.x,
    gatearray.Y: QuantumCircuit.y,
    gatearray.Z: QuantumCircuit.z,
    gatearray.S: QuantumCircuit.s,
    gatearray.T: QuantumCircuit.t,
    gatearray.Td: QuantumCircuit.tdg,
    gatearray.CNOT: QuantumCircuit.cnot,
    gatearray.I: QuantumCircuit.iden,
    gatearray.SWAP: QuantumCircuit.swap,
}


def handle_msg(label, args, qubits):
    if len(args) > 0 and args[0] == "left":
        print("state @%s:" % (label))
        m = int(args[1])
        qmath.print_subsystem_dist(qubits.state, m, qubits.n - m)
    elif len(args) > 0 and args[0] == "right":
        print("state @%s" % (label))
        m = int(args[1])
        qmath.print_subsystem_dist(qubits.state, qubits.n - m, m, right=True)
    else:
        print("state @%s: %s" % (label, qmath.rough_np_array(qubits.state)))


def distribution_from_counts(counts, n_qubits):
    n_states = n_qubits ** 2
    res = dict((("{0:02b}".format(i), 0) for i in range(n_states)))
    total = sum(counts.values())
    for state, count in counts.items():
        res[state[::-1]] = count / total

    return [res[k] for k in sorted(res.keys())]


def run_gate_array(
    gate_array,
    num_measures=1,
    print_dist=False,
    print_state=False,
    return_distribution=False,
):
    start = gate_array.pop(0)
    num_qbits = start.n

    # T.B.D: Control what backend (including real qc to use)
    simulator = Aer.get_backend("qasm_simulator")
    circuit = QuantumCircuit(num_qbits, num_qbits)

    for gate in gate_array:
        if isinstance(gate, gatearray.MSG):
            handle_msg(gate.label, gate.args, qubits)
            continue

        simulator_gate = gate_array_gate_to_simulator_gate_map[type(gate)]
        if isinstance(gate, gatearray.CNOT):
            simulator_gate(circuit, gate.ctrl, gate.target)

        elif isinstance(gate, gatearray.SWAP):
            simulator_gate(circuit, gate.a, gate.b)

        else:
            simulator_gate(circuit, gate.i)

    # Qiskit relies on explicit measurements. This make a lot of sense and
    # maybe we should add that support in our qc language. But until then
    # we add an explicit measurement of all qubits at the end of the simulation
    circuit.measure(range(num_qbits), range(num_qbits))
    job = execute(circuit, simulator, shots=num_measures)
    result = job.result()

    # Draw the circuit
    print(circuit.draw())

    if print_dist:
        print(
            "Final distribution (from shots): ",
            distribution_from_counts(result.get_counts(), num_qbits),
        )
    if print_state:
        print("Final state: currently not supported in qiskit driver")

    def measurement_from_str(state):
        state = list(state)
        state.reverse()
        return state

    for state, count in result.get_counts().items():
        measurement = measurement_from_str(state)
        measurement_output = ", ".join(measurement)
        print(f"Qubit measure: { measurement_output } ({ count } times)")

    # NOTE: This distribution is taken from the executed shots, it's not exactly
    # the same as the theoretical distribution used in vector and density drivers
    return (
        distribution_from_counts(result.get_counts(), num_qbits)
        if return_distribution
        else measurement
    )
