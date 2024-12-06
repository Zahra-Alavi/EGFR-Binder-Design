#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 09:39:42 2024

@author: zalavi
"""

import os
from Bio.PDB import PDBParser
from Bio.PDB.Polypeptide import PPBuilder
import sys

def extract_fasta_from_pdb(pdb_file):
    parser = PDBParser(QUIET=True)
    structure = parser.get_structure(os.path.basename(pdb_file), pdb_file)
    ppb = PPBuilder()
    fasta_sequences = []
    for model in structure:
        for chain in model:
            polypeptides = ppb.build_peptides(chain)
            for polypeptide in polypeptides:
                sequence = polypeptide.get_sequence()
                if sequence:
                    fasta_sequences.append(f'>{structure.id}_{chain.id}\n{sequence}\n')
    return fasta_sequences

def get_all_fasta_sequences(directory):
    fasta_sequences = []
    expanded_directory = os.path.expanduser(directory)  # Expand the path
    for filename in os.listdir(expanded_directory):
        if filename.endswith('.pdb'):
            pdb_file = os.path.join(expanded_directory, filename)
            fasta_sequences.extend(extract_fasta_from_pdb(pdb_file))
    return fasta_sequences

def write_fasta_to_file(fasta_sequences, output_file):
    with open(output_file, 'w') as f:
        for fasta in fasta_sequences:
            f.write(fasta)

if __name__ == "__main__":
    pdb_directory = sys.argv[1]  # Take the PDB directory from command-line argument
    output_file = sys.argv[2]  # Output text file for all sequences
    fasta_sequences = get_all_fasta_sequences(pdb_directory)
    write_fasta_to_file(fasta_sequences, output_file)
    print(f"FASTA sequences have been written to {output_file}")
    
    
    
    

