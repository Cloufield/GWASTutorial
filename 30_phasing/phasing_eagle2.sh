#!/usr/bin/env bash
# Cohort phasing with Eagle2. Expects sample_data.clean.alignment from prepare.phasing.sh. Run from 30_phasing/.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# --- configure (override with env vars if needed) ---
CHR="${CHR:-22}"
MAF_THRESH="${MAF_THRESH:-0.05}"
ALIGNED_BFILE="./sample_data.clean.alignment"
SUBSET_PREFIX="./sample_data.chr22.clean"
JPT_SAMPLE="../01_Dataset/JPT.sample"
EAGLE_GENETIC_MAP="${EAGLE_GENETIC_MAP:-${HOME}/tools/eagle/genetic_map_hg19_withX.txt.gz}"
OUT_PREFIX_EAGLE="./1KG.JPT.chr${CHR}.phased.eagle2.cohort_based"

plink2 \
	--bfile "${ALIGNED_BFILE}" \
	--keep "${JPT_SAMPLE}" \
	--maf "${MAF_THRESH}" \
	--chr "${CHR}" \
	--make-bed \
	--out "${SUBSET_PREFIX}"

out="${OUT_PREFIX_EAGLE}"
eagle \
	--bfile="${SUBSET_PREFIX}" \
	--geneticMapFile="${EAGLE_GENETIC_MAP}" \
	--outPrefix="${out}" \
	--maxMissingPerSnp=1 \
	--maxMissingPerIndiv=1 \
	--numThreads=4 \
	--chrom="${CHR}"

outputhaps="${out}.haps.gz"
outputsample="${out}.sample"
outputvcf="${out}.vcf"
shapeit \
	-convert \
	--input-haps "${outputhaps}" "${outputsample}" \
	--output-vcf "${outputvcf}"

bgzip -f "${outputvcf}"
tabix -p vcf "${outputvcf}.gz"
