#!/bin/bash

#the grm we calculated in step1
GRM=1kg_eas

# phenotype file
phenotypeFile=../01_Dataset/1kgeas_binary.txt

# disease prevalence used for conversion to liability-scale heritability
prevalence=0.5

# use 5PCs as covariates 
awk '{print $1,$2,$5,$6,$7,$8,$9}' ../05_PCA/plink_results_projected.sscore > 5PCs.txt

gcta \
  --grm ${GRM} \
  --pheno ${phenotypeFile} \
  --prevalence ${prevalence} \
  --qcovar  5PCs.txt \
  --reml \
  --out 1kg_eas
