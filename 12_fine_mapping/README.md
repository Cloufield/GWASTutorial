# Fine-mapping (under construction)

## Introduction

## File Preparation



## LD Matrix Calculation

!!! example Calculate LD matrix using PLINK
    ```
    plinkFile="../01_Dataset/1KG.EAS.auto.snp.norm.nodup.split.maf005.thinp020"
    
    plink \
      --bfile ${plinkFile} \
      --keep-allele-order \
      --r square \
      --extract sig_locus.snplist \
      --out sig_locus_mt
    
    ```
    
    Take a look at the LD matrix (first 5 rows and columns)

    ```
    head -5 sig_locus_mt.ld | cut -f 1-5

    1	-0.766746	0.850204	-0.173798	-0.359618
    -0.766746	1	-0.646211	0.207611	0.483833
    0.850204	-0.646211	1	-0.134361	-0.306715
    -0.173798	0.207611	-0.134361	1	-0.155776
    -0.359618	0.483833	-0.306715	-0.155776	1
    
    ```
    
Heatmap of the LD matrix:

![image](https://user-images.githubusercontent.com/40289485/212523500-6ec7cfb9-eda6-4ee0-9dce-463772821ca2.png)

## Fine-mapping using SusieR

## Reference

- Wang, G., Sarkar, A., Carbonetto, P. & Stephens, M. (2020). A simple new approach to variable selection in regression, with application to genetic fine mapping. Journal of the Royal Statistical Society, Series B 82, 1273–1300. https://doi.org/10.1111/rssb.12388
- Zou, Y., Carbonetto, P., Wang, G. & Stephens, M. (2021). Fine-mapping from summary data with the “Sum of Single Effects” model. bioRxiv https://doi.org/10.1101/2021.11.03.467167
- Schaid, Daniel J., Wenan Chen, and Nicholas B. Larson. "From genome-wide associations to candidate causal variants by statistical fine-mapping." Nature Reviews Genetics 19.8 (2018): 491-504.
- Purcell, Shaun, et al. "PLINK: a tool set for whole-genome association and population-based linkage analyses." The American journal of human genetics 81.3 (2007): 559-575.
