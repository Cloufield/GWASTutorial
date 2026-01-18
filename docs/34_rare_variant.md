
# Rare-variant association tests

## Introduction

Traditional genome-wide association studies (GWAS) focus on common variants (typically with minor allele frequency, MAF > 0.05). However, rare variants (MAF < 0.01 or 0.005) may also contribute to disease risk, especially for complex traits. Single-variant association tests have limited power to detect rare variant associations due to:

- **Low allele frequency**: Few carriers in the sample
- **Small effect sizes**: Individual rare variants may have modest effects
- **Multiple testing burden**: Testing many rare variants requires stringent significance thresholds

Rare-variant association tests address these challenges by aggregating information across multiple variants within a gene or genomic region. These methods can be broadly categorized into:

- **Burden tests**: Collapse variants into genetic scores (assumes all variants have the same direction of effect)
- **Adaptive Burden tests**: Use data-adaptive weights to prioritize variants
- **Variance component tests**: Test the variance of genetic effects (allows for both protective and risk variants)
- **Combined tests (Omnibus Tests)**: Combine both burden tests and variance component tests to maximize power

!!! info "When to use rare-variant association tests?"
    Rare-variant tests are particularly useful for:

    - **Gene-based analysis**: Testing whether a gene (or genomic region) is associated with a trait
    - **Functional annotation-based analysis**: Testing variants within specific functional categories (e.g., loss-of-function, missense)
    - **Pathway analysis**: Testing sets of genes in biological pathways
    - **Whole-exome or whole-genome sequencing studies**: Where many rare variants are available

!!! note "Common tools for rare-variant analysis"

    - **SKAT/SKAT-O**: Sequence Kernel Association Test (R package)
    - **REGENIE**: Supports burden, SKAT, and ACAT tests
    - **MAGMA**: Gene-based analysis from GWAS summary statistics
    - **ACAT/ACAT-O**: Aggregated Cauchy Association Test

## Burden test

Burden tests collapse multiple rare variants into a single genetic score, typically by counting the number of rare alleles carried by each individual. The basic idea is to assume that all variants in the region have the same direction of effect (all risk-increasing or all protective).

!!! info "Basic burden test model"
    For a region with $k$ rare variants, the burden score for individual $i$ is:
    
    $$B_i = \sum_{j=1}^{k} w_j G_{ij}$$
    
    where:
    - $G_{ij}$ is the genotype of individual $i$ at variant $j$ (0, 1, or 2)
    - $w_j$ is a weight for variant $j$ (often based on MAF or functional annotation)
    
    The association test is then performed by regressing the phenotype on the burden score:
    
    $$y_i = \alpha + \beta B_i + \epsilon_i$$
    
    where $\beta$ represents the effect of the burden score on the phenotype.

!!! example "Common burden score calculations"

    - **Simple count**: $w_j = 1$ for all variants (count of rare alleles)
    - **MAF-based weights**: $w_j = 1/\sqrt{MAF_j(1-MAF_j)}$ (inverse variance weighting)
    - **Functional weights**: Higher weights for loss-of-function or missense variants

!!! warning "Limitations of burden tests"

    - **Directional assumption**: Assumes all variants have effects in the same direction
    - **Power loss**: If both protective and risk variants exist, their effects may cancel out
    - **Variant selection**: Requires careful selection of which variants to include (e.g., MAF threshold, functional annotation)

!!! quote "Burden test references"

    - Morgenthaler, S., & Thilly, W. G. (2007). A strategy to discover genes that carry rare but relevant variants in disease association studies. *American journal of human genetics*, 80(4), 703-714.
    - Li, B., & Leal, S. M. (2008). Methods for detecting associations with rare variants for common diseases: application to analysis of sequence data. *The American Journal of Human Genetics*, 83(3), 311-321.

## SKAT and SKAT-O

The Sequence Kernel Association Test (SKAT) is a variance component test that tests the variance of genetic effects rather than the mean. Unlike burden tests, SKAT allows for both protective and risk variants in the same region, making it more flexible when the direction of effects is unknown.

