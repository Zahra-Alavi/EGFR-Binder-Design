#!/bin/bash

# Usage: ./pipeline.sh <GPU_ID> <START_INDEX> <END_INDEX>

# Log file
LOG_FILE="binder1_${GPU_ID}.log"

# Assign GPU
GPU_ID=$1
START_INDEX=$2
END_INDEX=$3
export CUDA_VISIBLE_DEVICES=$GPU_ID

# Initialize time variables
START_TIME=$(date +%s)
BACKBONE_TIME=0
SEQUENCE_TIME=0
PREDICTION_TIME=0
ESM_TIME=0
MERGE_TIME=0
FILTER_TIME=0

# Step 1: Backbone Design
cd RFdiffusion
echo "Running Backbone Design on GPU $GPU_ID..."
BACKBONE_START=$(date +%s)
conda run -n SE3nv bash -c "./binder_design.sh $START_INDEX $END_INDEX $GPU_ID"
BACKBONE_END=$(date +%s)
BACKBONE_TIME=$((BACKBONE_END - BACKBONE_START))
echo "Backbone Design completed in $BACKBONE_TIME seconds."

# Step 2: Convert PDBs to Silent File and Sequence Generation
cd binder1/binder1_${START_INDEX}_${END_INDEX}
echo "Converting PDBs to Silent File and Generating Sequences..."
SEQUENCE_START=$(date +%s)
conda run -n proteinmpnn_binder_design bash -c "~/dl_binder_design/include/silent_tools/silentfrompdbs *.pdb > binder1_${START_INDEX}_${END_INDEX}.silent"
mkdir -p ~/dl_binder_design/binder1_${GPU_ID}  # Unique directory per GPU
cp binder1_${START_INDEX}_${END_INDEX}.silent ~/dl_binder_design/binder1_${GPU_ID}
cd ~/dl_binder_design/binder1_${GPU_ID}
conda run -n proteinmpnn_binder_design bash -c "../mpnn_fr/dl_interface_design.py -silent binder1_${START_INDEX}_${END_INDEX}.silent -outsilent binder1_out_${START_INDEX}_${END_INDEX}.silent"	
SEQUENCE_END=$(date +%s)
SEQUENCE_TIME=$((SEQUENCE_END - SEQUENCE_START))
echo "Sequence Generation completed in $SEQUENCE_TIME seconds."

# Step 3: AF Prediction
echo "Running AlphaFold Prediction on GPU $GPU_ID..."
PREDICTION_START=$(date +%s)
conda run -n af2_binder_design bash -c "../af2_initial_guess/predict2.py -silent binder1_out_${START_INDEX}_${END_INDEX}.silent -outsilent binder1_out_af_${START_INDEX}_${END_INDEX}.silent"
PREDICTION_END=$(date +%s)
PREDICTION_TIME=$((PREDICTION_END - PREDICTION_START))
echo "Prediction completed in $PREDICTION_TIME seconds."

# Step 4: Extract PDB sequences and write to fasta file
conda run -n proteinmpnn_binder_design bash -c "~/dl_binder_design/include/silent_tools/silentextract binder1_out_af_${START_INDEX}_${END_INDEX}.silent"
PDB_DIRECTORY="~/dl_binder_design/binder1_${GPU_ID}" 
OUTPUT_FASTA="all_sequences_${GPU_ID}.txt"  # Unique FASTA file
echo "Extracting sequences from PDB files..."
python ~/dl_binder_design/extract_seq.py "$PDB_DIRECTORY" "$OUTPUT_FASTA"

# Step 5: Compute Log-Likelihood Scores Using ESM
echo "Computing log-likelihood scores with ESM on GPU $GPU_ID..."
ESM_START=$(date +%s)
conda run -n esmfold python ~/dl_binder_design/esm_likelihood.py "$OUTPUT_FASTA" esm_loglikelihoods_${GPU_ID}.txt
ESM_END=$(date +%s)
ESM_TIME=$((ESM_END - ESM_START))
echo "ESM log-likelihood computation completed in $ESM_TIME seconds."

# Step 6: Merge Scores
echo "Merging iPTM scores and ESM log-likelihoods for GPU $GPU_ID..."
MERGE_START=$(date +%s)
python ~/dl_binder_design/merge_scores.py out.sc esm_loglikelihoods_${GPU_ID}.txt merged_scores_${GPU_ID}.txt
MERGE_END=$(date +%s)
MERGE_TIME=$((MERGE_END - MERGE_START))
echo "Merging completed in $MERGE_TIME seconds."

# Step 7: Filter Based on iPTM and Log-Likelihood
echo "Filtering good binders based on iPTM score and ESM log-likelihood for GPU $GPU_ID..."
FILTER_START=$(date +%s)
python ~/dl_binder_design/filter_bindings.py merged_scores_${GPU_ID}.txt filtered_bindings_${GPU_ID}.txt 10 0.5 -4  # Adjust thresholds as needed
FILTER_END=$(date +%s)
FILTER_TIME=$((FILTER_END - FILTER_START))
echo "Filtering completed in $FILTER_TIME seconds."

# Final time summary
END_TIME=$(date +%s)
TOTAL_TIME=$((END_TIME - START_TIME))

echo "==========================" | tee -a $LOG_FILE
echo "Pipeline Runtime Summary for GPU $GPU_ID:" | tee -a $LOG_FILE
echo "Backbone Design Time: $BACKBONE_TIME seconds" | tee -a $LOG_FILE
echo "Sequence Generation Time: $SEQUENCE_TIME seconds" | tee -a $LOG_FILE
echo "Prediction Time: $PREDICTION_TIME seconds" | tee -a $LOG_FILE
echo "ESM Computation Time: $ESM_TIME seconds" | tee -a $LOG_FILE
echo "Merging Time: $MERGE_TIME seconds" | tee -a $LOG_FILE
echo "Filtering Time: $FILTER_TIME seconds" | tee -a $LOG_FILE
echo "Total Runtime: $TOTAL_TIME seconds" | tee -a $LOG_FILE
echo "==========================" | tee -a $LOG_FILE
