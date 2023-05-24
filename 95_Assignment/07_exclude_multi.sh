#!/bin/bash
touch mergelist2.txt

for chr in {1..22}
do

plink \
      --bfile 1kg-plink/ALL.chr"${chr}".phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes \
      --extract 1kg-prune/ALL.ldpruned.nohla.common.strict.chr${chr}.prune.in \
      --exclude 1kg-merge/ALL.ldpruned.nohla.common.strict.all-merge.missnp \
      --make-bed \
      --out 1kg-merge/ALL.ldpruned.nohla.common.strict.chr${chr}

echo "1kg-merge/ALL.ldpruned.nohla.common.strict.chr${chr}" >>mergelist2.txt

done


