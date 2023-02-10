
# Linkage disequilibrium(LD)

## LD Definition

Please check [here](https://cloufield.github.io/GWASTutorial/04_Data_QC/#ld-calculation).

Reference: Slatkin, M. (2008). Linkage disequilibrium—understanding the evolutionary past and mapping the medical future. Nature Reviews Genetics, 9(6), 477-485.

## Calculate LD

### LDstore2
LDstore2: http://www.christianbenner.com/#

Reference: Benner, C. et al. Prospects of fine-papping trait-associated genomic regions by using summary statistics from genome-wide association studies. Am. J. Hum. Genet. (2017).

### PLINK LD

Please check [Calculate LD using PLINK](https://cloufield.github.io/GWASTutorial/04_Data_QC/#ld-calculation).

## LD Lookup using LDlink

!!! quote "LDlink"
    LDlink is a suite of web-based applications designed to easily and efficiently interrogate linkage disequilibrium in population groups. Each included application is specialized for querying and displaying unique aspects of linkage disequilibrium.

    [https://ldlink.nci.nih.gov/?tab=home](https://ldlink.nci.nih.gov/?tab=home)

    Reference: Machiela, M. J., & Chanock, S. J. (2015). LDlink: a web-based application for exploring population-specific haplotype structure and linking correlated alleles of possible functional variants. Bioinformatics, 31(21), 3555-3557.

LDlink is a very useful tool for quick lookups of any information related to LD. 

### LDlink-LDpair


### LDlink-LDproxy


### Query in batch using LDlink API

LDlink provides API for queries using command line. 

!!! info "You need to register and get a token first."
    https://ldlink.nci.nih.gov/?tab=apiaccess

!!! example "Query LD proxies for variants using LDproxy API"
    ```
    curl -k -X GET 'https://ldlink.nci.nih.gov/LDlinkRest/ldproxy?var=rs3&pop=MXL&r2_d=r2&window=500000&    genome_build=grch37&token=faketoken123'
    ```

### LDlinkR

There is also a related R package for LDlink. 

!!! example "Query LD proxies for variants using LDlinkR"
```
install.packages("LDlinkR")

library(LDlinkR)

my_proxies <- LDproxy(snp = "rs671", 
                      pop = "EAS", 
                      r2d = "r2", 
                      token = "YourTokenHere123",
                      genome_build = "grch38"
                     )
```

Reference: Myers, T. A., Chanock, S. J., & Machiela, M. J. (2020). LDlinkR: an R package for rapidly calculating linkage disequilibrium statistics in diverse populations. Frontiers in genetics, 11, 157.

## LD-pruning

Please check [LD-pruning](https://cloufield.github.io/GWASTutorial/04_Data_QC/#ld-pruning)

## LD-clumping

Please check [LD-clumping](https://cloufield.github.io/GWASTutorial/10_PRS/#ctpt-using-plink)

## LD score

Definition: https://cloufield.github.io/GWASTutorial/08_LDSC/#ld-score

### LDSC

LD score can be estimated with [LDSC](https://github.com/bulik/ldsc/wiki/LD-Score-Estimation-Tutorial) using PLINK format genotype data as the reference panel.
```
plinkPrefix=chr22

python ldsc.py \
	--bfile ${plinkPrefix}
	--l2 \
	--ld-wind-cm 1\
	--out ${plinkPrefix}
```

Check [here](https://github.com/bulik/ldsc/wiki/LD-Score-Estimation-Tutoria) for details.

### GCTA

[GCTA]() also provides a function to estimate LD scores using PLINK format genotype data.

```
plinkPrefix=chr22

gcta64 \
    --bfile  ${plinkPrefix} \
    --ld-score \
    --ld-wind 1000 \
    --ld-rsq-cutoff 0.01 \
    --out  ${plinkPrefix}
```

Check [here](https://yanglab.westlake.edu.cn/software/gcta/#ComputingLDscores) for details.

## LD score regression

Please check [LD score regression](https://cloufield.github.io/GWASTutorial/08_LDSC/)

## Reference

- **LD review** :  Slatkin, M. (2008). Linkage disequilibrium—understanding the evolutionary past and mapping the medical future. Nature Reviews Genetics, 9(6), 477-485.
- **plink**: Purcell, S., Neale, B., Todd-Brown, K., Thomas, L., Ferreira, M. A., Bender, D., ... & Sham, P. C. (2007). PLINK: a tool set for whole-genome association and population-based linkage analyses. The American journal of human genetics, 81(3), 559-575.
- **gcta**: Yang, J., Lee, S. H., Goddard, M. E., & Visscher, P. M. (2011). GCTA: a tool for genome-wide complex trait analysis. The American Journal of Human Genetics, 88(1), 76-82.
- **ldstore**: Benner, C. et al. Prospects of fine-papping trait-associated genomic regions by using summary statistics from genome-wide association studies. Am. J. Hum. Genet. (2017).
- **ldlink**: Machiela, M. J., & Chanock, S. J. (2015). LDlink: a web-based application for exploring population-specific haplotype structure and linking correlated alleles of possible functional variants. Bioinformatics, 31(21), 3555-3557.
- **ldlinkR**: Myers, T. A., Chanock, S. J., & Machiela, M. J. (2020). LDlinkR: an R package for rapidly calculating linkage disequilibrium statistics in diverse populations. Frontiers in genetics, 11, 157.