from qiskit import QuantumCircuit, execute, Aer

from qp import gatearray


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


def distribution_from_counts(counts, n_qubits):
    """Return distribution of all states given `n_qubits` from `counts` from
    a Qiskit result.

    Qiskit returns counts for each detected state in the run shots.
    We first create a state dict with all probabilities set to 0 and then
    iterate over `counts` and compute the probability for each detected state.
    Last we map the state dict into an ordered list of probabilities.

    """
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
            print("No support for MSG in qiskit driver yet.")
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
            f"Final distribution (from { num_measures } shots): ",
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
