# Gene and gene-set analysis

## Table of Contents

- [MAGMA Introduction](#magma-introduction)
- [Install MAGMA](#install-magma)
- [Download reference files](#download-reference-files)
- [Format input files](#format-input-files)
- [Annotate SNPs](#annotate-snps)
- [Gene-based analysis](#gene-based-analysis)
- [Gene-set level analysis](#gene-set-level-analysis)
- [Reference](#reference)

### MAGMA Introduction
MAGMA is one the most commonly used tools for gene-based and gene-set analysis. 

Gene-level test in MAGMA employs a multiple linear principal components regression, and F test to obtain P values for genes.

The multiple linear principal components regression: 

$$
Y = \alpha_{0,g} + X_g \alpha_g + W \beta_g + \epsilon_g
$$

- $X_g$ : principal component matrix 
- $\alpha_g$ : genetic effects
- $W$ : covariate matrix
- $\beta_g$ : effects of covariates 

$X_g$ is obtained by first projecting the variant matrix of a gene onto its PC, and removing PCs with samll eigenvalues.

### Install MAGMA
Dowload MAGMA for your operating system from the following url:
https://ctg.cncr.nl/software/magma

For example:
```
cd ~/tools
mkdir MAGMA
cd MAGMA
wget https://ctg.cncr.nl/software/MAGMA/prog/magma_v1.10.zip
unzip magma_v1.10.zip
```
Add magma to your environment path.

Test if it is successfully installed.
```
$ magma --version
MAGMA version: v1.10 (linux)
```

### Download reference files

We nedd the following reference files:
- gene location files
- LD reference panel
- Gene-set files

The gene location files and LD reference panel can be downloaded from magma website. -> https://ctg.cncr.nl/software/magma
The third one can be downloaded form MsigDB. -> https://www.gsea-msigdb.org/gsea/msigdb/

### Format input files
```
zcat ../08_LDSC/BBJ_HDLC.txt.gz | awk 'NR>1 && $2==3 {print $1,$2,$3}' > HDLC_chr3.magma.input.snp.chr.pos.txt
zcat ../08_LDSC/BBJ_HDLC.txt.gz | awk 'NR>1 && $2==3 {print $1,10^(-$11)}' >  HDLC_chr3.magma.input.p.txt

```
### Annotate SNPs

```
snploc=./HDLC_chr3.magma.input.snp.chr.pos.txt
ncbi37=~/tools/magma/NCBI37/NCBI37.3.gene.loc
magma --annotate \
      --snp-loc ${snploc} \
      --gene-loc ${ncbi37} \
      --out HDLC_chr3
```

!!! tip
    Usually to capture the variants in the regulatory regions, we will add windows upstream and downstream of the genes with `--annotate window`. For example, `--annotate window=35,10` set a 35 kilobase pair(kb) upstream and 10kb downstream window.


### Gene-based analysis
```
ref=~/tools/magma/g1000_eas/g1000_eas
magma \
	--bfile $ref \
	--pval ./HDLC_chr3.magma.input.p.txt N=70657 \
	--gene-annot HDLC_chr3.genes.annot \
	--out HDLC_chr3

```
### Gene-set level analysis

!!! quote
    Competitive gene-set analysis tests whether the genes in a gene-set are more strongly associated with the phenotype of interest than other genes.

P values for each gene were converted to Z scores to perform gene-set level analysis.

$$
Z = \beta_{0,S} + S_S \beta_S + \epsilon
$$

- $S_S$ : indicator (if the gene is in a specified gene set)
- $\beta_S$ : difference in effects between genes in the specified set and genes ouside the set.

```
geneset=/home/he/tools/magma/MSigDB/msigdb_v2022.1.Hs_files_to_download_locally/msigdb_v2022.1.Hs_GMTs/msigdb.v2022.1.Hs.entrez.gmt
magma \
	--gene-results HDLC_chr3.genes.raw \
	--set-annot ${geneset} \
	--out HDLC_chr3
```

# Reference
- de Leeuw, Christiaan A., et al. "MAGMA: generalized gene-set analysis of GWAS data." PLoS computational biology 11.4 (2015): e1004219.
