

class Macro:
    def __init__(self, arguments, sequence):
        self.arguments = arguments
        self.sequence = sequence

    def __repr__(self):
        return 'Macro(%s): %s' % (self.arguments, self.sequence)


class Register:
    def __init__(self, qbits):
        self.qbits = qbits

    def __repr__(self):
        return 'Register(%s)' % self.qbits


class Operation:
    """A gate aplied to a register."""
    def __init__(self, operator, arguments):
        self.operator = operator
        self.arguments = arguments

    def __repr__(self):
        return '%s %s' % (self.operator, self.arguments)


class MacroCall:
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments

    def __repr__(self):
        return '%s %s' % (self.name, self.arguments)


class Sequence:
    """
    A sequence of macros or operations on qubits or registers.
    """
    def __init__(self):
        self.elements = []

    def add(self, element):
        self.elements.append(element)

    def __repr__(self):
        return 'Seq(%s)' % repr(self.elements)


class QCode:
    def __init__(self):
        self.macros = {}
        self.registers = {}

    def add_register(self, name, register):
        self.registers[name] = register

    def add_macro(self, name, macro):
        self.macros[name] = macro

    def add_program(self, sequence):
        self.program = sequence

    def __repr__(self):
        return 'Register: %s\nMacros: %s\nProgram: %s' % (repr(self.registers), repr(self.macros), repr(self.program))


if __name__ == "__main__":

    code = QCode()
    code.add_register('q0', Register([0]))
    code.add_register('q1', Register([1]))

    hello_sequence = Sequence()
    hello_sequence.add(Operation('X', ['a']))
    hello_sequence.add(Operation('H', ['a']))

    code.add_macro('hello', Macro(['a'], hello_sequence))
    program_sequence = Sequence()
    program_sequence.add(MacroCall('hello', 'q0'))
    program_sequence.add(MacroCall('hello', 'q1'))
    code.add_program(program_sequence)


    print repr(code)

 
