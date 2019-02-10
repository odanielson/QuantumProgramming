
import argparse
import numpy as np

from qcodecompiler import qcompile
from qsourceparser import parse


def run(program,
        gate_array_runner,
        num_measures=1,
        print_lines=False,
        print_qcode=False,
        print_dist=False,
        print_state=False,
        return_distribution=False):

    q_code = parse(program, print_lines=print_lines, print_qcode=print_qcode)
    gate_array = qcompile(q_code)
    return gate_array_runner(gate_array,
                             num_measures=num_measures,
                             print_dist=print_dist,
                             print_state=print_state,
                             return_distribution=return_distribution)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--driver', choices=['vector', 'density'],
                        default='vector')
    parser.add_argument('--print-lines', help='display line representation',
                        action='store_true', default=False)
    parser.add_argument('--print-qcode', help='display qcode representation',
                        action='store_true', default=False)
    parser.add_argument('--print-dist', help='display final distribution',
                        action='store_true', default=False)
    parser.add_argument('--print-state', help='display final state',
                        action='store_true', default=False)
    parser.add_argument('-n', '--num-measures', help='measure n times',
                        type=int, default=1)
    parser.add_argument('filename', help='<source file>')
    args = parser.parse_args()

    if args.driver == 'vector':
        from drivers.vector.simulator import run_gate_array

    elif args.driver == 'density':
        from drivers.density.simulator import run_gate_array

    else:
        print("Driver %s not found" % args.driver)

    np.set_printoptions(precision=2)  # Two decimals
    np.set_printoptions(suppress=True)  # Round small numbers to zero

    program = open(args.filename).read()

    run(program,
        run_gate_array,
        num_measures=args.num_measures,
        print_lines=args.print_lines,
        print_qcode=args.print_qcode,
        print_dist=args.print_dist,
        print_state=args.print_state)
