# QuantumProgramming


## Quantum Stack

    source code - quantum program source code

    @parser - transform source to the qcode internal program representation

    qcode - internal program representation of source containing declarations,
            macros, gates, register concept, measurements, etc

    @compiler - transform internal program representation to a quantum gate array

    gate array - gates operating on the entire set of qubits in each step

    @driver - feed the gate array to an implementation of a quantum computer (physical or not)

    quantum computer


## Gate Array

The gate array is an ordered list of elements representing operations on the
quantum computer. The first element is an initialization vector for the qubits
(implicitly defining the number of qubits). Then comes gates or measurement
operations.


The gate array is a list of named tuples, the number of qubits used
in the computation. Each tuple representes a tensor product of the elements in
the tuples, with the first element acting on the first qubit, and so on.

    [
       Start(4),
       X(3),
       H(0,2),
       CNOT(1,2),
       M(1),
       M(2)
    ]


## Driver

The driver takes a gate array as input, and outputs the values of the
qubits, if measured. Ex:

    (0, N/A, 1)


## Installation

    sudo apt-get install python-numpy


## Usage

    python simulator.py
