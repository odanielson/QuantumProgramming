#include <complex.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

typedef float complex cplx;
typedef cplx onebit_op[2][2];
typedef cplx twobit_op[4][4];

cplx Id[2][2] = {{1,0}, {0,1}};
cplx X[2][2] = {{0,1}, {1,0}};
cplx Y[2][2] = {{0,-I}, {I,0}};
cplx Z[2][2] = {{1,0}, {0,-1}};
cplx S[2][2] = {{1,0}, {0,I}};
cplx T[2][2] = {{1,0}, {0, 0}};
cplx Td[2][2];

const int num_1d_ops = 7;
onebit_op* obops[num_1d_ops] = {&Id, &X, &Y, &Z, &S, &T, &Td};
const char* obops_name[num_1d_ops] = {"Id", "X", "Y", "Z", "S", "T", "Td"};

cplx CNOT[4][4] = {{1,0,0,0}, {0,1,0,0}, {0,0,0,1}, {0,0,1,0}};

cplx CS[4][4] = {{1,0,0,0}, {0,1,0,0}, {0,0,1,0}, {0,0,0,I}};

const int num_pairs = num_1d_ops*num_1d_ops + 1; // Plus 1 for CNOT, don't add CS that is target.
twobit_op pairs[num_pairs];
const char* pairs_name[num_pairs];

// C = A*B as matrices.
void multiply(cplx A[2][2], cplx B[2][2], cplx C[2][2])
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
void scalar_multiply(cplx k, cplx A[2][2], cplx B[2][2])
{
    B[0][0] = k*A[0][0];
    B[0][1] = k*A[0][1];
    B[1][0] = k*A[1][0];
    B[1][1] = k*A[1][1];
}


// C = A tensor B where A, B are 2-dim matrices.
void tensor(cplx A[2][2], cplx B[2][2], cplx C[4][4])
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

void print2x2(cplx A[2][2])
{
    printf("%.2f+%.2f\t%.2f+%.2f\n%.2f+%.2f\t%.2f+%.2f\n",
           crealf(A[0][0]), cimagf(A[0][0]),
           crealf(A[0][1]), cimagf(A[0][1]),
           crealf(A[1][0]), cimagf(A[1][0]),
           crealf(A[1][1]), cimagf(A[1][1]));
}

void print4x4(cplx A[4][4])
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

void copy4x4(cplx A[4][4], cplx B[4][4])
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

int equals(cplx A[4][4], cplx B[4][4])
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


// Create all pairs of one dim operators, then adjoin two bit operators.
void setup_pairs()
{
    int i, j, k;
    char buf[64];

    for (i=0; i<num_1d_ops; i++)
    {
        for (j=0; j<num_1d_ops; j++)
        {
            k = i*num_1d_ops + j;
            tensor(*obops[i], *obops[j], pairs[k]);

            // Save name of pair
            sprintf(buf, "%s %s", obops_name[i], obops_name[j]);
            pairs_name[k] = strdup(buf);
        }
    }

    copy4x4(CNOT, pairs[k+1]);
    pairs_name[k+1] = strdup("CNOT");
}

void init()
{
    T[1][1] = (1+I)/sqrt(2);

    // Create Td
    multiply(T, Z, Td);
    multiply(Td, S, Td);
}

void find(twobit_op target)
{
    int i1, i2, i3, i4;
    twobit_op tmp1, tmp2, tmp3;
    long k=0;

    for (i1=0; i1<num_pairs; i1++)
    {
        for (i2=0; i2<num_pairs; i2++)
        {
            multiply4x4(pairs[i1], pairs[i2], tmp1);
            for (i3=0; i3<num_pairs; i3++)
            {
                multiply4x4(tmp1, pairs[i3], tmp2);
                for (i4=0; i4<num_pairs; i4++)
                {
                    multiply4x4(tmp2, pairs[i4], tmp3);
                    if (equals(target, tmp3))
                    { 
                        printf("%s : %s : %s : %s\n", pairs_name[i1], pairs_name[i2], pairs_name[i3], pairs_name[i4]);
                    }
                    k++;
                }
            }
        }
    }
    printf("stopped search after %ld million loops\n", k/1000000);
}

int main()
{
    init();
    setup_pairs();

    find(CS);
    return 0;
}
