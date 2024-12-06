#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 15:31:46 2024

@author: zalavi
"""

# =============================================================================
# import sys
# import pandas as pd
# 
# def main(out_sc_file, esm_ll_file, output_file):
#     # Read the out.sc file
#     out_sc = pd.read_csv(out_sc_file, delim_whitespace=True)
#     # Read the esm_loglikelihoods.txt file
#     esm_ll = pd.read_csv(esm_ll_file, sep='\t')
#     # Merge the dataframes on the sequence identifier
#     merged = pd.merge(out_sc, esm_ll, left_on='description', right_on='Sequence_ID')
#     # Write the merged dataframe to the output file
#     merged.to_csv(output_file, sep='\t', index=False)
# 
# if __name__ == "__main__":
#     out_sc_file = sys.argv[1]
#     esm_ll_file = sys.argv[2]
#     output_file = sys.argv[3]
#     main(out_sc_file, esm_ll_file, output_file)
# 
# =============================================================================




import sys
import pandas as pd

def main(out_sc_file, esm_ll_file, output_file):
    # Read the out.sc file
    out_sc = pd.read_csv(out_sc_file, delim_whitespace=True)
    # Read the esm_loglikelihoods.txt file
    esm_ll = pd.read_csv(esm_ll_file, sep='\t')

    # Filter out rows with "_pdb_B" in the Sequence_ID
    esm_ll = esm_ll[~esm_ll['Sequence_ID'].str.contains('.pdb_B')]

    # Remove the "_pdb_A" suffix from the Sequence_ID to match the format in out.sc
    esm_ll['Sequence_ID'] = esm_ll['Sequence_ID'].str.replace('.pdb_A', '')

    # Merge the dataframes on the sequence identifier
    merged = pd.merge(out_sc, esm_ll, left_on='description', right_on='Sequence_ID')

    # Write the merged dataframe to the output file
    merged.to_csv(output_file, sep='\t', index=False)

if __name__ == "__main__":
    out_sc_file = sys.argv[1]
    esm_ll_file = sys.argv[2]
    output_file = sys.argv[3]
    main(out_sc_file, esm_ll_file, output_file)

