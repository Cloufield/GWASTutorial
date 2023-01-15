# SNP-Heritability estimation by GCTA-GREML

## Introduction

GCTA:


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
plinkFile="../01_Dataset/1KG.EAS.auto.snp.norm.nodup.split.maf005.thinp020"
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
Analysis started at 12:24:19 JST on Sun Jan 15 2023.
Hostname: Home-Desktop

Options:

--bfile ../01_Dataset/1KG.EAS.auto.snp.norm.nodup.split.maf005.thinp020
--autosome
--maf 0.01
--make-grm
--out 1kg_eas

Note: GRM is computed using the SNPs on the autosomes.
Reading PLINK FAM file from [../01_Dataset/1KG.EAS.auto.snp.norm.nodup.split.maf005.thinp020.fam]...
504 individuals to be included from FAM file.
504 individuals to be included. 0 males, 0 females, 504 unknown.
Reading PLINK BIM file from [../01_Dataset/1KG.EAS.auto.snp.norm.nodup.split.maf005.thinp020.bim]...
1122299 SNPs to be included from BIM file(s).
Threshold to filter variants: MAF > 0.010000.
Computing the genetic relationship matrix (GRM) v2 ...
Subset 1/1, no. subject 1-504
  504 samples, 1122299 markers, 127260 GRM elements
IDs for the GRM file have been saved in the file [1kg_eas.grm.id]
Computing GRM...
  100% finished in 8.2 sec
1122299 SNPs have been processed.
  Used 1122299 valid SNPs.
The GRM computation is completed.
Saving GRM...
GRM has been saved in the file [1kg_eas.grm.bin]
Number of SNPs in each pair of individuals has been saved in the file [1kg_eas.grm.N.bin]

Analysis finished at 12:24:29 JST on Sun Jan 15 2023
Overall computational time: 9.52 sec.
```

## Estimation

```
#!/bin/bash

#the grm we calculated in step1
GRM=1kg_eas
# phenotype file
phenotypeFile=../01_Dataset/1kgeas_binary.txt
# disease prevalence used for conversion to liability-scale heritability
prevalence=0.4

gcta \
  --grm ${GRM} \
  --pheno ${phenotypeFIile} \
  --prevalence ${prevalence} \
  --reml \
  --out 1kg_eas

```

## Results

```bash
head 1kg_eas.hsq

Source  Variance        SE
V(G)    0.100469        0.094051
V(e)    0.138337        0.093889
Vp      0.238806        0.015077
V(G)/Vp 0.420715        0.392317
The estimate of variance explained on the observed scale is transformed to that on the underlying scale:
(Proportion of cases in the sample = 0.399602; User-specified disease prevalence = 0.400000)
V(G)/Vp_L       0.676703        0.631026
logL    105.187
logL0   103.680
```

## Reference

- Yang, J., Lee, S. H., Goddard, M. E., & Visscher, P. M. (2011). GCTA: a tool for genome-wide complex trait analysis. The American Journal of Human Genetics, 88(1), 76-82.
- [https://yanglab.westlake.edu.cn/software/gcta/#Overview](https://yanglab.westlake.edu.cn/software/gcta/#Overview)
