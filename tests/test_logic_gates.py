
from textwrap import dedent

from numpy import isclose

from drivers.vector.simulator import run_gate_array
from qrun import run


def test_or():

    table = {
        (0,0,0): [1,0,0,0,0,0,0,0],  # -> 0 0 0
        (0,1,0): [0,0,0,1,0,0,0,0],  # -> 0 1 1
        (1,0,0): [0,0,0,0,0,1,0,0],  # -> 1 0 1
        (1,1,0): [0,0,0,0,0,0,0,1],  # -> 1 1 1
    }

    for setup, facit in table.iteritems():

        setup = tuple(["X q%d" % i if v==1 else ""
                       for i, v in enumerate(setup)])
        program = dedent("""\
            register q0[0]
            register q1[1]
            register q2[2]

            include qclib/classical_logic.qc

            %s
            %s
            %s

            or q0 q1 q2
        """ % setup)

        result = run(program, run_gate_array, return_distribution=True)
        assert isclose(result, facit).all(), "%s failed" % program


def test_rev_CNOT():

    table = {
        (0,0): [1, 0, 0, 0],  # -> 0 0
        (0,1): [0, 0, 0, 1],  # -> 1 1
        (1,0): [0, 0, 1, 0],  # -> 1 0
        (1,1): [0, 1, 0, 0]   # -> 0 1
    }

    for setup, facit in table.iteritems():

        setup = tuple(["X q%d" % i if v==1 else ""
                       for i, v in enumerate(setup)])
        program = dedent("""\
            register q0[0]
            register q1[1]

            include qclib/reversed_gates.qc

            %s
            %s

            rev_CNOT q1 q0
        """ % setup)

        result = run(program, run_gate_array, return_distribution=True)
        assert isclose(result, facit).all(), "%s failed" % program
