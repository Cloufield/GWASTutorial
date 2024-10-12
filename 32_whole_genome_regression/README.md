

# Whole-genome regression : REGENIE

## Concepts

### Overview

!!! quote "Overview of REGENIE"
    Reference: https://rgcgithub.github.io/regenie/overview/

### Whole genome model

### Stacked regressions

### Firth correction

## Tutorial

### Installation

Please check [here](https://rgcgithub.github.io/regenie/install/)

### Step1

!!! example "Sample codes for running step 1"
    ```
    plinkFile=../01_Dataset/1KG.EAS.auto.snp.norm.nodup.split.rare002.common015.missing
    phenoFile=../01_Dataset/1kgeas_binary_regenie.txt
    covarFile=../05_PCA/plink_results_projected.sscore
    covarList="PC1_AVG,PC2_AVG,PC3_AVG,PC4_AVG,PC5_AVG,PC6_AVG,PC7_AVG,PC8_AVG,PC9_AVG,PC10_AVG"
    extract=../05_PCA/plink_results.prune.in
    
    # revise the header of covariate file
    sed -i 's/#FID/FID/' ../05_PCA/plink_results_projected.sscore
    mkdir tmpdir
    
    regenie \
      --step 1 \
      --bed ${plinkFile} \
      --extract ${extract} \
      --phenoFile ${phenoFile} \
      --covarFile ${covarFile} \
      --covarColList ${covarList} \
      --bt \
      --bsize 1000 \
      --lowmem \
      --lowmem-prefix tmpdir/regenie_tmp_preds \
      --out 1kg_eas_step1_BT
    ```


### Step2

!!! example "Sample codes for running step 2"
    ```
    plinkFile=../01_Dataset/1KG.EAS.auto.snp.norm.nodup.split.rare002.common015.missing
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
    ```

### Visualization

## Reference
- Mbatchou, J., Barnard, L., Backman, J., Marcketta, A., Kosmicki, J. A., Ziyatdinov, A., ... & Marchini, J. (2021). Computationally efficient whole-genome regression for quantitative and binary traits. Nature genetics, 53(7), 1097-1103.

