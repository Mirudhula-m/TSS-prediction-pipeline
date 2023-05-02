#! /bin/bash

source ~/.bashrc
chmod +x run_DNABert_visual.sh

# Source the init.sh file to access the data locations
source init.sh

conda activate dnabert

# Find the full path to the python executable within the deeptss environment
PYTHON_PATH=$(which python)

$PYTHON_PATH DNABERT/examples/run_finetune.py \
    --model_type dna \
    --tokenizer_name=dna$KMER \
    --model_name_or_path $MODEL_PATH \
    --task_name dnaprom \
    --do_visualize \
    --visualize_data_dir $DATA_PATH \
    --visualize_models $KMER \
    --data_dir $DATA_PATH \
    --max_seq_length 81 \
    --per_gpu_pred_batch_size=16   \
    --output_dir $MODEL_PATH \
    --predict_dir $PREDICTION_PATH \
    --n_process 96
