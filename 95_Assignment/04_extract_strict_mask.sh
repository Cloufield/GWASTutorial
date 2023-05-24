#!/bin/bash
mkdir -p 1kg-prune

touch strict_mask_variants.txt
touch high_ld_variants.txt

for chr in {1..22}
do
plink \
      --bfile 1kg-plink/ALL.chr"${chr}".phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes \
      --make-set 1kg/20141020.strict_mask.whole_genome.bed \
      --write-set \
      --out 1kg-prune/strict_mask_chr${chr}

cat "1kg-prune/strict_mask_chr${chr}.set" >>strict_mask_variants.txt

plink \
      --bfile 1kg-plink/ALL.chr"${chr}".phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes \
      --make-set high_ld_hg19.txt \
      --write-set \
      --out 1kg-prune/high_ld_chr${chr}

cat "1kg-prune/high_ld_chr${chr}.set" >>high_ld_variants.txt
done


