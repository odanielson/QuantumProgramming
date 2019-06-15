#include <iostream>
#include <math.h>
#include <stdio.h>

#include <thrust/complex.h>

/* Performance

cuda_search 32 1024 indicas 85ms to decompose the gate (1024x32 threads)

*/


#define GPU 1

typedef thrust::complex<float> cplx;
typedef cplx onebit_op[2][2];
typedef cplx twobit_op[4][4];

#define new_cplx(r,i)  
cplx Id[2][2] = {{1,0}, {0,1}};
cplx X[2][2] = {{0,1}, {1,0}};
cplx Y[2][2] = {{0,cplx(0,-1)}, {cplx(0,1),0}};
cplx Z[2][2] = {{1,0}, {0,-1}}; 
cplx S[2][2] = {{1,0}, {0,cplx(0, 1)}}; 
cplx T[2][2] = {{1,0}, {0, 0}}; 
cplx Td[2][2]; 

cplx CNOT[4][4] = {{1,0,0,0}, {0,1,0,0}, {0,0,0,1}, {0,0,1,0}};

cplx CS[4][4] = {{1,0,0,0}, {0,1,0,0}, {0,0,1,0}, {0,0,0,cplx(0, 1)}};

#define num_1d_ops 7
onebit_op* obops[num_1d_ops] = {&Id, &X, &Y, &Z, &S, &T, &Td};
const char* obops_name[num_1d_ops] = {"Id", "X", "Y", "Z", "S", "T", "Td"};

// Plus 1 for CNOT, don't add CS that is target.
// num_1d_ops*num_1d_ops + 1
#define num_pairs 50

twobit_op *pairs;
char* pairs_name[num_pairs];

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


void print_cplx(cplx &v) {
  printf("%.2f+%.2fi\t", v.real(), v.imag());
}

void print2x2(cplx A[2][2])
{
  print_cplx(A[0][0]);
  print_cplx(A[0][1]);
  printf("\n");
  print_cplx(A[1][0]);
  print_cplx(A[1][1]);
  printf("\n\n");
}

// Create all pairs of one dim operators, then adjoin two bit operators.
void setup_pairs()
{
#ifdef GPU
  cudaError_t err = cudaMallocManaged(&pairs, num_pairs * 16 * sizeof(cplx));
  if (err != cudaSuccess) {
    printf("Failed to allocated memory!\n");
    exit(1);
  }
#else
  pairs = (twobit_op*)calloc(num_pairs, sizeof(twobit_op));
#endif
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

void init() {
  T[1][1] = cplx(1, 1) / sqrt(cplx(2,0));

  // Create Td
  multiply(T, Z, Td);
  multiply(Td, S, Td);
}

// C = A*B as 4x4 matrices.
#ifdef GPU
__device__
#endif
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

#ifdef GPU
__device__
#endif
float cabsf(cplx x)
{
  return sqrt(x.real()*x.real() + x.imag() * x.imag());
}

#ifdef GPU
__device__
#endif
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

// GPU function to find gate combination
#ifdef GPU
__global__
#endif
void find(twobit_op *pairs, long n_combinations)
{

    cplx target[4][4] = {{1,0,0,0}, {0,1,0,0}, {0,0,1,0}, {0,0,0,cplx(0, 1)}};

    int i1, i2, i3, i4;
    twobit_op tmp1, tmp2, tmp3;
    long k=0;

    int match = 0;
    int num_pairs_2 = num_pairs * num_pairs;
    int num_pairs_3 = num_pairs_2 * num_pairs;
    long i = 0;

#ifdef GPU
    int index = blockIdx.x * blockDim.x + threadIdx.x;
    int stride = blockDim.x * gridDim.x;
#else
    int index = 0;
    int stride = 1;
#endif
    for (i = index; i < n_combinations; i += stride) {
      i1 = i % num_pairs;
      i2 = (i / num_pairs) % num_pairs;
      i3 = (i / num_pairs_2) % num_pairs;
      i4 = (i / num_pairs_3) % num_pairs;
      
      multiply4x4(pairs[i1], pairs[i2], tmp1);
      multiply4x4(tmp1, pairs[i3], tmp2);
      multiply4x4(tmp2, pairs[i4], tmp3);
      if (equals(target, tmp3))
      	{
      	  match++;
      	  printf("%d : %d : %d : %d\n", i1, i2, i3, i4);
      	}
      k++;
    }
    /* printf("found %d matches in %ld combinations\n", match, k); */
    /* printf("stopped search after %ld million loops\n", k/1000000); */
}



int main(int argc, char *argv[])
{
#ifdef GPU
  printf("running in GPU mode\n");
#else
  printf("running in non GPU mode\n");
#endif

  int blockSize = atoi(argv[1]);
  int numBlocks = atoi(argv[2]);
    
  init();
  
  setup_pairs();

  int n_gates = 4;
  long n_combinations = (long) pow(num_pairs, n_gates);

#ifdef GPU

  printf("using %d blocks with blockSize %d\n", numBlocks, blockSize);
  find<<<numBlocks, blockSize>>>(pairs, n_combinations);
  cudaError_t err = cudaDeviceSynchronize();
  if (err != cudaSuccess) {
    printf("failed to synchronize cuda device\n");
    printf("%s\n", cudaGetErrorString(err));
  }
#else
  find(pairs, n_combinations);
#endif
  
#ifdef GPU
  cudaFree(pairs);
#endif
  
  return 0;
}
