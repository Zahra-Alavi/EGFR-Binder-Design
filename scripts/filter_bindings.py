#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 16:09:12 2024

@author: zalavi
"""

import sys
import pandas as pd

def main(input_file, output_file, pae_threshold=10, iptm_threshold=0.5, ll_threshold=-4):
    # Read the merged scores file
    df = pd.read_csv(input_file, sep='\t')

    # Apply the filtering criteria
    filtered_df = df[
        (df['pae_interaction'] < pae_threshold) &
        (df['iptm_score'] > iptm_threshold) &
        (df['Avg_Log_Likelihood'] > ll_threshold)
    ]

    # Write the filtered results to the output file
    filtered_df.to_csv(output_file, sep='\t', index=False)

if __name__ == "__main__":
    input_file = sys.argv[1]  # merged_scores.txt
    output_file = sys.argv[2]  # filtered_bindings.txt
    pae_threshold = float(sys.argv[3]) if len(sys.argv) > 3 else 10
    iptm_threshold = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5
    ll_threshold = float(sys.argv[5]) if len(sys.argv) > 5 else -4
    main(input_file, output_file, pae_threshold, iptm_threshold, ll_threshold)
