
register a[0]
register b[1]

macro swap a b
    CNOT a b
    H a
    H b
    CNOT a b
    H a
    H b
    CNOT a b

X a
swap a b

