#!/bin/bash

plinkFile="../01_Dataset/1KG.EAS.auto.snp.norm.nodup.split.maf005.thinp020"

plink \
  --bfile ${plinkFile} \
  --keep-allele-order \
  --r square \
  --extract sig_locus.snplist \
  --out sig_locus_mt
