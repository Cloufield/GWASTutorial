#!/bin/bash
export PATH=~/tools/bin:$PATH
export OMP_NUM_THREADS=1

genotypeFile="../01_Dataset/1KG.EAS.auto.snp.norm.nodup.split.maf005.thinp020"  #!please set this to your own path

phenotypeFile="../01_Dataset/1kgeas_binary.txt" #!please set this to your own path

covariateFile="../05_PCA/plink_results_projected.sscore"

covariateCols=6-10
colName="B1"
threadnum=2

plink2 \
	--bfile ${genotypeFile} \
	--pheno ${phenotypeFile} \
	--pheno-name ${colName} \
	--maf 0.01 \
	--glm hide-covar allow-no-covars \
	--threads ${threadnum} \
	--out 1kgeas
