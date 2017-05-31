
register q0[0]  ; Quantum register 0
register q1[1]
register q2[2,3]

; Macro to say hello
macro hello a
    X a
    loop 5
        H a

hello q0
hello q1


X q2
