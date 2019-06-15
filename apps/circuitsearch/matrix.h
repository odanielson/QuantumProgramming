#pragma once

#include <complex.h>

typedef float complex cplx;
typedef cplx onebit_op[2][2];
typedef cplx twobit_op[4][4];

// C = A*B as 2x2 matrices.
void multiply2x2(onebit_op A, onebit_op B, onebit_op C);

// C = A*B as 4x4 matrices.
void multiply4x4(twobit_op A, twobit_op B, twobit_op C);

// C = A tensor B where A, B are 2-dim matrices.
void tensor(onebit_op A, onebit_op B, twobit_op C);

void print2x2(onebit_op A);
void print4x4(twobit_op A);
void copy4x4(twobit_op A, twobit_op B);

// Compare element-wise and return false if an element is not close.
int naive_equals(twobit_op A, twobit_op B);

