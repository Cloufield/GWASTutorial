#!/bin/bash

plinkFile="../01_Dataset/1KG.EAS.auto.snp.norm.nodup.split.maf005.thinp020"

gcta \
  --bfile ${plinkFile} \
  --autosome \
  --maf 0.01 \
  --make-grm \
  --out 1kg_eas
