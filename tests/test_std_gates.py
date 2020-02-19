from textwrap import dedent

from numpy import isclose

from drivers.vector.simulator import run_gate_array
from qrun import run


def test_hadamard():

    program = dedent(
        """\
        register q0[0]
        H q0
    """
    )

    result = run(program, run_gate_array, return_distribution=True)
    assert isclose(result, [0.5, 0.5]).all()


def test_x():

    program = dedent(
        """\
        register q0[0]
        X q0
    """
    )

    result = run(program, run_gate_array, return_distribution=True)
    assert isclose(result, [0.0, 1.0]).all()


def test_cnot():
    """Verify CNOT with control qbit lower than controlled qbit."""

    program = dedent(
        """\
        register q0[0]
        register q1[1]
        X q0
        CNOT q0 q1
    """
    )

    result = run(program, run_gate_array, return_distribution=True)
    assert isclose(result, [0.0, 0.0, 0.0, 1.0]).all()


def test_superposition_cnot():
    """Verify CNOT with control qbit lower than controlled qbit."""

    program = dedent(
        """\
        register q0[0]
        register q1[1]
        H q0
        CNOT q0 q1
    """
    )

    result = run(program, run_gate_array, return_distribution=True)
    assert isclose(result, [0.5, 0.0, 0.0, 0.5]).all()


def test_ud_cnot():
    """Verify CNOT with control qbit higher than controlled qbit."""
    program = dedent(
        """\
        register q0[0]
        register q1[1]
        register q2[2]
        register q3[3]
        X q2
        CNOT q2 q0
    """
    )

    result = run(program, run_gate_array)
    assert isclose(result, [1.0, 0.0, 1.0, 0.0]).all()


def test_superposition_ud_cnot():
    """Verify superposition CNOT with control qbit higher than controlled qbit."""
    program = dedent(
        """\
        register q0[0]
        register q1[1]
        H q1
        CNOT q1 q0
    """
    )

    result = run(program, run_gate_array, return_distribution=True)
    assert isclose(result, [0.5, 0.0, 0.0, 0.5]).all()


def test_q0q1q2_toffoli():

    table = {
        (0, 0, 0): [1, 0, 0, 0, 0, 0, 0, 0],
        (0, 0, 1): [0, 1, 0, 0, 0, 0, 0, 0],
        (0, 1, 0): [0, 0, 1, 0, 0, 0, 0, 0],
        (0, 1, 1): [0, 0, 0, 1, 0, 0, 0, 0],
        (1, 0, 0): [0, 0, 0, 0, 1, 0, 0, 0],
        (1, 0, 1): [0, 0, 0, 0, 0, 1, 0, 0],
        (1, 1, 0): [0, 0, 0, 0, 0, 0, 0, 1],
        (1, 1, 1): [0, 0, 0, 0, 0, 0, 1, 0],
    }

    for setup, facit in table.iteritems():

        setup = tuple(("X q%d" % i if v == 1 else "" for i, v in enumerate(setup)))
        program = dedent(
            """\
            register q0[0]
            register q1[1]
            register q2[2]

            include qclib/toffoli.qc

            %s
            %s
            %s
            toffoli q0 q1 q2
        """
            % setup
        )

        result = run(program, run_gate_array, return_distribution=True)
        assert isclose(result, facit).all(), "%s failed" % program


def test_q2q1q0_toffoli():

    table = {
        (0, 0, 0): [1, 0, 0, 0, 0, 0, 0, 0],  # 000
        (0, 0, 1): [0, 1, 0, 0, 0, 0, 0, 0],  # 001
        (0, 1, 0): [0, 0, 1, 0, 0, 0, 0, 0],  # 010
        (0, 1, 1): [0, 0, 0, 0, 0, 0, 0, 1],  # 111
        (1, 0, 0): [0, 0, 0, 0, 1, 0, 0, 0],  # 100
        (1, 0, 1): [0, 0, 0, 0, 0, 1, 0, 0],  # 101
        (1, 1, 0): [0, 0, 0, 0, 0, 0, 1, 0],  # 110
        (1, 1, 1): [0, 0, 0, 1, 0, 0, 0, 0],  # 011
    }

    for setup, facit in table.iteritems():

        setup = tuple(("X q%d" % i if v == 1 else "" for i, v in enumerate(setup)))
        program = dedent(
            """\
            register q0[0]
            register q1[1]
            register q2[2]

            include qclib/toffoli.qc

            %s
            %s
            %s
            toffoli q2 q1 q0
        """
            % setup
        )

        result = run(program, run_gate_array, return_distribution=True)
        assert isclose(result, facit, rtol=1e-04).all(), "%s failed" % program


def test_q1q0q2_toffoli():

    table = {
        (0, 0, 0): [1, 0, 0, 0, 0, 0, 0, 0],  # 000
        (0, 0, 1): [0, 1, 0, 0, 0, 0, 0, 0],  # 001
        (0, 1, 0): [0, 0, 1, 0, 0, 0, 0, 0],  # 010
        (0, 1, 1): [0, 0, 0, 1, 0, 0, 0, 0],  # 011
        (1, 0, 0): [0, 0, 0, 0, 1, 0, 0, 0],  # 100
        (1, 0, 1): [0, 0, 0, 0, 0, 1, 0, 0],  # 101
        (1, 1, 0): [0, 0, 0, 0, 0, 0, 0, 1],  # 111
        (1, 1, 1): [0, 0, 0, 0, 0, 0, 1, 0],  # 110
    }

    for setup, facit in table.iteritems():

        setup = tuple(("X q%d" % i if v == 1 else "" for i, v in enumerate(setup)))
        program = dedent(
            """\
            register q0[0]
            register q1[1]
            register q2[2]

            include qclib/toffoli.qc

            %s
            %s
            %s
            toffoli q1 q0 q2
        """
            % setup
        )

        result = run(program, run_gate_array, return_distribution=True)
        assert isclose(result, facit).all(), "%s failed" % program


def test_q1q2q0_toffoli():

    table = {
        (0, 0, 0): [1, 0, 0, 0, 0, 0, 0, 0],  # 000
        (0, 0, 1): [0, 1, 0, 0, 0, 0, 0, 0],  # 001
        (0, 1, 0): [0, 0, 1, 0, 0, 0, 0, 0],  # 010
        (0, 1, 1): [0, 0, 0, 0, 0, 0, 0, 1],  # 111
        (1, 0, 0): [0, 0, 0, 0, 1, 0, 0, 0],  # 100
        (1, 0, 1): [0, 0, 0, 0, 0, 1, 0, 0],  # 101
        (1, 1, 0): [0, 0, 0, 0, 0, 0, 1, 0],  # 110
        (1, 1, 1): [0, 0, 0, 1, 0, 0, 0, 0],  # 011
    }

    for setup, facit in table.iteritems():

        setup = tuple(("X q%d" % i if v == 1 else "" for i, v in enumerate(setup)))
        program = dedent(
            """\
            register q0[0]
            register q1[1]
            register q2[2]

            include qclib/toffoli.qc

            %s
            %s
            %s
            toffoli q1 q2 q0
        """
            % setup
        )

        result = run(program, run_gate_array, return_distribution=True)
        assert isclose(result, facit, rtol=1e-4).all(), "%s failed" % program
