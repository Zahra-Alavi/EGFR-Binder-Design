# EGFR Binder Design Pipeline

## 🧬 Overview

This repository contains a comprehensive pipeline for designing binders targeting the EGFR protein using advanced tools such as RFdiffusion, ProteinMPNN, AlphaFold2, and ESM2. The workflow includes backbone generation, sequence design, structure prediction, and ranking based on key binding metrics.

## 🛠️ Features

- **Backbone Design**: RFdiffusion is used to design backbone structures.
- **Sequence Design**: ProteinMPNN generates sequences optimized for the backbone.
- **Structure Prediction**: AlphaFold2 predicts the 3D structure of the binder-target complex.
- **Ranking**: ESM2 evaluates binders based on log-likelihood and interaction scores.
  
## ⚙️ Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/EGFR-Binder-Design.git
   cd EGFR-Binder-Design
   
2. Install dependencies via Conda:

   ```bash
    conda env create -f requirements/af2_binder_design.yml
    conda env create -f requirements/dl_binder_design.yml
    conda env create -f requirements/esmfold.yml
    conda env create -f requirements/SE3nv.yml

## 🚀 Running the Pipeline

1. Place your input PDB file (e.g., egfr_complete.pdb) in the inputs/ directory.
2. Launch the pipeline using:
   ```bash workflows/launch_parallel_pipelines.sh

3. Outputs will be saved in the outputs/ directory.

## 📝 Notes on Revised Scripts

The following scripts have been modified from the original repositories:
- `predict2.py`: Modified to include additional metrics (PAE, TM-scores).
- `confidence.py`: Revised to support the extended metrics.

## 📖 References

- RFdiffusion: [GitHub Repository](https://github.com/google-deepmind/alphafold/tree/main)
- AlphaFold2: [DeepMind Repository](https://github.com/google-deepmind/alphafold)
- ProteinMPNN: [dl_binder_design Repository](https://github.com/nrbennet/dl_binder_design)

## 📜 License

This project is licensed under the Apache License 2.0. See the LICENSE file for details.
