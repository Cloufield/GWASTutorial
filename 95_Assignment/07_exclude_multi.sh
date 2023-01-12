#!/bin/bash

for chr in {1..22}
do

plink \
      --bfile ALL.chr"${chr}".phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes \
      --extract ALL.ldpruned.nohla.common.strict.chr${chr}.prune.in \
      --exclude ALL.ldpruned.nohla.common.strict.all-merge.missnp \
      --make-bed \
      --out ALL.ldpruned.nohla.common.strict.chr${chr}


done


