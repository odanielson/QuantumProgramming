
macro HH a b
    H a
    H b


; a & b => apply X on c 
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


; Controlled Z: a => apply Z on b
macro CZ a b
    H b
    CNOT a b
    H b


; Doubly controlled Z: a AND b => apply Z on c
macro CCZ a b c
    H c
    toffoli a b c
    H c


; Upside-down CNOT: CNOT with qubit a defined before qubit b
macro udCNOT a b
    HH a b
    CNOT b a
    HH a b


; Upside-down CZ: CZ with qubit a defined before qubit b
macro udCZ a b
    H b
    rev_CNOT a b
    H b


;a --o--o-- a
;    |  |
;b --o--X-- sum
;    |
;0 --X----- carry
macro sum_with_carry a b c
    toffoli a b c
    CNOT a b
