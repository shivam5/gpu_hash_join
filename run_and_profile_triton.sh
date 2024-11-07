#!/bin/bash

mkdir -p profiling_output/ncu_metrics
mkdir -p profiling_output/outputs

# Define arrays of tables
TABLE1_ARRAY=("table1M_id10" "table1M_id100" "table1M_id1k" "table1M_id10k" "table1M_id100k")
TABLE2_ARRAY=("table1k")

# Iterate over all combinations
for TABLE1 in "${TABLE1_ARRAY[@]}"; do
    for TABLE2 in "${TABLE2_ARRAY[@]}"; do
        echo "Processing ${TABLE1} with ${TABLE2}..."

        # Export variables
        export TABLE1
        export TABLE2

        # Run benchmark with both outputs
        python profiler/ncu_profile.py \
            --bin "python src/performance.py --N1 data/$TABLE1 --N2 data/$TABLE2" \
            --output "profiling_output/ncu_metrics/${TABLE1}_${TABLE2}" \
            --format both \
            > "profiling_output/outputs/${TABLE1}_${TABLE2}.txt"

        echo "Completed ${TABLE1} with ${TABLE2}"
        echo "----------------------------------------"
    done
done

echo "All profiling completed!"