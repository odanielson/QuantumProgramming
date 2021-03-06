from textwrap import dedent

from numpy import isclose

from qp.drivers.vector.simulator import run_gate_array
from qp.qrun import run


def test_or():
    table = {
        (0, 0, 0): [1, 0, 0, 0, 0, 0, 0, 0],  # -> 0 0 0
        (0, 1, 0): [0, 0, 0, 1, 0, 0, 0, 0],  # -> 0 1 1
        (1, 0, 0): [0, 0, 0, 0, 0, 1, 0, 0],  # -> 1 0 1
        (1, 1, 0): [0, 0, 0, 0, 0, 0, 0, 1],  # -> 1 1 1
    }

    for setup, facit in table.items():

        setup = tuple(["X q%d" % i if v == 1 else "" for i, v in enumerate(setup)])
        program = dedent(
            """\
            register q0[0]
            register q1[1]
            register q2[2]

            include qclib/classical_logic.qc

            %s
            %s
            %s

            or q0 q1 q2
        """
            % setup
        )

        result = run(program, run_gate_array, return_distribution=True)
        assert isclose(result, facit).all(), "%s failed" % program
