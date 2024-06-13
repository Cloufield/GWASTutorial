#!/bin/bash
plinkFile=../04_Data_QC/sample_data.clean
sumStats=./t2d_plink_reduced.txt

plink \
    --bfile ${plinkFile} \
    --clump-p1 1 \
    --clump-r2 0.1 \
    --clump-kb 250 \
    --clump ${sumStats} \
    --clump-snp-field SNPID \
    --clump-field "p.value" \
    --memory 4000 \
    --out 1kgeas

awk 'NR!=1{print $3}' 1kgeas.clumped >  1kgeas.valid.snp
awk '{print $1,$4}' ${sumStats} > SNP.pvalue

echo "pT0.001 0 0.001" > range_list 
echo "pT0.05 0 0.05" >> range_list
echo "pT0.1 0 0.1" >> range_list
echo "pT0.2 0 0.2" >> range_list
echo "pT0.3 0 0.3" >> range_list
echo "pT0.4 0 0.4" >> range_list
echo "pT0.5 0 0.5" >> range_list

plink2 \
    --bfile ${plinkFile} \
    --score ${sumStats} 1 2 3 header cols=nallele,scoreavgs,denom,scoresums\
    --q-score-range range_list SNP.pvalue \
    --extract 1kgeas.valid.snp \
    --out 1kgeas

# First, we need to perform prunning
plink2 \
    --bfile ${plinkFile} \
    --indep-pairwise 200 50 0.25 \
    --out 1kgeas
# Then we calculate the first 5 PCs
plink2 \
    --bfile ${plinkFile} \
    --extract 1kgeas.prune.in \
    --pca 5 \
    --out 1kgeas
