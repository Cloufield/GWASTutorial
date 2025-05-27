# Fine-mapping

## Introduction

Fine-mapping : Fine-mapping aims to identify the causal variant(s) within a locus for a disease, given the evidence of the significant association of the locus (or genomic region) in GWAS of a disease.

Fine-mapping using individual data is usually performed by fitting the multiple linear regression model:

$$y = Xb + e$$

- $b = (b_1, …, b_J)^T$ is a vector of genetic effects of variants.

Fine-mapping (using Bayesian methods) aims to estimate the **PIP (posterior inclusion probability)**, which indicates the evidence for SNP j having a non-zero effect (namely, causal).

!!! info "PIP(Posterior Inclusion Probability)"
    PIP is often calculated by the sum of the **posterior probabilities** over all models that include variant j as causal.

    $$ PIP_j:=Pr(b_j\neq0|X,y) $$

!!! info "Bayesian methods and Posterior probability" 
    $$ Pr(M_m | O) = {{Pr(O | M_m) Pr(M_m)}\over{\sum_{i=1}^n{Pr( O | M_i) Pr(M_i)}}} $$

    $O$ : Observed data
    
    $M$ : Models (**the configurations of causal variants** in the context of fine-mapping).
    
    $Pr(M_m | O)$: **Posterior Probability** of Model m
    
    $Pr(O | M_m)$: **Likelihood** (the probability of observing your dataset given Model m is true.)
    
    $Pr(M_m)$: **Prior** distribution of Model m (the probability of Model m being true)
    
    ${\sum_{i=1}^n{Pr( O | M_i) Pr(M_i)}}$: **Evidence** (the probability of observing your dataset), namely $Pr(O)$

!!! info "Credible sets"
    A **credible set** refers to the minimum set of variants that contains all causal SNPs with probability $α$. (Under the single-causal-variant-per-locus assumption, the credible set is calculated by ranking variants based on their posterior probabilities, and then summing these until the cumulative sum is $>α$). We usually report 95% credible sets (α=95%) for fine-mapping analysis.

