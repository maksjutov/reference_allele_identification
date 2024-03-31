import pandas as pd
df = pd.read_csv('../FP_SNPs.txt',sep='\t')

# Remove GB37_position column
df = df.drop("GB37_position", axis=1)

# Rearrange columns
df = df[["chromosome", "GB38_position", "rs#", "allele1", "allele2"]]

# Add "chr" to chromosome number
df["chromosome"] = "chr" + df["chromosome"].astype(str)

# Add "rs" to SNP id
df["rs#"]= "rs" + df["rs#"].astype(str)

# Remove chr23 chromosome
df = df[df["chromosome"] != "chr23"]

# Save df as txt file
df.to_csv('../FP_SNPs_10k_GB38_twoAllelsFormat.txt', sep="\t", index=False)