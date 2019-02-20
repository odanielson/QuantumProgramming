
; Groover's algorithm with 4 qubits, reusing the auxillary qubits e_i.

register q0[0]
register q1[1]
register q2[2]
register q3[3]
register e1[4]
register e2[5]
register e3[6]
register e4[7]

include qclib/toffoli.qc

macro HHHH a b c d
    H a
    H b
    H c
    H d

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

macro CCCZ a b c d t
    toffoli a b t
    H d
    toffoli c t d
    H d
    toffoli a b t ; uncompute t

macro oracle a b c d t
    ; Just CCCZ marks 1111, flip (and restore) b to mark 1011 instead
    X b
    CCCZ a b c d t
    X b
    msg state after_oracle left 4

macro mean_inv a b c d t1 t2 t3 t4
    or a b t1
    or t1 c t2
    or t2 d t3
    ; by now t3 is (a OR b OR c OR d)
    CZ t3 d
    CZ t3 c
    CZ t3 b
    CZ t3 a
    ; if an even number of CZs were applied negations cancelled,
    ; correct that by first making t4 = true if cancellation occured
    toffoli d t3 t4
    toffoli c t3 t4
    toffoli b t3 t4
    toffoli a t3 t4
    X t4
    ; then apply Z once more to apply the correction (unless a=b=c=d=0 in input)
    CZ t3 t4
    ; uncompute temporary qubits
    X t4
    toffoli a t3 t4
    toffoli b t3 t4
    toffoli c t3 t4
    toffoli d t3 t4
    or t2 d t3
    or t1 c t2
    or a b t1

macro grover a b c d t1 t2 t3 t4
    oracle a b c d t4
    HHHH a b c d
    mean_inv a b c d t1 t2 t3 t4
    HHHH a b c d
    msg state after_grover left 4


HHHH q0 q1 q2 q3

; For 3 qubits, running two Grover iterations is the (first) maximum
; for the probability of measuring the marked element.
grover q0 q1 q2 q3 e1 e2 e3 e4
grover q0 q1 q2 q3 e1 e2 e3 e4
grover q0 q1 q2 q3 e1 e2 e3 e4
