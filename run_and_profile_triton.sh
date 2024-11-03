#!/bin/bash

mkdir -p profiling_output/ncu_metrics
mkdir -p profiling_output/outputs

# Export variables
export TABLE1="table1M_id10"
export TABLE2="table1k"

# Run benchmark with both outputs
python profiler/ncu_profile.py \
    --bin "python src/performance.py --N1 data/$TABLE1 --N2 data/$TABLE2" \
    --output "profiling_output/ncu_metrics/${TABLE1}_${TABLE2}" \
    --format both \
    > "profiling_output/outputs/${TABLE1}_${TABLE2}.txt"