### SKAT (Sequence Kernel Association Test)

SKAT models the genetic effects as random effects and tests whether the variance of these effects is greater than zero.

!!! info "SKAT model"
    For a region with $k$ variants, SKAT assumes:
    
    $$y_i = \alpha + \sum_{j=1}^{k} G_{ij} \beta_j + \epsilon_i$$
    
    where $\beta_j \sim N(0, w_j^2 \tau)$ are random effects with variance $\tau$. The null hypothesis is $H_0: \tau = 0$ (no association).
    
    The SKAT test statistic is:
    
    $$Q = (y - \hat{\mu})' K (y - \hat{\mu})$$
    
    where $K = GWG'$ is a kernel matrix, $G$ is the genotype matrix, and $W = diag(w_1^2, ..., w_k^2)$ contains variant weights.
    
    Under the null hypothesis, $Q$ follows a mixture of chi-square distributions, which can be approximated using moment matching.

!!! example "Common SKAT weights"

    - **Beta weights**: $w_j = Beta(MAF_j; 1, 25)$ - upweights rarer variants
    - **MAF-based**: $w_j = 1/\sqrt{MAF_j(1-MAF_j)}$
    - **Functional weights**: Higher weights for predicted deleterious variants

### SKAT-O (Optimal SKAT)

SKAT-O is an optimal test that combines burden and variance component tests. It searches over a range of correlation parameters $\rho$ (from 0 to 1) to find the optimal combination:

- $\rho = 0$: Pure variance component test (SKAT)
- $\rho = 1$: Pure burden test
- $0 < \rho < 1$: Weighted combination

!!! info "SKAT-O test statistic"
    SKAT-O uses a linear combination of burden and SKAT statistics:
    
    $$Q_\rho = (1-\rho) Q_{SKAT} + \rho Q_{Burden}$$
    
    The optimal $\rho$ is selected to maximize power, and the p-value is adjusted for multiple testing across different $\rho$ values.

!!! tip "When to use SKAT vs. SKAT-O?"

    - **SKAT**: Use when you expect both protective and risk variants, or when the direction of effects is unknown
    - **SKAT-O**: Use when you're uncertain about the genetic architecture (recommended as default)
    - **Burden test**: Use when you have strong prior knowledge that all variants have effects in the same direction

!!! quote "SKAT references"

    - Wu, M. C., Lee, S., Cai, T., Li, Y., Boehnke, M., & Lin, X. (2011). Rare-variant association testing for sequencing data with the sequence kernel association test. *The American Journal of Human Genetics*, 89(1), 82-93.
    - Lee, S., Emond, M. J., Bamshad, M. J., Barnes, K. C., Rieder, M. J., Nickerson, D. A., ... & Lin, X. (2012). Optimal unified approach for rare-variant association testing with application to small-sample case-control whole-exome sequencing studies. *The American Journal of Human Genetics*, 91(2), 224-237.

## ACAT: Aggregated Cauchy Association Test

ACAT (Aggregated Cauchy Association Test) is a fast and powerful p-value combination method that can combine p-values from multiple tests (e.g., different variant sets, different annotations) without requiring LD information or correlation structure.

!!! info "ACAT test statistic"
    For $k$ tests with p-values $p_1, p_2, ..., p_k$ and weights $w_1, w_2, ..., w_k$, the ACAT test statistic is:
    
    $$T_{ACAT} = \sum_{i=1}^{k} w_i \tan\{(0.5 - p_i)\pi\}$$
    
    The p-value of ACAT can be approximated by:
    
    $$p \approx \frac{1}{2} - \frac{\arctan(T_{ACAT}/w)}{\pi}$$
    
    where $w = \sum_{i=1}^{k} w_i$ is the sum of weights.

!!! info "Key advantages of ACAT"

    - **No LD required**: Only needs p-values and weights as input
    - **Fast computation**: Simple arithmetic operations, no matrix inversion
    - **Robust**: Works well even when tests are correlated
    - **Flexible**: Can combine p-values from different types of tests

