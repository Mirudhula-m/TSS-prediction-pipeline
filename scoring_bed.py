# This file is for comparing different bed files in order to score them
import argparse
from pybedtools import BedTool
import os
import glob
import csv
import numpy as np
import subprocess
import seaborn as sns
import matplotlib.pyplot as plt

# Initialize the argument parser
parser = argparse.ArgumentParser(description='Process input file')
parser.add_argument('-n', '--data_name', type=str, required=True, help='Name of cage directory that was used initially')
parser.add_argument('-ref', '--ref_gene_name', type=str, required=True, help='Name of the reference genome being used - hg38/mm10')
parser.add_argument('-user', '--user_name', type=str, required=True, help='User name on bridges2')

# Parse the arguments
args = parser.parse_args()

DEEPTSS_DIR="/ocean/projects/bio230007p/"+args.user_name+"/DeepTSS/data/"+args.data_name+"/OUT/"
high_tsv_path = DEEPTSS_DIR+"high_prob/pre_dev.tsv"
low_tsv_path = DEEPTSS_DIR+"low_prob/pre_dev.tsv"
bed_path = DEEPTSS_DIR+"/flanked.bed"
# bed_path = glob.glob(DEEPTSS_DIR + '*' + '.Scored.bed')[0]

DNABERT_OUT_PATH="/ocean/projects/bio230007p/"+args.user_name+"/DNABert/OUT/"+args.data_name
high_path = DNABERT_OUT_PATH+"/high/preds.npy"
low_path = DNABERT_OUT_PATH+"/low/preds.npy"

scoring_PATH="/ocean/projects/bio230007p/"+args.user_name+"/scoring_bed_files/"+args.data_name
if not os.path.exists(scoring_PATH) or not os.path.exists(scoring_PATH+"/high"):
	if not os.path.exists(scoring_PATH):
		os.makedirs(scoring_PATH)
	os.makedirs(scoring_PATH+"/high")
	os.makedirs(scoring_PATH+"/low")

scoring_high_path = scoring_PATH+"/high"
scoring_low_path = scoring_PATH+"/low"






deeptss_bed_path = scoring_high_path+"/deeptss.bed"
dnabert_bed_path = scoring_high_path+"/dnabert.bed"

print(os.path.isfile(deeptss_bed_path))
if not os.path.isfile(deeptss_bed_path):

	print("Required BED files not found. Pre-processing bed files...")
	print("This may take some time. Please be patient.")
	deeptss_bed_file = open(deeptss_bed_path, "w")
	dnabert_bed_file = open(dnabert_bed_path, "w")

	# load the predictions from the NumPy array
	pred2 = np.load(high_path)
	print(pred2.shape)


	tsv_data = np.loadtxt(high_tsv_path, dtype=str)


	# Loop over rows in TSV file
	row_num = 0
	for row in tsv_data:
		# Extract sequence index and prediction from TSV
		seq_index = int(row[2]) - 1
		prediction = int(row[1])

		# Extract BED information for this sequence
		with open(bed_path, "r") as bed_file:
			i = 0
			for line in bed_file:
				if i == seq_index:
					bed_info = line.strip()
					break
				i += 1

		if prediction == 1:
			deeptss_bed_file.write(f"{bed_info}\n")
		if pred2[row_num] == 1:
			dnabert_bed_file.write(f"{bed_info}\n")
		row_num += 1
	# Close BED files
	deeptss_bed_file.close()
	dnabert_bed_file.close()

	deeptss_bed_path = scoring_low_path+"/deeptss.bed"
	dnabert_bed_path = scoring_low_path+"/dnabert.bed"

if not os.path.isfile(deeptss_bed_path):

	# print("Required BED files not found. Pre-processing bed files...")
	# print("This may take some time. Please be patient.")
	deeptss_bed_file = open(deeptss_bed_path, "w")
	dnabert_bed_file = open(dnabert_bed_path, "w")

	# load the predictions from the NumPy array
	pred2 = np.load(low_path)
	print(pred2.shape)


	tsv_data = np.loadtxt(low_tsv_path, dtype=str)


	# Loop over rows in TSV file
	row_num = 0
	for row in tsv_data:
		# Extract sequence index and prediction from TSV
		seq_index = int(row[2]) - 1
		prediction = int(row[1])

		# Extract BED information for this sequence
		with open(bed_path, "r") as bed_file:
			i = 0
			for line in bed_file:
				if i == seq_index:
					bed_info = line.strip()
					break
				i += 1

		# Write new line to BED file(s) with BED info, depending on the prediction value
		if prediction == 1:
			deeptss_bed_file.write(f"{bed_info}\n")
		if pred2[row_num] == 1:
			dnabert_bed_file.write(f"{bed_info}\n")
		row_num += 1
	# Close BED files
	deeptss_bed_file.close()
	dnabert_bed_file.close()




