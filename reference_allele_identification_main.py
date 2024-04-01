import pandas as pd
import pysam
import time
import argparse
import logging
import os.path

logging.basicConfig(filename="log.txt", format='%(asctime)s %(message)s', filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
start_time = time.time()

parser = argparse.ArgumentParser(
    description="This script determines which of the two alleles is the reference allele. "
                "Three arguments are required. The fasta files must be indexed. The script doesn't handle situations when some "
                "chr*.fa files don't exist. The input file with SNPs must have the next columns: chr, B38_position, "
                "rs#, allele1, allele2. The header is not required")
parser.add_argument("--path_to_snp", required=True, type=str, help="path to SNPs file")
parser.add_argument("--path_to_fasta_dir", required=True, type=str, help="path to the dir with indexed fasta files")
parser.add_argument("--name_for_output_file", required=True, type=str, help="name of the output file")
args = parser.parse_args()

# Creating path variables for clarity
path_to_snp_file = args.path_to_snp
path_to_fasta_dir = args.path_to_fasta_dir
output_file = args.name_for_output_file

# Check the SNPs file exists
if not os.path.isfile(args.path_to_snp):
    logger.critical("SNPs file does not exist")
    raise ValueError('SNPs file does not exist')

# Check the SNPs file in txt format
if not args.path_to_snp.endswith(".txt"):
    logger.critical("SNPs file should be a txt file")
    raise ValueError("SNPs file should be a txt file")

# Check directories with fasta files exist
if not os.path.isdir(args.path_to_fasta_dir):
    logger.critical("The directories with the fasta files do not exist")
    raise ValueError("The directories with the fasta files do not exist")

list_of_lists_with_all_parameters_for_output_file = []
with open(path_to_snp_file) as SNPs:
    # Check the header line
    first_line = SNPs.readline().strip().split('\t')
    if first_line == ["chromosome", "GB38_position", "rs#", "allele1", "allele2"]:
        logging.info("The file has the header line")
        # Skip the header line
        next(SNPs)
    else:
        logging.info("The file doesn't have the header line")
    for line in SNPs:
        # Parsing the SNPs file. Strip and split every row to add them to list of lists
        line_as_list = line.strip().split('\t')
        chr = line_as_list[0]
        GB38_position = line_as_list[1]
        GB38_position_as_int = int(GB38_position)
        rs = line_as_list[2]
        allele1 = line_as_list[3]
        allele2 = line_as_list[4]

        # Assume one-based system

        reference_file = pysam.FastaFile(filename=path_to_fasta_dir + "{}.fa".format(chr),
                                         filepath_index=path_to_fasta_dir + "{}.fa.fai".format(chr))
        # Get reference allele to put it later in column
        reference_allele = reference_file.fetch(reference=chr, start=GB38_position_as_int,
                                                end=GB38_position_as_int + 1)

        # Add column based on reference value

        if reference_allele == allele1:
            info_about_reference = "allele1 is a reference"
        elif reference_allele == allele2:
            info_about_reference = "allele2 is a reference"
        else:
            info_about_reference = "Neither the first nor the second allele is a reference allele"

        list_of_lists_with_all_parameters_for_output_file.append(
            [chr, GB38_position, rs, allele1, allele2, reference_allele, info_about_reference])

logging.info('Completed reading the files')

df_with_snps_and_reference_info = pd.DataFrame(list_of_lists_with_all_parameters_for_output_file,
                     columns=["chromosome", "GB38_position", "rs#", "allele1", "allele2", "reference", "check of reference"])

logging.info('The dataframe was created')

df_with_snps_and_reference_info.to_csv(output_file, sep="\t", index=False, encoding='utf-8')

time_of_script_execution = time.time() - start_time

logging.info("The script completed in " + str(round(time_of_script_execution, 2)) + " seconds")
