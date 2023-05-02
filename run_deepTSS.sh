#! /bin/bash

source ~/.bashrc
chmod +x run_deepTSS.sh

# Source the init.sh file to access the data locations
source init.sh

# Activate conda env for DeepTSS
conda activate deeptss

# Find the full path to the python executable within the deeptss environment
PYTHON_PATH=$(which python)

$PYTHON_PATH DeepTSS/main.py -i $BAM_LOC -hg $REF_GENE_LOC -cons $PHYL_LOC -out $CAGE_DIR -dir_name OUT