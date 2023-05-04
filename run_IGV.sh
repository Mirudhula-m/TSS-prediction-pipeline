#! /bin/bash

source ~/.bashrc
chmod +x run_IGV.sh

# Source the init.sh file to access the data locations
source init.sh

# Find the full path to the python executable environment
PYTHON_PATH=$(which python)



$PYTHON_PATH run_IGV_server.py -ref $REF_GENE_NAME -i $CAGE_DIR_NAME -o ./run_IGV/IGV_visualization -user $USERNAME