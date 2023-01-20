#!/bin/bash

plinkFile=../01_Dataset/1KG.EAS.auto.snp.norm.nodup.split.maf005.thinp020
sumStats=../06_Association_tests/1kgeas.B1.glm.firth

plink \
    --bfile ${plinkFile} \
    --clump-p1 0.0001 \
    --clump-r2 0.1 \
    --clump-kb 250 \
    --clump ${sumStats} \
    --clump-snp-field ID \
    --clump-field P \
    --out 1kg_eas
