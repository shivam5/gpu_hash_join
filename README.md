# gpu_hash_join
Implementing hash join on GPUs

## Setting up your environment
```
./setup.sh
```
Or follow the steps manually if some step gives error


## How to run
Activate conda environment
```
conda activate ./hash_join_env
```

Run benchmarks (only measure cpu wall clock time) on single table:
```
python src/performance.py --N1 data/table1M_id10 --N2 data/table1k
```

Run benchmarks (only measure cpu wall clock time) on multiple tables:
```
python src/performance.py --N1 data/table1M_id10 data/table1M_id100 --N2 data/table1k
```

Run benchmarks (only measure cpu wall clock time) on all tables (default):
```
python src/performance.py
```


Test joins
```
python src/tester_functional.py
```

Just test triton matrix multiplication
```
python src/triton_matmul.py
```


## Performance benchmarking
1. Download [data](https://gtvault-my.sharepoint.com/:u:/g/personal/smittal98_gatech_edu/EWVMBa56y2BFtU9BZyyiSwoBhx1qsk-VX2WTX9Duk0ne9Q?e=orKvac) and place in this folder.
2. Extract using `tar -xvf data.tar`. A folder named `data` should be created.
3. Run profiler script for triton benchmark:
```
./run_and_profile_triton.sh
```
4. Run profiler script for cuda baseline:
```
./run_and_profile_cuda_baseline.sh
```


## References:

1. https://triton-lang.org/main/getting-started/tutorials/03-matrix-multiplication.html