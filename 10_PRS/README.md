# Polygenic risk scores

## Definition

**Polygenic risk score(PRS)**, as known as **polygenic score (PGS)** or **genetic risk score (GRS)**, is a score that summarizes the effect sizes of genetic variants on a certain disease or trait (weighted sum of disease/trait-associated alleles).

To calculate the PRS for sample j, 

$$PRS_j = \sum_{i=0}^{i=M} x_{i,j} \beta_{i}$$

- $\beta_i$ : effect size for variant $i$
- $x_{i,j}$ : the effect allele count for sample $j$ at variant $i$
- $M$ : the number of variants

## PRS Analysis Workflow

1. **Developing PRS model** using base data
2. Performing **validation** to obtain best-fit parameters
3. **Testing** in an independent population

## Methods

|Category|Description| Representative Methods |
|-|-|-|
|P value thresholding| P + T |C+T, PRSice|
|Beta shrinkage| genome-wide PRS model |LDpred, PRS-CS|

In this tutorial, we will first briefly introduce how to develop PRS model using the sample data and then demonstrate how we can download PRS models from PGS Catalog and apply to our sample genotype data. 

## C+T/P+T using PLINK

P+T stands for Pruning + Thresholding, also known as Clumping and Thresholding(C+T), which is a very simple and straightforward approach to constructing PRS models.
 
!!! info "Clumping"

    Clumping: LD-pruning based on P value. It is a approach to select variants when there are multiple significant associations in high LD in the same region.
    
    The three important parameters for clumping in PLINK are:

    - clump-p1 0.0001       # Significance threshold for index SNPs
    - clump-r2 0.50         # LD threshold for clumping
    - clump-kb 250          # Physical distance threshold for clumping

!!! example "Clumping using PLINK"

    ```
    #!/bin/bash
    
    plinkFile=../01_Dataset/1KG.EAS.auto.snp.norm.nodup.split.maf005.thinp020
    sumStats=../06_Association_tests/1kgeas.B1.glm.firth
    
    plink \
        --bfile ${plinkFile} \
        --clump-p1 0.0001 \
        --clump-r2 0.1 \
        --clump-kb 250 \
        --clump ${sumStats} \
        --clump-snp-field ID \
        --clump-field P \
        --out 1kg_eas
    ```
    
    log
    ```
    --clump: 40 clumps formed from 307 top variants.
    ```
    check only the header and the first "clump" of SNPs.
    
    ```
    head -n 2 1kg_eas.clumped
     CHR    F              SNP         BP        P    TOTAL   NSIG    S05    S01   S001  S0001    SP2
       2    1   2:55574452:G:C   55574452   2.18e-09      111     16     15     20     17     43 2:55376609:T:G(1),2:55376892:T:G(1),2:55379420:A:G(1),2:55384226:A:G(    1),2:55397522:A:T(1),2:55405037:T:A(1),2:55405468:G:A(1),2:55410835:C:T(1),2:55424229:G:A(1),2:55426447:A:G(1),2:55452014:C:T(1),2:55460751:C:T(1),2:55461053:A:G(    1),2:55465633:T:G(1),2:55470115:C:T(1),2:55478226:A:G(1),2:55482911:C:T(1),2:55489629:T:C(1),2:55491330:G:A(1),2:55495251:C:T(1),2:55500234:A:G(1),2:55501125:C:T(    1),2:55513738:C:T(1),2:55521039:A:G(1),2:55554956:C:A(1),2:55555726:T:C(1),2:55557192:C:T(1),2:55560347:C:A(1),2:55563020:A:G(1),2:55578761:C:T(1),2:55582635:T:C(    1),2:55584526:T:C(1),2:55585577:A:T(1),2:55587807:G:T(1),2:55598053:T:C(1),2:55602809:G:A(1),2:55605264:A:G(1),2:55607830:C:T(1),2:55609851:C:T(1),2:55610999:C:T(    1),2:55611741:A:G(1),2:55611766:T:C(1),2:55612986:G:C(1),2:55617255:C:T(1),2:55618813:C:T(1),2:55619407:C:A(1),2:55619923:C:T(1),2:55620927:G:A(1),2:55621660:T:C(    1),2:55622431:A:C(1),2:55625464:C:T(1),2:55632329:T:C(1),2:55632724:T:C(1),2:55635477:C:T(1),2:55636351:T:C(1),2:55636755:T:C(1),2:55636795:A:C(1),2:55638697:T:C(    1),2:55642350:T:C(1),2:55643047:G:A(1),2:55643666:A:C(1),2:55650512:G:A(1),2:55650572:G:C(1),2:55650886:G:A(1),2:55650940:C:A(1),2:55653053:G:C(1),2:55653269:C:A(    1),2:55654354:A:G(1),2:55654847:A:G(1),2:55659155:A:G(1),2:55662423:T:C(1),2:55669642:G:C(1),2:55685127:A:G(1),2:55685669:G:C(1),2:55687290:G:C(1),2:55695696:A:G(    1),2:55696124:A:G(1),2:55709416:G:A(1),2:55720739:G:C(1),2:55724035:T:C(1)
    ```

