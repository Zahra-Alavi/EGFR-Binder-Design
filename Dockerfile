# Use a base image with Conda pre-installed
FROM continuumio/miniconda3

# Set the working directory in the container
WORKDIR /app

# Copy the repository files into the container
COPY . .

# Create Conda environments
RUN conda env create -f requirements/af2_binder_design.yml && \
    conda env create -f requirements/dl_binder_design.yml && \
    conda env create -f requirements/esmfold.yml && \
    conda env create -f requirements/SE3nv.yml

# Install additional dependencies for BioNeMo
RUN pip install -r requirements/bionemo_requirements.txt

# Activate the environment and set the entrypoint
SHELL ["conda", "run", "-n", "af2_binder_design", "/bin/bash", "-c"]
ENTRYPOINT ["bash"]
