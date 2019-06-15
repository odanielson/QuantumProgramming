#include <math.h>
#include <stdio.h>
#include "matrix.h"

// C = A*B as matrices.
void multiply2x2(onebit_op A, onebit_op B, onebit_op C)
{
    cplx c00, c01, c10, c11;
    c00 = A[0][0]*B[0][0] + A[0][1]*B[1][0];
    c01 = A[0][0]*B[0][1] + A[0][1]*B[1][1];
    c10 = A[1][0]*B[0][0] + A[1][1]*B[1][0];
    c11 = A[1][0]*B[0][1] + A[1][1]*B[1][1];

    C[0][0] = c00;
    C[0][1] = c01;
    C[1][0] = c10;
    C[1][1] = c11;
}

// C = A*B as 4x4 matrices.
void multiply4x4(twobit_op A, twobit_op B, twobit_op C)
{
    int i, j, k;
    cplx sum;

    for (i=0; i<4; i++)
    {
        for (j=0; j<4; j++)
        {
            sum = 0;
            for (k=0; k<4; k++)
            {
                sum = sum + A[i][k] * B[k][j];
            }
            C[i][j] = sum;
        }
    }
}

// B = k*A, k scalar, B 2-dim matrix .
void scalar_multiply(cplx k, onebit_op A, onebit_op B)
{
    B[0][0] = k*A[0][0];
    B[0][1] = k*A[0][1];
    B[1][0] = k*A[1][0];
    B[1][1] = k*A[1][1];
}


// C = A tensor B where A, B are 2-dim matrices.
void tensor(onebit_op A, onebit_op B, twobit_op C)
{
    onebit_op tmp;
    scalar_multiply(A[0][0], B, tmp);
    C[0][0] = tmp[0][0];
    C[0][1] = tmp[0][1];
    C[1][0] = tmp[1][0];
    C[1][1] = tmp[1][1];

    scalar_multiply(A[0][1], B, tmp);
    C[0][2] = tmp[0][0];
    C[0][3] = tmp[0][1];
    C[1][2] = tmp[1][0];
    C[1][3] = tmp[1][1];

    scalar_multiply(A[1][0], B, tmp);
    C[2][0] = tmp[0][0];
    C[2][1] = tmp[0][1];
    C[3][0] = tmp[1][0];
    C[3][1] = tmp[1][1];

    scalar_multiply(A[1][1], B, tmp);
    C[2][2] = tmp[0][0];
    C[2][3] = tmp[0][1];
    C[3][2] = tmp[1][0];
    C[3][3] = tmp[1][1];
}

void print2x2(onebit_op A)
{
    printf("%.2f+%.2f\t%.2f+%.2f\n%.2f+%.2f\t%.2f+%.2f\n",
           crealf(A[0][0]), cimagf(A[0][0]),
           crealf(A[0][1]), cimagf(A[0][1]),
           crealf(A[1][0]), cimagf(A[1][0]),
           crealf(A[1][1]), cimagf(A[1][1]));
}

void print4x4(twobit_op A)
{
    int i;
    for (i=0; i<4; i++)
    {
        printf("%.2f+%.2f\t%.2f+%.2f\t%.2f+%.2f\t%.2f+%.2f\n",
               crealf(A[i][0]), cimagf(A[i][0]),
               crealf(A[i][1]), cimagf(A[i][1]),
               crealf(A[i][2]), cimagf(A[i][2]),
               crealf(A[i][3]), cimagf(A[i][3]));
    }
}

void copy4x4(twobit_op A, twobit_op B)
{
    int i, j;
    for (i=0; i<4; i++)
    {
        for (j=0; j<4; j++)
        {
            B[i][j] = A[i][j];
        }
    }
}

float cabsf(cplx x)
{
    return sqrt(crealf(x)*crealf(x) + cimagf(x)*cimagf(x));
}

int naive_equals(twobit_op A, twobit_op B)
{
    int i, j;
    for (i=0; i<4; i++)
    {
        for (j=0; j<4; j++)
        {
            if (cabsf(B[i][j] - A[i][j]) > 0.1)
            {
                return 0;
            }
        }
    }
    return 1;
}

cplx trace(twobit_op A)
{
    int i;

    cplx sum = 0;
    for (i=0; i<4; i++)
    {
        sum += A[i][i];
    }
    return sum;
}

// From Fowler 2018, "Constructing arbitrary Steane code single
// logical qubit fault-tolerant gates". Rather than taking the
// square root as done in the article, just use epsilon^2 in
// comparisons to avoid needless computation.
// NOTE: First argument is conjugate-transposed (hence Ad or A
// dagger).
float fowler_metric_squared(cplx Ad[4][4], cplx B[4][4])
{
    const int m = 4; // Hard-coded for 4x4 matrices.
    twobit_op C;
    multiply4x4(Ad, B, C);
    return (m - cabsf(trace(C))) / m;
}

int fowler_equals(twobit_op A, twobit_op B)
{
    const float epsilon_squared = 0.01; // = 0.1^2
    return fowler_metric_squared(A, B) < epsilon_squared;
}

void conjugate_transpose(twobit_op A)
{
    int i, j;
    for (i=0; i<4; i++)
    {
        for (j=0; j<i; j++)
        {
            cplx tmp;
            tmp = A[i][j];
            A[i][j] = conjf(A[j][i]);
            A[j][i] = conjf(tmp);
        }
    }
}


