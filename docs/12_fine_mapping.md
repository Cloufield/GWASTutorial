# Fine-mapping

## Introduction

Fine-mapping aims to identify the causal variant(s) within a locus for a disease, given the evidence of the significant association of the locus (or genomic region) in GWAS of a disease.

After identifying a significant association signal in GWAS, fine-mapping helps narrow down which specific variant(s) are likely to be causal, rather than just being in linkage disequilibrium (LD) with the true causal variant.

!!! info "What is fine-mapping?"
    Fine-mapping is a statistical approach used to identify the most likely causal variant(s) within a genomic region that shows significant association with a trait. It helps distinguish between:
    - **Causal variants**: Variants that directly affect the trait
    - **Tag variants**: Variants that are associated only because they are in LD with causal variants

Fine-mapping using individual-level data is usually performed by fitting the multiple linear regression model:

$$y = Xb + e$$

where:
- $y$ is the phenotype vector
- $X$ is the genotype matrix
- $b = (b_1, …, b_J)^T$ is a vector of genetic effects of variants
- $e$ is the error term

Fine-mapping using Bayesian methods aims to estimate the **PIP (posterior inclusion probability)**, which indicates the evidence for variant $j$ having a non-zero effect (i.e., being causal).

!!! info "PIP (Posterior Inclusion Probability)"
    PIP is the probability that a variant is causal, given the observed data. It is calculated by summing the **posterior probabilities** over all models that include variant $j$ as causal:

    $$ PIP_j := Pr(b_j \neq 0 | X, y) $$

    - PIP ranges from 0 to 1
    - Higher PIP values indicate stronger evidence that the variant is causal
    - Variants with PIP > 0.5 are often considered strong candidates for being causal

!!! info "Bayesian methods and Posterior probability"
    Bayesian fine-mapping uses Bayes' theorem to calculate the posterior probability of each model (configuration of causal variants):

    $$ Pr(M_m | O) = \frac{Pr(O | M_m) Pr(M_m)}{\sum_{i=1}^n Pr(O | M_i) Pr(M_i)} $$

    where:
    - $O$: Observed data (genotypes and phenotypes)
    - $M$: Models (the configurations of causal variants in the context of fine-mapping)
    - $Pr(M_m | O)$: **Posterior Probability** of model $m$ (probability that model $m$ is true given the data)
    - $Pr(O | M_m)$: **Likelihood** (the probability of observing the data given that model $m$ is true)
    - $Pr(M_m)$: **Prior** distribution of model $m$ (the prior probability that model $m$ is true)
    - $\sum_{i=1}^n Pr(O | M_i) Pr(M_i)$: **Evidence** (the probability of observing the data), namely $Pr(O)$

!!! info "Credible sets"
    A **credible set** is the minimum set of variants that contains all causal variants with probability $\alpha$. 

    Under the single-causal-variant-per-locus assumption, the credible set is calculated by:
    1. Ranking variants based on their posterior probabilities
    2. Summing these probabilities until the cumulative sum is $\geq \alpha$
    
    We usually report **95% credible sets** ($\alpha = 0.95$) for fine-mapping analysis, meaning there is a 95% probability that the true causal variant is included in the set.
    
    !!! tip "Interpreting credible sets"
        - Smaller credible sets indicate better fine-mapping resolution
        - If multiple causal variants exist, methods like SuSiE can identify multiple credible sets

