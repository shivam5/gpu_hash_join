#!/bin/bash

# Load the necessary modules
module load cuda gcc/12.3.0

# Define arrays of table sizes
TABLE1_ARRAY=("1M_id10" "1M_id100" "1M_id1k" "1M_id10k" "1M_id100k")
TABLE2_ARRAY=("1k" "10k")

# Create output directories if they don't exist
mkdir -p profiling_output_cuda/outputs
mkdir -p profiling_output_cuda/ncu_metrics

# Compile the CUDA program
/usr/local/cuda-12.4/bin/nvcc baseline/main.cpp baseline/utils.cu -o a.out -lcudart

# Check if compilation was successful
if [ $? -ne 0 ]; then
    echo "Compilation failed!"
    exit 1
fi

# Iterate over all combinations
for TABLE1 in "${TABLE1_ARRAY[@]}"; do
    for TABLE2 in "${TABLE2_ARRAY[@]}"; do
        echo "Processing table${TABLE1} with ${TABLE2}..."
        
        # Run the executable and capture output
        python profiler/ncu_profile.py \
            --bin "./a.out $TABLE1 $TABLE2" \
            --output "profiling_output_cuda/ncu_metrics/${TABLE1}_${TABLE2}" \
            --format both \
            > "profiling_output_cuda/outputs/${TABLE1}_${TABLE2}.txt"

        # python profiler/ncu_profile.py --bin "./a.out $TABLE1 $TABLE2" 2>&1 | tee "profiling_output_cuda/outputs/table${TABLE1}_${TABLE2}.txt"
        
        if [ $? -eq 0 ]; then
            echo "Successfully processed table${TABLE1} with ${TABLE2}"
        else
            echo "Error processing table${TABLE1} with ${TABLE2}"
        fi
        
        echo "----------------------------------------"
    done
done

echo "All combinations completed!"

python baseline/ground_truth.py
python baseline/evaluate.py
