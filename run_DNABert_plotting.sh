#! /bin/bash

source ~/.bashrc
chmod +x run_DNABert_plotting.sh

# Source the init.sh file to access the data locations
source init.sh

conda activate main

# Find the full path to the python executable within the deeptss environment
PYTHON_PATH=$(which python)

$PYTHON_PATH DNABert_visualize.py -n $CAGE_DIR_NAME

# $PYTHON_PATH DNABERT/examples/visualize.py \
#     --kmer $KMER \
#     --model_path $MODEL_PATH \
