# gpu_hash_join
Implementing hash join on GPUs

# Setting up your environment
```
./setup.sh
```
Or follow the steps manally if some step gives error

# How to run

source gpu_hash_join/bin/activate
Activate conda environment
```
conda activate ./env
or
conda activate /home/hice1/smittal98/gpu_hash_join/env
```

Test joins
```
python3 src/tester_functional.py
```

Just test triton matrix multiplication
```
python3 src/triton_matmul.py
```

# References:

1. https://triton-lang.org/main/getting-started/tutorials/03-matrix-multiplication.html