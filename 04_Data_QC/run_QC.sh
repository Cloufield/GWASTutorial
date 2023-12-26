#!/bin/bash
#$ -S /bin/bash
export PATH=~/tools/bin:$PATH
export OMP_NUM_THREADS=1

genotypeFile="../01_Dataset/1KG.EAS.auto.snp.norm.nodup.split.rare002.common015.missing"

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
        --hwe 1e-6 \
        --indep-pairwise 50 5 0.2 \
        --out plink_results

plink \
        --bfile ${genotypeFile} \
        --extract plink_results.prune.in \
        --het \
        --out plink_results

awk 'NR>1 && $6>0.1 || $6<-0.1 {print $1,$2}' plink_results.het > high_het.sample

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

plink \
	--bfile ${genotypeFile} \
	--geno 0.02 \
	--mind 0.02 \
	--hwe 1e-6 \
	--remove high_het.sample \
	--keep-allele-order \
	--make-bed \
	--out sample_data.clean
