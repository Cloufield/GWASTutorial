#!/bin/bash

plinkFile="../04_Data_QC/sample_data.clean"
prunedSNP="../04_Data_QC/plink_results.prune.in"

gcta \
  --bfile ${plinkFile} \
  --extract ${prunedSNP} \
  --autosome \
  --maf 0.01 \
  --make-grm \
  --out 1kg_eas

