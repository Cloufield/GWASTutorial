
# Linkage disequilibrium(LD)

## LD Definition


Reference: Slatkin, M. (2008). Linkage disequilibrium—understanding the evolutionary past and mapping the medical future. Nature Reviews Genetics, 9(6), 477-485.

## Calculate LD

### LDstore2
LDstore2: http://www.christianbenner.com/#

Reference: Benner, C. et al. Prospects of fine-papping trait-associated genomic regions by using summary statistics from genome-wide association studies. Am. J. Hum. Genet. (2017).

### PLINK LD

[Calculate LD using PLINK](https://cloufield.github.io/GWASTutorial/04_Data_QC/#ld-calculation) 


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

Reference: Myers, T. A., Chanock, S. J., & Machiela, M. J. (2020). LDlinkR: an R package for rapidly calculating linkage disequilibrium statistics in diverse populations. Frontiers in genetics, 11, 157.


## LD-pruning

[LD-pruning](https://cloufield.github.io/GWASTutorial/04_Data_QC/#ld-pruning)

## LD-clumping

[LD-clumping](https://cloufield.github.io/GWASTutorial/10_PRS/#ctpt-using-plink)

## LD score

### LDSC

### GCTA

## LD score regression

## Reference
