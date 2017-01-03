
register inputx[0:3]
register inputy[4:7]
register result[0:12]

H inputx
H inputx
X inputy
CNOT inputx, result
