#! /bin/bash

source ~/.bashrc
chmod +x run_preprocess_for_DNABert.sh

# Source the init.sh file to access the data locations
source init.sh

conda activate preprocess

# Find the full path to the python executable within the deeptss environment
PYTHON_PATH=$(which python)

$PYTHON_PATH preprocess_for_DNABert.py -i $DEEPTSS_OUT -o $OUT_DIR -ref $REF_GENE_LOC -chrSizes $REF_CHROM_SIZES_LOC -kmer $KMER