#!/bin/bash

plinkFile="../04_Data_QC/sample_data.clean" #!!!please set this to your own path

plink \
	--bfile ${plinkFile} \
	--make-set high-ld-hg19.txt \
	--write-set \
	--out hild
