#!/bin/bash
# This script assumes you have both conda and unzip packages installed
# and that they are added to PATH environmental variable.

# Creating the conda environment and installing necessary packages
conda create -n Ganics python=3.11 -y
conda activate Ganics
conda install jupyter -y
pip install -r requirements.txt

# Extracting the datasets
unzip "dataset/*.zip" -d "dataset"

# Extracting the test images if requested
if [ "$1" = "test" ]; then
        unzip "tmp/test_imgs.zip" -d "tmp"
fi