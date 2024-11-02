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

Test joins
```
python3 src/tester_functional.py
```

Just test triton matrix multiplication
```
python3 src/triton_matmul.py
```


## Performance benchmarking
1. Download [data](https://gtvault-my.sharepoint.com/:u:/g/personal/klee965_gatech_edu/EZvJ8HSacrxKvR8Mq8WU0_4BX8Urv6qKi26pP7YFSykrzw?e=aeTCIL) and place in this folder.
2. Extract using `tar -xvf data.tar`. A folder named `data` should be created.
3. Run `python src/performance.py`

## References:

1. https://triton-lang.org/main/getting-started/tutorials/03-matrix-multiplication.html