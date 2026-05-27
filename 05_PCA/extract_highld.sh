#!/bin/bash
# Module: 05_PCA | Script: extract_highld.sh
# Prerequisites: 04_Data_QC/sample_data.clean, high-ld-hg19.txt
# Steps: exclude_hild

set -euo pipefail
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$(dirname "$0")"

export PATH="${HOME}/tools/bin:${PATH:-}"

plinkFile="${REPO_ROOT}/04_Data_QC/sample_data.clean"
hildList="high-ld-hg19.txt"

# Step: exclude_hild
plink \
	--bfile "${plinkFile}" \
	--make-set "${hildList}" \
	--write-set \
	--out hild
