
from textwrap import dedent

from numpy import isclose

from drivers.vector.simulator import run_gate_array
from qrun import run


def test_hadamard():

    program = dedent("""\
        register q0[0]
        H q0
    """)

    result = run(program, run_gate_array, return_distribution=True)
    assert isclose(result, [0.5, 0.5]).all()


def test_x():

    program = dedent("""\
        register q0[0]
        X q0
    """)

    result = run(program, run_gate_array, return_distribution=True)
    assert isclose(result, [0.0, 1.0]).all()


def test_cnot():

    program = dedent("""\
        register q0[0]
        register q1[1]
        X q0
        CNOT q0 q1
    """)

    result = run(program, run_gate_array, return_distribution=True)
    assert isclose(result, [0.0, 0.0, 0.0, 1.0]).all()
