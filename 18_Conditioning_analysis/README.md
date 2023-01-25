Conditioning analysis
---


Multiple association signals could harbore in one loci, especially when observering complex LD structure in the regional plot.
Conditioning on one signal allows to separate the independent signals.

Several ways to perform the conditioning analysis:
* Adding the lead variant to the covariates step-wisely and rerun the association test.
* [GCTA-COJO](https://www.nature.com/articles/ng.2213).

# Adding the lead variant to the covariates

First, extract the individual genotype (dosage) to the text file. Then add it to covariates.

```sh
plink2 \
  --pfile topmed_pgen/chr12.dose.Rsq0.3 vzs \
  --extract genotype/COQ10A.list \
  --threads 1 \
  --export A \
  --out genotype/chr12:56274390:A:G
```

The exported format could be found in [Export non-PLINK 2 fileset](https://www.cog-genomics.org/plink/2.0/data#export).

!!! note

Major allele dosage would be outputed. If adding `ref-first`, ref allele would be outputed. It does not matter as a covariate.

Then just paste it to the covariates table and run association test.

# GCTA-COJO

If raw genotypes are not available, GCTA-COJO performs conditioning analysis using sumstats and external LD reference.


`cojo-top-SNPs 10` will perform a step-wise model selection to select 10 independently associated SNPs.

```
gcta
    --bfile FLG
  --chr 1
  --maf 0.001
  --cojo-file FLG_cojo.input
  --cojo-top-SNPs 10
  --extract-region-bp 1 152383617 5000
  --out FLG_cojo.output
```

Input file format `less FLG_cojo.input`:
```
ID      ALLELE1 ALLELE0 A1FREQ  BETA    SE      P       N
chr1:11171:CCTTG:C      C       CCTTG   0.0831407       -0.0459889      0.0710074       0.5172  180590
chr1:13024:G:A  A       G       1.63957e-05     -3.2714 3.26302 0.3161  180590
```
Here `A1` is the effect allele. 

Then `--cojo-cond` could be used to generate new sumstats conditioned on the above selected variant(s).

`bfile` is used to generate LD. A size of [> 4000 samples](https://yanglab.westlake.edu.cn/software/gcta/#COJO) is suggested. Estimation of LD in GATC is based on the hard-call genotype.



