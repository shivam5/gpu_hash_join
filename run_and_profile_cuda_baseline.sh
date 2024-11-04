1. `module load cuda gcc/12.3.0`
2. `cd baseline`
3. `nvcc main.cpp utils.cu -o a.out -lcudart`
4. `cd ..`
5. `python profiler/ncu_profile.py --bin ./baseline/a.out`