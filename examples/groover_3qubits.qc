
register q0[0]
register q1[1]
register q2[2]
register e1[3]
register e2[4]
register e3[5]
register e4[6]


macro HH a b
    H a
    H b

macro HHH a b c
    HH a b
    H c

macro rev_CNOT a b
    HH a b
    CNOT b a
    HH a b

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

macro or a b t1
    CNOT a t1
    CNOT b t1
    toffoli a b t1

macro oror a b c t1 t2
    CNOT a t1
    CNOT b t1
    toffoli a b t1

    CNOT c t2
    CNOT t1 t2
    toffoli c t1 t2
    toffoli a b t1
    CNOT b t1
    CNOT a t1

macro CZ a b
    H b
    CNOT a b
    H b

macro rev_CZ a b
    H b
    rev_CNOT a b
    H b

macro oracle a b c
    Z b

;macro mean_inv a b c t1 t2 t3
;    toffoli a b t1
;    toffoli t1 c t2
;    toffoli a b t1
;    CNOT t2 t3
;    toffoli t1 c t2
;    rev_CZ t3 c
;    rev_CZ t3 b
;    rev_CZ t3 a
;    CNOT t2 t3

macro mean_inv a b c t1 t2
    oror a b c t1 t2
    rev_CZ t2 c
    rev_CZ t2 b
    rev_CZ t2 a

macro groover a b c t1 t2
    oracle a b c
    HHH a b c
    mean_inv a b c t1 t2
    HHH a b c


HHH q0 q1 q2

groover q0 q1 q2 e1 e2
groover q0 q1 q2 e1 e3
groover q0 q1 q2 e1 e4
;groover q0 q1 q2 t1 t2 t3
;groover q0 q1 q2 t1 t2 t3
;groover q0 q1 q2 t1 t2 t3
;groover q0 q1 q2 t1 t2 t3
