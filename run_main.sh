#! /bin/bash

#SBATCH --job-name=ccline     ## Name of the job
#SBATCH --output=logger.out    ## Output file

## Run on a GPU
#SBATCH --ntasks=1    

#SBATCH --partition=GPU-shared
#SBATCH --gres=gpu:v100-32:4


## Job memory request
#SBATCH --mem=60gb
## Time limit hrs:min:sec
#SBATCH --time 01:00:00

source ~/.bashrc
chmod +x run_main.sh

# Activate conda env for main
conda activate main

# Source the init.sh script
source init.sh
# Find the full path to the python executable within the deeptss environment
PYTHON_PATH=$(which python)

$PYTHON_PATH main.py \
			-run_dTSS $run_dTSS \
			-run_preprocess $run_preprocess \
			-run_dBERT $run_dBERT \
			-calculate_visual $calculate_visual \
 			-get_visual $get_visual \
			-get_bscores $get_bscores \
			-run_IGV $run_IGV \
			-user $USERNAME