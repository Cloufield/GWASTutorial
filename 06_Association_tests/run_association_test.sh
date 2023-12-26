#!/bin/bash
export PATH=~/tools/bin:$PATH
export OMP_NUM_THREADS=1

genotypeFile="../04_Data_QC/sample_data.clean"
phenotypeFile="../01_Dataset/1kgeas_binary.txt"
covariateFile="../05_PCA/plink_results_projected.sscore"

covariateCols=6-10
colName="B1"
threadnum=2

plink2 \
	--bfile ${genotypeFile} \
	--pheno ${phenotypeFile} \
	--pheno-name ${colName} \
	--maf 0.01 \
	--covar ${covariateFile} \
	--covar-col-nums ${covariateCols} \
	--glm hide-covar firth firth-residualize single-prec-cc \
	--threads ${threadnum} \
	--out 1kgeas
