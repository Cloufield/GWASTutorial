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
    Add GCTA to the path where you have added to your environment like `ln -s /home/yunye/tools/gcta/gcta-1.94.1-linux-kernel-3-x86_64 /home/yunye/tools/bin/gcta`.

## Make GRM

We use the QCed genotypes from previous sections. Additionally, we include only LD-pruned SNPs with MAF>0.01.

```bash
#!/bin/bash
plinkFile="../04_Data_QC/sample_data.clean"
prunedSNP="../04_Data_QC/plink_results.prune.in"

gcta \
  --bfile ${plinkFile} \
  --extract ${prunedSNP} \
  --autosome \
  --maf 0.01 \
  --make-grm \
  --out 1kg_eas
```



```
*******************************************************************
* GCTA (Genome-wide Complex Trait Analysis)
* Version v1.94.1 Mac
* (C) 2010-present, Yang Lab, Westlake University
* Please report bugs to Jian Yang jian.yang@westlake.edu.cn
* MIT License
*******************************************************************
Analysis started at 10:30:35 JST on Fri Oct 25 2024.
Hostname: Yunyes-MacBook-Air.local

Options: 
 
--bfile ../04_Data_QC/sample_data.clean 
--extract ../04_Data_QC/plink_results.prune.in 
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
Get 218959 SNPs from list [../04_Data_QC/plink_results.prune.in].
After extracting SNP, 218950 SNPs remain.
Threshold to filter variants: MAF > 0.010000.
Computing the genetic relationship matrix (GRM) v2 ...
Subset 1/1, no. subject 1-500
  500 samples, 218950 markers, 125250 GRM elements
IDs for the GRM file have been saved in the file [1kg_eas.grm.id]
Computing GRM...
  100% finished in 1.3 sec
218950 SNPs have been processed.
  Used 218895 valid SNPs.
The GRM computation is completed.
Saving GRM...
GRM has been saved in the file [1kg_eas.grm.bin]
Number of SNPs in each pair of individuals has been saved in the file [1kg_eas.grm.N.bin]

Analysis finished at 10:30:37 JST on Fri Oct 25 2024
Overall computational time: 2.31 sec.


```

## Estimation

```
#!/bin/bash

#the grm we calculated in step1
GRM=1kg_eas

# phenotype file
phenotypeFile=../01_Dataset/1kgeas_binary.txt

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
* GCTA (Genome-wide Complex Trait Analysis)
* Version v1.94.1 Mac
* (C) 2010-present, Yang Lab, Westlake University
* Please report bugs to Jian Yang jian.yang@westlake.edu.cn
* MIT License
*******************************************************************
Analysis started at 10:30:39 JST on Fri Oct 25 2024.
Hostname: Yunyes-MacBook-Air.local

Accepted options:
--grm 1kg_eas
--pheno ../01_Dataset/1kgeas_binary.txt
--prevalence 0.5
--qcovar 5PCs.txt
--reml
--out 1kg_eas

Note: This is a multi-thread program. You could specify the number of threads by the --thread-num option to speed up the computation if there are multiple processors in your machine.

Reading IDs of the GRM from [1kg_eas.grm.id].
500 IDs are read from [1kg_eas.grm.id].
Reading the GRM from [1kg_eas.grm.bin].
GRM for 500 individuals are included from [1kg_eas.grm.bin].
Reading phenotypes from [../01_Dataset/1kgeas_binary.txt].
Non-missing phenotypes of 503 individuals are included from [../01_Dataset/1kgeas_binary.txt].
Reading quantitative covariate(s) from [5PCs.txt].
5 quantitative covariate(s) of 501 individuals are included from [5PCs.txt].
Assuming a disease phenotype for a case-control study: 248 cases and 250 controls 
5 quantitative variable(s) included as covariate(s).
498 individuals are in common in these files.

Performing  REML analysis ... (Note: may take hours depending on sample size).
498 observations, 6 fixed effect(s), and 2 variance component(s)(including residual variance).
Calculating prior values of variance components by EM-REML ...
Updated prior values:  0.12507 0.125103
logL: 94.8795
Running AI-REML algorithm ...
Iter.	logL	V(G)	V(e)	
1	94.88	0.11602	0.13397	
2	94.88	0.09717	0.15242	
3	94.89	0.09868	0.15093	
4	94.89	0.09856	0.15105	
5	94.89	0.09857	0.15104	
Log-likelihood ratio converged.

Calculating the logLikelihood for the reduced model ...
(variance component 1 is dropped from the model)
Calculating prior values of variance components by EM-REML ...
Updated prior values: 0.24901
logL: 94.78258
Running AI-REML algorithm ...
Iter.	logL	V(e)	
1	94.79	0.24900	
2	94.79	0.24899	
Log-likelihood ratio converged.

Summary result of REML analysis:
Source	Variance	SE
V(G)	0.098572	0.229001
V(e)	0.151038	0.227241
Vp	0.249609	0.016025
V(G)/Vp	0.394903	0.914119
The estimate of variance explained on the observed scale is transformed to that on the underlying liability scale:
(Proportion of cases in the sample = 0.497992; User-specified disease prevalence = 0.500000)
V(G)/Vp_L	0.620322	1.435918

Sampling variance/covariance of the estimates of variance components:
5.244129e-02	-5.191137e-02	
-5.191137e-02	5.163826e-02	

Summary result of REML analysis has been saved in the file [1kg_eas.hsq].

Analysis finished at 10:30:39 JST on Fri Oct 25 2024
Overall computational time: 0.08 sec.
```

!!! warning
    We only included a limited number of samples (<500) in this analysis, which is insufficient.

It is helpful to check the [FAQ section of GCTA](https://yanglab.westlake.edu.cn/software/gcta/#FAQ) if you encounter any errors. 

## Reference

- Yang, J., Lee, S. H., Goddard, M. E., & Visscher, P. M. (2011). GCTA: a tool for genome-wide complex trait analysis. The American Journal of Human Genetics, 88(1), 76-82.
- [https://yanglab.westlake.edu.cn/software/gcta/#Overview](https://yanglab.westlake.edu.cn/software/gcta/#Overview)
