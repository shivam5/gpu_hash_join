#!/bin/bash

# Load the necessary modules
module load cuda gcc/12.3.0

# Compile the CUDA program
/usr/local/cuda-12.4/bin/nvcc main.cpp utils.cu -o a.out -lcudart

# Run the executable
./a.out