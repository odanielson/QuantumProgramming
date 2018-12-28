; Create GHZ state |000> + |111> which generalizes the Bell state.

register q0[0]
register q1[1]
register q2[2]

H q0
CNOT q0 q1
CNOT q1 q2

msg state all_qubits left 3

; Since the q0 q1 are entangled with q2, this will not be a pure state.
msg state first_two_qubits left 2

msg state right_qubit right 1
