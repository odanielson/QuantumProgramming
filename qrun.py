
import sys

from qcodecompiler import qcompile
from qsourceparser import parse


def run(filename):
    text = open(filename).read()
    q_code = parse(text)
    gate_array = qcompile(q_code)
    run_gate_array(gate_array)


if __name__ == "__main__":
    try:
        driver = sys.argv[1]
        filename = sys.argv[2]

    except IndexError:
        print("Usage: %s [vector|density] <sourcefile>" % sys.argv[0])
        exit(1)

    if driver == 'vector':
        from drivers.vector.simulator import run_gate_array

    elif driver == 'density':
        from drivers.density.simulator import run_gate_array

    else:
        print("Driver %s not found" % driver)

    run(filename)
