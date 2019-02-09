
include qclib/toffoli.qc


macro or a b t1
    CNOT a t1
    CNOT b t1
    toffoli a b t1
