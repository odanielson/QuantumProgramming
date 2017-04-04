

import copy

from qcode import Operation, MacroCall, Sequence
from gatearray import str_to_gate


def qcompile(qcode):
    # add start code to gate_array
    gate_array = compile_sequence(qcode, qcode.program)
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

def compile_sequence(qcode, sequence):
    gate_array = []
    for item in sequence.elements:

        if isinstance(item, Operation):
            gate = str_to_gate[item.operator]
            indices = [qcode.registers[argument].qbits[0] for
                       argument in item.arguments]
            gate_array.append(gate(*indices))

        elif isinstance(item, MacroCall):
            macro = qcode.macros[item.name]
            call_symbols = get_macro_to_macrocall_arguments_map(macro.arguments, item.arguments)
            unrolled = unroll_sequence(macro.sequence, call_symbols)
            gate_array.append(compile_sequence(qcode, unrolled))

    return gate_array
