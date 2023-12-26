#!/bin/bash

plinkFile="../04_Data_QC/sample_data.clean"
outPrefix="plink_results"
threadnum=2

plink \
        --bfile ${plinkFile} \
        --make-set high-ld-hg19.txt \
        --write-set \
        --out hild

# pruning
plink2 \
        --bfile ${plinkFile} \
	--maf 0.01 \
	--exclude hild.set \
	--threads ${threadnum} \
	--indep-pairwise 500 50 0.2 \
        --out ${outPrefix}

# remove related samples using knig-cuttoff
plink2 \
        --bfile ${plinkFile} \
	--extract ${outPrefix}.prune.in \
        --king-cutoff 0.0884 \
	--threads ${threadnum} \
        --out ${outPrefix}

# pca after pruning and removing related samples
plink2 \
        --bfile ${plinkFile} \
        --keep ${outPrefix}.king.cutoff.in.id \
	--extract ${outPrefix}.prune.in \
	--freq counts \
	--threads ${threadnum} \
        --pca approx allele-wts \
        --out ${outPrefix}

# projection (related and unrelated samples)
plink2 \
        --bfile ${plinkFile} \
	--threads ${threadnum} \
        --read-freq ${outPrefix}.acount \
	--score ${outPrefix}.eigenvec.allele 2 6 header-read no-mean-imputation variance-standardize \
        --score-col-nums 7-16 \
        --out ${outPrefix}_projected
