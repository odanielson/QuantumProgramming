register x0[0]
register x1[1]
register x2[2]
register a0[3]


; From "A meet-in-the-middle algorithm for fast synthesis
; of depth-optimal quantum circuits" by Amy, Maslov, Mosca
; and Roetteler 2013.
macro CT c t a
    CNOT c t
    H a
    Sd c
    CNOT t a
    CNOT a c
    T c
    Td a
    CNOT t c
    CNOT t a
    T c
    Td a
    CNOT c a
    H c
    T c
    H c
    CNOT c a
    Td c
    T a
    CNOT t a
    CNOT t c
    T a
    Td c
    CNOT a c
    S c
    CNOT t a
    CNOT c t
    H a

macro CS c t
    T t
    CNOT c t
    T c
    Td t
    CNOT c t

macro fourier a b c ancilla
    H a
    CS b a
    CT c a ancilla
    H b
    CS c b
    H c

X x1
fourier x0 x1 x2 a0
msg state theend left 3

