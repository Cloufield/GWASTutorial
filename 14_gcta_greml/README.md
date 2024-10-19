# SNP-Heritability estimation by GCTA-GREML

## Introduction

The basic model behind GCTA-GREML is the linear mixed model (LMM):

$$y = X\beta + Wu + e$$

$$ Var(y) = V = WW^{'}\delta^2_u + I \delta^2_e$$

- $X$ :  covariate matrix
- $W$ :  standardized genotype matrix

GCTA defines $A = WW^{'}/N$ and $\delta^2_g$ as the variance explained by SNPs.

So the oringinal model can be written as:

$$y = X\beta + g + e$$

- $g$ : a vector of total genetic effects

$$ Var(y) = V = A\delta^2_g + I \delta^2_e$$

- $A$ can be regarded as genetic relationship matrix (GRM)  
- $\delta^2_e$ can be estimated by the restricted maximum likelihood (REML) method using all SNPs.

!!! quote GCTA-GREML
    For details, please check Yang, J., Lee, S. H., Goddard, M. E., & Visscher, P. M. (2011). GCTA: a tool for genome-wide complex trait analysis. The American Journal of Human Genetics, 88(1), 76-82. [link](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3014363/).

## Donwload

Download the version of GCTA for your system from : https://yanglab.westlake.edu.cn/software/gcta/#Download

!!! example 

    ```bash
    wget https://yanglab.westlake.edu.cn/software/gcta/bin/gcta-1.94.1-linux-kernel-3-x86_64.zip
    unzip gcta-1.94.1-linux-kernel-3-x86_64.zip
    cd gcta-1.94.1-linux-kernel-3-x86_64.zip

    ./gcta-1.94.1
    *******************************************************************
    * Genome-wide Complex Trait Analysis (GCTA)
    * version v1.94.1 Linux
    * Built at Nov 15 2022 21:14:25, by GCC 8.5
    * (C) 2010-present, Yang Lab, Westlake University
    * Please report bugs to Jian Yang <jian.yang@westlake.edu.cn>
    *******************************************************************
    Analysis started at 12:22:19 JST on Sun Jan 15 2023.
    Hostname: Home-Desktop
    
    Error: no analysis has been launched by the option(s)
    Please see online documentation at https://yanglab.westlake.edu.cn/software/gcta/
    ```

!!! tip 
    Add GCTA to your environment

## Make GRM


```bash
#!/bin/bash
plinkFile="../01_Dataset/1KG.EAS.auto.snp.norm.nodup.split.rare002.common015.missing"
gcta \
  --bfile ${plinkFile} \
  --autosome \
  --maf 0.01 \
  --make-grm \
  --out 1kg_eas
```



```
*******************************************************************
* Genome-wide Complex Trait Analysis (GCTA)
* version v1.94.1 Linux
* Built at Nov 15 2022 21:14:25, by GCC 8.5
* (C) 2010-present, Yang Lab, Westlake University
* Please report bugs to Jian Yang <jian.yang@westlake.edu.cn>
*******************************************************************
Analysis started at 17:21:24 JST on Tue Dec 26 2023.
Hostname: Yunye

Options:

--bfile ../04_Data_QC/sample_data.clean
--autosome
--maf 0.01
--make-grm
--out 1kg_eas

Note: GRM is computed using the SNPs on the autosomes.
Reading PLINK FAM file from [../04_Data_QC/sample_data.clean.fam]...
500 individuals to be included from FAM file.
500 individuals to be included. 0 males, 0 females, 500 unknown.
Reading PLINK BIM file from [../04_Data_QC/sample_data.clean.bim]...
1224104 SNPs to be included from BIM file(s).
Threshold to filter variants: MAF > 0.010000.
Computing the genetic relationship matrix (GRM) v2 ...
Subset 1/1, no. subject 1-500
  500 samples, 1224104 markers, 125250 GRM elements
IDs for the GRM file have been saved in the file [1kg_eas.grm.id]
Computing GRM...
  100% finished in 7.4 sec
1224104 SNPs have been processed.
  Used 1128732 valid SNPs.
The GRM computation is completed.
Saving GRM...
GRM has been saved in the file [1kg_eas.grm.bin]
Number of SNPs in each pair of individuals has been saved in the file [1kg_eas.grm.N.bin]

Analysis finished at 17:21:32 JST on Tue Dec 26 2023
Overall computational time: 8.51 sec.
```

## Estimation

```
#!/bin/bash

#the grm we calculated in step1
GRM=1kg_eas

# phenotype file
phenotypeFile=../01_Dataset/1kgeas_binary_gcta.txt

# disease prevalence used for conversion to liability-scale heritability
prevalence=0.5

# use 5PCs as covariates 
awk '{print $1,$2,$5,$6,$7,$8,$9}' ../05_PCA/plink_results_projected.sscore > 5PCs.txt

gcta \
  --grm ${GRM} \
  --pheno ${phenotypeFile} \
  --prevalence ${prevalence} \
  --qcovar  5PCs.txt \
  --reml \
  --out 1kg_eas

```

## Results

!!! warning
    This is just to show the analysis pipeline. The trait was simulated under an unreal condition (effect size is extremely large) so the result is meaningless here. 
    
    For real analysis, you need a larger sample size to get robust estimation. Please see the [GCTA FAQ](https://yanglab.westlake.edu.cn/software/gcta/#FAQ) 

```bash
*******************************************************************
* Genome-wide Complex Trait Analysis (GCTA)
* version v1.94.1 Linux
* Built at Nov 15 2022 21:14:25, by GCC 8.5
* (C) 2010-present, Yang Lab, Westlake University
* Please report bugs to Jian Yang <jian.yang@westlake.edu.cn>
*******************************************************************
Analysis started at 17:36:37 JST on Tue Dec 26 2023.
Hostname: Yunye

Accepted options:
--grm 1kg_eas
--pheno ../01_Dataset/1kgeas_binary_gcta.txt
--prevalence 0.5
--qcovar 5PCs.txt
--reml
--out 1kg_eas

Note: This is a multi-thread program. You could specify the number of threads by the --thread-num option to speed up the computation if there are multiple processors in your machine.

Reading IDs of the GRM from [1kg_eas.grm.id].
500 IDs are read from [1kg_eas.grm.id].
Reading the GRM from [1kg_eas.grm.bin].
GRM for 500 individuals are included from [1kg_eas.grm.bin].
Reading phenotypes from [../01_Dataset/1kgeas_binary_gcta.txt].
Non-missing phenotypes of 503 individuals are included from [../01_Dataset/1kgeas_binary_gcta.txt].
Reading quantitative covariate(s) from [5PCs.txt].
5 quantitative covariate(s) of 501 individuals are included from [5PCs.txt].
Assuming a disease phenotype for a case-control study: 248 cases and 250 controls
5 quantitative variable(s) included as covariate(s).
498 individuals are in common in these files.

Performing  REML analysis ... (Note: may take hours depending on sample size).
498 observations, 6 fixed effect(s), and 2 variance component(s)(including residual variance).
Calculating prior values of variance components by EM-REML ...
Updated prior values:  0.12498 0.124846
logL: 95.34
Running AI-REML algorithm ...
Iter.   logL    V(G)    V(e)
1       95.34   0.14264 0.10708
2       95.37   0.18079 0.06875
3       95.40   0.18071 0.06888
4       95.40   0.18071 0.06888
Log-likelihood ratio converged.

Calculating the logLikelihood for the reduced model ...
(variance component 1 is dropped from the model)
Calculating prior values of variance components by EM-REML ...
Updated prior values: 0.24901
logL: 94.78319
Running AI-REML algorithm ...
Iter.   logL    V(e)
1       94.79   0.24900
2       94.79   0.24899
Log-likelihood ratio converged.

Summary result of REML analysis:
Source  Variance        SE
V(G)    0.180708        0.164863
V(e)    0.068882        0.162848
Vp      0.249590        0.016001
V(G)/Vp 0.724021        0.654075
The estimate of variance explained on the observed scale is transformed to that on the underlying liability scale:
(Proportion of cases in the sample = 0.497992; User-specified disease prevalence = 0.500000)
V(G)/Vp_L       1.137308        1.027434

Sampling variance/covariance of the estimates of variance components:
2.717990e-02    -2.672171e-02
-2.672171e-02   2.651955e-02

Summary result of REML analysis has been saved in the file [1kg_eas.hsq].

Analysis finished at 17:36:38 JST on Tue Dec 26 2023
Overall computational time: 0.08 sec.
```

## Reference

- Yang, J., Lee, S. H., Goddard, M. E., & Visscher, P. M. (2011). GCTA: a tool for genome-wide complex trait analysis. The American Journal of Human Genetics, 88(1), 76-82.
- [https://yanglab.westlake.edu.cn/software/gcta/#Overview](https://yanglab.westlake.edu.cn/software/gcta/#Overview)
