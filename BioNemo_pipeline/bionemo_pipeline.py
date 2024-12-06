#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 17:51:53 2024

@author: zalavi
"""



import os
import json
from bionemo.sdk import BioNeMoClient
from bionemo.models import RFDiffusionModel, ProteinMPNNModel, AlphaFoldModel, ESM2Model

def main():
    # Initialize BioNeMo Client
    client = BioNeMoClient(api_key='your-API-key')

    # Define input parameters
    target_pdb_path = 'path/to/target.pdb'  # Upload your target PDB file to BioNeMo Cloud
    binding_sites = {
        'BS1': {
            'contigs': '[A350-450/0 30-130]',
            'hotspot_res': '[A356, A440, A441]'
        },
        'BS2': {
            'contigs': '[A1-200/0 30-130]',
            'hotspot_res': '[A11, A12, A13, A15, A16, A17, A18]'
        }
    }
    linkers = {
        'linker1': 'GGGGS' * 10,
        'linker2': 'AEAAAAKEAAAAKEAAAAKEAAAAKALEAEAAAAKEAAAAKEAAAAKEAAAAKA',
        'linker3': 'EAAAK' * 9
    }
    top_n = 10  # Number of top binders to select

    # Step 1: Generate binders for each binding site
    binders = {}
    for bs_name, bs_params in binding_sites.items():
        binders[bs_name] = generate_binders(client, target_pdb_path, bs_name, bs_params)

    # Step 2: Generate combinations with linkers
    combined_sequences = generate_combinations(binders['BS1'], binders['BS2'], linkers)

    # Step 3: Predict structures of combined sequences
    final_predictions = predict_structures(client, combined_sequences, 'final_predictions')

    # Step 4: Evaluate predictions and select top candidates
    final_top_binders = evaluate_and_select_top(client, final_predictions, top_n)

    # Output final results
    save_final_results(final_top_binders, 'final_top_binders.json')

def generate_binders(client, target_pdb_path, bs_name, bs_params):
    binders = []

    # Define conditions: conditional and unconditional
    for conditional in [True, False]:
        # Step 1: Run RFDiffusion
        rf_backbones = run_rfdiffusion(client, target_pdb_path, bs_params, conditional, bs_name)

        # Step 2: Run ProteinMPNN
        sequences = run_protein_mpnn(client, rf_backbones, bs_name)

        # Step 3: Predict structures with AlphaFold
        predictions = predict_structures(client, sequences, f'{bs_name}_predictions')

        # Step 4: Evaluate and select top N binders
        top_binders = evaluate_and_select_top(client, predictions, top_n=10)

        binders.extend(top_binders)

    return binders

def run_rfdiffusion(client, target_pdb_path, bs_params, conditional, bs_name):
    # Initialize RFDiffusion model
    rf_model = RFDiffusionModel(client)

    # Prepare parameters
    params = {
        'contigs': bs_params['contigs'],
        'hotspot_residues': bs_params['hotspot_res'],
        'target_pdb': target_pdb_path
    }
    if conditional:
        params['ckpt_override_path'] = 'models/Complex_beta_ckpt.pt'

    # Run RFDiffusion job
    job = rf_model.run_inference(params=params)
    job_id = job['job_id']

    # Wait for job completion
    result = client.wait_for_completion(job_id)
    backbones = result['output']['backbone_pdbs']

    return backbones

def run_protein_mpnn(client, backbones, bs_name):
    # Initialize ProteinMPNN model
    mpnn_model = ProteinMPNNModel(client)

    sequences = []
    for backbone_pdb in backbones:
        # Run ProteinMPNN job
        job = mpnn_model.run_inference(input_pdb=backbone_pdb)
        job_id = job['job_id']

        # Wait for job completion
        result = client.wait_for_completion(job_id)
        seq = result['output']['designed_sequence']
        sequences.append(seq)

    return sequences

def predict_structures(client, sequences, output_prefix):
    # Initialize AlphaFold model
    af_model = AlphaFoldModel(client)

    predictions = []
    for idx, sequence in enumerate(sequences):
        # Run AlphaFold job
        job = af_model.run_inference(sequence=sequence)
        job_id = job['job_id']

        # Wait for job completion
        result = client.wait_for_completion(job_id)
        prediction = {
            'sequence_id': f'{output_prefix}_{idx}',
            'sequence': sequence,
            'structure': result['output']['predicted_structure_pdb'],
            'metrics': result['output']['prediction_metrics']
        }
        predictions.append(prediction)

    return predictions

def evaluate_and_select_top(client, predictions, top_n=10):
    # Initialize ESM2 model
    esm_model = ESM2Model(client)

    # Evaluate predictions
    evaluated_predictions = []
    for pred in predictions:
        sequence = pred['sequence']

        # Compute ESM log-likelihood
        job = esm_model.run_inference(sequence=sequence)
        job_id = job['job_id']
        result = client.wait_for_completion(job_id)
        esm_log_likelihood = result['output']['log_likelihood']

        # Extract metrics from AlphaFold prediction
        ipae = pred['metrics']['ipae']
        iptm = pred['metrics']['iptm']

        # Store evaluation metrics
        pred['esm_log_likelihood'] = esm_log_likelihood
        pred['ipae'] = ipae
        pred['iptm'] = iptm
        evaluated_predictions.append(pred)

    # Apply filtering based on metrics
    # Define thresholds or sorting criteria
    # For demonstration, we'll sort based on iptm score
    sorted_predictions = sorted(
        evaluated_predictions,
        key=lambda x: (-x['iptm'], x['ipae'], -x['esm_log_likelihood'])
    )

    # Select top N candidates
    top_predictions = sorted_predictions[:top_n]

    return top_predictions

def generate_combinations(bs1_binders, bs2_binders, linkers):
    combined_sequences = []
    for bs1 in bs1_binders:
        for bs2 in bs2_binders:
            for linker_name, linker_seq in linkers.items():
                combined_seq = bs1['sequence'] + linker_seq + bs2['sequence']
                combined_id = f"{bs1['sequence_id']}_{bs2['sequence_id']}_{linker_name}"
                combined_sequences.append({
                    'sequence_id': combined_id,
                    'sequence': combined_seq
                })
    return combined_sequences

def save_final_results(final_binders, output_file):
    with open(output_file, 'w') as f:
        json.dump(final_binders, f, indent=4)
    print(f"Final top binders saved to {output_file}")

if __name__ == '__main__':
    main()
