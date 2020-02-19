import numpy as np

from qp.drivers.vector.simulator import expand_double_gate, expand_single_gate
from qp.gates import CNOT, X
from qp.drivers.vector.qubit import Qubits


def test_expand_double_gate():
    """Verify double gate operation on non adjacent qubits where first
    qubit is less than second qubit."""
    for n_qubits in range(3, 8):
        for left in range(0, n_qubits):
            for right in range(left + 1, n_qubits):
                # Initialize qubits with left in state |1>
                qubits = Qubits(n_qubits)
                expand_single_gate(X, left, n_qubits) | qubits

                # run CNOT left right
                expand_double_gate(CNOT, left, right, n_qubits) | qubits

                # Get expected state index from the binary representation
                # where the left and right bit is 1.
                bits = [0] * n_qubits
                bits[left] = 1
                bits[right] = 1
                state_index = sum(
                    [2 ** i for i, b in enumerate(reversed(bits)) if (b == 1)]
                )
                assert np.isclose(qubits.distribution()[state_index], 1.0)
