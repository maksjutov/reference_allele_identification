# reference_allele_identification
The script **reference_allele_identification_main.py** determines which of the two alleles is the reference allele.  Three arguments are required: --path_to_snp, --path_to_fasta_dir, --name_for_output_file. The fasta files must be indexed. The script doesn't handle situations when some chr*.fa files don't exist. The input file with SNPs must have the next columns: chr, B38_position, rs#, allele1, allele2, but the header line is not required.

The script **transforming_original_FP_SNPs_file.py** transforms **FP_SNPs.txt** to **FP_SNPs_10k_GB38_twoAllelsFormat.txt** by removing "GRCh37_position" column, changing order columns to "chromosome",	"GB38_position",	"rs#",	"allele1",	"allele2" and modifying values in "chromosome" column from 1 to chr1, and "rs#" column from 2887286 to rs2887286.

The dockerfile copies **reference_allele_identification_main.py** and downloads required python packages.
