
all: circuitsearch cuda_search

circuitsearch: main.c
	clang -lm main.c -o circuitsearch


cuda_search: cuda_search.cu
	nvcc cuda_search.cu -o cuda_search
