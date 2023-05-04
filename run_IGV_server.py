import os
import subprocess
import argparse

# Running the python file through command lines;
parser = argparse.ArgumentParser()
parser.add_argument('-ref', type=str, required=True, help='Name of the reference genome being used [Ex: hg38]; ')
parser.add_argument('-i', type=str, required=True, help='The input directory contains lists of .bed outputs; ')
parser.add_argument('-o', type=str, required=True, help='The output directory path for bashscript and snapshot;')
parser.add_argument('-user', '--user_name', type=str, required=True, help='User name on bridges2')


args = parser.parse_args()

# Set the input and output directories
ref_genome = os.path.splitext(args.ref)[0]
input_directory_path = "/ocean/projects/bio230007p/"+args.user_name+"/scoring_bed_files/" + args.i
input_dir_path_high = os.path.join(input_directory_path, "high")
input_dir_path_low = os.path.join(input_directory_path, "low")
output_directory_path_high = os.path.join(args.o, args.i, "high")
output_directory_path_low = os.path.join(args.o, args.i, "low")

def write_batch_file(ref_G, input_beds, output_dir):
    """
        This function is for automatically write batch script for IGV and launch the IGV
        with the according batch scripts;
    """
    
    mode = input("Which mode you want to launch the IGV? [INTERACT/AUTO]")

    if mode == "INTERACT":
        # Create the output directory and subdirectory if they do not exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        batch_file = os.path.join(output_dir, "igv_batch_script_INTERACT.txt")
        with open(batch_file, "w") as f:
            # Load the reference genome
            f.write("genome {}\n".format(ref_G))
            # Load the input BED files
            input_dir_path = os.path.abspath(input_beds)
            for bed in os.listdir(input_dir_path):
                if bed.endswith(".bed"):
                    bed_path = os.path.join(input_dir_path, bed)
                    f.write("load {}\n".format(os.path.abspath(bed_path)))
        
        return batch_file
    
    if mode == "AUTO":
        #Costomize your own batch script for running IGV;
        num_snapshot = input("How many regions you want to take a shot of?\n")
        regions = []
        for i in range(int(num_snapshot)):
            regions.append(input("Where is the {} region? [Ex: chr1:10,000-20,000]".format(i+1)))

        # Create the output directory and subdirectory if they do not exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        batch_file = os.path.join(output_dir, "igv_batch_script.txt")
        with open(batch_file, "w") as f:
            # Load the reference genome
            f.write("genome {}\n".format(ref_G))
            # Load the input BED files
            input_dir_path = os.path.abspath(input_beds)
            for bed in os.listdir(input_dir_path):
                if bed.endswith(".bed"):
                    bed_path = os.path.join(input_dir_path, bed)
                    f.write("load {}\n".format(os.path.abspath(bed_path)))

            # Save a screenshot
            f.write("snapshotDirectory {}\n".format(os.path.abspath(output_dir)))

            for i in range(len(regions)):
                # Zoom in to the region of interest
                f.write("goto {}\n".format(regions[i]))
                f.write("snapshot ROI_{}.png\n".format(i+1,regions[i]))
        return batch_file
    
    return " ***** PLEASE CORRECT YOUR CHOICE OF MODE! ***** "

def launch_igv(batch_file):
    igv_path = "./run_IGV/IGV_2.4.13/igv.sh"
    batch_path = os.path.abspath(batch_file)
    subprocess.run([igv_path, "-b", batch_path])




# Write the batch file & Launch IGV with the batch file
batch_file_high = write_batch_file(ref_genome, input_directory_path, output_directory_path_high)
launch_igv(batch_file_high)

batch_file_low = write_batch_file(ref_genome, input_directory_path, output_directory_path_low)
launch_igv(batch_file_low)


