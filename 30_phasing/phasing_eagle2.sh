#!/bin/bash 
inputbed=./sample_data.clean.alignment
jptsample=../01_Dataset/JPT.sample
inputbedchr22=./sample_data.chr22.clean

geneticmap=~/tools/eagle/genetic_map_hg19_withX.txt.gz
out=./1KG.JPT.chr22.phased.eagle2.cohort_based

eagle \
    --bfile=${inputbedchr22} \
    --geneticMapFile=${geneticmap} \
    --outPrefix=${out} \
    --maxMissingPerSnp=1 \
    --maxMissingPerIndiv=1 \
    --numThreads=4 \
    --chrom=22

outputhaps=${out}.haps.gz
outputsample=${out}.sample
outputvcf=${out}.vcf

shapeit \
    -convert \
    --input-haps ${outputhaps} ${outputsample} \
    --output-vcf ${outputvcf}

bgzip ${outputvcf} && \
tabix -p vcf ${outputvcf}.gz