## Beta shrinkage using PRS-CS

$$ \beta_j | \Phi_j \sim N(0,\phi\Phi_j) ,  \Phi_j \sim g $$

Reference: Ge, T., Chen, C. Y., Ni, Y., Feng, Y. C. A., & Smoller, J. W. (2019). Polygenic prediction via Bayesian regression and continuous shrinkage priors. Nature communications, 10(1), 1-10.

## Parameter tuning

|Method|Description|
|-|-|
|Cross-validation| 10-fold cross validation. This method usually requires large-scale genotype dataset.|
|Independent population| Perform validation in an independent population of the same ancestry. |
|Pseudo-validation|A few methods can estimate a single optimal shrinkage parameter using only the base GWAS summary statistics.|

## PGS Catalog

Just like GWAS Catalog, you can now download published PRS  models from PGS catalog. 

URL: http://www.pgscatalog.org/

<img width="800" alt="image" src="https://user-images.githubusercontent.com/40289485/213737219-efe31848-ab72-4962-9045-2203a0733728.png">

Reference: Lambert, S. A., Gil, L., Jupp, S., Ritchie, S. C., Xu, Y., Buniello, A., ... & Inouye, M. (2021). The Polygenic Score Catalog as an open database for reproducibility and systematic evaluation. Nature Genetics, 53(4), 420-425.

## Calculate PRS using PLINK

```
plink --score
```

## Regressions for evaluation of PRS

$$Phenotype \sim PRS_{phenotype} + Covariates$$

$$logit(P) \sim PRS_{phenotype} + Covariates$$

Covariates usually include sex, age and top 10 PCs.

## Evaluation

### ROC, AIC, AUC, and C-index

ROC : receiver operating characteristic curve shows the performance of a classification model at all thresholds.

- "y" : True Positive rate. ${{TP}\over{TP + FN}}$
- "x" : False Positive rate. ${{FP}\over{FP + TN}}$

AUC: area under the ROC Curve, a common measure for the performance of a classification model.


!!! info "AIC"
    Akaike Information Criterion (AIC): a measure for comparison of different statistical models.

    $$AIC = 2k - 2ln(\hat{L})$$

    - $k$ : number of estimated parameters
    - $\hat{L}$ : maximum value of the model likelihood function


!!! info  "C-index"
    **C-index**: concordance index, which is a metric to evaluate the predictive performance of models and is commonly used in survival analysis. It is a measure of the probability that the predicted scores $M_i$ and $ M_j$ by a model of two randomly selected individuals $i$ and $j$, have the reverse relative order as their true event times $T_i, T_j$.

    $$ C = Pr (M_j > M_i | T_j < T_i) $$

    Interpretation: Individuals with higher scores should have higher risk of the disease events
    
    Reference: Harrell, F. E., Califf, R. M., Pryor, D. B., Lee, K. L., & Rosati, R. A. (1982). Evaluating the yield of medical tests. Jama, 247(18), 2543-2546.
    Reference: Longato, E., Vettoretti, M., & Di Camillo, B. (2020). A practical perspective on the concordance index for the evaluation and selection of prognostic time-to-event models. Journal of Biomedical Informatics, 108, 103496.

