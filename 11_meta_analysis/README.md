# Meta-analysis

## Aims

Meta-analysis is one of the most commonly used statistical methods to combine the evidence from multiple studies into a single result. 

!!! note "Potential problems for small-scale genome-wide association studies"
    - Low coverage of markers and genetic variability
    - Less accurate effect size estimation
    - Low statistical power

To address these problems, meta-analysis is a powerful approach to integrate multiple GWAS summary statistics, especially when more and more summary statistics are publicly available.
. This method allows us to obtain increases in statistical power as sample size increases. 

## Fixed effects meta-analysis

$$ \bar{\beta_{ij}} = {{\sum_{i=1}^{k} {w_{ij} \beta_{ij}}}\over{\sum_{i=1}^{k} {w_{ij}}}} $$

- $w_{ij} = 1 / Var(\beta_{ij})$

## Heterogeneity test

!!! info "Cochran's Q test"

    $$ Q = \sum_{i=1}^{k} {w_i (\beta_i - \bar{\beta})^2} $$

!!! info "$I^2$"
    $$ I_j^2 =  {{Q_j - df_j}\over{Q_j}}\times 100% =  {{Q - (k - 1)}\over{Q}}\times 100% $$

## Random effects meta-analysis

$$ r_j^2 = max\left(0, {{Q_j - (N_j -1)}\over{\sum_iw_{ij} - ({{\sum_iw_{ij}^2} \over {\sum_iw_{ij}}})}}\right)$$

$$ \bar{\beta_j}^* = {{\sum_{i=1}^{k} {w_{ij}^* \beta_i}}\over{\sum_{i=1}^{k} {w_{ij}^*}}} $$

$$w_{ij}^* = {{1}\over{r_j^2 + Var(\beta_{ij})}} $$

!!! quote

## METAL

## MR-MEGA
