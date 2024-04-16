# Genetic Data Processing

This project includes Python scripts for processing genetic data files in TPED and TFAM formats. The scripts read these files, extract sample IDs, and reformat the data into a comprehensive output file.

## Requirements

Before running the scripts, ensure you have Python installed on your machine. You can download Python from [python.org](https://www.python.org/downloads/).

## Files Description

- `read_tfam_file.py`: This script reads a TFAM file to extract sample IDs.
- `process_tped_file.py`: This script processes a TPED file, reads corresponding sample IDs from a TFAM file, and generates a formatted output file containing genetic data.

## Input Files

You will need the following input files:
- TPED file: Contains genotype information.
- TFAM file: Contains family data.

Ensure these files are correctly formatted according to the standard TPED and TFAM file formats.

## Output Files

The script will generate an output file containing the following columns:
- Chromosome
- Sample_ID
- Genetic_Dist
- Physical_Pos
- Additional columns for each genetic marker processed

## How to Run the Scripts

1. Place your TPED and TFAM files in a known directory.
2. Update the script variables to point to your files:
   ```python
   tped_file_path = 'path/to/your/TPED_file.tped'
   tfam_file_path = 'path/to/your/TFAM_file.tfam'
   output_file_path = 'path/to/your/output_file.txt'

