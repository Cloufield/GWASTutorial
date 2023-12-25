# Sample Dataset

504 EAS individuals from 1000 Genome Project Phase 3 version 5

- Url: [http://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/](http://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/)

## Genotype Data Processing

- Selected only autosomal variants
- Split multi-allelic variants
- Variants were normalized
- Remove duplicated variants
- Selected only SNP (ATCG)
- Selected 2% rare SNPs (`plink --mac 2 --max--maf 0.01 --thin 0.02`)
- Selected 15% common SNPs (`plink --maf 0.01 --thin 0.15`)
- Converted to plink bed format and merged to a single file  

## Download

Simply run `download_sampledata.sh` and the dataset will be downloaded and decompressed.

!!! warning "Sample dataset is currently hosted on Dropbox which may not be accessible for users in certain regions."

```
./download_sampledata.sh
```

or you can manually download it from [this link](https://www.dropbox.com/scl/fi/v3h431srji9ad7xh0qj6z/1KG.EAS.auto.snp.norm.nodup.split.rare002.common015.zip?rlkey=imv1rivhchxzyz6si2wr7ddcs&dl=0).

And you will get the following files in `1KG.EAS.auto.snp.norm.nodup.split.rare002.common015`:
```
1KG.EAS.auto.snp.norm.nodup.split.rare002.common015.bed
1KG.EAS.auto.snp.norm.nodup.split.rare002.common015.bim
1KG.EAS.auto.snp.norm.nodup.split.rare002.common015.fam
```

## Phenotype Simulation
Phenotypes were simply simulated using GCTA with the 1KG EAS dataset.

```Bash
gcta  \
  --bfile 1KG.EAS.auto.snp.norm.nodup.split.rare002.common015 \
  --simu-cc 250 254  \
  --simu-causal-loci causal.snplist  \
  --simu-hsq 0.8  \
  --simu-k 0.5  \
  --simu-rep 1  \
  --out 1kgeas_binary
```

``` 
$ cat causal.snplist
2:55620927:G:A 3
8:97094292:C:T 3
20:42758834:T:C 3
7:134326056:G:T 3
1:167562605:G:A 3
```

## Reference
- 1000 Genomes Project Consortium. (2015). A global reference for human genetic variation. Nature, 526(7571), 68.
- Yang, J., Lee, S. H., Goddard, M. E., & Visscher, P. M. (2011). GCTA: a tool for genome-wide complex trait analysis. The American Journal of Human Genetics, 88(1), 76-82.
