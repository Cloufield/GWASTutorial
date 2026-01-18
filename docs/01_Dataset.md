# Sample Dataset

504 EAS individuals from 1000 Genomes Project Phase 3 version 5

- CHB: Han Chinese in Beijing, China
- JPT: Japanese in Tokyo, Japan
- CHS: Southern Han Chinese
- CDX: Chinese Dai in Xishuanagbanna, China
- KHV: Kinh in Ho Chi Minh City, Vietnam

Url: [http://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/](http://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/)

Genome build:  human_g1k_v37.fasta (hg19)

## Genotype Data Processing

- Selected only autosomal variants
- Split multi-allelic variants
- Variants were normalized
- Remove duplicated variants
- Selected only SNP (ATCG)
- Selected 2% rare SNPs (`plink --mac 2 --max-maf 0.01 --thin 0.02`)
- Selected 15% common SNPs (`plink --maf 0.01 --thin 0.15`)
- Converted to plink bed format and merged to a single file  
- Randomly added some missing data points

## Download

!!! note 
    The sample dataset `1KG.EAS.auto.snp.norm.nodup.split.rare002.common015.missing.zip` has been included in `01_Dataset` when you clone the repository. There is no need to download it again if you clone this repository.

You can also simply run `download_sampledata.sh` in `01_Dataset` and the dataset will be downloaded and decompressed.

```
./download_sampledata.sh
```

!!! warning "Sample dataset is currently hosted on Dropbox which may not be accessible for users in certain regions."

or you can manually download it from [this link](https://www.dropbox.com/scl/fi/41ep8xbdccp9xw5epim19/1KG.EAS.auto.snp.norm.nodup.split.rare002.common015.missing.zip?rlkey=tklapxwypeg79b1sx03o6ycs7&dl=1).

Unzip the dataset `unzip -j 1KG.EAS.auto.snp.norm.nodup.split.rare002.common015.missing.zip`, and you will get the following files:

```
1KG.EAS.auto.snp.norm.nodup.split.rare002.common015.missing.bed
1KG.EAS.auto.snp.norm.nodup.split.rare002.common015.missing.bim
1KG.EAS.auto.snp.norm.nodup.split.rare002.common015.missing.fam
```

## Phenotype Simulation

Phenotypes were simulated using GCTA with the 1KG EAS dataset. GCTA provides a function to simulate GWAS data based on observed genotype data.

### Quantitative Trait Model

For a quantitative trait, phenotypes are simulated using the simple additive genetic model:

$$y = Wu + \epsilon$$

where:
- $y$ is the phenotype vector
- $W$ is the genotype matrix (coded as 0, 1, or 2 for the number of effect alleles)
- $u$ is the vector of SNP effects
- $\epsilon$ is the vector of residual effects

**Simulation procedure:**

1. **Causal variant effects**: Given a set of SNPs assigned as causal variants, the effects ($u$) are generated from a standard normal distribution: $u \sim N(0, 1)$

2. **Residual effects**: The residual effects ($\epsilon$) are generated from a normal distribution with mean 0 and variance $\sigma^2_g(1/h^2 - 1)$:
   $$\epsilon \sim N(0, \sigma^2_g(1/h^2 - 1))$$
   
   where:
   - $\sigma^2_g$ is the empirical variance of $Wu$ (genetic variance)
   - $h^2$ is the user-specified heritability

### Case-Control Study Model

For a case-control study, GCTA assumes a **threshold-liability model**:

1. Disease liabilities are simulated in the same way as phenotypes for a quantitative trait using the model $y = Wu + \epsilon$

2. Any individual with disease liability exceeding a certain threshold $T$ is assigned as a case, and a control otherwise

3. The threshold $T$ is determined from the normal distribution truncating the proportion $K$ (disease prevalence)

### Example Command

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

!!! warning
    This simulation is just used for showing the analysis pipeline and data format. The trait was simulated under an unreal condition (effect sizes are extremely large) so the result itself is meaningless.   

    Allele frequency and Effect size

    <img width="700" alt="image" src="https://github.com/Cloufield/GWASTutorial/assets/40289485/d5133405-290c-4436-b61e-60f8a750f194">


## References
- 1000 Genomes Project Consortium. (2015). A global reference for human genetic variation. Nature, 526(7571), 68.
- Yang, J., Lee, S. H., Goddard, M. E., & Visscher, P. M. (2011). GCTA: a tool for genome-wide complex trait analysis. The American Journal of Human Genetics, 88(1), 76-82.
