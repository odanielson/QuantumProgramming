
; Groover's algorithm with 3 qubits, reusing the auxillary qubits e_i.

register q0[0]
register q1[1]
register q2[2]
register e1[3]
register e2[4]
register e3[5]

include qclib/toffoli.qc

macro XXX a b c
    X a
    X b
    X c

macro HH a b
    H a
    H b

macro HHH a b c
    HH a b
    H c

macro or a b t1
    CNOT a t1
    CNOT b t1
    toffoli a b t1

macro CCZ a b c
    H c
    toffoli a b c
    H c

macro CZ a b
    H b
    CNOT a b
    H b

macro oracle a b c
    ; Just CCZ marks 111, flip (and restore) b to mark 101 instead
    ;msg state before_oracle left 3
    X b
    CCZ a b c
    X b

macro mean_inv a b c t1 t2 t3
    or a b t1
    or t1 c t2
    ; by now t2 is (a OR b OR c)
    CZ t2 c
    CZ t2 b
    CZ t2 a
    ; if an even number of CZs were applied negations cancelled,
    ; correct that by first making t3 = true if cancellation occured
    toffoli c t2 t3
    toffoli b t2 t3
    toffoli a t2 t3
    X t3
    ; then apply Z once more to apply the correction (unless a=b=c=0 in input)
    CZ t2 t3
    ; uncompute temporary qubits
    X t3
    toffoli a t2 t3
    toffoli b t2 t3
    toffoli c t2 t3
    or t1 c t2
    or a b t1

macro grover a b c t1 t2 t3
    oracle a b c
    HHH a b c
    mean_inv a b c t1 t2 t3
    HHH a b c
    msg state after_grover left 3
    msg state after_grover_tmp right 3


HHH q0 q1 q2

; For 3 qubits, running two Grover iterations is the (first) maximum
; for the probability of measuring the marked element.
grover q0 q1 q2 e1 e2 e3
grover q0 q1 q2 e1 e2 e3

msg state byend left 3
