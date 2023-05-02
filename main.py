import subprocess
import os
import argparse

# Initialize the argument parser
parser = argparse.ArgumentParser(description='Process input file')
parser.add_argument('-run_dTSS', '--run_dTSS', type=str, required=True, help='1/0 for running DeepTSS')
parser.add_argument('-run_preprocess', '--run_preprocess', type=str, required=True, help='1/0 for running Preprocessing for DNABERT')
parser.add_argument('-run_dBERT', '--run_dBERT', type=str, required=True, help='1/0 for running DNABERT')
parser.add_argument('-calculate_visual', '--calculate_visual', type=str, required=True, help='1/0 for calculating visalization scores')
parser.add_argument('-get_visual', '--get_visual', type=str, required=True, help='1/0 for getting visualization plots')
parser.add_argument('-get_bscores', '--get_bscores', type=str, required=True, help='1/0 for calculating Bed file scores with refTSS')

# Parse the arguments
args = parser.parse_args()

# Run DeepTSS
if args.run_dTSS == str(1):
	print("RUNNING DEEPTSS")
	subprocess.run(['./run_deepTSS.sh'])
else:
	print("SKIPPING DEEPTSS")

# Pre-process output data from DeepTSS for DNABert
if args.run_preprocess == str(1):
	print("ENTERING PREPROCESSING STEP FOR DNABERT")
	subprocess.run(['./run_preprocess_for_DNABert.sh'])
else:
	print("SKIPPING PREPROCESSING STEP FOR DNABERT")

# Run DNABERT

# Source the init.sh script
subprocess.call("./init.sh")

OUT_DIR = os.getenv('OUT_DIR')
DNABERT_PATH="/ocean/projects/bio230007p/mukundan/DNABert"

if args.run_dBERT == str(1):
	print("RUNNING DNABERT")

	print("----RUNNING HIGH CONFIDENCE SEQUENCES----")
	os.environ['DATA_PATH'] = OUT_DIR+"/high_prob"#"/jet/home/mukundan/DNABERT/examples/sample_data/ft/6"
	#OUT_DIR+"/high_prob"
	os.environ['PREDICTION_PATH'] = DNABERT_PATH+"/OUT/high"
	#/high
	subprocess.run(['./run_DNABert.sh'])

	print("----RUNNING LOW CONFIDENCE SEQUENCES----")
	os.environ['DATA_PATH'] = OUT_DIR+"/low_prob"
	os.environ['PREDICTION_PATH'] = DNABERT_PATH+"/OUT/low"
	subprocess.run(['./run_DNABert.sh'])
else:
	print("SKIPPING DNABERT")


# Calculating Attention scores and visualizing
if args.calculate_visual == str(1):
	print("CALCULATING VISUALIZATION SCORES")
	print("----VISUALIZING HIGH CONFIDENCE SEQUENCES----")
	os.environ['DATA_PATH'] = OUT_DIR+"/high_prob"
	os.environ['PREDICTION_PATH'] = DNABERT_PATH+"/OUT/high"
	subprocess.run(['./run_DNABert_visual.sh'])

	print("----VISUALIZING LOW CONFIDENCE SEQUENCES----")
	os.environ['DATA_PATH'] = OUT_DIR+"/low_prob"
	os.environ['PREDICTION_PATH'] = DNABERT_PATH+"/OUT/low"
	subprocess.run(['./run_DNABert_visual.sh'])
else:
	print("SKIPPING VISUALIZATION SCORE CALCULATION")

if args.get_visual == str(1):
	print("GETTING VISUALIZATION PLOTS")
	subprocess.run(['./run_DNABert_plotting.sh'])
else:
	print("SKIPPING VISUALZATION PLOTS")

if args.get_bscores == str(1):
	print("SCORING BED FILES")
	subprocess.run(['./run_scoring_bed.sh'])
else:
	print("SKIPPING SCORING BED FILES")







