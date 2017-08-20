
register q1[0:7]
register q2[8:15]

macro kalle r
    X r
    H r


macro hello r1 r2
    kalle r1
    H r2
    H q2


# macros can use other macros defined above
macro ada
    X q1 
    kalle q2


X q1
H q1

ada
hello q1 q2

X q1

