

import copy

from qcode import Operation, MacroCall, Message, Sequence
from gatearray import str_to_gate, START, MSG


def get_num_bits(qcode):
    highest_bit = 0
    for reg in qcode.registers.values():
        if max(reg.qbits) > highest_bit:
            highest_bit = max(reg.qbits)
    return highest_bit + 1


def get_start_code(qcode):
    return START(n=get_num_bits(qcode))


def qcompile(qcode):
    gate_array = []
    gate_array.append(get_start_code(qcode))
    gate_array += compile_sequence(qcode, qcode.program)
    return gate_array


def unroll_item(item, call_symbols):
    new_item = copy.deepcopy(item)
    for (i, argument) in enumerate(new_item.arguments):
        if argument in call_symbols:
            new_item.arguments[i] = call_symbols[argument]

    return new_item


def unroll_sequence(sequence, call_symbols):
    new_seq = Sequence()
    for item in sequence.elements:
        new_seq.add(unroll_item(item, call_symbols))

    return new_seq


def get_macro_to_macrocall_arguments_map(macro_args, macrocall_args):
    call_symbols = {}
    for (i, arg) in enumerate(macro_args):
        call_symbols[arg] = macrocall_args[i]
    return call_symbols


def compile_operation(registers, operation):
    gate = str_to_gate[operation.operator]
    gate_array = []

    #  Pre-condition: All registers have the same number of qbits.
    register_width = len(registers[operation.arguments[0]].qbits)

    for i in xrange(register_width):
        indices = [registers[arg].qbits[i] for arg in operation.arguments]
        gate_array.append(gate(*indices))

    return gate_array


def compile_message(registers, msg):
    gate_array = [MSG(msg.arguments[0], msg.arguments[1], msg.arguments[2:])]
    return gate_array


def compile_sequence(qcode, sequence):
    gate_array = []
    for item in sequence.elements:

        if isinstance(item, Operation):
            gate_array += compile_operation(qcode.registers, item)

        elif isinstance(item, MacroCall):
            macro = qcode.macros[item.name]
            call_symbols = get_macro_to_macrocall_arguments_map(
                macro.arguments, item.arguments)
            unrolled = unroll_sequence(macro.sequence, call_symbols)
            gate_array += compile_sequence(qcode, unrolled)

        elif isinstance(item, Message):
            gate_array += compile_message(qcode.registers, item)

    return gate_array
