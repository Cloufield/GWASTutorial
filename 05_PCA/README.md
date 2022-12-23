# 5.Principle conponent analysis
PCA is by far the most commonly used dimension reduction approach used in population genetics which could identify the diffenrence in ancestry among the sample individuals.
For GWAS we also need to include top PCs to adjust for the population stratification.

Please read the following paper on how we apply PCA to genetic data:
Price, A., Patterson, N., Plenge, R. et al. Principal components analysis corrects for stratification in genome-wide association studies. Nat Genet 38, 904–909 (2006). https://doi.org/10.1038/ng1847 https://www.nature.com/articles/ng1847

Simply speaking, GRM (genetic relationship matrix) is first estimated and then PCA is applied to this matrix to generate PCs for each individual.

So before association analysis, we will learn how to run PCA analysis first.

- [5.1 Preparation](#51-preparation)
- [5.2 PCA steps](#52-pca-steps)
- [5.3 Sample codes](#53-sample-codes)
- [5.4 Plotting the PCs](#54-plotting-the-pcs)
- [5.5 PCA-UMAP](#55-pca-umap)
- [References](#references)
---------

## 5.1 Preparation

excluding SNPs in high-LD or HLA regions. 

Please check https://genome.sph.umich.edu/wiki/Regions_of_high_linkage_disequilibrium_(LD)
- 0.1 simply copy the list of high-LD or HLA regions in Genome build version(.bed format) to a text file `high-ld.txt`.
```
$cat high-ld-hg19.txt 
1	48000000	52000000	highld
2	86000000	100500000	highld
2	134500000	138000000	highld
2	183000000	190000000	highld
3	47500000	50000000	highld
3	83500000	87000000	highld
3	89000000	97500000	highld
5	44500000	50500000	highld
5	98000000	100500000	highld
5	129000000	132000000	highld
5	135500000	138500000	highld
6	25000000	35000000	highld
6	57000000	64000000	highld
6	140000000	142500000	highld
7	55000000	66000000	highld
8	7000000	13000000	highld
8	43000000	50000000	highld
8	112000000	115000000	highld
10	37000000	43000000	highld
11	46000000	57000000	highld
11	87500000	90500000	highld
12	33000000	40000000	highld
12	109500000	112000000	highld
20	32000000	34500000	highld
```
- 0.2 use `high-ld.txt` to extract all SNPs which are located in the regions described in the file using the code as follows:
```
plink --file ${plinkFile} --make-set high-ld.txt --write-set --out hild
```
For example:
```
plinkFile="../01_Dataset/1KG.EAS.auto.snp.norm.nodup.split.maf005.thinp020" #!please set this to your own path

plink \
	--bfile ${plinkFile} \
	--make-set high-ld-hg19.txt \
	--write-set \
	--out hild
```
And all SNPs in the regions will be extracted to hild.set.

```
$head hild.set
highld
1:48000156:C:G
1:48002096:C:G
1:48003081:T:C
1:48004776:C:T
1:48006500:A:G
1:48006546:C:T
1:48008102:T:G
1:48009994:C:T
1:48009997:C:A
```
- 0.3 exclude these SNPs using `--exclude hild.set` when pruning.

Note: the reason why we want to exclude such high-LD or HLA regions is described in:
- Price, A. L., Weale, M. E., Patterson, N., Myers, S. R., Need, A. C., Shianna, K. V., Ge, D., Rotter, J. I., Torres, E., Taylor, K. D., Goldstein, D. B., & Reich, D. (2008). Long-range LD can confound genome scans in admixed populations. American journal of human genetics, 83(1), 132–139. https://doi.org/10.1016/j.ajhg.2008.06.005 

---------
## 5.2 PCA steps

- 1.Pruning (https://www.cog-genomics.org/plink/2.0/ld#indep)
- 2.Removing relatives (usually 2-degree) (https://www.cog-genomics.org/plink/2.0/distance#king_cutoff)
- 3.Run PCA using un-related samples and independent SNPs (https://www.cog-genomics.org/plink/2.0/strat#pca)
- 4.Project to all samples (https://www.cog-genomics.org/plink/2.0/score#pca_project)

---------
## 5.3 Sample codes
```
plinkFile="" #please set this to your own path
outPrefix="plink_results"
threadnum=2
hildset = hild.set 

# pruning
plink2 \
        --bfile ${plinkFile} \
	--threads ${threadnum} \
	--exclude ${hildset} \ 
	--indep-pairwise 500 50 0.2 \
        --out ${outPrefix}

# remove related samples using king-cuttoff
plink2 \
        --bfile ${plinkFile} \
	--extract ${outPrefix}.prune.in \
        --king-cutoff 0.0884 \
	--threads ${threadnum} \
        --out ${outPrefix}

# pca after pruning and removing related samples
plink2 \
        --bfile ${plinkFile} \
        --keep ${outPrefix}.king.cutoff.in.id \
	--extract ${outPrefix}.prune.in \
	--freq counts \
	--threads ${threadnum} \
        --pca approx allele-wts \
        --out ${outPrefix}

# projection (related and unrelated samples)
plink2 \
        --bfile ${plinkFile} \
	--threads ${threadnum} \
        --read-freq ${outPrefix}.acount \
	--score ${outPrefix}.eigenvec.allele 2 5 header-read no-mean-imputation variance-standardize \
        --score-col-nums 6-15 \
        --out ${outPrefix}_projected
```
After step 3, the 'allele-wts' modifier requests an additional one-line-per-allele .eigenvec.allele file with PCs expressed as allele weights instead of sample weights.

We will get the `plink_results.eigenvec.allele` file, which will be used to project onto all samples along with a allele count `plink_results.acount` file.
```
$head plink_results.eigenvec.allele
#CHROM	ID	REF	ALT	A1	PC1	PC2	PC3	PC4	PC5	PC6	PC7	PC8	PC9	PC10
1	1:13273:G:C	G	C	G	1.12369	-0.320826	-0.0206569	-0.218665	0.869801	0.378433	-0.0723841	-0.227555	0.0361673	-0.368192
1	1:13273:G:C	G	C	C	-1.12369	0.320826	0.0206569	0.218665	-0.869801	-0.378433	0.0723841	0.227555	-0.0361673	0.368192
1	1:14599:T:A	T	A	T	0.99902	-1.15824	-1.80519	-0.36774	0.179881	0.25242	0.068899	0.206564	-0.342483	0.103762
1	1:14599:T:A	T	A	A	-0.99902	1.15824	1.80519	0.36774	-0.179881	-0.25242	-0.068899	-0.206564	0.342483	-0.103762
1	1:14930:A:G	A	G	A	-0.0704343	-0.35091	-0.41535	-0.304856	0.081039	-0.49408	-0.0667606	-0.0698847	0.245836	0.330869
1	1:14930:A:G	A	G	G	0.0704343	0.35091	0.41535	0.304856	-0.081039	0.49408	0.0667606	0.0698847	-0.245836	-0.330869
1	1:69897:T:C	T	C	T	-0.514024	0.563153	-0.997768	-0.298234	-0.840608	-0.247155	0.545471	-0.675274	-0.787836	-0.509647
1	1:69897:T:C	T	C	C	0.514024	-0.563153	0.997768	0.298234	0.840608	0.247155	-0.545471	0.675274	0.787836	0.509647
1	1:86331:A:G	A	G	A	-0.169641	-0.0125126	-0.531174	-0.0219291	0.614439	0.140143	0.133833	-0.570109	0.392805	-0.065334

#head plink_results.acount
#CHROM	ID	REF	ALT	ALT_CTS	OBS_CT
1	1:13273:G:C	G	C	63	1004
1	1:14599:T:A	T	A	90	1004
1	1:14930:A:G	A	G	417	1004
1	1:69897:T:C	T	C	879	1004
1	1:86331:A:G	A	G	87	1004
1	1:91581:G:A	G	A	499	1004
1	1:122872:T:G	T	G	259	1004
1	1:135163:C:T	C	T	91	1004
1	1:233473:C:G	C	G	156	1004

```
Please check https://www.cog-genomics.org/plink/2.0/score#pca_project for more details on projection.
Eventually, we will get the PCA results for all samples.
```
head plink_results_projected.sscore
#FID	IID	ALLELE_CT	NAMED_ALLELE_DOSAGE_SUM	PC1_AVG	PC2_AVG	PC3_AVG	PC4_AVG	PC5_AVG	PC6_AVG	PC7_AVG	PC8_AVG	PC9_AVG	PC10_AVG
0	HG00403	219504	219504	0.000643981	-0.0297502	-0.0151499	-0.0122381	0.0229149	0.0235408	-0.033705	-0.0075127	-0.0125402	0.00271677
0	HG00404	219504	219504	-0.000492225	-0.031018	-0.00764244	-0.0204998	0.0284068	-0.00872449	0.0123353	-0.00492058	-0.00557003	0.0248966
0	HG00406	219504	219504	0.00620984	-0.034375	-0.00898555	-0.00335076	-0.0217559	-0.0182433	0.00333925	-0.00760613	-0.0340018	0.00641082
0	HG00407	219504	219504	0.00678586	-0.0239308	-0.00704419	-0.00466139	0.00985433	0.000889767	0.00679557	-0.0200495	-0.0131869	0.0350328
0	HG00409	219504	219504	-0.00236345	-0.0231604	0.0320665	0.0145563	0.0236768	0.00704788	0.012859	0.0319605	-0.0130627	0.0110219
0	HG00410	219504	219504	0.000670927	-0.0210665	0.0467767	0.00293079	0.0184061	0.045967	0.00384994	0.0212317	-0.0296434	0.0237174
0	HG00419	219504	219504	0.00526139	-0.0369818	-0.00974662	0.00855412	-0.0053907	-0.00102057	0.0063254	0.0140126	-0.00600854	0.00732882
0	HG00421	219504	219504	0.00038356	-0.0319534	-0.00648054	0.00311739	-0.022044	0.0064945	-0.0105273	-0.0276718	-0.00973368	0.0208449
0	HG00422	219504	219504	0.00437335	-0.0323416	-0.0111979	0.0106245	-0.0267334	0.00142919	-0.00487295	-0.0124099	-0.00467014	-0.0188086
```

## 5.4 Plotting the PCs 
You can now create scatterplots of the PCs using R or python.
(under construction)

Requrements:
- python>3
- numpy,pandas,seaborn,matplotlib

## 5.5 PCA-UMAP
(optional) 
We can also apply another non-linear dimension reduction algorithm called UMAP to the PCs to further identfy the local structures. (PCA-UMAP)

For more details, please check:
- https://umap-learn.readthedocs.io/en/latest/index.html

An example of PCA and PCA-UMAP for population genetics:
- Sakaue, S., Hirata, J., Kanai, M., Suzuki, K., Akiyama, M., Lai Too, C., ... & Okada, Y. (2020). Dimensionality reduction reveals fine-scale structure in the Japanese population with consequences for polygenic risk prediction. Nature communications, 11(1), 1-11.

# References
- (PCA) Price, A., Patterson, N., Plenge, R. et al. Principal components analysis corrects for stratification in genome-wide association studies. Nat Genet 38, 904–909 (2006). https://doi.org/10.1038/ng1847 https://www.nature.com/articles/ng1847
- (why removing high-LD regions) Price, A. L., Weale, M. E., Patterson, N., Myers, S. R., Need, A. C., Shianna, K. V., Ge, D., Rotter, J. I., Torres, E., Taylor, K. D., Goldstein, D. B., & Reich, D. (2008). Long-range LD can confound genome scans in admixed populations. American journal of human genetics, 83(1), 132–139. https://doi.org/10.1016/j.ajhg.2008.06.005 
- (UMAP) McInnes, L., Healy, J., & Melville, J. (2018). Umap: Uniform manifold approximation and projection for dimension reduction. arXiv preprint arXiv:1802.03426.
- (UMAP in population genetics) Diaz-Papkovich, A., Anderson-Trocmé, L. & Gravel, S. A review of UMAP in population genetics. J Hum Genet 66, 85–91 (2021). https://doi.org/10.1038/s10038-020-00851-4 https://www.nature.com/articles/s10038-020-00851-4
- (king-cutoff) Manichaikul, A., Mychaleckyj, J. C., Rich, S. S., Daly, K., Sale, M., & Chen, W. M. (2010). Robust relationship inference in genome-wide association studies. Bioinformatics, 26(22), 2867-2873.
