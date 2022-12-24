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
Bulik-Sullivan, Brendan K., et al. "LD Score regression distinguishes confounding from polygenicity in genome-wide association studies." Nature genetics 47.3 (2015): 291-295.


## Install LDSC

LDSC can be downloaded from github (GPL-3.0 license):
[https://github.com/bulik/ldsc](https://github.com/bulik/ldsc)

```
# change to your directory for tools
cd ~/tools

# clone the ldsc github repository
git clone https://github.com/bulik/ldsc.git

# create a virtual environment for ldsc (python2)
cd ldsc
conda env create --file environment.yml  
```

## Data Preparation 

In this tutoial, we will use sample summary statistics for HDLC and LDLC from Jenger. 
- Kanai, Masahiro, et al. "Genetic analysis of quantitative traits in the Japanese population links cell types to complex human diseases." Nature genetics 50.3 (2018): 390-400.

Download sample summary statistics : 
```Bash
# HDL-c and LDL-c in Biobank Japan
wget -O BBJ_LDLC.txt.gz http://jenger.riken.jp/61analysisresult_qtl_download/
wget -O BBJ_HDLC.txt.gz http://jenger.riken.jp/47analysisresult_qtl_download/
```

Download reference files:
```
# snplist

# EAS ld score files

# weight

# EAS frequency

# Cell type ld score files

```


Munge sumstats
```
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


## LD score regression

Estimation of heritbility and confuding factors (cryptic relateness and population stratification) 

-Bulik-Sullivan, Brendan K., et al. "LD Score regression distinguishes confounding from polygenicity in genome-wide association studies." Nature genetics 47.3 (2015): 291-295.

```
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


## Cross-trait LD score regression

Estimation of genetic correlation

-Bulik-Sullivan, Brendan, et al. "An atlas of genetic correlations across human diseases and traits." Nature genetics 47.11 (2015): 1236-1241.

```
ldsc.py \
  --rg BBJ_HDLC.sumstats.gz,BBJ_LDLC.sumstats.gz \
  --ref-ld-chr ~/tools/ldsc/resource/eas_ldscores/ \
  --w-ld-chr ~/tools/ldsc/resource/eas_ldscores/ \
  --out BBJ_HDLC_LDLC

```

## Partitioned LD regression
-Finucane, Hilary K., et al. "Partitioning heritability by functional annotation using genome-wide association summary statistics." Nature genetics 47.11 (2015): 1228-1235.

```
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
-Finucane, Hilary K., et al. "Heritability enrichment of specifically expressed genes identifies disease-relevant tissues and cell types." Nature genetics 50.4 (2018): 621-629.

```
ldsc.py \
  --h2-cts BBJ_HDLC.sumstats.gz \
  --ref-ld-chr-cts ~/tools/ldsc/resource/Cahoy_EAS_1000Gv3_ldscores/Cahoy.EAS.ldcts \
  --ref-ld-chr ~/tools/ldsc/resource/1000G_Phase3_EAS_baseline_v1_2_ldscores/baseline. \
  --w-ld-chr ~/tools/ldsc/resource/1000G_Phase3_EAS_weights_hm3_no_MHC/weights.EAS.hm3_noMHC. \
  --out BBJ_HDLC_baseline_cts
```

## Reference
-Bulik-Sullivan, Brendan K., et al. "LD Score regression distinguishes confounding from polygenicity in genome-wide association studies." Nature genetics 47.3 (2015): 291-295.
-Bulik-Sullivan, Brendan, et al. "An atlas of genetic correlations across human diseases and traits." Nature genetics 47.11 (2015): 1236-1241.
-Finucane, Hilary K., et al. "Partitioning heritability by functional annotation using genome-wide association summary statistics." Nature genetics 47.11 (2015): 1228-1235.
-Finucane, Hilary K., et al. "Heritability enrichment of specifically expressed genes identifies disease-relevant tissues and cell types." Nature genetics 50.4 (2018): 621-629.