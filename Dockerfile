from python
RUN mkdir allele_indentification_dir
COPY reference_allele_identification_main.py ./allele_indentification_dir
RUN pip install pandas pysam
