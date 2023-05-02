import argparse
from pybedtools import BedTool
import os

# Initialize the argument parser
parser = argparse.ArgumentParser(description='Process input file')

# Add the input file argument
parser.add_argument('-i', '--input', type=str, required=True, help='Path to input file')
# Add the output file argument
parser.add_argument('-o', '--output', type=str, required=True, help='Path to output file')
# Add the output file argument
parser.add_argument('-ref', '--reference_genome', type=str, required=True, help='Path to reference genome sequence')
# Add the output file argument
parser.add_argument('-chrSizes', '--chrom_sizes', type=str, required=True, help='Path to reference genome chromosome sizes')
# Add the output file argument
parser.add_argument('-kmer', '--KMER', type=str, required=True, help='K-mer length')

# Parse the arguments
args = parser.parse_args()

# Access the input file path using args.input
bed_path = args.input
out_path = args.output
ref_seq = args.reference_genome
kmer_length = int(args.KMER)
chromSizes_path = args.chrom_sizes

seq_file_path = out_path+"/bed2seq_out.fasta"
seq_only_file_path = out_path+"/bed2seq_out.txt"
kmer_file_path = out_path+"/dev.tsv"
flanked_file_path = out_path+"/flanked.bed"

# Read in the bed file using pybedtools
bed = BedTool(bed_path)

# Construct the bedtools slop command
bedtools_cmd = f"bedtools slop -i {bed_path} -g {chromSizes_path} -l {247} -r {50} > {flanked_file_path}"
# Execute the command using os.system()
os.system(bedtools_cmd)

# Use bedtools getfasta to extract the sequences from the genome fasta file
os.system('bedtools getfasta -fi {} -bed {} -fo {} -name'.format(ref_seq, out_path+"/flanked.bed", seq_file_path))

# Use awk to extract only the sequence part of the output file and save it to a new file
"""
/^>/ {next}: This pattern matches any input line that starts with the > character, 
which indicates a header line in the FASTA format. When a header line is matched, 
the next keyword is used to skip to the next input line without processing the current line. 
This effectively skips over the header line and moves to the next line, which contains 
the sequence data.
{print}: This pattern matches any input line that does not start with the > character, 
which includes all lines containing the sequence data. When a sequence line is matched, 
the print keyword is used to output the line to standard output (i.e., the console or 
terminal). This effectively outputs only the sequence data and excludes the header lines.
"""
os.system("awk '/^>/ {{next}} {{print}}' {} | tr '[:lower:]' '[:upper:]' > {}".format(seq_file_path, seq_only_file_path))

# Different range probabilities

# set up directories
output_dir_high = out_path+'/high_prob'
output_dir_low = out_path+'/low_prob'
for output_dir in [output_dir_high, output_dir_low]:
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

# Define the probability ranges
high_prob_range = (0.7, 1)
low_prob_range = (0, 0.3)
mid_prob_range = (0.3, 0.7)

# Open the input files and read their contents
with open(bed_path, "r") as bed_file, open(seq_only_file_path, "r") as seq_file:
    bed_lines = bed_file.readlines()
    seq_lines = seq_file.readlines()    

with open(output_dir_high+"/pre_dev.tsv", "w"):
    pass
with open(output_dir_low+"/pre_dev.tsv", "w"):
    pass

index = 1
# Loop over the bed lines and extract the relevant information
for i, bed_line in enumerate(bed_lines):
    # Split the bed line into its columns
    bed_cols = bed_line.strip().split("\t")

    # Get the probability and convert it to a float
    prob = float(bed_cols[-2])

    # Determine which folder the output file should be stored in
    if (prob >= high_prob_range[0] and prob <= high_prob_range[1]) or (prob >= low_prob_range[0] and prob <= low_prob_range[1]):
        folder = output_dir_high
    else:
        folder = output_dir_low

    # Determine the label based on the probability
    if prob >= 0.5:
        label = "1"
    else:
        label = "0"

    # Write the sequence and label to the appropriate output file
    out_path = os.path.join(folder, "pre_dev.tsv")
    with open(out_path, "a") as out_file:
        out_file.write("{}\t{}\t{}\n".format(seq_lines[i].strip(), label, index))
        index = index+1


def seq2kmer(seq, k):
    """
    Convert original sequence to kmers
    
    Arguments:
    seq -- str, original sequence.
    k -- int, kmer of length k specified.
    
    Returns:
    kmers -- str, kmers separated by space
    """
    kmer = [seq[x:x+k] for x in range(len(seq)+1-k)]
    kmers = " ".join(kmer)
    return kmers


# Define a wrapper function to apply seq2kmer to each sequence
def process_sequences(seq_file_path, kmer_file_path, kmer_length):
    with open(seq_file_path, 'r') as seq_file, open(kmer_file_path, 'a') as kmer_file:
        for line in seq_file:
            # Split the line into its columns
            columns = line.strip().split('\t')
            
            # Extract the sequence and label
            sequence = columns[0]
            label = columns[1]
            kmers = seq2kmer(sequence, kmer_length)
            kmer_file.write(kmers+"\t")
            kmer_file.write(label+"\n")



# Call the wrapper function to process all sequences and write the kmers to a file
seq_prob_file_path = output_dir_high+"/pre_dev.tsv"
kmer_file_path = output_dir_high+"/dev.tsv"
with open(kmer_file_path, "w") as kmer_file:
    kmer_file.write("sequence\tlabel\n")
    
process_sequences(seq_prob_file_path, kmer_file_path, kmer_length)

seq_prob_file_path = output_dir_low+"/pre_dev.tsv"
kmer_file_path = output_dir_low+"/dev.tsv"
with open(kmer_file_path, "w") as kmer_file:
    kmer_file.write("sequence\tlabel\n")

process_sequences(seq_prob_file_path, kmer_file_path, kmer_length)





