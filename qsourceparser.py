
from collections import namedtuple
import sys

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


if __name__ == "__main__":

    text = open(sys.argv[1], 'r').read()
    parse(text)