### R2 and pseudo-R2

!!! info "Coefficient of determination"
    $R^2$ : coefficient of determination, which measures the amount of variance explained by the regression model.
    
    In linear regression:

    $$ R^2 = 1 - {{RSS}\over{TSS}} $$

    - $RSS$ : sum of squares of residuals
    - $TSS$ : total sum of squares

!!! info "Pseudo-R2 (Nagelkerke)" 

    In logistic regression, 

    One of the most commonly used Pseudo-R2 for PRS analysis is Nagelkerke's $R^2$

    $$R^2_{Nagelkerke} = {{1 - ({{L_0}\over{L_M}})^{2/n}}\over{1 - L_0^{2/n}}}$$

    - $L_0$ : Likelihood of the null model
    - $L_full$ : Likelihood of the full model

### R2 on the liability scale (Lee)

!!! info "R2 on liability scale"

    $R^2$ on the liability scale for ascertained case-control studies
    
    $$ R^2_l = {{R_o^2 C}\over{1 + R_o^2 \theta C }} $$

    - $C$ and $\theta$ are correcting factors for ascertainment
    - $C = {{K(1-K)}\over{Z^2}}{{K(1-K)}\over{P(1-P)}}$ 
    - $\theta = m {{P-K}\over{1-K}} ( m{{P-K}\over{1-K}} - t)$  

    - $K$ : population disease prevalence
    - $P$ : sample disease prevalence
    - $t$: the threshold on the normal distribution truncating the proportion of disease prevalence K
    - $m = z / K$ : mean liability for cases
    - $z = f(t)$ : the value of probability density function of standard normal distribution at t 
    
    Reference : Lee, S. H., Goddard, M. E., Wray, N. R., & Visscher, P. M. (2012). A better coefficient of determination for genetic profile analysis. Genetic epidemiology, 36(3), 214-224.

    The authors also provided R codes for calculation (removed unrelated codes for simplicity)
    
    ```R
    # R2 on the liability scale using the transformation

    nt = total number of the sample
    ncase = number of cases
    ncont = number of controls
    thd = the threshold on the normal distribution which truncates the proportion of disease prevalence
    K = population prevalence
    P = proportion of cases in the case-control samples

    #threshold
    thd = -qnorm(K,0,1)
    
    #value of standard normal density function at thd
    zv = dnorm(thd) 

    #mean liability for case
    mv = zv/K 
    
    #linear model
    lmv = lm(y∼g) 
    
    #R20 : R2 on the observed scale
    R2O = var(lmv$fitted.values)/(ncase/nt*ncont/nt)

    # calculate correction factors
    theta = mv*(P-K)/(1-K)*(mv*(P-K)/(1-K)-thd) 
    cv = K*(1-K)/zv^2*K*(1-K)/(P*(1-P)) 
    
    # convert to R2 on the liability scale
    R2 = R2O*cv/(1+R2O*theta*cv)
    ```

## Bootstrap Confidence Interval Methods for R2

Bootstrap is a commonly used resampling method to generate a sampling distribution from the known sample dataset. It repeatedly takes random samples with replacement from the known sample dataset.

Steps:

- Sample with replacement B times. (B should be large.)
- Estimate the parameter using the bootstrp sample. 
- Obtain the approximate distribution of the parameter.

The percentile bootstrap interval is then defined as the interval between $100 \times \alpha /2$ and $100 \times (1 - \alpha /2)$ percentiles of the parameters estimated by bootstrapping. We can use this method to estimate the  bootstrap interval for $R^2$.

## Meta-scoring methods for PRS

