from simulator import run_gate_array
from qcodecompiler import qcompile
from qcode import QCode, Sequence, Register, Macro, MacroCall, Operation


if __name__ == "__main__":

    code = QCode()
    code.add_register("q0", Register([0, 1]))
    code.add_register("q1", Register([2]))
    code.add_register("q2", Register([3]))
    code.add_register("q3", Register([4]))

    hello_sequence = Sequence()
    hello_sequence.add(Operation("X", ["a"]))
    hello_sequence.add(Operation("H", ["a"]))

    code.add_macro("hello", Macro(["a"], hello_sequence))
    program_sequence = Sequence()
    program_sequence.add(MacroCall("hello", ["q0"]))
    program_sequence.add(MacroCall("hello", ["q1"]))
    program_sequence.add(Operation("X", ["q2"]))
    program_sequence.add(Operation("H", ["q2"]))
    program_sequence.add(Operation("CNOT", ["q2", "q3"]))
    code.add_program(program_sequence)

    print(repr(code))

    gate_array = qcompile(code)
    print(gate_array)

    run_gate_array(gate_array)

    # Should result in this gate array
    # gate_array = [
    #     Start(2),
    #     X(0),
    #     X(1)
    #     H(0),
    #     H(1)
    #     X(2),
    #     H(2)
    # ]

    # register q0[0, 1]
    # register q1[2]

    # macro hello a
    #     X a
    #     H a

    # hello q0
    # hello q1
