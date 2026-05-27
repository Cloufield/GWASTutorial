#!/bin/bash
# Module: 05_PCA | Script: run_pca.sh
# Prerequisites: 04_Data_QC/sample_data.clean.{bed,bim,fam}, high-ld-hg19.txt
# Steps: exclude_hild | prune | king | pca | project

set -euo pipefail
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$(dirname "$0")"

plinkFile="${REPO_ROOT}/04_Data_QC/sample_data.clean"
outPrefix="plink_results"
threadnum=2
hildList="high-ld-hg19.txt"

export PATH="${HOME}/tools/bin:${PATH:-}"

# Step: exclude_hild
plink \
	--bfile "${plinkFile}" \
	--make-set "${hildList}" \
	--write-set \
	--out hild

# Step: prune
plink2 \
	--bfile "${plinkFile}" \
	--maf 0.01 \
	--exclude hild.set \
	--threads "${threadnum}" \
	--indep-pairwise 500 50 0.2 \
	--out "${outPrefix}"

# Step: king
plink2 \
	--bfile "${plinkFile}" \
	--extract "${outPrefix}.prune.in" \
	--king-cutoff 0.0884 \
	--threads "${threadnum}" \
	--out "${outPrefix}"

# Step: pca
plink2 \
	--bfile "${plinkFile}" \
	--keep "${outPrefix}.king.cutoff.in.id" \
	--extract "${outPrefix}.prune.in" \
	--freq counts \
	--threads "${threadnum}" \
	--pca approx allele-wts 10 \
	--out "${outPrefix}"

# Step: project
plink2 \
	--bfile "${plinkFile}" \
	--threads "${threadnum}" \
	--read-freq "${outPrefix}.acount" \
	--score "${outPrefix}.eigenvec.allele" 2 6 header-read no-mean-imputation variance-standardize \
	--score-col-nums 7-16 \
	--out "${outPrefix}_projected"
