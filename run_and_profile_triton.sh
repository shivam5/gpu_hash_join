mkdir -p profiling_output/ncu_metrics
mkdir -p profiling_output/outputs
export TABLE1="table1M_id10"
export TABLE2="table1k"
python profiler/ncu_profile.py --bin "python src/performance.py --N1 data/$TABLE1 --N2 data/$TABLE2" --output profiling_output/ncu_metrics/${TABLE1}${TABLE2}.txt > profiling_output/outputs/${TABLE1}${TABLE2}.txt
