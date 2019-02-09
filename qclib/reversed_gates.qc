

; rev_CNOT implements a CNOT gate where the
; the control qbit `a` have a higher qbit number
; Question: This rather feels like a limitation
; in the driver, maybe we should build a generic
; reversibility there instead?
macro rev_CNOT a b
    H a
    H b
    CNOT b a
    H a
    H b
