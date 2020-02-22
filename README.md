# QuantumProgramming

![unittests](https://github.com/odanielson/QuantumProgramming/workflows/unittests/badge.svg)

## Quantum Stack

    source code - quantum program source code

    @parser - transform source to the qcode internal program representation

    qcode - internal program representation of source containing declarations,
            macros, gates, register concept, measurements, etc

    @compiler - transform internal program representation to a quantum gate
                array

    gate array - sequence of operations on qubits

    @driver - feed the gate array to an implementation of a quantum computer
              (physical or not)

    quantum computer

### Gate Array

The gate array is an ordered list of elements representing operations on the
quantum computer. Each element is a named tuple. The type represent the
operation and the fields which qubit to act on etc.

    [
       START(4),
       X(3),
       H(0),
       H(2),
       CNOT(1,2)
    ]


### Driver

The driver takes a gate array as input, and outputs the values of the
qubits, if measured. Ex:

    (0, N/A, 1)

Available drivers are

| Driver            | Description           |
| ----------------- | --------------------- |
| drivers/vector    | linear algebra driver |
| drivers/density   | density matrix driver |
| drivers/qiskit    | driver to run qc program using qiskit (qiskit.org) which in turn support multiple backends (simulators as well as real qc devices) |

# Installation

    pip3 install ./

# Usage

Run a quantum program in file `examples/hadamard.qc` with

    qrun examples/hadamard.qc

or get more help with

    qrun -h

# Development

Install for development in local env with

    make env

and then use with

    ./env/bin/qrun

Run tests with

    make check
    make test