!!! note "Commonly used tools for fine-mapping"
    
    **Methods assuming only one causal variant** in the locus:
    - **ABF** (Approximate Bayes Factor): Fast method for single causal variant fine-mapping
    
    **Methods assuming multiple causal variants** in the locus:
    - **SuSiE / SuSiE-RSS**: Sum of Single Effects model (works with individual-level data or summary statistics)
    - **CAVIAR, CAVIARBF, eCAVIAR**: Bayesian fine-mapping methods
    - **FINEMAP**: Bayesian fine-mapping using summary statistics
    
    **Methods assuming a small number of larger causal effects with many infinitesimal effects**:
    - **SuSiE-inf**: Extension of SuSiE for mixed effects
    - **FINEMAP-inf**: Extension of FINEMAP for mixed effects
    
    **Methods for cross-ancestry fine-mapping**:
    - **SUSIEX**: Extension of SuSiE for cross-ancestry analysis
    - **MESuSiE** (Multi-ancestry SuSiE): Uses GWAS summary statistics from multiple ancestries; models both shared and ancestry-specific causal signals; handles diverse LD patterns across ancestries; uses variational inference for scalable computation
    - **MultiSuSiE**: Extension of SuSiE to multiple ancestries that allows causal effect sizes to vary across populations; demonstrates improved power and resolution with lower computational cost in large multi-ancestry datasets
    
    For more information, check [here](https://cloufield.github.io/CTGCatalog/Tools_Fine_mapping_README/).

In this tutorial, we will introduce **SuSiE** as an example. SuSiE stands for "Sum of Single Effects" model.

### SuSiE model

The key idea behind SuSiE is to decompose the genetic effect vector as a sum of single effects:

$$b = \sum_{l=1}^L b_l $$

where:
- Each vector $b_l = (b_{l1}, …, b_{lJ})^T$ is a **single effect** vector (a vector with only one non-zero element)
- $L$ is the upper bound on the number of causal variants
- This model can be fitted using **Iterative Bayesian Stepwise Selection (IBSS)**

!!! info "Why 'Sum of Single Effects'?"
    SuSiE models the genetic effect as a sum of multiple single effects, where each single effect corresponds to one causal variant. This allows SuSiE to:
    - Identify multiple causal variants in a region
    - Account for LD between variants
    - Provide PIPs and credible sets for each causal variant

### SuSiE-RSS (Summary Statistics)

For fine-mapping with summary statistics using SuSiE (SuSiE-RSS), IBSS was modified (IBSS-ss) to take sufficient statistics as input. SuSiE-RSS approximates the sufficient statistics from summary statistics (effect sizes, standard errors, and LD matrix) to perform fine-mapping without requiring individual-level data. 

!!! quote "SuSiE and SuSiE-RSS references"
    For details of SuSiE and SuSiE-RSS, please check:
    
    - **SuSiE (individual-level data)**: Wang, G., Sarkar, A., Carbonetto, P., & Stephens, M. (2020). A simple new approach to variable selection in regression, with application to genetic fine mapping. *Journal of the Royal Statistical Society: Series B*, 82(5), 1273-1300.
    
    - **SuSiE-RSS (summary statistics)**: Zou, Y., Carbonetto, P., Wang, G., & Stephens, M. (2022). Fine-mapping from summary data with the "Sum of Single Effects" model. *PLoS Genetics*, 18(7), e1010299. [Link](https://journals.plos.org/plosgenetics/article?id=10.1371/journal.pgen.1010299)



## File Preparation

Before performing fine-mapping, you need to prepare:

1. **Summary statistics for the locus**: GWAS summary statistics (effect sizes, standard errors, p-values) for variants in the region of interest
2. **SNP list for calculating LD matrix**: List of variant IDs to extract from reference panel for LD calculation
3. **Reference panel**: Genotype data (e.g., 1000 Genomes) for calculating LD matrix

!!! tip "Locus selection"
    Typically, you would:
    - Identify lead variants from GWAS (e.g., variants with $p < 5 \times 10^{-8}$)
    - Define a region around each lead variant (e.g., ±500 kb or ±1 Mb)
    - Extract summary statistics for all variants in that region

!!! example "Using Python (gwaslab) to identify lead variants and extract locus data"
    ```python
    import gwaslab as gl
    import pandas as pd
    import numpy as np
    
    # Load summary statistics
    sumstats = gl.Sumstats("../06_Association_tests/1kgeas.B1.glm.firth", fmt="plink2")
    
    # Perform basic quality checks
    sumstats.basic_check()
    
    # Identify lead variants (independent significant variants)
    sumstats.get_lead()
    
    # Output example:
    # Fri Jan 13 23:31:43 2023 Start to extract lead variants...
    # Fri Jan 13 23:31:43 2023  -Processing 1122285 variants...
    # Fri Jan 13 23:31:43 2023  -Significance threshold : 5e-08
    # Fri Jan 13 23:31:43 2023  -Sliding window size: 500  kb
    # Fri Jan 13 23:31:44 2023  -Found 59 significant variants in total...
    # Fri Jan 13 23:31:44 2023  -Identified 3 lead variants!
    # Fri Jan 13 23:31:44 2023 Finished extracting lead variants successfully!
    
    # Display lead variants
    print(sumstats.data[sumstats.data["STATUS"] == "LEAD"])
    # SNPID CHR POS EA  NEA SE  Z P OR  N STATUS
    # 110723  2:55574452:G:C  2 55574452  C G 0.160948  -5.98392  2.178320e-09  0.381707  503 9960099
    # 424615  6:29919659:T:C  6 29919659  T C 0.155457  -5.89341  3.782970e-09  0.400048  503 9960099
    # 635128  9:36660672:A:G  9 36660672  G A 0.160275  5.63422 1.758540e-08  2.467060  503 9960099
    ```
    
    We will perform fine-mapping for the first significant locus whose lead variant is `2:55574452:G:C` (chromosome 2, position 55574452).
    
    
    ```python
    # Filter variants in the locus (±500 kb around lead variant)
    locus = sumstats.filter_value('CHR==2 & POS>55074452 & POS<56074452')
    
    # Fill missing data (e.g., calculate BETA from OR if needed)
    locus.fill_data(to_fill=["BETA"])
    
    # Harmonize alleles (ensure consistent strand and allele coding)
    locus.harmonize(basic_check=False, ref_seq="/path/to/reference/genome.fasta")
    
    # Export summary statistics for the locus
    locus.data.to_csv("sig_locus.tsv", sep="\t", index=None)
    
    # Export SNP list for LD matrix calculation
    locus.data["SNPID"].to_csv("sig_locus.snplist", sep="\t", index=None, header=None)
    ```
    
    Check in terminal:
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
    
    head sig_locus.snplist
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

The LD (linkage disequilibrium) matrix is essential for fine-mapping, as it captures the correlation structure between variants in the region. Fine-mapping methods use the LD matrix to distinguish between causal variants and variants that are associated only due to LD.

!!! info "Why is LD matrix important?"
    - Fine-mapping methods need to account for LD to identify which variants are truly causal
    - The LD matrix is typically calculated from a reference panel (e.g., 1000 Genomes Project)
    - The reference panel should match the ancestry of your study population

!!! example "Calculate LD matrix using PLINK"
    ```bash
    #!/bin/bash
    
    # Path to reference panel (PLINK binary format)
    plinkFile="../01_Dataset/1KG.EAS.auto.snp.norm.nodup.split.rare002.common015.missing/1KG.EAS.auto.snp.norm.nodup.split.rare002.common015.missing"
    
    # Calculate LD correlation (r) matrix
    plink \
      --bfile ${plinkFile} \
      --keep-allele-order \
      --r square \
      --extract sig_locus.snplist \
      --out sig_locus_mt
    
    # Calculate LD r2 matrix (optional, for visualization)
    plink \
      --bfile ${plinkFile} \
      --keep-allele-order \
      --r2 square \
      --extract sig_locus.snplist \
      --out sig_locus_mt_r2
    ```
    
    !!! note "PLINK LD matrix options"
        - `--r square`: Calculate correlation coefficient (r) matrix
        - `--r2 square`: Calculate squared correlation coefficient (r²) matrix
        - `--extract`: Only include variants in the SNP list
        - `--keep-allele-order`: Preserve allele order from the reference panel
    
    Inspect the LD matrix (first 5 rows and columns):
    
    ```bash
    # LD correlation (r) matrix
    head -5 sig_locus_mt.ld | cut -f 1-5
    # 1       -0.145634       0.252616        -0.0876317      -0.0876317
    # -0.145634       1       -0.0916734      -0.159635       -0.159635
    # 0.252616        -0.0916734      1       0.452333        0.452333
    # -0.0876317      -0.159635       0.452333        1       1
    # -0.0876317      -0.159635       0.452333        1       1
    
    # LD r2 matrix
    head -5 sig_locus_mt_r2.ld | cut -f 1-5
    # 1       0.0212091       0.0638148       0.00767931      0.00767931
    # 0.0212091       1       0.00840401      0.0254833       0.0254833
    # 0.0638148       0.00840401      1       0.204605        0.204605
    # 0.00767931      0.0254833       0.204605        1       1
    # 0.00767931      0.0254833       0.204605        1       1
    ```
    
    !!! note "LD matrix format"
        - The LD matrix is symmetric (LD between variant i and j equals LD between j and i)
        - Diagonal elements are 1 (perfect correlation with itself)
        - Off-diagonal elements range from -1 to 1 for r, and 0 to 1 for r²
    
    Heatmap visualization of the LD matrix:
    
    ![LD matrix heatmap](https://user-images.githubusercontent.com/40289485/212523500-6ec7cfb9-eda6-4ee0-9dce-463772821ca2.png)

## Fine-mapping with summary statistics using SuSiE-R

### Installation

!!! example "Install SuSiE-R package"
    ```r
    # Install from CRAN
    install.packages("susieR")
    
    # Or install from GitHub for latest version
    # install.packages("devtools")
    # devtools::install_github("stephenslab/susieR")
    ```

### Running SuSiE-RSS

!!! example "Fine-mapping with summary statistics using SuSiE-RSS"
    ```r
    library(susieR)
    
    # Load summary statistics and LD matrix
    sumstats <- read.table("sig_locus.tsv", header=TRUE, sep="\t")
    R <- as.matrix(read.table("sig_locus_mt.ld", header=FALSE))
    
    # Extract required data
    bhat <- sumstats$BETA  # Effect sizes
    shat <- sumstats$SE    # Standard errors
    n <- sumstats$N[1]     # Sample size (should be the same for all variants)
    
    # Run SuSiE-RSS
    fitted_rss <- susie_rss(
      bhat = bhat,      # Estimated effects (vector of length p)
      shat = shat,      # Standard errors (vector of length p)
      R = R,            # LD correlation matrix (p x p)
      n = n,            # Sample size
      L = 10            # Maximum number of causal variants
    )
    
    # View results
    summary(fitted_rss)
    ```
    
    !!! info "SuSiE-RSS parameters"
        - `bhat`: Estimated effect sizes (BETA) from GWAS (vector of length $p$)
        - `shat`: Standard errors of effect sizes (vector of length $p$)
        - `R`: LD correlation (r) matrix ($p \times p$), where $p$ is the number of variants
        - `n`: Sample size (scalar, should be the same for all variants)
        - `L`: Maximum number of causal variants to consider (default: `L = 10`)
        
        !!! tip "Alternative input: z-scores"
            Instead of `bhat` and `shat`, you can provide z-scores directly:
            ```r
            z <- sumstats$BETA / sumstats$SE  # Calculate z-scores
            fitted_rss <- susie_rss(z = z, R = R, n = n, L = 10)
            ```

### Interpreting SuSiE results

!!! info "Key outputs from SuSiE"
    - **PIPs**: Posterior inclusion probabilities for each variant
    - **Credible sets**: Sets of variants that contain causal variants with specified probability
    - **Effect estimates**: Estimated effect sizes for each causal variant
    
    ```r
    # Extract PIPs
    pip <- fitted_rss$pip  # Posterior inclusion probabilities
    
    # Extract credible sets
    sets <- fitted_rss$sets
    
    # View credible sets
    print(sets)
    
    # Get variants in credible sets
    credible_set_variants <- sumstats$SNPID[sets$cs[[1]]]  # First credible set
    ```

!!! quote "SuSiE-R tutorial"
    For more details and advanced usage, please check the [SuSiE-R tutorial - Fine-mapping with susieR using summary statistics](https://stephenslab.github.io/susieR/articles/finemapping_summary_statistics.html)

!!! tip "Using SuSiE in Python (Jupyter notebook)"
    You can also use SuSiE in Python through the `susieR` R package via `rpy2`, or use the Python implementation. 
    
    For a complete Python example, check: [finemapping_susie.ipynb](https://github.com/Cloufield/GWASTutorial/blob/main/12_fine_mapping/finemapping_susie.ipynb)

Example output visualization:

<img width="770" alt="SuSiE fine-mapping results" src="https://user-images.githubusercontent.com/40289485/212628837-d20c0a59-9a6a-46a5-8c2d-a12fd427c794.png">


## References

### SuSiE method papers

- **SuSiE (individual-level data)**: Wang, G., Sarkar, A., Carbonetto, P., & Stephens, M. (2020). A simple new approach to variable selection in regression, with application to genetic fine mapping. *Journal of the Royal Statistical Society: Series B*, 82(5), 1273-1300. https://doi.org/10.1111/rssb.12388

- **SuSiE-RSS (summary statistics)**: Zou, Y., Carbonetto, P., Wang, G., & Stephens, M. (2022). Fine-mapping from summary data with the "Sum of Single Effects" model. *PLoS Genetics*, 18(7), e1010299. https://doi.org/10.1371/journal.pgen.1010299

### Fine-mapping reviews

- Schaid, D. J., Chen, W., & Larson, N. B. (2018). From genome-wide associations to candidate causal variants by statistical fine-mapping. *Nature Reviews Genetics*, 19(8), 491-504. https://doi.org/10.1038/s41576-018-0016-z

### Software and tools

- **PLINK**: Purcell, S., Neale, B., Todd-Brown, K., Thomas, L., Ferreira, M. A., Bender, D., ... & Sham, P. C. (2007). PLINK: a tool set for whole-genome association and population-based linkage analyses. *The American Journal of Human Genetics*, 81(3), 559-575. https://doi.org/10.1086/519795

- **SuSiE-R documentation**: [https://stephenslab.github.io/susieR/](https://stephenslab.github.io/susieR/)

- **Fine-mapping tools catalog**: [https://cloufield.github.io/CTGCatalog/Tools_Fine_mapping_README/](https://cloufield.github.io/CTGCatalog/Tools_Fine_mapping_README/)
