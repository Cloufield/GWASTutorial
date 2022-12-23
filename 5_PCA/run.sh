#!/bin/bash

plinkFile="../1_Dataset/1KG.EAS.auto.snp.norm.nodup.split.maf005.thinp020" #!!!please set this to your own path
outPrefix="plink_results"
threadnum=2

#hildset = hild # change to file of SNPs located in HLA and high ld region 

# pruning
plink2 \
        --bfile ${plinkFile} \
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
	--score ${outPrefix}.eigenvec.allele 2 5 header-read no-mean-imputation variance-standardize \
        --score-col-nums 6-15 \
        --out ${outPrefix}_projected
