register q0[0]
register q1[1]

macro CZ a b
    H b
    msg state cz_1
    CNOT a b
    msg state cz_2
    H b

X q0
X q1
H q0

msg state before
CZ q0 q1
msg state after
