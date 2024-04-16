def read_tfam_file(tfam_file_path):
    sample_ids = []
    with open(tfam_file_path, 'r') as tfam_file:
        for line in tfam_file:
            parts = line.strip().split()
            sample_ids.append(parts[1])  # Assuming the second column is the sample ID
    return sample_ids

def process_tped_file(tped_file_path, tfam_file_path, output_file_path):
    sample_ids = read_tfam_file(tfam_file_path)
    genotype_data = {}

    with open(tped_file_path, 'r') as tped:
        for line in tped:
            parts = line.strip().split()
            chrom, marker, gen_dist, phys_pos = parts[:4]
            genotypes = parts[4:]
            genotype_data[marker] = genotypes
    with open(output_file_path, 'w') as output:
        header = ['Chromosome', 'Sample_ID', 'Genetic_Dist', 'Physical_Pos'] + list(genotype_data.keys())
        output.write('\t'.join(header) + '\n')

        for i, sample_id in enumerate(sample_ids):
            row = [''] * 4
            row[1] = sample_id

            for marker in genotype_data.keys():
                genotype = genotype_data[marker][2*i:2*i+2]
                row.append(''.join(genotype))

            output.write('\t'.join(row) + '\n')

# Usage
tped_file_path = ''  # Path to your TPED file
tfam_file_path = ''  # Path to your TFAM file
output_file_path = ''  # Path for the output file

process_tped_file(tped_file_path, tfam_file_path, output_file_path)
