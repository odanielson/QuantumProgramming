
register x0[0]  ; Quantum register 0
register t0[1]
register y0[2]

register x1[3]
register t1[4]
register y1[5]


macro f_constant x f
    ; x=0 => f=1
    ; x=1 => f=1
    X f

macro f_constant_unentangle x f
    ; x=0, f=0 => f=0
    ; x=1, f=0 => f=0
    ; nothing to do, f and x is not entangled

macro f_balanced x f
    ; x=0 => f=0
    ; x=1 => f=1
    CNOT x f

macro f_balanced_unentangle x f
    ; x=0, f=0 => f=0
    ; x=1, f=1 => f=0
    CNOT x f

macro deutsch_pre x y
    H x
    X y
    H y

macro deutsch_post f y
    CNOT f y

macro deutsch_post2 x
    H x


; Recipe for deutsch algorithm
;
; deutsch_pre x y
; function x t   (function compute f(x) in t)
; deutsch_post t0 y0  (compute f(x) xor y)
; function_unentangle x t  (unentangle t)
; deutsch_post2 x   (prepare x for measurement)

; constant example
deutsch_pre x0 y0
f_constant x0 t0
deutsch_post t0 y0
f_constant_unentangle x0 t0
deutsch_post2 x0  ; Constant function should give 0 in x0

; non constant example
deutsch_pre x1 y1
f_balanced x1 t1
deutsch_post t1 y1
f_balanced_unentangle x1 t1
deutsch_post2 x1  ; Non constant function should give 1 in x1
