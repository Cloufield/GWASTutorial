#!/bin/bash

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
