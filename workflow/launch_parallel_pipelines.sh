#!/bin/bash

# Total number of GPUs
NUM_GPUS=4

# Total number of binders
TOTAL_BINDERS=2800

# Binders per GPU
BINDERS_PER_GPU=$((TOTAL_BINDERS / NUM_GPUS))  # 250

# Loop over each GPU and launch a pipeline instance
for GPU_ID in $(seq 0 $((NUM_GPUS - 1))); do
    START_INDEX=$((GPU_ID * BINDERS_PER_GPU + 1))
    END_INDEX=$(( (GPU_ID + 1) * BINDERS_PER_GPU ))
    
    echo "Launching pipeline for GPU $GPU_ID: Binders $START_INDEX to $END_INDEX"
    
    # Run the pipeline in the background
    bash pipeline.sh $GPU_ID $START_INDEX $END_INDEX &
    
    # Optional: Limit the number of concurrent jobs
    sleep 1  # Small delay to prevent overwhelming the system
done

# Wait for all background jobs to finish
wait

echo "All pipeline instances have completed."