!!! example "ACAT applications"

    - **ACAT-V**: Combines p-values from individual variant tests within a gene
    - **ACAT-O**: Optimal combination of burden and variance component tests (similar to SKAT-O)
    - **ACAT-G**: Combines p-values from multiple genes in a pathway

!!! quote "ACAT reference"
    The most distinctive feature of ACAT is that it only takes the p values (and weights) as input, and the p value of ACAT can be well approximated by a Cauchy distribution. Specifically, neither the linkage disequilibrium (LD) information in a region of the genome nor the correlation structure of set-level test statistics is needed for calculating the p value of ACAT.
    
    Liu, Y., Chen, S., Li, Z., Morrison, A. C., Boerwinkle, E., & Lin, X. (2019). ACAT: a fast and powerful p value combination method for rare-variant analysis in sequencing studies. *The American Journal of Human Genetics*, 104(3), 410-421.

## Practical considerations

### Variant selection and annotation

Before performing rare-variant tests, you need to:

**Define the variant set**: Which variants to include?
   
   - MAF threshold (e.g., MAF < 0.01 or 0.005)
   - Functional annotation (e.g., loss-of-function, missense, regulatory)
   - Quality filters (e.g., call rate, Hardy-Weinberg equilibrium)

**Define the region**: Gene boundaries, regulatory regions, or custom intervals

**Weight assignment**: How to weight variants?

   - MAF-based weights (upweight rarer variants)
   - Functional weights (upweight predicted deleterious variants)
   - Equal weights

!!! tip "Common MAF thresholds"

    - **Ultra-rare**: MAF < 0.0001 (singletons/doubletons)
    - **Rare**: MAF < 0.001
    - **Low-frequency**: MAF < 0.01
    - **Including low-frequency**: MAF < 0.05

### Multiple testing correction

When testing multiple genes or regions, you need to correct for multiple testing:

- **Bonferroni correction**: Divide significance threshold by number of tests
- **False discovery rate (FDR)**: Control the expected proportion of false discoveries
- **Permutation-based**: Empirical p-values from permuted data

### Software tools

!!! note "Common tools for rare-variant analysis"

    - **SKAT R package**: `SKAT`, `SKATBinary`, `SKATBinary.SSD.All` functions
    - **REGENIE**: Command-line tool supporting burden, SKAT, ACAT tests
    - **MAGMA**: Gene-based analysis from GWAS summary statistics
    - **ACAT R package**: `ACAT` function for p-value combination

## References

### General rare-variant analysis
- Lee, S., Abecasis, G. R., Boehnke, M., & Lin, X. (2014). Rare-variant association analysis: study designs and statistical tests. *The American Journal of Human Genetics*, 95(1), 5-23.
- Auer, P. L., & Lettre, G. (2015). Rare variant association studies: considerations, challenges and opportunities. *Genome medicine*, 7(1), 1-11.

### Burden tests
- Morgenthaler, S., & Thilly, W. G. (2007). A strategy to discover genes that carry rare but relevant variants in disease association studies. *American journal of human genetics*, 80(4), 703-714.
- Li, B., & Leal, S. M. (2008). Methods for detecting associations with rare variants for common diseases: application to analysis of sequence data. *The American Journal of Human Genetics*, 83(3), 311-321.

### SKAT and SKAT-O
- Wu, M. C., Lee, S., Cai, T., Li, Y., Boehnke, M., & Lin, X. (2011). Rare-variant association testing for sequencing data with the sequence kernel association test. *The American Journal of Human Genetics*, 89(1), 82-93.
- Lee, S., Emond, M. J., Bamshad, M. J., Barnes, K. C., Rieder, M. J., Nickerson, D. A., ... & Lin, X. (2012). Optimal unified approach for rare-variant association testing with application to small-sample case-control whole-exome sequencing studies. *The American Journal of Human Genetics*, 91(2), 224-237.

### ACAT
- Liu, Y., Chen, S., Li, Z., Morrison, A. C., Boerwinkle, E., & Lin, X. (2019). ACAT: a fast and powerful p value combination method for rare-variant analysis in sequencing studies. *The American Journal of Human Genetics*, 104(3), 410-421.