
from collections import namedtuple
import sys

RawLine = namedtuple("RawLine", "linenumber raw")

IndentedLine = namedtuple("IndentedLine", "linenumber raw indentation")

Line = namedtuple("Line", "linenumber raw indentation operator arguments")


def indentation_level(line):
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
    position = line.find(';')
    if position >= 0:
        return line[:position]

    return line


def parse_lines(text):
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


Block = namedtuple("Block", "head body")


def parse_blocks(lines):
    """Returns `[]Block` from `lines`."""
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

    return blocks

# op arg1
# macro hello
#    op arg1
#    loop 3
#        op arg1 arg2
#        loop 7
#             op arg1
# op arg1

# 0 op arg1
# 0 macro hello
# 1 op arg1
# 1 loop 3
# 2 op arg1 arg2
# 2 loop 7
# 3 op arg1
# 0 op arg1


# 0 op arg1
#
# 0 macro hello
# 1 op arg1
# 1 loop 3
# 2 op arg1 arg2
# 2 loop 7
# 3 op arg1
#
# 0 op arg1

# return blocks(section1) ++ blocks(section2) ++ blocks(section3)


# def parse_blocks(lines, indentation=0):

#     head = lines.pop(0)
#     body = []
#     while lines and (head.indentation + 1 == lines[0].indentation):
#         body.append(lines.pop(0))

#     return Block(head, body)


# def parse_macro(head, tail):
#     macro_name = head.arguments[0]
#     macros[macro_name] = []
#     while len(tail) > 0 and head.indentation + 1 = tail[0].indentation:
#         macros[macro_name].append(tail.pop(0))

#     return tail


# def parse_instructions(lines):
#     assert len(lines) > 0, "There must be at least 1 instruction"
#     level = lines[0].indentation

#     while len(lines) > 0:
#         line = lines.pop(0)

#         if line.operator in operators:
#             pass

#         elif line.operator == 'macro':
#             lines = parse_macro(line, lines)

#         else:
#             raise AssertionError("Operator %s on line %d is neither a valid "
#                                  "operator or keyword" % (line.operator,
#                                                           line.linenumber))

def parse(text, verbose=True):
    """Return QCode object from qsource text input."""

    lines = parse_lines(text)
    if verbose:
        print "\nLine representation:\n"
        print "\n".join([str(line) for line in lines])

    blocks = parse_blocks(lines)

    def print_blocks(blocks):
        for block in blocks:
            print "%sBlock: %s" % (" " * block.head.indentation *4, block.head)
            print_blocks(block.body)

    if verbose:
        print "\nBlock representation:\n"
        print_blocks(blocks)

if __name__ == "__main__":

    text = open(sys.argv[1], 'r').read()
    parse(text)
