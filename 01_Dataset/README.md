# Sample Dataset

504 EAS individuals from 1000 Genome Project Phase 3 version 5

- Url: [http://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/](http://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/)

## Genotype Data Processing

- Selected only autosomal variants
- Split multi-allelic variants
- Variants were normalized
- Remove duplicated variants
- Selected only SNP (ATCG)
- Selected only SNPs with MAF>0.05
- Randomly selected 20% of SNPs (`plink --thin 0.2`)
- Converted to plink bed format and merged to a single file  

## Download

Simply run `download_sampledata.sh` and the dataset will be downloaded and decompressed.

```
./download_sampledata.sh
```

And you will get the following files:
```
1KG.EAS.auto.snp.norm.nodup.split.maf005.thinp020.bed
1KG.EAS.auto.snp.norm.nodup.split.maf005.thinp020.bim
1KG.EAS.auto.snp.norm.nodup.split.maf005.thinp020.fam
```

## Phenotype Simulation
Phenotypes were simply simulated using GCTA with the 1KG EAS dataset (without thinning).
```Bash
gcta64  \
  --bfile 1KG.EAS.auto.snp.norm.nodup.split.maf005 \ 
  --simu-cc 200 304 \
  --simu-causal-loci causal_10.snplist  \
  --simu-hsq 0.8  \
  --simu-k 0.4 \
  --simu-rep 1 \
  --out 1kgeas_binary
```

``` 
$ cat causal_10.snplist
3:176520196:C:T 3
1:217437563:C:T 3
9:36591968:T:G 3
6:29898352:T:C 3
2:55620927:G:A 3
13:92117183:G:A 3
14:78760515:T:C 3
11:102442005:T:G 3
11:56317673:T:A 3
7:139979401:G:C 3
```

## Reference
- 1000 Genomes Project Consortium. (2015). A global reference for human genetic variation. Nature, 526(7571), 68.
- Yang, J., Lee, S. H., Goddard, M. E., & Visscher, P. M. (2011). GCTA: a tool for genome-wide complex trait analysis. The American Journal of Human Genetics, 88(1), 76-82.
