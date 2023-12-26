#!/bin/bash

awk '{print $1,$2,$5,$6,$7,$8,$9}' ../05_PCA/plink_results_projected.sscore > 5PCs.txt

gcta \
  --grm 1kg_eas \
  --pheno ../01_Dataset/1kgeas_binary_gcta.txt \
  --prevalence 0.5 \
  --qcovar  5PCs.txt \
  --reml \
  --out 1kg_eas
