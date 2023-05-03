#! /bin/bash

source ~/.bashrc
chmod +x create_run_IGV.sh

# create directory if not exist
if [ ! -d "./run_IGV" ]; then
    mkdir ./run_IGV
fi

# download and unzip IGV 2.4.13
wget -O IGV_2.4.13.zip http://data.broadinstitute.org/igv/projects/downloads/2.4/IGV_2.4.13.zip
unzip -q IGV_2.4.13.zip -d ./run_IGV
rm IGV_2.4.13.zip

# download and unzip IGV 2.16.1
wget -O IGV_2.16.1.zip https://data.broadinstitute.org/igv/projects/downloads/2.16/IGV_2.16.1.zip
unzip -q IGV_2.16.1.zip -d ./run_IGV
rm IGV_2.16.1.zip

# create input and IGV_visualization directories
mkdir ./run_IGV/input
mkdir ./run_IGV/IGV_visualization

mv ./run_IGV_local.py ./run_IGV