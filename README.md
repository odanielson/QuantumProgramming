# QuantumProgramming


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

## Installation

    sudo apt-get install python-numpy


## Usage

    python simulator.py

or

    python qcodeprogram.py
