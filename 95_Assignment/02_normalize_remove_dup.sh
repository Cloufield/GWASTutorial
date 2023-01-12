#!/bin/bash
for chr in {1..22}
do
    bcftools norm -m-any --check-ref w -f human_g1k_v37.fasta \
      ALL.chr"${chr}".phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz | \
      bcftools annotate -I +'%CHROM:%POS:%REF:%ALT' | \
        bcftools norm -Ob --rm-dup both \
          > ALL.chr"${chr}".phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.bcf ;

    bcftools index ALL.chr"${chr}".phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.bcf ;
done

