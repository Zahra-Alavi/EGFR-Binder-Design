#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 15:03:01 2024

@author: zalavi
"""

import sys
import torch
import esm

def compute_log_likelihood(sequences):
    model, alphabet = esm.pretrained.esm1b_t33_650M_UR50S()
    batch_converter = alphabet.get_batch_converter()
    model.eval()

    results = []
    for header, seq in sequences:
        batch_labels, batch_strs, batch_tokens = batch_converter([(header, seq)])
        with torch.no_grad():
            token_probs = model(batch_tokens, repr_layers=[], return_contacts=False)["logits"]
            # Compute log-likelihood
            log_probs = torch.nn.functional.log_softmax(token_probs, dim=-1)
            seq_tokens = batch_tokens[0, 1:-1]  # Exclude start and end tokens
            seq_log_probs = log_probs[0, :-1].gather(1, seq_tokens.unsqueeze(1)).squeeze()
            total_log_likelihood = seq_log_probs.sum().item()
            avg_log_likelihood = seq_log_probs.mean().item()
        results.append((header, total_log_likelihood, avg_log_likelihood))
    return results

if __name__ == "__main__":
    fasta_file = sys.argv[1]
    output_file = sys.argv[2]

    # Read sequences from FASTA
    sequences = []
    with open(fasta_file, 'r') as f:
        header = ''
        seq = ''
        for line in f:
            if line.startswith('>'):
                if seq:
                    sequences.append((header, seq))
                    seq = ''
                header = line.strip()[1:]  # Remove '>'
            else:
                seq += line.strip()
        if seq:
            sequences.append((header, seq))

    # Compute log-likelihoods
    results = compute_log_likelihood(sequences)

    # Write results to output file
    with open(output_file, 'w') as f:
        f.write('Sequence_ID\tTotal_Log_Likelihood\tAvg_Log_Likelihood\n')
        for header, total_ll, avg_ll in results:
            f.write(f'{header}\t{total_ll}\t{avg_ll}\n')
