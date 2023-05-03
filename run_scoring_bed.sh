#! /bin/bash

source ~/.bashrc
chmod +x run_scoring_bed.sh

# Source the init.sh file to access the data locations
source init.sh

conda activate preprocess

# Find the full path to the python executable within the deeptss environment
PYTHON_PATH=$(which python)

$PYTHON_PATH scoring_bed.py -n $CAGE_DIR_NAME -ref $REF_GENE_NAME -user $USERNAME