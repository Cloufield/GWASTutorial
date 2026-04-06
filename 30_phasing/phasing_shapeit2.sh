#!/usr/bin/env bash
# Reference-based SHAPEIT2 phasing. Expects sample_data.clean.alignment from prepare.phasing.sh. Run from 30_phasing/.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# --- configure (override with env vars if needed) ---
CHR="${CHR:-22}"
MAF_THRESH="${MAF_THRESH:-0.05}"
ALIGNED_BFILE="./sample_data.clean.alignment"
SUBSET_PREFIX="./sample_data.chr22.clean"
SHAPEIT_STUDY_PREFIX="./sample_data.chr22.shapeit_ref"
SHAPEIT_REF_EXTRACT_SNPS="./shapeit_chr22.refpanel_snps.txt"
JPT_SAMPLE="../01_Dataset/JPT.sample"
POSITIONS_FILE="${SHAPEIT_PANEL_POSITIONS:-${SCRIPT_DIR}/chr22_phase1_shapeit_panel_positions.txt}"

SHAPEIT2_REFERENCE_DIR="${SHAPEIT2_REFERENCE_DIR:-${HOME}/tools/shapeit2/shapeit.v2.904.3.10.0-693.11.6.el7.x86_64/reference/ALL.integrated_phase1_SHAPEIT_16-06-14.nomono}"
SHAPEIT2_GENETIC_MAP="${SHAPEIT2_REFERENCE_DIR}/genetic_map_chr${CHR}_combined_b37.txt"
SHAPEIT2_REFHAP_GZ="${SHAPEIT2_REFERENCE_DIR}/ALL.chr${CHR}.integrated_phase1_v3.20101123.snps_indels_svs.genotypes.nomono.haplotypes.gz"
SHAPEIT2_REFLEGEND_GZ="${SHAPEIT2_REFERENCE_DIR}/ALL.chr${CHR}.integrated_phase1_v3.20101123.snps_indels_svs.genotypes.nomono.legend.gz"
SHAPEIT2_REFSAMPLE="${SHAPEIT2_REFERENCE_DIR}/ALL.integrated_phase1_v3.20101123.snps_indels_svs.genotypes.sample"
OUT_PREFIX_SHAPEIT="./1KG.JPT.chr${CHR}.phased.shapeit2.reference_based"

plink2 \
	--bfile "${ALIGNED_BFILE}" \
	--keep "${JPT_SAMPLE}" \
	--maf "${MAF_THRESH}" \
	--chr "${CHR}" \
	--make-bed \
	--out "${SUBSET_PREFIX}"

awk -v chr="${CHR}" -v posfile="${POSITIONS_FILE}" '
BEGIN {
	while ((getline p < posfile) > 0) {
		if (p ~ /^#/ || p == "") continue
		keep[p + 0] = 1
	}
	close(posfile)
}
$1 == chr && keep[$4] {
	print $2
}' "${SUBSET_PREFIX}.bim" > "${SHAPEIT_REF_EXTRACT_SNPS}"

plink2 \
	--bfile "${SUBSET_PREFIX}" \
	--extract "${SHAPEIT_REF_EXTRACT_SNPS}" \
	--make-bed \
	--out "${SHAPEIT_STUDY_PREFIX}"

out="${OUT_PREFIX_SHAPEIT}"
outputhaps="${out}.haps"
outputsample="${out}.sample"
outputlog="${out}"
outputlogcheck="${out}.check"

shapeit -check \
	-B "${SHAPEIT_STUDY_PREFIX}" \
	-M "${SHAPEIT2_GENETIC_MAP}" \
	--input-ref "${SHAPEIT2_REFHAP_GZ}" "${SHAPEIT2_REFLEGEND_GZ}" "${SHAPEIT2_REFSAMPLE}" \
	--output-log "${outputlogcheck}"

excludesnp="${outputlogcheck}.snp.strand.exclude"
echo "EAS" > "${SCRIPT_DIR}/group.list"
includegrp="${SCRIPT_DIR}/group.list"

shapeit --input-bed "${SHAPEIT_STUDY_PREFIX}" \
	--input-map "${SHAPEIT2_GENETIC_MAP}" \
	--input-ref "${SHAPEIT2_REFHAP_GZ}" "${SHAPEIT2_REFLEGEND_GZ}" "${SHAPEIT2_REFSAMPLE}" \
	--output-max "${outputhaps}" "${outputsample}" \
	--output-log "${outputlog}" \
	--exclude-snp "${excludesnp}" \
	--thread 1 \
	--include-grp "${includegrp}" \
	--seed 123 \
	--states 200 \
	--window 2

outputvcf="${out}.vcf"
shapeit \
	-convert \
	--input-haps "${outputhaps}" "${outputsample}" \
	--output-vcf "${outputvcf}"

bgzip -f "${outputvcf}"
tabix -p vcf "${outputvcf}.gz"
