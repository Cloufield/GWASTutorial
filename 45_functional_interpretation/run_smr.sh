#!/bin/bash
# =============================================================================
# SMR analysis: T2D (BBJ) GWAS x EAS mQTL (Hatton et al. 2024)
#
# Input:
#   - GWAS: T2D BBJ summary statistics (10_PRS/t2d_bbj_v2.tar.gz)
#   - mQTL: Hatton et al. (2024) blood mQTL in BESD format (EAS)
#   - LD ref: 1KG EAS (01_Dataset/)
# =============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
WORK_DIR="${SCRIPT_DIR}"
DATA_DIR="${SCRIPT_DIR}/../10_PRS"
LD_REF_ORIG="${SCRIPT_DIR}/../01_Dataset/1KG.EAS.auto.snp.norm.nodup.split.rare002.common015.missing"
LD_REF="${WORK_DIR}/1KG_EAS_rsid"

MQTL_URL="https://yanglab.westlake.edu.cn/data/SMR/EAS.tar.gz"
MQTL_DIR="${WORK_DIR}/EAS_mQTL"

GWAS_MA="${WORK_DIR}/t2d_bbj.ma"
OUTPUT="${WORK_DIR}/t2d_smr_mqtl"

# -----------------------------------------------------------------------------
# Helper: filter SMR results by Bonferroni-corrected p_SMR and p_HEIDI
# -----------------------------------------------------------------------------
filter_smr_results() {
    local smr_file="$1"
    local filtered_file="$2"
    local label="$3"

    if [ ! -f "${smr_file}" ]; then
        echo ">>> ${label}: output file not found, skipping filter."
        return
    fi

    local n_probes
    n_probes=$(awk 'NR>1' "${smr_file}" | wc -l)
    if [ "${n_probes}" -eq 0 ]; then
        echo ">>> ${label}: no probes in results."
        return
    fi

    local smr_thresh
    smr_thresh=$(awk "BEGIN { printf \"%.6e\", 0.05 / ${n_probes} }")
    local heidi_thresh=0.05

    echo ""
    echo ">>> Filtering ${label} results..."
    echo ">>>   Number of probes tested: ${n_probes}"
    echo ">>>   p_SMR threshold (Bonferroni): ${smr_thresh}"
    echo ">>>   p_HEIDI threshold: >= ${heidi_thresh}"

    awk -v smr_t="${smr_thresh}" -v heidi_t="${heidi_thresh}" '
        NR == 1 { print; next }
        $19+0 < smr_t+0 && ($20 == "NA" || $20+0 >= heidi_t+0)
    ' "${smr_file}" > "${filtered_file}"

    local n_hits
    n_hits=$(awk 'NR>1' "${filtered_file}" | wc -l)
    echo ">>>   Pleiotropic hits: ${n_hits}"

    if [ "${n_hits}" -gt 0 ]; then
        echo ""
        echo ">>> Filtered results (saved to ${filtered_file}):"
        column -t "${filtered_file}"
    else
        echo ">>> No probes passed both thresholds."
    fi
}

# -----------------------------------------------------------------------------
# Step 1: Extract T2D BBJ GWAS summary statistics
# -----------------------------------------------------------------------------
T2D_GZ="${DATA_DIR}/T2D.auto.rsq07.mac10.txt.gz"

if [ ! -f "${T2D_GZ}" ]; then
    echo ">>> Extracting T2D BBJ archive..."
    tar -xzf "${DATA_DIR}/t2d_bbj_v2.tar.gz" -C "${DATA_DIR}"
fi

# -----------------------------------------------------------------------------
# Step 2: Download and extract EAS mQTL BESD data
# -----------------------------------------------------------------------------
if [ ! -d "${MQTL_DIR}" ]; then
    echo ">>> Downloading EAS mQTL data (this may take a while, ~2.5 GB)..."
    wget -q -O "${WORK_DIR}/EAS.tar.gz" "${MQTL_URL}"

    echo ">>> Extracting mQTL data..."
    mkdir -p "${MQTL_DIR}"
    tar -xzf "${WORK_DIR}/EAS.tar.gz" -C "${MQTL_DIR}"
    rm -f "${WORK_DIR}/EAS.tar.gz"
else
    echo ">>> EAS mQTL data already exists, skipping download."
fi

# Discover the BESD prefix (find the .besd file inside the extracted directory)
MQTL_PREFIX=$(find "${MQTL_DIR}" -name "*.besd" -print -quit | sed 's/\.besd$//')