if args.ref_gene_name == "mm10.fa":
	ref_file_name = "refTSS_v3.3_mouse_coordinate.mm10.bed"
else:
	ref_file_name = "refTSS_v3.3_human_coordinate.hg38.bed"



# High

print("High Confidence Metrics:")


# Compare resulting BED files to reference BED file using bedtools
reference_bed_path = "/ocean/projects/bio230007p/"+args.user_name+"/scoring_bed_files/"+ref_file_name

deeptss_intersect_path = scoring_high_path+"/deeptss_intersect.bed"
deeptss_comp_interesect_path = scoring_high_path+"/deeptss_comp_intersect.bed"
deeptss_ref_comp_interesect_path = scoring_high_path+"/deeptss_ref_comp_intersect.bed"

dnabert_intersect_path = scoring_high_path+"/dnabert_intersect.bed"
dnabert_comp_interesect_path = scoring_high_path+"/dnabert_comp_intersect.bed"
dnabert_ref_comp_interesect_path = scoring_high_path+"/dnabert_ref_comp_intersect.bed"

mix_intersect_path = scoring_high_path+"/mix_intersect_path.bed"

deeptss_bed_file_path = scoring_high_path+"/deeptss.bed"
dnabert_bed_path = scoring_high_path+"/dnabert.bed"


# Run bedtools intersect to compare BED files
subprocess.run(["bedtools", "intersect", "-a", deeptss_bed_path, "-b", reference_bed_path, "-wa"], stdout=open(deeptss_intersect_path, "w"))
subprocess.run(["bedtools", "intersect", "-a", deeptss_bed_path, "-b", reference_bed_path, "-v"], stdout=open(deeptss_comp_interesect_path, "w"))
subprocess.run(["bedtools", "intersect", "-a", reference_bed_path, "-b", deeptss_bed_path, "-v"], stdout=open(deeptss_ref_comp_interesect_path, "w"))

subprocess.run(["bedtools", "intersect", "-a", dnabert_bed_path, "-b", reference_bed_path, "-v"], stdout=open(dnabert_comp_interesect_path, "w"))
subprocess.run(["bedtools", "intersect", "-a", dnabert_bed_path, "-b", reference_bed_path, "-wa"], stdout=open(dnabert_intersect_path, "w"))
subprocess.run(["bedtools", "intersect", "-a", reference_bed_path, "-b", dnabert_bed_path, "-v"], stdout=open(dnabert_ref_comp_interesect_path, "w"))

# subprocess.run(["bedtools", "intersect", "-a", reference_bed_path, "-b", dnabert_bed_path, deeptss_bed_path], stdout=open(mix_intersect_path, "w"))

# Print the results of the comparisons

# intersects present in A and ref
deeptss_intersect_data = np.loadtxt(deeptss_intersect_path, dtype=str)
dnabert_intersect_data = np.loadtxt(dnabert_intersect_path, dtype=str)

# present in A not in ref
deeptss_comp_intersect_data = np.loadtxt(deeptss_comp_interesect_path, dtype=str)
dnabert_comp_intersect_data = np.loadtxt(dnabert_comp_interesect_path, dtype=str)

# present in ref not in A
deeptss_ref_intersect_data = np.loadtxt(deeptss_ref_comp_interesect_path, dtype=str)
dnabert_ref_intersect_data = np.loadtxt(dnabert_ref_comp_interesect_path, dtype=str)

# present in all three
# mixed_intersect_data = np.loadtxt(mix_intersect_path, dtype=str)

data1 = [len(deeptss_intersect_data), len(deeptss_comp_intersect_data), len(deeptss_ref_intersect_data)]#, len(mixed_intersect_data)]
data2 = [len(dnabert_intersect_data), len(dnabert_comp_intersect_data), len(dnabert_ref_intersect_data)]#, len(mixed_intersect_data)]

# create a bar plot using seaborn
plt.figure()
sns.set_style("whitegrid")
plt.figure(figsize=(8,6))
ax = sns.barplot(x=["Both", "DTSS not RefTSS", "RefTSS not DTSS"], y=data1, palette="Blues")

# set the axis labels and title
ax.set(ylabel='Number of TSS locations', title='Intersection of RefTSS and DeepTSS')
plt.savefig(scoring_high_path+"/deeptss.png")

# create a bar plot using seaborn
plt.figure()
sns.set_style("whitegrid")
plt.figure(figsize=(8,6))
ax = sns.barplot(x=["Both", "DBERT not RefTSS", "RefTSS not DBERT"], y=data2, palette="Blues")

