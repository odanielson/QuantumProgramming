
from collections import namedtuple
import sys
import qcode

RawLine = namedtuple("RawLine", "linenumber raw")

IndentedLine = namedtuple("IndentedLine", "linenumber raw indentation")

Line = namedtuple("Line", "linenumber raw indentation operator arguments")

Block = namedtuple("Block", "head body")


def indentation_level(line):
    """Return indentation level in `line (Line)`."""
    level = 0
    try:
        while line.raw[level] == " ":
            level += 1
    except IndexError:
        print("Invalid line %s on line %d" % (line.raw, line.linenumber))

    assert level % 4 == 0, (
        "Indentation level not a multiple of 4 on line %d" % line.linenumber)
    return level / 4


def no_comments(line):
    """Return `line (str)` stripped from comments."""
    position = line.find(';')
    if position >= 0:
        return line[:position]

    return line


def parse_lines(text):
    """Return `[]Line` from qsource found in `text (str)`."""
    raw_lines = [RawLine(i, no_comments(line)) for i, line in
                 enumerate(text.splitlines())]

    raw_lines = [line for line in raw_lines if
                 line.raw and not line.raw.isspace()]

    indented_lines = [IndentedLine(
        line.linenumber, line.raw, indentation_level(line))
        for line in raw_lines]

    lines = []
    for indented_line in indented_lines:
        instruction = indented_line.raw.strip()
        fields = instruction.split()
        operator = fields[0]
        arguments = fields[1:]
        lines.append(Line(indented_line.linenumber,
                          indented_line.raw,
                          indented_line.indentation,
                          operator,
                          arguments))
    return lines


def parse_blocks(lines):
    """Returns `[]Block` from `lines ([]Line)`."""
    blocks = []
    while len(lines) > 0:
        head = lines.pop(0)

        if len(lines) > 0:
            next_line = lines[0]
            if next_line.indentation == head.indentation:
                blocks.append(Block(head, []))

            elif next_line.indentation > head.indentation:
                blocks.append(Block(head, parse_blocks(lines)))

            elif next_line.indentation < head.indentation:
                blocks.append(Block(head, []))
                return blocks
        else:
             blocks.append(Block(head, []))

    return blocks

def parse_register(source):
    """Parse a string representation of a register and return a tuple
    with its name and register object. E.g. 'q2[2,3]' -> (q2,Register([2,3]))."""
    (name, _, tail) = source.partition('[')
    (elements0, _, _) = tail.partition(']')
    elements1 = elements0.split(':')
    elements = [int(s) for s in elements1]
    return (name, qcode.Register(elements))

def parse_macro(qc, block):
    name = block.head.arguments[0]
    args = block.head.arguments[1:]
    seq = parse_sequence(qc, block.body)
    return (name, args, seq)


def parse_sequence(qc, blocks):
    """Parse a sequence of blocks and store macros and register in
    the `qc` QCode object.
    """
    seq = qcode.Sequence()
    for block in blocks:
        if block.head.operator == 'register':
            (name, reg) = parse_register(block.head.arguments[0])
            qc.add_register(name, reg)
        elif block.head.operator == 'macro':
            (name, args, s) = parse_macro(qc, block)
            qc.add_macro(name, qcode.Macro(args, s))
        elif block.head.operator in ['X', 'Z', 'T', 'Td', 'H', 'CNOT', 'SWAP']:
            op = block.head.operator
            args = block.head.arguments
            seq.add(qcode.Operation(op, args))
        else:  # macro call
            name = block.head.operator
            args = block.head.arguments
            seq.add(qcode.MacroCall(name, args))
    return seq


def parse_qcode(blocks):
    """Returns a qcode.Sequence corresponding to the blocks."""
    qc = qcode.QCode()
    seq = parse_sequence(qc, blocks)
    qc.add_program(seq)
    return qc


def parse(text, verbose=True):
    """Return QCode object from qsource text input."""

    lines = parse_lines(text)
    if verbose:
        print "\nLine representation:\n"
        print "\n".join([str(line) for line in lines])

    blocks = parse_blocks(lines)

    def print_blocks(blocks):
        for block in blocks:
            print "%sBlock: %s" % (" " * block.head.indentation * 4,
                                   block.head)
            print_blocks(block.body)

    if verbose:
        print "\nBlock representation:\n"
        print_blocks(blocks)

    qc = parse_qcode(blocks)

    def print_qcode(qc):
        print repr(qc)

    if verbose:
        print "\nQcode representation\n"
        print_qcode(qc)

    return qc

if __name__ == "__main__":

    text = open(sys.argv[1], 'r').read()
    parse(text)
