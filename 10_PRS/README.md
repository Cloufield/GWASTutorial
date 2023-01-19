# Polygenic risk scores

## Table of Contents

- [PRS Analysis Workflow](#prs-analysis-workflow)
- [Practice]()
    - [C+T: PLINK](#ct-plink)
    - [Beta-shrinkage: PRS-CS](#beta-shrinkage-prs-cs)
    - [Download PRS model from PGS Catalog](#download-prs-model-from-pgs-catalog)
    - [Calculate PRS using PLINK](#calculate-prs-using-plink)
- [Reference](#reference)

# PRS Analysis Workflow

1. **Developing PRS model** using base data
2. Performing **validation** to obtain best-fit parameters
3. **Testing** in an independent population

## Methods

|Category|Description| Methods |
|-|-|-|
|P value thresholding| |C+T, PRSice|
|Beta shrinkage| |LDpred, PRS-CS|

# Practice

In this tutorial, we will first briefy introduce how to develop PRS model using the sample data and then demonstrate how we can download PRS models from PGS Catalog and apply to our sample genotype data. 

## C+T: PLINK


## Beta shrinkage: PRS-CS


## Download PRS model from PGS Catalog

URL: http://www.pgscatalog.org/

## Calculate PRS using PLINK



## Regressions

## ROC and AUC

## C-index

## R2 and pseudo-R2

!!! info "Coefficient of determination"
    $R^2$ : coefficient of determination, which measures the amount of variance explained by the regression model.
    
    In linear regression:

    $$ R_2 = 1 - {{RSS}\over{TSS}} $$

    - $RSS$ : sum of squares of residuals
    - $TSS$ : total sum of squares

!!! info "Pseudo-R2"
    In logistic regression, 

    One of the most commonly used Pseudo-R2 for PRS analysis is Nagelkerke's $R^2$

    $$R_{Nagelkerke} = {{1 - ({{L_0}\over{L_M}})^{2/n}}\over{1 - L_0^{2/n}}}$$

    - $L_0$ : Likelihood of the null model
    - $L_M$ : Likelihood of the fitted model

## R2 on liability scale



# Reference

- PLINK : Purcell, Shaun, et al. "PLINK: a tool set for whole-genome association and population-based linkage analyses." The American journal of human genetics 81.3 (2007): 559-575.
- PGS Catalog : Lambert, Samuel A., et al. "The Polygenic Score Catalog as an open database for reproducibility and systematic evaluation." Nature Genetics 53.4 (2021): 420-425.
- PRS-CS: Ge, Tian, et al. "Polygenic prediction via Bayesian regression and continuous shrinkage priors." Nature communications 10.1 (2019): 1-10.
- PRS Tutorial: Choi, Shing Wan, Timothy Shin-Heng Mak, and Paul F. O’Reilly. "Tutorial: a guide to performing polygenic risk score analyses." Nature protocols 15.9 (2020): 2759-2772.

