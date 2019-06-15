#include <complex.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

#include "matrix.h"

onebit_op Id = {{1,0}, {0,1}};
onebit_op X = {{0,1}, {1,0}};
onebit_op Y = {{0,-I}, {I,0}};
onebit_op Z = {{1,0}, {0,-1}};
onebit_op H = {{1,1}, {1,-1}};
onebit_op S = {{1,0}, {0,I}};
onebit_op T = {{1,0}, {0, 0}};
onebit_op Td;

const int num_1d_ops = 8;
onebit_op* obops[num_1d_ops] = {&Id, &X, &Y, &Z, &H, &S, &T, &Td};
const char* obops_name[num_1d_ops] = {"Id", "X", "Y", "Z", "H", "S", "T", "Td"};

twobit_op CNOT = {{1,0,0,0}, {0,1,0,0}, {0,0,0,1}, {0,0,1,0}};

twobit_op CS = {{1,0,0,0}, {0,1,0,0}, {0,0,1,0}, {0,0,0,I}};

const int num_pairs = num_1d_ops*num_1d_ops + 1; // Plus 1 for CNOT, don't add CS that is target.
twobit_op pairs[num_pairs];
const char* pairs_name[num_pairs];


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
    int i, j;

    T[1][1] = (1+I)/sqrt(2);

    for (i=0; i<2; i++)
        for (j=0; j<2; j++)
            H[i][j] /= sqrt(2);

    // Create Td
    multiply2x2(T, Z, Td);
    multiply2x2(Td, S, Td);
}

void find(twobit_op target)
{
    int i1, i2, i3, i4, i5;
    twobit_op tmp1, tmp2, tmp3, result;
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
                    for (i5=0; i5<num_pairs; i5++)
                    {
                        multiply4x4(tmp2, pairs[i4], result);
                        if (fowler_equals(target, result))
                        {
                            printf("%s : %s : %s : %s : %s\n", pairs_name[i1], pairs_name[i2], pairs_name[i3], pairs_name[i4], pairs_name[i5]);
                        }
                        k++;
                    }
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
