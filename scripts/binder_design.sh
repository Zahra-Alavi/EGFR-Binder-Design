#!/bin/bash

# Usage: ./binder_design.sh <START_INDEX> <END_INDEX>

START_INDEX=$1
END_INDEX=$2
GPU_ID=$3 

# Specify the output path and input PDB file
OUTPUT_DIR=binder/binder_${START_INDEX}_${END_INDEX}/GPU_${GPU_ID}
INPUT_PDB=input_pdbs/egfr_complete.pdb

# Create the output directory if it doesn't exist
mkdir -p $OUTPUT_DIR

# Run RFdiffusion
python scripts/run_inference.py \
    inference.output_prefix=$OUTPUT_DIR \
    inference.input_pdb=$INPUT_PDB \
    'contigmap.contigs=[A350-450/0 30-130]' \
    'ppi.hotspot_res=[A356, A440, A441]' \
    inference.num_designs=5 \
    denoiser.noise_scale_ca=0 \
    denoiser.noise_scale_frame=0 \
    #inference.ckpt_override_path=models/Complex_beta_ckpt.pt
