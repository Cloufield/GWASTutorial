#!/bin/bash
mkdir -p 1kg-norm-nodup
gunzip 1kg/human_g1k_v37.fasta.gz

for chr in {1..22}
do
    bcftools norm -m-any --check-ref w -f 1kg/human_g1k_v37.fasta \
      1kg/ALL.chr"${chr}".phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz | \
      bcftools annotate -x ID -I +'%CHROM:%POS:%REF:%ALT' | \
        bcftools norm -Ob --rm-dup both \
          > 1kg-norm-nodup/ALL.chr"${chr}".phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.bcf ;

    bcftools index 1kg-norm-nodup/ALL.chr"${chr}".phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.bcf ;
done