if [ -z "${MQTL_PREFIX}" ]; then
    echo "ERROR: No .besd file found in ${MQTL_DIR}. Check the archive structure."
    exit 1
fi
echo ">>> mQTL BESD prefix: ${MQTL_PREFIX}"

# -----------------------------------------------------------------------------
# Step 3: Build chr:pos -> rsID mapping from mQTL .esi file
#
# The mQTL .esi uses rsIDs while the LD reference .bim and GWAS data use
# chr:pos:ref:alt format. We remap both the GWAS .ma and LD reference .bim
# to rsIDs so all three datasets share a common SNP identifier.
# -----------------------------------------------------------------------------
MAPPING="${WORK_DIR}/chrpos_to_rsid.txt"

if [ ! -f "${MAPPING}" ]; then
    echo ">>> Building chr:pos -> rsID mapping from mQTL .esi file..."
    awk '{ print $1":"$4, $2 }' "${MQTL_PREFIX}.esi" > "${MAPPING}"
    echo ">>> Mapping file: $(wc -l < "${MAPPING}") entries"
fi

# -----------------------------------------------------------------------------
# Step 4: Convert T2D GWAS to GCTA-COJO format (.ma) with rsIDs
#
# T2D columns (space-delimited):
#   CHR POS SNPID Allele1 Allele2 AC_Allele2 AF_Allele2 N BETA SE ...  p.value ...
#
# COJO .ma format:
#   SNP  A1  A2  freq  b  se  p  n
#
# A1 = Allele2 (effect allele, BETA corresponds to Allele2).
# SNP IDs are mapped from chr:pos to rsIDs using the mQTL .esi mapping.
# SNPs without a matching rsID are dropped.
# -----------------------------------------------------------------------------
if [ ! -f "${GWAS_MA}" ]; then
    echo ">>> Converting T2D GWAS to COJO .ma format (with rsID mapping)..."
    zcat "${T2D_GZ}" | awk '
        NR == FNR { map[$1] = $2; next }
        FNR == 1  { print "SNP\tA1\tA2\tfreq\tb\tse\tp\tn"; next }
        {
            key = $1":"$2
            if (key in map) {
                print map[key]"\t"$5"\t"$4"\t"$7"\t"$9"\t"$10"\t"$12"\t"$8
            }
        }
    ' "${MAPPING}" - > "${GWAS_MA}"
    echo ">>> Created ${GWAS_MA} ($(wc -l < "${GWAS_MA}") lines)"
else
    echo ">>> COJO .ma file already exists, skipping conversion."
fi

# -----------------------------------------------------------------------------
# Step 5: Create LD reference panel with rsIDs
#
# Copy .bed/.fam from the original reference and generate a new .bim
# with rsIDs mapped from the mQTL .esi file.
# SNPs without a mapping retain their original chr:pos:ref:alt ID.
# -----------------------------------------------------------------------------
if [ ! -f "${LD_REF}.bed" ]; then
    echo ">>> Creating LD reference with rsIDs..."
    cp "${LD_REF_ORIG}.bed" "${LD_REF}.bed"
    cp "${LD_REF_ORIG}.fam" "${LD_REF}.fam"

    awk '
        NR == FNR { map[$1] = $2; next }
        {
            key = $1":"$4
            if (key in map) $2 = map[key]
            print $1"\t"$2"\t"$3"\t"$4"\t"$5"\t"$6
        }
    ' "${MAPPING}" "${LD_REF_ORIG}.bim" > "${LD_REF}.bim"
    echo ">>> LD reference created at ${LD_REF}"
else
    echo ">>> LD reference with rsIDs already exists, skipping."
fi

# -----------------------------------------------------------------------------
# Step 6: Run SMR & HEIDI analysis with EAS mQTL
# -----------------------------------------------------------------------------
echo "==========================================================================="
echo "T2D (EAS) x EAS mQTL (Hatton et al. 2024)"
echo "All datasets are ancestry-matched (East Asian)."
echo "==========================================================================="

echo ">>> Running SMR & HEIDI analysis (mQTL)..."
smr \
    --bfile "${LD_REF}" \
    --gwas-summary "${GWAS_MA}" \
    --beqtl-summary "${MQTL_PREFIX}" \
    --maf 0.01 \
    --diff-freq 1 \
    --thread-num 4 \
    --out "${OUTPUT}"

echo ""
echo ">>> mQTL SMR analysis complete. Results: ${OUTPUT}.smr"

filter_smr_results "${OUTPUT}.smr" "${OUTPUT}.filtered.smr" "mQTL"
