#!/bin/bash
for chr in $(seq 1 22)
do
echo $chr
wget -P ./1kg/ ftp://ftp-trace.ncbi.nih.gov/1000genomes/ftp/release/20130502/ALL.chr${chr}.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz
wget -P ./1kg/ ftp://ftp-trace.ncbi.nih.gov/1000genomes/ftp/release/20130502/ALL.chr${chr}.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz.tbi
done

wget -P ./1kg/ ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/technical/reference/human_g1k_v37.fasta.gz
wget -P ./1kg/ ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/technical/reference/human_g1k_v37.fasta.fai 

wget -P ./1kg/ ftp://ftp-trace.ncbi.nih.gov/1000genomes/ftp/release/20130502/integrated_call_samples_v3.20130502.ALL.panel
wget -P ./1kg/ ftp://ftp-trace.ncbi.nih.gov/1000genomes/ftp/release/20130502/supporting/accessible_genome_masks/20141020.strict_mask.whole_genome.bed