# set the axis labels and title
ax.set(ylabel='Number of TSS locations', title='Intersection of RefTSS and DNABERT')
plt.savefig(scoring_high_path+"/dnabert.png")



print("Number of intersections with Deeptss:")
print(len(deeptss_intersect_data))

print("Number of intersections with Dnabert:")
print(len(dnabert_intersect_data))



# Low


print("Low Confidence Metrics:")

deeptss_intersect_path = scoring_low_path+"/deeptss_intersect.bed"
deeptss_comp_interesect_path = scoring_low_path+"/deeptss_comp_intersect.bed"
deeptss_ref_comp_interesect_path = scoring_low_path+"/deeptss_ref_comp_intersect.bed"

dnabert_intersect_path = scoring_low_path+"/dnabert_intersect.bed"
dnabert_comp_interesect_path = scoring_low_path+"/dnabert_comp_intersect.bed"
dnabert_ref_comp_interesect_path = scoring_low_path+"/dnabert_ref_comp_intersect.bed"

mix_intersect_path = scoring_low_path+"/mix_intersect_path.bed"

deeptss_bed_file_path = scoring_low_path+"/deeptss.bed"
dnabert_bed_path = scoring_low_path+"/dnabert.bed"


# Run bedtools intersect to compare BED files
subprocess.run(["bedtools", "intersect", "-a", deeptss_bed_path, "-b", reference_bed_path, "-wa"], stdout=open(deeptss_intersect_path, "w"))
subprocess.run(["bedtools", "intersect", "-a", deeptss_bed_path, "-b", reference_bed_path, "-v"], stdout=open(deeptss_comp_interesect_path, "w"))
subprocess.run(["bedtools", "intersect", "-a", reference_bed_path, "-b", deeptss_bed_path, "-v"], stdout=open(deeptss_ref_comp_interesect_path, "w"))

subprocess.run(["bedtools", "intersect", "-a", dnabert_bed_path, "-b", reference_bed_path, "-v"], stdout=open(dnabert_comp_interesect_path, "w"))
subprocess.run(["bedtools", "intersect", "-a", dnabert_bed_path, "-b", reference_bed_path, "-wa"], stdout=open(dnabert_intersect_path, "w"))
subprocess.run(["bedtools", "intersect", "-a", reference_bed_path, "-b", dnabert_bed_path, "-v"], stdout=open(dnabert_ref_comp_interesect_path, "w"))

# subprocess.run(["bedtools", "intersect", "-a", reference_bed_path, "-b", dnabert_bed_path, deeptss_bed_path], stdout=open(mix_intersect_path, "w"))

# Print the results of the comparisons

# intersects present in A and ref
deeptss_intersect_data = np.loadtxt(deeptss_intersect_path, dtype=str)
dnabert_intersect_data = np.loadtxt(dnabert_intersect_path, dtype=str)

# present in A not in ref
deeptss_comp_intersect_data = np.loadtxt(deeptss_comp_interesect_path, dtype=str)
dnabert_comp_intersect_data = np.loadtxt(dnabert_comp_interesect_path, dtype=str)

# present in ref not in A
deeptss_ref_intersect_data = np.loadtxt(deeptss_ref_comp_interesect_path, dtype=str)
dnabert_ref_intersect_data = np.loadtxt(dnabert_ref_comp_interesect_path, dtype=str)

# present in all three
# mixed_intersect_data = np.loadtxt(mix_intersect_path, dtype=str)

data1 = [len(deeptss_intersect_data), len(deeptss_comp_intersect_data), len(deeptss_ref_intersect_data)]#, len(mixed_intersect_data)]
data2 = [len(dnabert_intersect_data), len(dnabert_comp_intersect_data), len(dnabert_ref_intersect_data)]#, len(mixed_intersect_data)]

# create a bar plot using seaborn
plt.figure()
sns.set_style("whitegrid")
plt.figure(figsize=(8,6))
ax = sns.barplot(x=["Both", "DTSS not RefTSS", "RefTSS not DTSS"], y=data1, palette="Blues")

# set the axis labels and title
ax.set(ylabel='Number of TSS locations', title='Intersection of RefTSS and DeepTSS')
plt.savefig(scoring_low_path+"/deeptss.png")

# create a bar plot using seaborn
plt.figure()
sns.set_style("whitegrid")
plt.figure(figsize=(8,6))
ax = sns.barplot(x=["Both", "DBERT not RefTSS", "RefTSS not DBERT"], y=data2, palette="Blues")

# set the axis labels and title
ax.set(ylabel='Number of TSS locations', title='Intersection of RefTSS and DNABERT')
plt.savefig(scoring_low_path+"/dnabert.png")


print("Number of intersections with Deeptss:")
print(len(deeptss_intersect_data))

print("Number of intersections with Dnabert:")
print(len(dnabert_intersect_data))