!!! note "Commonly used tools for fine-mapping"
    
    Methods assuming only **one causal variant** in the locus
    
    - ABF
    
    Methods assuming **multiple causal variants** in the locus
    
    - SUSIE / SUSIE-RSS
    - CAVIAR, CAVIARBF, eCAVIAR
    - FINEMAP

    Methods assuming a small number of **larger causal effects** with a large number of **infinitesimal effects**
    
    - SUSIE-inf
    - FINEMAP-inf

    Methods for **Cross-ancestry** fine-mapping
    
    - SUSIEX
    
    You can check [here](https://cloufield.github.io/CTGCatalog/Tools_Fine_mapping_README/) for more information.

In this tutorial, we will introduce SuSiE as an example. SuSiE stands for Sum of Single Effects” model.

The key idea behind SuSiE is : 

$$b = \sum_{l=1}^L b_l $$

where each vector $b_l = (b_{l1}, …, b_{lJ})^T$ is a so-called **single effect** vector (a vector with only one non-zero element).  L is the upper bound of number of causal variants. And this model could be fitted using **Iterative Bayesian Stepwise Selection (IBSS)**.

For fine-mapping with summary statistics using Susie (SuSiE-RSS), IBSS was modified (IBSS-ss) to take sufficient statistics (which can be computed from other combinations of summary statistics) as input. SuSie will then approximate the sufficient statistics to run fine-mapping. 

!!! quote 
    For details of SuSiE and SuSiE-RSS, please check : Zou, Y., Carbonetto, P., Wang, G., & Stephens, M. (2022). Fine-mapping from summary data with the “Sum of Single Effects” model. PLoS Genetics, 18(7), e1010299. [Link](https://journals.plos.org/plosgenetics/article?id=10.1371/journal.pgen.1010299)



## File Preparation

- Sumstats for the loci
- SNP list for calculating LD matrix

!!! example "Using python to check novel loci and extract the files."
    ```python
    import gwaslab as gl
    import pandas as pd
    import numpy as np
    
    sumstats = gl.Sumstats("../06_Association_tests/1kgeas.B1.glm.firth",fmt="plink2")
    ...
    
    sumstats.basic_check()
    ...
    
    sumstats.get_lead()
    
    Fri Jan 13 23:31:43 2023 Start to extract lead variants...
    Fri Jan 13 23:31:43 2023  -Processing 1122285 variants...
    Fri Jan 13 23:31:43 2023  -Significance threshold : 5e-08
    Fri Jan 13 23:31:43 2023  -Sliding window size: 500  kb
    Fri Jan 13 23:31:44 2023  -Found 59 significant variants in total...
    Fri Jan 13 23:31:44 2023  -Identified 3 lead variants!
    Fri Jan 13 23:31:44 2023 Finished extracting lead variants successfully!
    
    SNPID CHR POS EA  NEA SE  Z P OR  N STATUS
    110723  2:55574452:G:C  2 55574452  C G 0.160948  -5.98392  2.178320e-09  0.381707  503 9960099
    424615  6:29919659:T:C  6 29919659  T C 0.155457  -5.89341  3.782970e-09  0.400048  503 9960099
    635128  9:36660672:A:G  9 36660672  G A 0.160275  5.63422 1.758540e-08  2.467060  503 9960099
    ```
    We will perform fine-mapping for the first significant loci whose lead variant is `2:55574452:G:C`.
    
    
    ```
    # filter in the variants in the this locus.
    
    locus = sumstats.filter_value('CHR==2 & POS>55074452 & POS<56074452')
    locus.fill_data(to_fill=["BETA"])
    locus.harmonize(basic_check=False, ref_seq="/Users/he/mydata/Reference/Genome/human_g1k_v37.fasta")
    locus.data.to_csv("sig_locus.tsv",sep="\t",index=None)
    locus.data["SNPID"].to_csv("sig_locus.snplist",sep="\t",index=None,header=None)
    ```
    
    check in terminal:
    ```bash
    head sig_locus.tsv
    SNPID   CHR     POS     EA      NEA     BETA    SE      Z       P       OR      N       STATUS
    2:54535206:C:T  2       54535206        T       C       0.30028978      0.142461        2.10786 0.0350429       1.35025 503     9960099
    2:54536167:C:G  2       54536167        G       C       0.14885099      0.246871        0.602952        0.546541        1.1605  503     9960099
    2:54539096:A:G  2       54539096        G       A       -0.0038474211   0.288489        -0.0133355      0.98936 0.99616 503     9960099
    2:54540264:G:A  2       54540264        A       G       -0.1536723      0.165879        -0.926409       0.354234        0.857553        503     9960099
    2:54540614:G:T  2       54540614        T       G       -0.1536723      0.165879        -0.926409       0.354234        0.857553        503     9960099
    2:54540621:A:G  2       54540621        G       A       -0.1536723      0.165879        -0.926409       0.354234        0.857553        503     9960099
    2:54540970:T:C  2       54540970        C       T       -0.049506452    0.149053        -0.332144       0.739781        0.951699        503     9960099
    2:54544229:T:C  2       54544229        C       T       -0.14338203     0.151172        -0.948468       0.342891        0.866423        503     9960099
    2:54545593:T:C  2       54545593        C       T       -0.1536723      0.165879        -0.926409       0.354234        0.857553        503     9960099
    
    head  sig_locus.snplist
    2:54535206:C:T
    2:54536167:C:G
    2:54539096:A:G
    2:54540264:G:A
    2:54540614:G:T
    2:54540621:A:G
    2:54540970:T:C
    2:54544229:T:C
    2:54545593:T:C
    2:54546032:C:G
    ```

## LD Matrix Calculation

!!! example Calculate LD matrix using PLINK
    ```
    #!/bin/bash
    
    plinkFile="../01_Dataset/1KG.EAS.auto.snp.norm.nodup.split.rare002.common015.missing/1KG.EAS.auto.snp.norm.nodup.split.rare002.common015.missing"
    
    # LD r matrix
    plink \
      --bfile ${plinkFile} \
      --keep-allele-order \
      --r square \
      --extract sig_locus.snplist \
      --out sig_locus_mt
    
    # LD r2 matrix
    plink \
      --bfile ${plinkFile} \
      --keep-allele-order \
      --r2 square \
      --extract sig_locus.snplist \
      --out sig_locus_mt_r2
    ```
    Take a look at the LD matrix (first 5 rows and columns)
    
    ```
    head -5 sig_locus_mt.ld | cut -f 1-5
    1       -0.145634       0.252616        -0.0876317      -0.0876317
    -0.145634       1       -0.0916734      -0.159635       -0.159635
    0.252616        -0.0916734      1       0.452333        0.452333
    -0.0876317      -0.159635       0.452333        1       1
    -0.0876317      -0.159635       0.452333        1       1
    
    head -5 sig_locus_mt_r2.ld | cut -f 1-5
    1       0.0212091       0.0638148       0.00767931      0.00767931
    0.0212091       1       0.00840401      0.0254833       0.0254833
    0.0638148       0.00840401      1       0.204605        0.204605
    0.00767931      0.0254833       0.204605        1       1
    0.00767931      0.0254833       0.204605        1       1
    ```
    Heatmap of the LD matrix:
    
    ![image](https://user-images.githubusercontent.com/40289485/212523500-6ec7cfb9-eda6-4ee0-9dce-463772821ca2.png)

## Fine-mapping with summary statistics using SusieR 

!!! note Susie in R
    ```
    install.packages("susieR")
    
    # Fine-mapping with summary statistics
    fitted_rss2 = susie_rss(bhat = sumstats$betahat, shat = sumstats$sebetahat, R = R, n = n, L = 10)
    ```
    
    `R` : a `p` x `p` LD r matrix.
    `N` : Sample size.
    `bhat` : Alternative summary data giving the estimated effects (a vector of length `p`). This, together with shat, may be provided instead of z.
    `shat` : Alternative summary data giving the standard errors of the estimated effects (a vector of length `p`). This, together with bhat, may be provided instead of z.
    `L` : Maximum number of non-zero effects in the susie regression model. (defaul : `L = 10`)

!!! quote SusieR tutorial
    
    For deatils, please check [SusieR tutorial - Fine-mapping with susieR using summary statistics](https://stephenslab.github.io/susieR/articles/finemapping_summary_statistics.html)

!!! tip "Use susieR in jupyter notebook (with Python):"
    
    Please check : https://github.com/Cloufield/GWASTutorial/blob/main/12_fine_mapping/finemapping_susie.ipynb

<img width="770" alt="image" src="https://user-images.githubusercontent.com/40289485/212628837-d20c0a59-9a6a-46a5-8c2d-a12fd427c794.png">


## Reference

- Wang, G., Sarkar, A., Carbonetto, P. & Stephens, M. (2020). A simple new approach to variable selection in regression, with application to genetic fine mapping. Journal of the Royal Statistical Society, Series B 82, 1273–1300. https://doi.org/10.1111/rssb.12388
- Zou, Y., Carbonetto, P., Wang, G. & Stephens, M. (2021). Fine-mapping from summary data with the “Sum of Single Effects” model. bioRxiv https://doi.org/10.1101/2021.11.03.467167
- Schaid, Daniel J., Wenan Chen, and Nicholas B. Larson. "From genome-wide associations to candidate causal variants by statistical fine-mapping." Nature Reviews Genetics 19.8 (2018): 491-504.
- Purcell, Shaun, et al. "PLINK: a tool set for whole-genome association and population-based linkage analyses." The American journal of human genetics 81.3 (2007): 559-575.
