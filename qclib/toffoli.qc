
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
