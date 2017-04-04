from qcodecompiler import qcompile
from qcode import QCode, Sequence, Register, Macro, MacroCall, Operation


if __name__ == "__main__":

    code = QCode()
    code.add_register('q0', Register([0,1]))
    code.add_register('q1', Register([2]))

    hello_sequence = Sequence()
    hello_sequence.add(Operation('X', ['a']))
    hello_sequence.add(Operation('H', ['a']))


    code.add_macro('hello', Macro(['a'], hello_sequence))
    program_sequence = Sequence()
    program_sequence.add(MacroCall('hello', ['q0']))
    program_sequence.add(MacroCall('hello', ['q1']))
    code.add_program(program_sequence)


    print repr(code)

    gate_array = qcompile(code)
    print gate_array

    # Should result in this gate array
    # gate_array = [
    #     Start(2),
    #     X(0),
    #     X(1)
    #     H(0),
    #     H(1)
    #     X(2),
    #     H(2),
    #     M(0),
    #     M(1)
    # ]

    # register q0[0, 1]
    # register q1[2]

    # macro hello a
    #     X a
    #     H a

    # hello q0
    # hello q1
