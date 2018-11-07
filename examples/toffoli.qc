register x0[0]
register x1[1]
register x2[2]
register y0[3]
register y1[4]
register y2[5]
register z0[6]
register z1[7]
register z2[8]

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

; 0 AND 0 = 0
toffoli x0 x1 x2

; 1 AND 0 = 0
X y0
toffoli y0 y1 y2

; Skip 0 AND 1 combination to reduce number of qubits

; 1 AND 1 = 1
X z0
X z1
toffoli z0 z1 z2

; Hence expected output is 0 0 0 1 0 0 1 1 1
