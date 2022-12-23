#!/bin/bash

plinkFile="../01_Dataset/1KG.EAS.auto.snp.norm.nodup.split.maf005.thinp020" #!!!please set this to your own path

plink \
	--bfile ${plinkFile} \
	--make-set high-ld-hg19.txt \
	--write-set \
	--out hild
