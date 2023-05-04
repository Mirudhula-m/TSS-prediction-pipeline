#! /bin/bash

source ~/.bashrc
chmod +x init.sh

#######################
# Make changes here
#######################
# psc username
export USERNAME="mukundan"
# DeepTSS
export CAGE_DIR_NAME="cervical_cancer_line"
#"fantom6_human_dermal_fibroblasts"
#"fantom5_adipocyte_breast"
#"human_pancreatic"
#"mouse_pancreatic"
export BAM_FILE_NAME="ccline.bam"
#"CNhi10452_150325_SN554_0245_AC6N6UACXX_NoIndex_L002_R1_001.F6-001-RNA-001-01C07-FE82.CAC.10003.bam"
#"Adipocyte_breast_donor1"
export REF_GENE_NAME="hg38.fa"
#"hg38.fa"
#"mm10.fa"
export REF_CHROM_SIZES="hg38.chrom.sizes"
#"hg38.chrom.sizes"
#"mm10.chrom.sizes"
export PHYL_NAME="hg38.phyloP100way.bw"
#"hg38.phyloP100way.bw"
#"mm10.60way.phyloP60way.bw"

# DNABERT
export KMER=4


# Deciding which sections of the analysis to run
export run_dTSS=0
export run_preprocess=0
export run_dBERT=0
export calculate_visual=0
export get_visual=0
export get_bscores=1
export run_IGV=1




#################################################
# Fixed Data locations -- DO NOT CHANGE THESE UNLESS THE ROOT FOLDER IS DIFFERENT
#################################################
# DeepTSS
export DATA_DIR="/ocean/projects/bio230007p/$USERNAME/DeepTSS/data"
export CAGE_DIR="$DATA_DIR/$CAGE_DIR_NAME"
export BAM_LOC="$CAGE_DIR/$BAM_FILE_NAME"

export COMMON_DATA_DIR="/ocean/projects/bio230007p/$USERNAME/DeepTSS"
export REF_GENE_LOC="$COMMON_DATA_DIR/$REF_GENE_NAME"
export REF_CHROM_SIZES_LOC="$COMMON_DATA_DIR/$REF_CHROM_SIZES"
export PHYL_LOC="$COMMON_DATA_DIR/$PHYL_NAME"

# DeepTSS out
export OUT_DIR="$CAGE_DIR/OUT"
export DEEPTSS_OUT=$(find "$OUT_DIR" -maxdepth 1 -name "*.Scored.bed")

# DNABERT
export DNABERT_PATH="/ocean/projects/bio230007p/$USERNAME/DNABert"
export MODEL_PATH="/ocean/projects/bio230007p/$USERNAME/DNABert/DNA_bert_$KMER"
#dna_model"
# export DATA_PATH="$OUT_DIR"

# export PREDICTION_PATH="$DNABERT_PATH/OUT"
