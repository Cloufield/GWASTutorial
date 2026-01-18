# Linear Mixed Models in GWAS

## Introduction

Linear Mixed Models (LMM) are a powerful statistical framework used in genome-wide association studies (GWAS) to account for population structure, cryptic relatedness, and other sources of confounding that can lead to spurious associations.

Unlike standard linear regression models that assume independence between individuals, LMMs incorporate both **fixed effects** (the genetic variant being tested) and **random effects** (modeling genetic relatedness through a kinship or genetic relationship matrix). This allows LMMs to properly control for population stratification and relatedness, which are common sources of false positives in GWAS.

!!! info "Why use LMM in GWAS?"
    - **Population structure**: Different ancestral backgrounds can create spurious associations
    - **Cryptic relatedness**: Unrecognized familial relationships can inflate test statistics
    - **Family studies**: Explicitly accounts for known family structures
    - **Improved power**: More accurate association testing by properly modeling covariance structure

The general LMM framework for GWAS can be written as:

$$y = X\beta + Zu + \epsilon$$

where:
- $y$ is the phenotype vector
- $X$ is the genotype matrix for the variant being tested (fixed effect)
- $\beta$ is the genetic effect of interest
- $Z$ is the design matrix for random effects
- $u \sim N(0, \sigma_g^2 K)$ represents random effects with covariance matrix $K$ (kinship/genetic relationship matrix)
- $\epsilon \sim N(0, \sigma_e^2 I)$ is the residual error
