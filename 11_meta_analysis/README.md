# Meta-analysis

## Aims

Meta-analysis is one of the most commonly used statistical methods to combine the evidence from multiple studies into a single result. 

!!! note "Potential problems for small-scale genome-wide association studies"
    - Low coverage of markers and genetic variability
    - Less accurate effect size estimation
    - Low statistical power

To address these problems, meta-analysis is a powerful approach to integrate multiple GWAS summary statistics, especially when more and more summary statistics are publicly available.
. This method allows us to obtain increases in statistical power as sample size increases. 

## Fixed effect IVW

$$ \bar{\beta} = {{\sum_{i=1}^{k} {w_i \beta_i}}\over{\sum_{i=1}^{k} {w_i}}} $$

- $w_i = 1 / \delta^2_i$


## 


## Heterogeneity test

!!! info "Cochran's Q test"

    $$ Q = \sum_{i=1}^{k} {w_i (\beta_i - \bar{\beta})^2} $$

!!! info "$I^2$"
    $$ I^2 =  {{Q - df}\over{Q}}\times 100% =  {{Q - (k - 1)}\over{Q}}\times 100% $$

## METAL

## MR-MEGA