It has been shown recently that the PRS models generated from multiple traits using a meta-scoring method potentially outperforms PRS models generated from a single trait.
Inouye et al. first used this approach for generating a PRS model for CAD from multiple PRS models. 

!!! note "Potential advantages of meta-score for PRS generation"
    
    - increased marker coverage
    - reduced genotyping or imputation uncertainty
    - more accurate effect size estimates

    Reference: Inouye, M., Abraham, G., Nelson, C. P., Wood, A. M., Sweeting, M. J., Dudbridge, F., ... & UK Biobank CardioMetabolic Consortium CHD Working Group. (2018). Genomic risk prediction of coronary artery disease in 480,000 adults: implications for primary prevention. Journal of the American College of Cardiology, 72(16), 1883-1893.

!!! info "elastic net"
    Elastic net is a common approach for variable selection when there are highly correlated variables (for example, PRS of correlated diseases are often highly correlated.). When fitting linear or logistic models, L1 and L2 penalties are added (regularization). 

    $$ \hat{\beta} \equiv argmin({\parallel y- X \beta \parallel}^2 + \lambda_2{\parallel \beta \parallel}^2 + \lambda_1{\parallel \beta \parallel} ) $$

    After validation, PRS can be generated from distinct PRS for other genetically correlated diseases :  

    $$PRS_{meta} = {w_1}PRS_{Trait1} + {w_2}PRS_{Trait2} + {w_3}PRS_{Trait3} + ... $$

    An example: Abraham, G., Malik, R., Yonova-Doing, E., Salim, A., Wang, T., Danesh, J., ... & Dichgans, M. (2019). Genomic risk score offers predictive performance comparable to clinical risk factors for ischaemic stroke. Nature communications, 10(1), 1-10.


## Reference

- **PLINK** : Purcell, Shaun, et al. "PLINK: a tool set for whole-genome association and population-based linkage analyses." The American journal of human genetics 81.3 (2007): 559-575.
- **PGS Catalog** : Lambert, Samuel A., et al. "The Polygenic Score Catalog as an open database for reproducibility and systematic evaluation." Nature Genetics 53.4 (2021): 420-425.
- **PRS-CS** : Ge, Tian, et al. "Polygenic prediction via Bayesian regression and continuous shrinkage priors." Nature communications 10.1 (2019): 1-10.
- **PRS Tutorial**: Choi, Shing Wan, Timothy Shin-Heng Mak, and Paul F. O’Reilly. "Tutorial: a guide to performing polygenic risk score analyses." Nature protocols 15.9 (2020): 2759-2772.
- **R2 on liability scale**: Lee, S. H., Goddard, M. E., Wray, N. R., & Visscher, P. M. (2012). A better coefficient of determination for genetic profile analysis. Genetic epidemiology, 36(3), 214-224.
- **metaGRS 1**: Inouye, M., Abraham, G., Nelson, C. P., Wood, A. M., Sweeting, M. J., Dudbridge, F., ... & UK Biobank CardioMetabolic Consortium CHD Working Group. (2018). Genomic risk prediction of coronary artery disease in 480,000 adults: implications for primary prevention. Journal of the American College of Cardiology, 72(16), 1883-1893.
- **metaGRS 2**: Abraham, G., Malik, R., Yonova-Doing, E., Salim, A., Wang, T., Danesh, J., ... & Dichgans, M. (2019). Genomic risk score offers predictive performance comparable to clinical risk factors for ischaemic stroke. Nature communications, 10(1), 1-10.
- **C-index 1**: Harrell, F. E., Califf, R. M., Pryor, D. B., Lee, K. L., & Rosati, R. A. (1982). Evaluating the yield of medical tests. Jama, 247(18), 2543-2546.
- **C-index 2**: Longato, E., Vettoretti, M., & Di Camillo, B. (2020). A practical perspective on the concordance index for the evaluation and selection of prognostic time-to-event models. Journal of Biomedical Informatics, 108, 103496.
