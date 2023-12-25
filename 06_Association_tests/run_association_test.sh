#!/bin/bash
export PATH=~/tools/bin:$PATH
export OMP_NUM_THREADS=1

#genotypeFile="../01_Dataset/1KG.EAS.auto.snp.norm.nodup.split.maf005.thinp020"  #!please set this to your own path

#phenotypeFile="../01_Dataset/1kgeas_binary.txt" #!please set this to your own path

genotypeFile="../01_Dataset/1KG.EAS.auto.snp.norm.nodup.split.rare002.common015/1KG.EAS.auto.snp.norm.nodup.split.rare002.common015"
phenotypeFile="../01_Dataset/1KG.EAS.auto.snp.norm.nodup.split.rare002.common015/1kgeas_binary.txt"

covariateFile="../05_PCA/plink_results_projected.sscore"

covariateCols=6-10
colName="B1"
threadnum=2

plink2_2023 \
	--bfile ${genotypeFile} \
	--pheno ${phenotypeFile} \
	--pheno-name ${colName} \
	--maf 0.01 \
	--covar ${covariateFile} \
	--covar-col-nums ${covariateCols} \
	--glm hide-covar firth firth-residualize single-prec-cc \
	--threads ${threadnum} \
	--out 1kgeas2
