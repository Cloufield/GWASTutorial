#!/bin/bash
# Module: 14_gcta_greml | Script: 3_gcta_reml.sh
# Step: reml

set -euo pipefail
cd "$(dirname "$0")"

REPO_ROOT="$(cd .. && pwd)"
GRM=1kg_eas
phenotypeFile="${REPO_ROOT}/01_Dataset/1kgeas_binary.txt"
prevalence=0.5

awk '{print $1,$2,$5,$6,$7,$8,$9}' "${REPO_ROOT}/05_PCA/plink_results_projected.sscore" > 5PCs.txt

gcta \
	--grm "${GRM}" \
	--pheno "${phenotypeFile}" \
	--prevalence "${prevalence}" \
	--qcovar 5PCs.txt \
	--reml \
	--out 1kg_eas
