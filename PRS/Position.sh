#!/bin/bash

# Base directory where all your .bgen and .sample files are located
base_dir=""

# Assuming your .bgen and .sample files follow the naming convention 'ukb22828_cX_b0_v3.bgen' and 'ukb22828_cX_b0_v3_s487159.sample'
# where X is the chromosome number

# Path to your positions file
positions_file=""

# Read each line from the positions file
while IFS=$'\t' read -r chr position
do
  # Remove carriage return characters from the position
  position=$(echo $position | tr -d '\r')

  # Construct the file names based on the chromosome number
  bgen_file="${base_dir}/ukb22828_c${chr}_b0_v3.bgen"
  sample_file="${base_dir}/ukb22828_c${chr}_b0_v3_s487159.sample"

  # Define the output name using the chromosome and position for uniqueness
  output_name="${base_dir}/subset_chr${chr}_pos${position}"

  # Run Plink command using the correct .bgen and .sample files for the chromosome
  ./plink2 \
    --bgen "$bgen_file" ref-first \
    --sample "$sample_file" \
    --chr $chr \
    --from-bp $position \
    --to-bp $position \
    --make-bed \
    --out "$output_name" \
    --threads 16

  # Echo a message to indicate progress
  echo "Processed subset for chr${chr} at position ${position}"

  # You can include additional processing here if needed

done < "$positions_file"
