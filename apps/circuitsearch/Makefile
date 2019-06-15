
all: circuitsearch cuda_search

circuitsearch: main.c matrix.c
	clang -O2 -lm main.c matrix.c -o circuitsearch


cuda_search: cuda_search.cu
	nvcc cuda_search.cu -o cuda_search
