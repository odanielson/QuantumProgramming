
import sys

from qcodecompiler import qcompile
from qsourceparser import parse
from simulator import run_gate_array


def run(filename):
    text = open(filename).read()
    q_code = parse(text)
    gate_array = qcompile(q_code)
    run_gate_array(gate_array)


if __name__ == "__main__":
    try:
        filename = sys.argv[1]
    except IndexError:
        print("Usage: %s <sourcefile>")
        exit(1)

    run(filename)
