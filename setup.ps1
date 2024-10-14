# This script assumes you have conda installed and added to PATH environmental variable.

# Creating the conda environment and installing necessary packages
conda create -n Ganics python=3.11 -y
conda activate Ganics
conda install jupyter -y
pip install -r requirements.txt

# Extracting the datasets
Get-ChildItem "dataset\*.zip" | ForEach-Object {
    Expand-Archive $_.FullName -DestinationPath "dataset"
}

# Extracting the test images if requested
if ($args[0] -eq "test") {
    Expand-Archive "tmp\test_imgs.zip" -DestinationPath "tmp"
}
