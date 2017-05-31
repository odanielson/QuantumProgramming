

class Macro:
    """A macro with arguments which can be registers or variables and
    a sequence of operations or macro calls.
    """

    def __init__(self, arguments, sequence):
        self.arguments = arguments
        self.sequence = sequence

    def __repr__(self):
        return 'Macro(%s): %s' % (self.arguments, self.sequence)


class Register:
    """A register with one to many qubits."""

    def __init__(self, qbits):
        self.qbits = qbits

    def __repr__(self):
        return 'Register(%s)' % self.qbits


class Operation:
    """A gate applied to arguments which can be registers or variables."""

    def __init__(self, operator, arguments):
        self.operator = operator
        self.arguments = arguments

    def __repr__(self):
        return '%s %s' % (self.operator, self.arguments)


class MacroCall:
    """A macro call with arguments which can be registers or variables."""

    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments

    def __repr__(self):
        return '%s %s' % (self.name, self.arguments)


class Sequence:
    """
    A sequence of macro calls or operations on qubits or registers.
    """
    def __init__(self):
        self.elements = []

    def add(self, element):
        self.elements.append(element)

    def __repr__(self):
        return 'Seq(%s)' % repr(self.elements)


class QCode:
    """Internal program representation."""

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
        return 'Register: %s\nMacros: %s\nProgram: %s' % (
            repr(self.registers), repr(self.macros), repr(self.program))
