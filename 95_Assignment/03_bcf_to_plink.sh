#!/bin/bash
for chr in {1..22}
do
plink \
      --bcf ALL.chr"${chr}".phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.bcf \
      --keep-allele-order \
      --vcf-idspace-to _ \
      --const-fid \
      --allow-extra-chr 0 \
      --split-x b37 no-fail \
      --make-bed \
      --out ALL.chr"${chr}".phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes 
done
