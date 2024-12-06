EGFR Binder Design Pipeline

🧬 Overview

This repository contains a comprehensive pipeline for designing binders targeting the EGFR protein using advanced tools such as RFdiffusion, ProteinMPNN, AlphaFold2, and ESM2. The workflow includes backbone generation, sequence design, structure prediction, and ranking based on key binding metrics.

🛠️ Features

Backbone Design: Generate backbones using RFdiffusion.
Sequence Design: Optimize sequences for generated backbones with ProteinMPNN.
Structure Prediction: Predict binder-target complexes using AlphaFold2 with customized metrics.
Ranking: Score and rank designs using log-likelihood scores and interaction metrics from ESM2.
⚙️ Setup Instructions

Step 1: Clone the Repository
git clone https://github.com/yourusername/EGFR-Binder-Design.git
cd EGFR-Binder-Design
Step 2: Install Dependencies
Set up the required environments using Conda:

conda env create -f requirements/af2_binder_design.yml
conda env create -f requirements/dl_binder_design.yml
conda env create -f requirements/esmfold.yml
conda env create -f requirements/SE3nv.yml
Step 3 (Optional): Use Docker
To simplify setup, you can use the provided Dockerfile:

docker build -t egfr-binder-design .
docker run --gpus all -v $(pwd):/app -it egfr-binder-design
🚀 Running the Pipeline

Place your input PDB file (e.g., egfr_complete.pdb) in the inputs/ directory.
Launch the pipeline using:
bash workflows/launch_parallel_pipelines.sh
Outputs will be saved in the outputs/ directory.
📋 Project Structure

EGFR-Binder-Design/
├── README.md              # Project documentation
├── LICENSE                # License file (Apache 2.0)
├── workflows/             # Workflow scripts
│   ├── launch_parallel_pipelines.sh
│   └── pipeline.sh
├── requirements/          # Environment definitions
│   ├── af2_binder_design.yml
│   ├── dl_binder_design.yml
│   ├── esmfold.yml
│   └── SE3nv.yml
├── scripts/               # Python and Bash scripts
│   ├── confidence.py
│   ├── esm_likelihood.py
│   ├── extract_seq.py
│   ├── merge_scores.py
│   ├── filter_bindings.py
│   ├── predict2.py
│   └── binder_design.sh
├── inputs/                # Input files (e.g., PDB files)
│   └── egfr_complete.pdb
├── outputs/               # Outputs from the pipeline
│   └── (empty initially)
└── .gitignore             # Specifies files to ignore in version control
📝 Notes on Revised Scripts

predict2.py: Modified from the original AlphaFold2 script to include additional metrics like PAE and TM-scores.
confidence.py: Extended to compute new metrics for improved evaluation.
📖 References

RFdiffusion
ProteinMPNN
AlphaFold2
ESM2
📜 License

This project is licensed under the Apache License 2.0. See the LICENSE file for details.