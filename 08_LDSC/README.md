# LD score regression

## Table of Contents
- [Introduction](#introduction)
- [Install LDSC](#install-ldsc)
- [Data Preparation](#data-preparation)
- [LD score regression](#ld-score-regression)
- [Cross-trait LD score regression](#cross-trait-ld-score-regression)
- [Partitioned LD regression](#partitioned-ld-regression)
- [Celltype specificity LD regression](#celltype-specificity-ld-regression)

## Introduction

LDSC is one of the most commonly used command line tool to estimate hertability, genetic correlation and cell/tissue type specificity from GWAS summary statistics. 

LD: Linkage disequilibrium

For details of LD score regression, please refer to :
- Bulik-Sullivan, Brendan K., et al. "LD Score regression distinguishes confounding from polygenicity in genome-wide association studies." Nature genetics 47.3 (2015): 291-295.


## Install LDSC

LDSC can be downloaded from github (GPL-3.0 license):
[https://github.com/bulik/ldsc](https://github.com/bulik/ldsc)

For ldsc, we need anaconda to create virtual environment. 
If you haven't installed Anaconda, please check [how to install anaconda](https://cloufield.github.io/GWASTutorial/80_anaconda/).

```Bash
# change to your directory for tools
cd ~/tools

# clone the ldsc github repository
git clone https://github.com/bulik/ldsc.git

# create a virtual environment for ldsc (python2)
cd ldsc
conda env create --file environment.yml  

# activate ldsc environment
conda activate ldsc
```


## Data Preparation 

In this tutoial, we will use sample summary statistics for HDLC and LDLC from Jenger. 
- Kanai, Masahiro, et al. "Genetic analysis of quantitative traits in the Japanese population links cell types to complex human diseases." Nature genetics 50.3 (2018): 390-400.

The Miami plot for the two traits:

<img width="682" alt="image" src="https://user-images.githubusercontent.com/40289485/209749071-171c150a-19aa-41f0-b6e6-2ef5fa87370d.png">

### Download sample summary statistics

```Bash
# HDL-c and LDL-c in Biobank Japan
wget -O BBJ_LDLC.txt.gz http://jenger.riken.jp/61analysisresult_qtl_download/
wget -O BBJ_HDLC.txt.gz http://jenger.riken.jp/47analysisresult_qtl_download/
```

### Download reference files

```Bash
# change to your ldsc directory
cd ~/tools/ldsc
mkdir resource
cd ./resource

# snplist
wget https://storage.googleapis.com/broad-alkesgroup-public/LDSCORE/w_hm3.snplist.bz2

# EAS ld score files
wget https://storage.googleapis.com/broad-alkesgroup-public/LDSCORE/eas_ldscores.tar.bz2

# EAS weight
wget https://storage.googleapis.com/broad-alkesgroup-public/LDSCORE/1000G_Phase3_EAS_weights_hm3_no_MHC.tgz

# EAS frequency
wget https://storage.googleapis.com/broad-alkesgroup-public/LDSCORE/1000G_Phase3_EAS_plinkfiles.tgz

# EAS baseline model
wget https://storage.googleapis.com/broad-alkesgroup-public/LDSCORE/1000G_Phase3_EAS_baseline_v1.2_ldscores.tgz

# Cell type ld score files
wget https://storage.googleapis.com/broad-alkesgroup-public/LDSCORE/LDSC_SEG_ldscores/Cahoy_EAS_1000Gv3_ldscores.tar.gz

```
You can then decompress the files and organize them.

## Munge sumstats

Before the analysis, we need to format and clean the raw sumstats.

```Bash
snplist=~/tools/ldsc/resource/w_hm3.snplist
munge_sumstats.py \
	--sumstats BBJ_HDLC.txt.gz \
	--merge-alleles $snplist \
	--a1 ALT \
	--a2 REF \
	--out BBJ_HDLC
munge_sumstats.py \
  --sumstats BBJ_LDLC.txt.gz \
	--a1 ALT \
  --a2 REF \
  --merge-alleles $snplist \
  --out BBJ_LDLC
```

After munging, you will get two munged and formatted files:

```
BBJ_HDLC.sumstats.gz
BBJ_LDLC.sumstats.gz
```
And these are the files we will use to run LD score regression.

## LD score regression

Univariate LD score regression is utilized to estimate heritbility and confuding factors (cryptic relateness and population stratification) of a certain trait. 

- Reference : Bulik-Sullivan, Brendan K., et al. "LD Score regression distinguishes confounding from polygenicity in genome-wide association studies." Nature genetics 47.3 (2015): 291-295.

Using the munged sumstats, we can run:

```Bash
ldsc.py \
  --h2 BBJ_HDLC.sumstats.gz \
  --ref-ld-chr ~/tools/ldsc/resource/eas_ldscores/ \
  --w-ld-chr ~/tools/ldsc/resource/eas_ldscores/ \
  --out BBJ_HDLC

ldsc.py \
  --h2 BBJ_LDLC.sumstats.gz \
  --ref-ld-chr ~/tools/ldsc/resource/eas_ldscores/ \
  --w-ld-chr ~/tools/ldsc/resource/eas_ldscores/ \
  --out BBJ_LDLC

```

Lest's check the results for HDLC:

```Bash
cat BBJ_HDLC.log
*********************************************************************
* LD Score Regression (LDSC)
* Version 1.0.1
* (C) 2014-2019 Brendan Bulik-Sullivan and Hilary Finucane
* Broad Institute of MIT and Harvard / MIT Department of Mathematics
* GNU General Public License v3
*********************************************************************
Call: 
./ldsc.py \
--h2 BBJ_HDLC.sumstats.gz \
--ref-ld-chr /home/he/tools/ldsc/resource/eas_ldscores/ \
--out BBJ_HDLC \
--w-ld-chr /home/he/tools/ldsc/resource/eas_ldscores/ 

Beginning analysis at Sat Dec 24 20:40:34 2022
Reading summary statistics from BBJ_HDLC.sumstats.gz ...
Read summary statistics for 1020377 SNPs.
Reading reference panel LD Score from /home/he/tools/ldsc/resource/eas_ldscores/[1-22] ... (ldscore_fromlist)
Read reference panel LD Scores for 1208050 SNPs.
Removing partitioned LD Scores with zero variance.
Reading regression weight LD Score from /home/he/tools/ldsc/resource/eas_ldscores/[1-22] ... (ldscore_fromlist)
Read regression weight LD Scores for 1208050 SNPs.
After merging with reference panel LD, 1012040 SNPs remain.
After merging with regression SNP LD, 1012040 SNPs remain.
Using two-step estimator with cutoff at 30.
Total Observed scale h2: 0.1583 (0.0281)
Lambda GC: 1.1523
Mean Chi^2: 1.2843
Intercept: 1.0563 (0.0114)
Ratio: 0.1981 (0.0402)
Analysis finished at Sat Dec 24 20:40:41 2022
Total time elapsed: 6.57s
```

We can see that from the log:

- Observed scale h2 = 0.1583
- lambda GC = 1.1523 
- intercept = 1.0563
- Ratio = 0.1981

According to LDSC documents, Ratio measures the proportion of the inflation in the mean chi^2 that the LD Score regression intercept ascribes to causes other than polygenic heritability. The value of ratio should be close to zero, though in practice values of 10-20% are not uncommon.

- Ratio = (intercept-1)/(mean(chi^2)-1)

## Cross-trait LD score regression

Cross-trait LD score regression is employed to estimate the genetic correlation between a pair of traits.

- Reference: Bulik-Sullivan, Brendan, et al. "An atlas of genetic correlations across human diseases and traits." Nature genetics 47.11 (2015): 1236-1241.

```Bash
ldsc.py \
  --rg BBJ_HDLC.sumstats.gz,BBJ_LDLC.sumstats.gz \
  --ref-ld-chr ~/tools/ldsc/resource/eas_ldscores/ \
  --w-ld-chr ~/tools/ldsc/resource/eas_ldscores/ \
  --out BBJ_HDLC_LDLC

```
Let's check the results:

```
*********************************************************************
* LD Score Regression (LDSC)
* Version 1.0.1
* (C) 2014-2019 Brendan Bulik-Sullivan and Hilary Finucane
* Broad Institute of MIT and Harvard / MIT Department of Mathematics
* GNU General Public License v3
*********************************************************************
Call: 
./ldsc.py \
--ref-ld-chr /home/he/tools/ldsc/resource/eas_ldscores/ \
--out BBJ_HDLC_LDLC \
--rg BBJ_HDLC.sumstats.gz,BBJ_LDLC.sumstats.gz \
--w-ld-chr /home/he/tools/ldsc/resource/eas_ldscores/ 

Beginning analysis at Thu Dec 29 21:02:37 2022
Reading summary statistics from BBJ_HDLC.sumstats.gz ...
Read summary statistics for 1020377 SNPs.
Reading reference panel LD Score from /home/he/tools/ldsc/resource/eas_ldscores/[1-22] ... (ldscore_fromlist)
Read reference panel LD Scores for 1208050 SNPs.
Removing partitioned LD Scores with zero variance.
Reading regression weight LD Score from /home/he/tools/ldsc/resource/eas_ldscores/[1-22] ... (ldscore_fromlist)
Read regression weight LD Scores for 1208050 SNPs.
After merging with reference panel LD, 1012040 SNPs remain.
After merging with regression SNP LD, 1012040 SNPs remain.
Computing rg for phenotype 2/2
Reading summary statistics from BBJ_LDLC.sumstats.gz ...
Read summary statistics for 1217311 SNPs.
After merging with summary statistics, 1012040 SNPs remain.
1012040 SNPs with valid alleles.

Heritability of phenotype 1
---------------------------
Total Observed scale h2: 0.1054 (0.0383)
Lambda GC: 1.1523
Mean Chi^2: 1.2843
Intercept: 1.1234 (0.0607)
Ratio: 0.4342 (0.2134)

Heritability of phenotype 2/2
-----------------------------
Total Observed scale h2: 0.0543 (0.0211)
Lambda GC: 1.0833
Mean Chi^2: 1.1465
Intercept: 1.0583 (0.0335)
Ratio: 0.398 (0.2286)

Genetic Covariance
------------------
Total Observed scale gencov: 0.0121 (0.0106)
Mean z1*z2: -0.001
Intercept: -0.0198 (0.0121)

Genetic Correlation
-------------------
Genetic Correlation: 0.1601 (0.1821)
Z-score: 0.8794
P: 0.3792


Summary of Genetic Correlation Results
p1                    p2      rg      se       z       p  h2_obs  h2_obs_se  h2_int  h2_int_se  gcov_int  gcov_int_se
BBJ_HDLC.sumstats.gz  BBJ_LDLC.sumstats.gz  0.1601  0.1821  0.8794  0.3792  0.0543     0.0211  1.0583     0.0335   -0.0198       0.0121

Analysis finished at Thu Dec 29 21:02:47 2022
Total time elapsed: 10.39s
```


## Partitioned LD regression

- Reference: Finucane, Hilary K., et al. "Partitioning heritability by functional annotation using genome-wide association summary statistics." Nature genetics 47.11 (2015): 1228-1235.

```Bash
ldsc.py \
  --h2 BBJ_HDLC.sumstats.gz \
  --overlap-annot \
  --ref-ld-chr ~/tools/ldsc/resource/1000G_Phase3_EAS_baseline_v1_2_ldscores/baseline. \
  --frqfile-chr ~/tools/ldsc/resource/1000G_Phase3_EAS_plinkfiles/1000G.EAS.QC. \
  --w-ld-chr ~/tools/ldsc/resource/1000G_Phase3_EAS_weights_hm3_no_MHC/weights.EAS.hm3_noMHC. \
  --out BBJ_HDLC_baseline

```

## Celltype specificity LD regression 

LDSC-SEG

- Reference: Finucane, Hilary K., et al. "Heritability enrichment of specifically expressed genes identifies disease-relevant tissues and cell types." Nature genetics 50.4 (2018): 621-629.

```Bash
ldsc.py \
  --h2-cts BBJ_HDLC.sumstats.gz \
  --ref-ld-chr-cts ~/tools/ldsc/resource/Cahoy_EAS_1000Gv3_ldscores/Cahoy.EAS.ldcts \
  --ref-ld-chr ~/tools/ldsc/resource/1000G_Phase3_EAS_baseline_v1_2_ldscores/baseline. \
  --w-ld-chr ~/tools/ldsc/resource/1000G_Phase3_EAS_weights_hm3_no_MHC/weights.EAS.hm3_noMHC. \
  --out BBJ_HDLC_baseline_cts
```

## Reference
- Bulik-Sullivan, Brendan K., et al. "LD Score regression distinguishes confounding from polygenicity in genome-wide association studies." Nature genetics 47.3 (2015): 291-295.
- Bulik-Sullivan, Brendan, et al. "An atlas of genetic correlations across human diseases and traits." Nature genetics 47.11 (2015): 1236-1241.
- Finucane, Hilary K., et al. "Partitioning heritability by functional annotation using genome-wide association summary statistics." Nature genetics 47.11 (2015): 1228-1235.
- Finucane, Hilary K., et al. "Heritability enrichment of specifically expressed genes identifies disease-relevant tissues and cell types." Nature genetics 50.4 (2018): 621-629.
- Kanai, Masahiro, et al. "Genetic analysis of quantitative traits in the Japanese population links cell types to complex human diseases." Nature genetics 50.3 (2018): 390-400.
