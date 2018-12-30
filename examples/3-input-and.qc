; This example demonstrates how two toffolis can be chained to
; produce an AND macro with three input bits. One ancillary
; qubit is required.

register x0[0]
register x1[1]
register x2[2]
register a0[3]
register r0[4]

include examples/stdlib.qc

macro AND3 i1 i2 i3 a r  ; ix is input, a ancillary qubit, r result
    toffoli i1 i2 a
    toffoli i3 a r

X x0  ; Comment out any of the three X gates to get 0 instead of 1 in r0
X x1
X x2
AND3 x0 x1 x2 a0 r0

