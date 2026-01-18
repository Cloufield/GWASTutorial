# SAIGE: Saddlepoint Approximation for Accurate P-values

## Introduction

SAIGE (Scalable and Accurate Implementation of Generalized mixed model) is an R package developed for genome-wide association studies (GWAS) in large-scale datasets and biobanks. SAIGE addresses two critical challenges in GWAS:

1. **Case-control imbalance**: Standard logistic regression can produce biased p-values when case-control ratios are highly unbalanced (e.g., 1:10 or more extreme)
2. **Sample relatedness**: Accounts for genetic relatedness and population structure using generalized linear mixed models (GLMMs)

SAIGE uses **saddlepoint approximation (SPA)** to accurately calculate p-values for binary traits, especially when dealing with rare variants or unbalanced case-control ratios where standard asymptotic methods fail.

!!! quote "SAIGE overview"
    SAIGE is an R package developed with Rcpp for genome-wide association tests in large-scale data sets and biobanks. The method efficiently controls for case-control imbalance and sample relatedness in large-scale genetic association studies.
    
    Reference: [SAIGE Documentation](https://saigegit.github.io/SAIGE-doc/)

## Case-control imbalance

### The problem

In case-control GWAS, standard logistic regression assumes that the test statistic follows an asymptotic normal distribution. However, this assumption breaks down when:

1. **Unbalanced case-control ratios**: When the number of cases is much smaller than controls (e.g., 1:10, 1:100, or more extreme)
2. **Rare variants**: When testing variants with low minor allele frequency (MAF < 0.01), especially in the smaller group
3. **Small sample sizes**: When the effective sample size is small due to imbalance

!!! warning "Consequences of case-control imbalance"
    When case-control ratios are highly unbalanced, standard logistic regression can produce:
    - **Inflated test statistics**: P-values that are too small (anti-conservative)
    - **Biased effect estimates**: Maximum likelihood estimates may be biased or infinite
    - **Type I error inflation**: False positive rate higher than expected
    - **Poor calibration**: P-values don't follow the expected uniform distribution under the null

!!! example "Example of case-control imbalance"
    Consider a study with:
    - 1,000 cases and 10,000 controls (1:10 ratio)
    - Testing a rare variant with MAF = 0.001
    
    In this scenario:
    - Expected number of minor alleles in cases: ~2 (1,000 × 0.001 × 2)
    - Expected number of minor alleles in controls: ~20 (10,000 × 0.001 × 2)
    - Standard logistic regression may fail or produce unreliable p-values due to the small number of carriers in cases

### Why standard methods fail

Standard logistic regression uses the **score test** or **Wald test**, which rely on asymptotic theory:

$$Z = \frac{\hat{\beta}}{SE(\hat{\beta})} \sim N(0, 1)$$

This approximation works well when:
- Sample sizes are large
- Case-control ratio is balanced (close to 1:1)
- Variant frequency is not too rare

However, when these conditions are violated, the normal approximation becomes inaccurate, leading to:
- **Sparse data**: Few carriers in the smaller group
- **Boundary effects**: Estimates near the boundary of the parameter space
- **Non-normal distributions**: The test statistic distribution deviates from normal

!!! info "Mathematical intuition"
    The score test statistic for logistic regression is:
    
    $$S = \frac{\sum_{i=1}^{n} (y_i - \hat{\mu}_i) G_i}{\sqrt{\sum_{i=1}^{n} \hat{\mu}_i(1-\hat{\mu}_i) G_i^2}}$$
    
    where:
    - $y_i$ is the phenotype (0 or 1)
    - $\hat{\mu}_i$ is the fitted probability under the null
    - $G_i$ is the genotype (0, 1, or 2)
    
    When case-control ratios are unbalanced and variants are rare, the denominator can be very small, and the distribution of $S$ may not be well-approximated by a normal distribution.

## Saddlepoint approximation (SPA)

### Overview

**Saddlepoint approximation (SPA)** is a method for approximating the distribution of a random variable by inverting its moment-generating function (MGF). Unlike normal approximation, SPA can provide accurate tail probabilities even when:
- Sample sizes are small
- Data are sparse
- The distribution is skewed or has heavy tails

SAIGE uses SPA to calculate accurate p-values for the score test statistic in logistic regression, especially for rare variants and unbalanced case-control ratios.

!!! info "Key advantage of SPA"
    SPA provides **second-order accuracy** (relative error $O(n^{-1})$) compared to normal approximation (relative error $O(n^{-1/2})$), making it particularly useful for:
    - Rare variants (MAF < 0.01)
    - Unbalanced case-control ratios
    - Small effective sample sizes

### Mathematical foundation

The saddlepoint approximation method works as follows:

1. **Moment-generating function (MGF)**: For a random variable $X$, the MGF is:
   
   $$M_X(t) = E[e^{tX}]$$

2. **Cumulant-generating function (CGF)**: The natural logarithm of the MGF:
   
   $$K_X(t) = \log M_X(t)$$

3. **Saddlepoint equation**: The saddlepoint $\hat{t}$ is found by solving:
   
   $$K'_X(\hat{t}) = x$$
   
   where $K'_X(t)$ is the first derivative of the CGF.

4. **Saddlepoint approximation**: The probability density function (PDF) is approximated as:
   
   $$f_X(x) \approx \frac{1}{\sqrt{2\pi K''_X(\hat{t})}} \exp\{K_X(\hat{t}) - \hat{t}x\}$$
   
   where $K''_X(\hat{t})$ is the second derivative of the CGF evaluated at the saddlepoint.

5. **Tail probability**: The cumulative distribution function (CDF) can be approximated using:
   
   $$P(X \leq x) \approx \Phi(w) + \phi(w)\left(\frac{1}{w} - \frac{1}{v}\right)$$
   
   where:
   - $w = \text{sign}(\hat{t})\sqrt{2[\hat{t}x - K_X(\hat{t})]}$
   - $v = \hat{t}\sqrt{K''_X(\hat{t})}$
   - $\Phi$ and $\phi$ are the standard normal CDF and PDF, respectively

!!! note "Why it's called 'saddlepoint'"
    The method is named "saddlepoint" because the point $\hat{t}$ where $K'_X(\hat{t}) = x$ corresponds to a saddle point in the complex plane when extending the CGF to complex values. This point provides the best approximation for the tail probability.

### Application to GWAS

In the context of GWAS with logistic regression, SAIGE applies SPA to the score test statistic:

$$S = \frac{\sum_{i=1}^{n} (y_i - \hat{\mu}_i) G_i}{\sqrt{\sum_{i=1}^{n} \hat{\mu}_i(1-\hat{\mu}_i) G_i^2}}$$

The key steps are:

1. **Compute the CGF**: For the score statistic $S$, compute its cumulant-generating function under the null hypothesis
2. **Find the saddlepoint**: Solve the saddlepoint equation for the observed test statistic value
3. **Calculate p-value**: Use the saddlepoint approximation to compute the tail probability

### Handling relatedness

SAIGE accounts for genetic relatedness through the random effects $u_i$ in the GLMM:

$$Var(\mathbf{u}) = \sigma_g^2 \mathbf{K}$$

where $\mathbf{K}$ is the $N \times N$ genetic relationship matrix (GRM). This can be:
- **Full GRM**: Computed from all variants (memory-intensive for large samples)
- **Sparse GRM**: Computed from a subset of variants with pruning (more memory-efficient)

!!! info "Sparse GRM in SAIGE"
    SAIGE can use a sparse GRM by:
    1. LD-pruning variants (e.g., $r^2 < 0.1$)
    2. Computing GRM from pruned variants
    3. Setting small entries to zero (sparsification)
    
    This reduces memory usage while maintaining accuracy for accounting for relatedness.


### Output interpretation

SAIGE Step 2 output typically includes:

- **CHR**: Chromosome
- **POS**: Genomic position
- **SNPID**: Variant ID
- **Allele1**: Reference allele
- **Allele2**: Alternative allele
- **AF_Allele2**: Allele frequency of Allele2
- **N**: Sample size
- **BETA**: Effect size estimate (log-odds ratio for binary traits)
- **SE**: Standard error
- **Tstat**: Test statistic
- **p.value**: P-value (calculated using SPA)
- **p.value.NA**: P-value using normal approximation (for comparison)
- **Is.converge**: Whether the SPA calculation converged

!!! tip "Interpreting SAIGE output"
    - Compare `p.value` (SPA) with `p.value.NA` (normal approximation) to see the impact of SPA
    - Check `Is.converge` to ensure SPA calculations converged
    - For rare variants, `p.value` (SPA) is typically more accurate than `p.value.NA`

## References

### SAIGE method papers

- **SAIGE (main method)**: Zhou W, Nielsen JB, Fritsche LG, Dey R, Gabrielsen ME, Wolford BN, LeFaive J, VandeHaar P, Gagliano SA, Gifford A, Bastarache LA, Wei WQ, Denny JC, Lin M, Hveem K, Kang HM, Abecasis GR, Willer CJ, Lee S. Efficiently controlling for case-control imbalance and sample relatedness in large-scale genetic association studies. *Nature Genetics*. 2018 Sep;50(9):1335-1341. doi: [10.1038/s41588-018-0184-y](https://doi.org/10.1038/s41588-018-0184-y). PMID: 30104761.

- **SAIGE-GENE (set-based tests)**: Zhou W*, Zhao Z*, Nielsen JB, Fritsche LG, LeFaive J, Gagliano Taliun SA, Bi W, Gabrielsen ME, Daly MJ, Neale BM, Hveem K, Abecasis GR, Willer CJ, Lee S. Scalable generalized linear mixed model for region-based association tests in large biobanks and cohorts. *Nature Genetics*. 2020 Jun;52(6):634-639. doi: [10.1038/s41588-020-0621-6](https://doi.org/10.1038/s41588-020-0621-6). PMID: 32424355.

- **SAIGE-GENE+ (enhanced set-based tests)**: Wei Zhou*, Wenjian Bi*, Zhangchen Zhao*, Kushal K. Dey, Karthik A. Jagadeesh, Konrad J. Karczewski, Mark J. Daly, Benjamin M. Neale, Seunggeun Lee. Set-based rare variant association tests for biobank scale sequencing data sets. *medRxiv* 2021.07.12.21260400. doi: [10.1101/2021.07.12.21260400](https://doi.org/10.1101/2021.07.12.21260400).

### Saddlepoint approximation

- **Classical reference**: Daniels HE. Saddlepoint approximations in statistics. *The Annals of Mathematical Statistics*. 1954;25(4):631-650.

- **Application to score tests**: Dey R, Lee S. A note on the use of saddlepoint approximation for testing in generalized linear mixed models. *Biometrika*. 2019;106(4):987-992. doi: [10.1093/biomet/asz040](https://doi.org/10.1093/biomet/asz040).

- **Saddlepoint approximation in genetics**: Dey R, Schmidt EM, Abecasis GR, Lee S. A fast and accurate algorithm to test for binary phenotypes and its application to PheWAS. *The American Journal of Human Genetics*. 2017;101(1):37-49. doi: [10.1016/j.ajhg.2017.05.014](https://doi.org/10.1016/j.ajhg.2017.05.014).

### Case-control imbalance and rare variants

- **Firth correction**: Firth D. Bias reduction of maximum likelihood estimates. *Biometrika*. 1993;80(1):27-38. doi: [10.1093/biomet/80.1.27](https://doi.org/10.1093/biomet/80.1.27).

- **Rare variant testing**: Lee S, Abecasis GR, Boehnke M, Lin X. Rare-variant association analysis: study designs and statistical tests. *The American Journal of Human Genetics*. 2014;95(1):5-23. doi: [10.1016/j.ajhg.2014.06.009](https://doi.org/10.1016/j.ajhg.2014.06.009).

### Software and documentation

- **SAIGE Documentation**: [https://saigegit.github.io/SAIGE-doc/](https://saigegit.github.io/SAIGE-doc/)
- **SAIGE GitHub**: [https://github.com/weizhouUMICH/SAIGE](https://github.com/weizhouUMICH/SAIGE)
- **Contact**: saige.genetics@gmail.com
