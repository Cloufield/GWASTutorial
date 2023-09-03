
# TWAS

## Background

Most variants identified in GWAS are located in regulatory regions, and these genetic variants could potentially affect complex traits through gene expression. However, due to the limitation of samples and high cost, it is difficult to measure gene expression at a large scale. Consequently, many expression-trait associations have not been detected, especially for those with small effect sizes. To address these issues, alternative approaches have been proposed and transcriptome-wide association study (TWAS) has become a common and easy-to-perform approach to identify genes whose expression is significantly associated with complex traits in individuals without directly measured expression levels.     

## Definition

TWAS is a method to identify significant expression-trait associations using expression imputation from genetic data or summary statistics. 

## FUSION

In this tutorial, we will introduce FUSION, which is one of the most commonly used tools for performing transcriptome-wide association studies (TWAS). 

url : http://gusevlab.org/projects/fusion/

FUSION trains predictive models of the genetic component of a functional/molecular phenotype and predicts and tests that component for association with disease using GWAS summary statistics. The goal is to identify associations between a GWAS phenotype and a functional phenotype that was only measured in reference data. (http://gusevlab.org/projects/fusion/)

!!! quote
    Gusev, A., Ko, A., Shi, H., Bhatia, G., Chung, W., Penninx, B. W., ... & Pasaniuc, B. (2016). Integrative approaches for large-scale transcriptome-wide association studies. Nature genetics, 48(3), 245-252.

### Algorithm for imputing expression into GWAS summary statistics

ImpG-Summary algorithm was extended to impute the Z scores for the cis genetic component of expression.

$Z$ : a vector of standardized  effect  sizes  (z  scores)  of SNPs for the target trait at a given locus

We impute the Z score of the expression and trait as a linear combination of elements of $Z$ with weights $W$.

$$
W = \Sigma_{e,s}\Sigma_{s,s}^{-1}
$$

- $\Sigma_{e,s}$ : covariance among all SNPs (LD)

- $\Sigma_{s,s}$ : covariance matrix between all SNPs and gene expression

Both $\Sigma_{e,s}$ and $\Sigma_{s,s}$ are estimated from reference datsets.

$$
Z \sim N(0, \Sigma_{s,s} )
$$

The variance of $WZ$ (imputed z score of expression and trait) 
$$
Var(WZ) = W\Sigma_{s,s}W^t 
$$

The imputation Z score can be obtained by:

$$
{{WZ}\over{W\Sigma_{s,s}W^t}^{1/2}}
$$

!!! quote "ImpG-Summary algorithm"
    Pasaniuc, B., Zaitlen, N., Shi, H., Bhatia, G., Gusev, A., Pickrell, J., ... & Price, A. L. (2014). Fast and accurate imputation of summary statistics enhances evidence of functional enrichment. Bioinformatics, 30(20), 2906-2914.


### Installation

Download FUSION from github and install

```
wget https://github.com/gusevlab/fusion_twas/archive/master.zip
unzip master.zip
cd fusion_twas-master
```

Download and unzip the LD reference data (1000 genome)
```
wget https://data.broadinstitute.org/alkesgroup/FUSION/LDREF.tar.bz2
tar xjvf LDREF.tar.bz2
```

Download and unzip plink2R
```
wget https://github.com/gabraham/plink2R/archive/master.zip
unzip master.zip
```

Install R packages
```
# R >= 4.0
R

install.packages(c('optparse','RColorBrewer'))
install.packages('plink2R-master/plink2R/',repos=NULL)
```

### Example

Input:

1. GWAS summary statistics (in LDSC format)
2. pre-computed gene expression weights (from http://gusevlab.org/projects/fusion/)

!!! info "Input GWAS sumstats fromat"
    1. SNP (rsID)
    2. A1 (effect allele)
    3. A2 (non-effect allele)
    4. Z  (Z score)

    Example:
    ```
    SNP	A1	A2	N	CHISQ	Z
    rs6671356	C	T	70100.0	0.172612905312	0.415467092935
    rs6604968	G	A	70100.0	0.291125788806	0.539560736902
    rs4970405	A	G	70100.0	0.102204513891	0.319694407037
    rs12726255	G	A	70100.0	0.312418295691	0.558943911042
    rs4970409	G	A	70100.0	0.0524226849517	0.228960007319
    ```

Get sample sumstats and weights

```
wget https://data.broadinstitute.org/alkesgroup/FUSION/SUM/PGC2.SCZ.sumstats

mkdir WEIGHTS
cd WEIGHTS
wget https://data.broadinstitute.org/alkesgroup/FUSION/WGT/GTEx.Whole_Blood.tar.bz2
tar xjf GTEx.Whole_Blood.tar.bz2
```


Expression imputation
```
Rscript FUSION.assoc_test.R \
--sumstats PGC2.SCZ.sumstats \
--weights ./WEIGHTS/GTEx.Whole_Blood.pos \
--weights_dir ./WEIGHTS/ \
--ref_ld_chr ./LDREF/1000G.EUR. \
--chr 22 \
--out PGC2.SCZ.22.dat
```

Results

```
head PGC2.SCZ.22.dat
PANEL	FILE	ID	CHR	P0	P1	HSQ	BEST.GWAS.ID	BEST.GWAS.Z	EQTL.ID	EQTL.R2	EQTL.Z	EQTL.GWAS.Z	NSNP	NWGT	MODEL	MODELCV.R2	MODELCV.PV	TWAS.Z	TWAS.P
NA	../WEIGHTS//GTEx.Whole_Blood/GTEx.Whole_Blood.ENSG00000273311.1.DGCR11.wgt.RDat	DGCR11	22	19033675	19035888	0.0551	rs2238767	-2.98	rs2283641	 0.013728	  4.33	 2.5818	408	 1	top1	0.014	0.018	 2.5818	9.83e-03
NA	../WEIGHTS//GTEx.Whole_Blood/GTEx.Whole_Blood.ENSG00000100075.5.SLC25A1.wgt.RDat	SLC25A1	22	19163095	19166343	0.0740	rs2238767	-2.98	rs762523	 0.080367	  5.36	-1.8211	406	 1	top1	0.08	7.2e-08	-1.8216.86e-02
NA	../WEIGHTS//GTEx.Whole_Blood/GTEx.Whole_Blood.ENSG00000070371.11.CLTCL1.wgt.RDat	CLTCL1	22	19166986	19279239	0.1620	rs4819843	 3.04	rs809901	 0.072193	  5.53	-1.9928	456	19	enet	0.085	2.8e-08	-1.8806.00e-02
NA	../WEIGHTS//GTEx.Whole_Blood/GTEx.Whole_Blood.ENSG00000232926.1.AC000078.5.wgt.RDat	AC000078.5	22	19874812	19875493	0.2226	rs5748555	-3.15	rs13057784	 0.052796	  5.60	-0.1652	514	44	enet	0.099	2e-09  0.0524	9.58e-01
NA	../WEIGHTS//GTEx.Whole_Blood/GTEx.Whole_Blood.ENSG00000185252.13.ZNF74.wgt.RDat	ZNF74	22	20748405	20762745	0.1120	rs595272	 4.09	rs1005640	 0.001422	  3.44	-1.3677	301	 8	enet	0.008	0.054	-0.8550	3.93e-01
NA	../WEIGHTS//GTEx.Whole_Blood/GTEx.Whole_Blood.ENSG00000099940.7.SNAP29.wgt.RDat	SNAP29	22	21213771	21245506	0.1286	rs595272	 4.09	rs4820575	 0.061763	  5.94	-1.1978	416	27	enet	0.079	9.4e-08	-1.0354	3.00e-01
NA	../WEIGHTS//GTEx.Whole_Blood/GTEx.Whole_Blood.ENSG00000272600.1.AC007308.7.wgt.RDat	AC007308.7	22	21243494	21245502	0.2076	rs595272	 4.09	rs165783	 0.100625	  6.79	-0.8871	408	12	lasso	0.16	5.4e-1-1.2049	2.28e-01
NA	../WEIGHTS//GTEx.Whole_Blood/GTEx.Whole_Blood.ENSG00000183773.11.AIFM3.wgt.RDat	AIFM3	22	21319396	21335649	0.0676	rs595272	 4.09	rs565979	 0.036672	  4.50	-0.4474	362	 1	top1	0.037	0.00024	-0.4474	6.55e-01
NA	../WEIGHTS//GTEx.Whole_Blood/GTEx.Whole_Blood.ENSG00000230513.1.THAP7-AS1.wgt.RDat	THAP7-AS1	22	21356175	21357118	0.2382	rs595272	 4.09	rs2239961	 0.105307	 -7.04	-0.3783	347	 5	lasso	0.15	7.6e-1 0.2292	8.19e-01

```


