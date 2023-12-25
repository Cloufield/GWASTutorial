#!/bin/bash
#$ -S /bin/bash
export PATH=~/tools/bin:$PATH
export OMP_NUM_THREADS=1

genotypeFile="../01_Dataset/1KG.EAS.auto.snp.norm.nodup.split.maf005.thinp020"

plink \
        --bfile ${genotypeFile} \
        --missing \
        --freq \
        --hardy \
        --out plink_results

plink2 \
	--bfile ${genotypeFile} \
        --freq \
	--out plink_results

plink \
        --bfile ${genotypeFile} \
        --maf 0.01 \
        --geno 0.01 \
        --mind 0.02 \
        --hwe 5e-6 \
        --indep-pairwise 50 5 0.2 \
        --out plink_results

plink \
        --bfile ${genotypeFile} \
        --extract plink_results.prune.in \
        --het \
        --out plink_results

plink \
        --bfile ${genotypeFile} \
        --extract plink_results.prune.in \
        --genome \
        --out plink_results

plink \
	--bfile ${genotypeFile} \
        --chr 22 \
        --r2 \
        --out plink_results
