
import numpy as np

from qubit import Qubits


class Gate(object):
    """Gate represent a Quantum gate.

    Supported operations:

        Gate * Gate   => Tensor product between gate and gate
        Gate | qubits => Gate applied on qubits state

    """

    def __init__(self, name, matrix):
        self.name = name
        self.matrix = matrix

    def __mul__(self, gate):
        assert isinstance(gate, Gate)
        return Gate('Custom', np.kron(self.matrix, gate.matrix))

    def __or__(self, qubits):
        """Apply gate on `qubits`."""
        assert isinstance(qubits, Qubits), (
            "A gate can only be applied on a Qubits object")
        qubits.state = self.matrix * qubits.state

    def __str__(self):
        return self.name


Hadamard = Gate('Hadamard',
                np.matrix([[1.0, 1.0], [1.0, -1.0]],
                          dtype=np.complex256) / np.sqrt(2))
Identity = Gate('Identity',
               np.matrix([[1.0, 0.0], [0.0, 1.0]], dtype=np.complex256))
