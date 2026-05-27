#!/bin/bash
# Module: 12_fine_mapping | Script: calculate_ldr.sh
# Step: calculate_ld

set -euo pipefail
cd "$(dirname "$0")"

plinkFile="../01_Dataset/1KG.EAS.auto.snp.norm.nodup.split.rare002.common015.missing"

plink \
  --bfile ${plinkFile} \
  --keep-allele-order \
  --r square \
  --extract sig_locus.snplist \
  --out sig_locus_mt

plink \
  --bfile ${plinkFile} \
  --keep-allele-order \
  --r2 square \
  --extract sig_locus.snplist \
  --out sig_locus_mt_r2
