import os
import subprocess
import argparse

def write_batch_file(output_dir, input_beds):
    """
        This function is for automatically write batch script for IGV and launch the IGV
        with the according batch scripts;
    """

    mode =  input("What mode you want to choose?[INTERACT/AUTO]     ")

    if mode == "INTERACT":
        genome = input("What is the source of genome for your input?\n")
        batch_file = os.path.join(output_dir, "igv_batch_script_INTERACT.txt")
        with open(batch_file, "w") as f:
            # Load the reference genome
            f.write("genome {}\n".format(genome))
            # Load the input BED file
            input_files_str = ",".join([os.path.abspath(bed) for bed in input_beds])
            f.write("load {}\n".format(input_files_str))
        
        return batch_file
    
    if mode == "AUTO":
        #Costomize your own batch script for running IGV;
        genome = input("What is the source of genome for your input?\n")
        num_snapshot = input("How many regions you want to take a shot of?\n")
        regions = []
        for i in range(int(num_snapshot)):
            regions.append(input("Where is the {} region? [Ex: chr1:10,000-20,000]".format(i+1)))

        batch_file = os.path.join(output_dir, "igv_batch_script.txt")
        with open(batch_file, "w") as f:
            # Load the reference genome
            f.write("genome {}\n".format(genome))
            # Load the input BED file
            input_files_str = ",".join([os.path.abspath(bed) for bed in input_beds])
            f.write("load {}\n".format(input_files_str))

            # Save a screenshot
            f.write("snapshotDirectory {}\n".format(os.path.abspath(output_dir)))

            for i in range(len(regions)):
                # Zoom in to the region of interest
                f.write("goto {}\n".format(regions[i]))
                f.write("snapshot ROI_{}.png\n".format(i+1,regions[i]))
        return batch_file
    
    return " ***** PLEASE CORRECT YOUR CHOICE OF MODE! ***** "

def launch_igv(batch_file):
    igv_path = "./IGV_2.16.1/igv.sh"
    batch_path = os.path.abspath(batch_file)
    subprocess.run([igv_path, "-b", batch_path])


# Running the python file through command lines;
parser = argparse.ArgumentParser()
parser.add_argument('-i', nargs='+', help='The input lists of bed files: PLEASE USE "[input1, input2, input3]" FORMAT')
parser.add_argument('-o', type=str, help='The output directory path for the snapshot;')
args = parser.parse_args()


# Set the input and output directories
#input_beds = ["/Users/zhichengluo/Desktop/data/high_conf/deeptss.bed","/Users/zhichengluo/Desktop/data/high_conf/dnabert.bed","/Users/zhichengluo/Desktop/data/low_conf/deeptss.bed","/Users/zhichengluo/Desktop/data/low_conf/dnabert.bed"]
input_beds = args.i
output_dir = args.o


# Write the batch file
batch_file = write_batch_file(output_dir, input_beds)

# Launch IGV with the batch file
launch_igv(batch_file)


