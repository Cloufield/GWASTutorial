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
3. **Evaluation** in an independent population

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
    
    plinkFile=../04_Data_QC/sample_data.clean
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
    2    1   2:55513738:C:T   55513738   1.69e-15       52      0      3      1      6     42 2:55305475:A:T(1),2:55338196:T:C(1),2:55347135:G:A(1),2:55351853:A:G(1),2:55363460:G:A(1),2:55395372:A:G(1),2:55395578:G:A(1),2:55395807:C:T(1),2:55405847:C:A(1),2:55408556:C:A(1),2:55410835:C:T(1),2:55413644:C:G(1),2:55435439:C:T(1),2:55449464:T:C(1),2:55469819:A:T(1),2:55492154:G:A(1),2:55500529:A:G(1),2:55502651:A:G(1),2:55508333:G:C(1),2:55563020:A:G(1),2:55572944:T:C(1),2:55585915:A:G(1),2:55599810:C:T(1),2:55605943:A:G(1),2:55611766:T:C(1),2:55612986:G:C(1),2:55619923:C:T(1),2:55622624:G:A(1),2:55624520:C:T(1),2:55628936:G:C(1),2:55638830:T:C(1),2:55639023:A:T(1),2:55639980:C:T(1),2:55640649:G:A(1),2:55641045:G:A(1),2:55642887:C:T(1),2:55647729:A:G(1),2:55650512:G:A(1),2:55659155:A:G(1),2:55665620:A:G(1),2:55667476:G:T(1),2:55670729:A:G(1),2:55676257:C:T(1),2:55685927:C:A(1),2:55689569:A:T(1),2:55689913:T:C(1),2:55693097:C:G(1),2:55707583:T:C(1),2:55720135:C:G(1)
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
plink --score <score_filename> [variant ID col.] [allele col.] [score col.] ['header']
```

- `<score_filename>`: the score file
- `[variant ID col.]`: the column number for variant IDs
- `[allele col.]`: the column number for effect alleles
- `[score col.]`: the column number for betas
- `['header']`: skip the first header line

Please check [here](https://www.cog-genomics.org/plink/1.9/score) for detailed documents on `plink --score`.

!!! example 
    ```
    # genotype data
    plinkFile=../04_Data_QC/sample_data.clean
    # summary statistics for scoring
    sumStats=./t2d_plink_reduced.txt
    # SNPs after clumpping
    awk 'NR!=1{print $3}' 1kgeas.clumped >  1kgeas.valid.snp
    
    plink \
        --bfile ${plinkFile} \
        --score ${sumStats} 1 2 3 header \
        --extract 1kgeas.valid.snp \
        --out 1kgeas
    ```


For thresholding using P values,  we can create a range file and a p-value file.

The options we use:
```
--q-score-range <range file> <data file> [variant ID col.] [data col.] ['header']
```

!!! example
    ```
    # SNP - P value file for thresholding
    awk '{print $1,$4}' ${sumStats} > SNP.pvalue
    
    # create a range file with 3 columns: range label, p-value lower bound, p-value upper bound
    head range_list
    pT0.001 0 0.001
    pT0.05 0 0.05
    pT0.1 0 0.1
    pT0.2 0 0.2
    pT0.3 0 0.3
    pT0.4 0 0.4
    pT0.5 0 0.5
    ```
    
    and then calculate the scores using the p-value ranges:
    
    ```
    plink2 \
    --bfile ${plinkFile} \
    --score ${sumStats} 1 2 3 header cols=nallele,scoreavgs,denom,scoresums\
    --q-score-range range_list SNP.pvalue \
    --extract 1kgeas.valid.snp \
    --out 1kgeas
    ```

    You will get the following files:
    ```
    1kgeas.pT0.001.sscore
    1kgeas.pT0.05.sscore
    1kgeas.pT0.1.sscore
    1kgeas.pT0.2.sscore
    1kgeas.pT0.3.sscore
    1kgeas.pT0.4.sscore
    1kgeas.pT0.5.sscore
    ```

    Take a look at the files:
    
    ```
    head 1kgeas.pT0.1.sscore
    #IID    ALLELE_CT       DENOM   SCORE1_AVG      SCORE1_SUM
    HG00403 54554   54976   2.84455e-05     1.56382
    HG00404 54574   54976   5.65172e-05     3.10709
    HG00406 54284   54976   -3.91872e-05    -2.15436
    HG00407 54348   54976   -9.87606e-05    -5.42946
    HG00409 54760   54976   1.67157e-05     0.918963
    HG00410 54656   54976   3.74405e-05     2.05833
    HG00419 54052   54976   -6.4035e-05     -3.52039
    HG00421 54210   54976   -1.55942e-05    -0.857305
    HG00422 54102   54976   5.28824e-05     2.90726
    ```

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
- **metaGRS 1**: Inouye, M., Abraham, G., Nelson, C. P., Wood, A. M., Sweeting, M. J., Dudbridge, F., ... & UK Biobank CardioMetabolic Consortium CHD Working Group. (2018). Genomic risk prediction of coronary artery disease in 480,000 adults: implications for primary prevention. Journal of the American College of Cardiology, 72(16), 1883-1893.
- **metaGRS 2**: Abraham, G., Malik, R., Yonova-Doing, E., Salim, A., Wang, T., Danesh, J., ... & Dichgans, M. (2019). Genomic risk score offers predictive performance comparable to clinical risk factors for ischaemic stroke. Nature communications, 10(1), 1-10.
