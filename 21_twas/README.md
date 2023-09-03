
# TWAS

## Background

Most variants identified in GWAS are located in regulatory regions, and these genetic variants could potentially affect complex traits through gene expression. However, due to the limitation of samples and high cost, it is difficult to measure gene expression at a large scale. Consequently, many expression-trait associations have not been detected, especially for those with small effect size. To address these issues, alternative approaches have been proposed and transcriptome-wide association study (TWAS) has become a common and easy-to-perform approach to identify genes whose expression is significantly associated with complex traits in individuals without directly measured expression levels.     

## Definition

TWAS is a method to identify significant expression-trait associations using expression imputation from genetic data or summary statistics. 

## FUSION

In this tutorial, we will introduce FUSION, which is one of the most commonly used tools for performing transcriptome-wide association studies (TWAS). 

url : http://gusevlab.org/projects/fusion/

FUSION trains predictive models of the genetic component of a functional/molecular phenotype and predicts and tests that component for association with disease using GWAS summary statistics. The goal is to identify associations between a GWAS phenotype and a functional phenotype that was only measured in reference data. (http://gusevlab.org/projects/fusion/)

!!! quote
    Gusev, A., Ko, A., Shi, H., Bhatia, G., Chung, W., Penninx, B. W., ... & Pasaniuc, B. (2016). Integrative approaches for large-scale transcriptome-wide association studies. Nature genetics, 48(3), 245-252.

### Alogrithm for imputing expression into GWAS summary statistics

ImpG-Summary algorithm was extended to impute the Z scores for the cis genetic component of expression.

$Z$ : a vector of standardized  effect  sizes  (z  scores)  of SNPs for the target trait at a given locus

We impute the Z score of the expression and trait as a linear combination of elements of $Z$ with weights $W$.

$$
W = \Sigma_{e,s}\Sigma_{s,s}^{-1}
$$

- $\Sigma_{e,s}$ : covariance among all SNPs (LD)

- $\Sigma_{s,s}$ : covariance matrix between all SNPs and gene expression

Both $\Sigma_{e,s}$ and $\Sigma_{s,s}$ are estimated from reference datsets.

$$
Z \sim N(0, \Sigma_{s,s} )
$$

The variance of $WZ$ (imputed z score of expression and trait) 
$$
Var(WZ) = W\Sigma_{s,s}W^t )
$$

the imputation Z score can be obtained by:

$$
{{WZ}\over{W\Sigma_{s,s}W^t}^{1/2}}
$$

!!! quote "ImpG-Summary algorithm"
    Pasaniuc, B., Zaitlen, N., Shi, H., Bhatia, G., Gusev, A., Pickrell, J., ... & Price, A. L. (2014). Fast and accurate imputation of summary statistics enhances evidence of functional enrichment. Bioinformatics, 30(20), 2906-2914.
