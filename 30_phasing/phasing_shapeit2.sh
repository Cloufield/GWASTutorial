#!/bin/bash 
inputbed=./sample_data.clean.alignment
jptsample=../01_Dataset/JPT.sample
inputbedchr22=./sample_data.chr22.clean

plink2 \
        --bfile ${inputbed} \
        --make-bed \
	--keep ${jptsample} \
	--maf 0.05 \
        --chr 22 \
        --out ${inputbedchr22}

geneticmap=~/tools/shapeit2/shapeit.v2.904.3.10.0-693.11.6.el7.x86_64/reference/ALL.integrated_phase1_SHAPEIT_16-06-14.nomono/genetic_map_chr22_combined_b37.txt

out=./1KG.JPT.chr22.phased.shapeit2.reference_based
outputhaps=${out}.haps
outputsample=${out}.sample
outputlog=${out}
outputlogcheck=${out}.check


inputrefhap=~/tools/shapeit2/shapeit.v2.904.3.10.0-693.11.6.el7.x86_64/reference/ALL.integrated_phase1_SHAPEIT_16-06-14.nomono/ALL.chr22.integrated_phase1_v3.20101123.snps_indels_svs.genotypes.nomono.haplotypes.gz
inputreflegend=~/tools/shapeit2/shapeit.v2.904.3.10.0-693.11.6.el7.x86_64/reference/ALL.integrated_phase1_SHAPEIT_16-06-14.nomono/ALL.chr22.integrated_phase1_v3.20101123.snps_indels_svs.genotypes.nomono.legend.gz
inputrefsample=~/tools/shapeit2/shapeit.v2.904.3.10.0-693.11.6.el7.x86_64/reference/ALL.integrated_phase1_SHAPEIT_16-06-14.nomono/ALL.integrated_phase1_v3.20101123.snps_indels_svs.genotypes.sample

shapeit -check \
        -B ${inputbedchr22} \
        -M ${geneticmap} \
        --input-ref ${inputrefhap} ${inputreflegend} ${inputrefsample} \
        --output-log ${outputlogcheck}

excludesnp=${outputlogcheck}.snp.strand.exclude
echo "EAS" > group.list
includegrp=group.list

shapeit --input-bed ${inputbedchr22} \
        --input-map ${geneticmap} \
	--input-ref ${inputrefhap} ${inputreflegend} ${inputrefsample} \
        --output-max ${outputhaps} ${outputsample} \
        --output-log ${outputlog} \
        --exclude-snp  ${excludesnp} \
	--thread 1 \
	--include-grp ${includegrp} \
	--seed 123 \
	--states 200 \
	--window 2

outputvcf=${out}.vcf
shapeit \
    -convert \
	--input-haps ${outputhaps} ${outputsample} \
    --output-vcf ${outputvcf}

bgzip ${outputvcf} && \
tabix -p vcf ${outputvcf}.gz
