#!/bin/bash
# Module: 06_Association_tests | Script: run_association_test.sh
# Prerequisites: 04_Data_QC/sample_data.clean, 01_Dataset/1kgeas_binary.txt, 05_PCA/plink_results_projected.sscore
# Steps: glm_binary

set -euo pipefail
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$(dirname "$0")"

export PATH="${HOME}/tools/bin:${PATH:-}"
export OMP_NUM_THREADS=1

genotypeFile="${REPO_ROOT}/04_Data_QC/sample_data.clean"
phenotypeFile="${REPO_ROOT}/01_Dataset/1kgeas_binary.txt"
covariateFile="${REPO_ROOT}/05_PCA/plink_results_projected.sscore"
covariateCols=6-10
colName="B1"
threadnum=2

# Step: glm_binary
plink2 \
	--bfile "${genotypeFile}" \
	--pheno "${phenotypeFile}" \
	--pheno-name "${colName}" \
	--maf 0.01 \
	--covar "${covariateFile}" \
	--covar-col-nums "${covariateCols}" \
	--glm hide-covar firth firth-residualize single-prec-cc \
	--threads "${threadnum}" \
	--out 1kgeas
