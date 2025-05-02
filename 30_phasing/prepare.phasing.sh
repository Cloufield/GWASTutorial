#!/bin/bash

before_alignment_bfile="../04_Data_QC/sample_data.clean"
foralignment="./1KG_foralignment.tsv"

awk -F'\t' '{
  split($2, arr, ":");
  print $2 "\t" arr[3] "\t" arr[4]
}' ${before_alignment_bfile}.bim > ${foralignment}

after_alignment_bfile="./sample_data.clean.alignment"

plink \
	--bfile ${before_alignment_bfile} \
	--a1-allele ${foralignment} 2 \
	--make-bed \
	--out ${after_alignment_bfile}

