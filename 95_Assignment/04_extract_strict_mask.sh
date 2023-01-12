#!/bin/bash

touch strict_mask_variants.txt
touch high_ld_variants.txt

for chr in {1..22}
do
plink \
      --bfile ALL.chr"${chr}".phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes \
      --make-set 20141020.strict_mask.whole_genome.bed \
      --write-set \
      --out strict_mask_chr${chr}

cat "strict_mask_chr${chr}.set" >>strict_mask_variants.txt

plink \
      --bfile ALL.chr"${chr}".phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes \
      --make-set high_ld_hg19.txt \
      --write-set \
      --out high_ld_chr${chr}

cat "high_ld_chr${chr}.set" >>high_ld_variants.txt
done


