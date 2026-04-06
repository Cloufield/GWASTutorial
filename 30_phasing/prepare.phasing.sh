#!/usr/bin/env bash
# Align alleles to the reference FASTA (PLINK 2 --ref-from-fa). Run from 30_phasing/.
set -euo pipefail

# --- configure (override with env vars if needed) ---
REF_FASTA="${REF_FASTA:-${HOME}/refs/human_g1k_v37.fasta}"
CLEAN_BFILE="../04_Data_QC/sample_data.clean"
ALIGNED_BFILE="./sample_data.clean.alignment"

plink2 \
	--bfile "${CLEAN_BFILE}" \
	--fa "${REF_FASTA}" \
	--ref-from-fa \
	--make-bed \
	--out "${ALIGNED_BFILE}"
