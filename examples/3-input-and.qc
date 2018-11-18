; This example demonstrates how two toffolis can be chained to
; produce an AND macro with three input bits. One ancillary
; qubit is required.

register x0[0]
register x1[1]
register x2[2]
register a0[3]
register r0[4]

macro toffoli a b c
    H c
    CNOT b c
    Td c
    CNOT a c
    T c
    CNOT b c
    Td c
    CNOT a c
    T b
    T c
    H c
    SWAP b c
    CNOT a c
    T a
    Td c
    CNOT a c
    SWAP b c

macro AND3 i1 i2 i3 a r  ; ix is input, a ancillary qubit, r result
    toffoli i1 i2 a
    toffoli i3 a r

X x0  ; Comment out any of the three X gates to get 0 instead of 1 in r0
X x1
X x2
AND3 x0 x1 x2 a0 r0

