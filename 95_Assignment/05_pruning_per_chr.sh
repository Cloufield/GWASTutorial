#!/bin/bash

touch mergelist.txt

for chr in {1..22}
do
plink \
      --bfile 1kg-plink/ALL.chr"${chr}".phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes \
      --maf 0.05 \
      --extract strict_mask_variants.txt \
      --exclude	high_ld_variants.txt \
      --indep-pairwise 500 50 0.2 \
      --out 1kg-prune/ALL.ldpruned.nohla.common.strict.chr${chr}

plink \
      --bfile 1kg-plink/ALL.chr"${chr}".phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes \
      --extract 1kg-prune/ALL.ldpruned.nohla.common.strict.chr${chr}.prune.in \
      --make-bed \
      --out 1kg-prune/ALL.ldpruned.nohla.common.strict.chr${chr}

echo "1kg-prune/ALL.ldpruned.nohla.common.strict.chr${chr}" >>mergelist.txt

done


