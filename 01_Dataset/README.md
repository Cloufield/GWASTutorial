# Sample Dataset

504 EAS individuals from 1000 Genome Project Phase 3 v5
- Url: [http://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/](http://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/)
- Citation: 1000 Genomes Project Consortium. (2015). A global reference for human genetic variation. Nature, 526(7571), 68.

# Genotype Data Processing
- Selected only autosomal variants
- Split muktiallelic varaints
- Variants were normalized
- Remove duplicated variants
- Selected only SNP (ATCG)
- Selected only SNPs with MAF>0.05
- Randomly selected 20% of SNPs (`plink --thin 0.2`)
- Converted to plink bed format and merged to a single file  

# Download
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

