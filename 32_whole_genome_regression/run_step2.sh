#/bin/bash

plinkFile=../01_Dataset/1KG.EAS.auto.snp.norm.nodup.split.maf005.thinp020
phenoFile=../01_Dataset/1kgeas_binary_regenie.txt
covarFile=../05_PCA/plink_results_projected.sscore
covarList="PC1_AVG,PC2_AVG,PC3_AVG,PC4_AVG,PC5_AVG,PC6_AVG,PC7_AVG,PC8_AVG,PC9_AVG,PC10_AVG"
extract=../05_PCA/plink_results.prune.in

sed -i 's/#FID/FID/' ../05_PCA/plink_results_projected.sscore
mkdir tmpdir

regenie \
  --step 2 \
  --bed ${plinkFile} \
  --ref-first \
  --phenoFile ${phenoFile} \
  --covarFile ${covarFile} \
  --covarColList ${covarList} \
  --bt \
  --bsize 400 \
  --firth --approx --pThresh 0.01 \
  --pred 1kg_eas_step1_BT_pred.list \
  --out 1kg_eas_step1_BT
