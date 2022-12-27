# Association test

## File preparation
To perform association analysis, usually we need the following files:

- **Genotype file** (or dosage file) : usually in PLINK format, VCF format, or BGEN format.
- **Phenotype file** : plain text file.
- **Covariate file** (optional): plain text file. Usually covaraites include age, sex, and top Pricipal Components. 

For example,

```
# phenotype file for a simulated binary trait
head 1kgeas_binary.txt 
FID IID B1
0 HG00403 2 
0 HG00404 1 
0 HG00406 2 
0 HG00407 2 
0 HG00409 2 
0 HG00410 2 
0 HG00419 1 
0 HG00421 2 
0 HG00422 1

# the covariates file (only top PCs)
#FID	IID	ALLELE_CT	NAMED_ALLELE_DOSAGE_SUM	PC1_AVG	PC2_AVG	PC3_AVG	PC4_AVG	PC5_AVG	PC6_AVG	PC7_AVG	PC8_AVG	PC9_AVG	PC10_AVG
0	HG00403	224016	224016	0.000246109	0.0292717	-0.0127437	-0.0135105	0.0301317	0.0196699	0.0232392	-0.0205941	-0.00416543	0.0121819
0	HG00404	224016	224016	-0.000716664	0.032043	-0.00573731	-0.0189504	0.0277385	-0.0154478	-0.0136551	-0.00147269	0.00510851	0.0268694
0	HG00406	224016	224016	0.00681476	0.0346759	-0.00706221	-0.0054266	-0.025458	-0.0166505	-0.00510707	-0.00105581	-0.0224028	0.0202523
0	HG00407	224016	224016	0.00695106	0.0244759	-0.00890072	-0.000694057	0.00946838	-0.00773378	-0.0139923	-0.0204871	-0.0003338	0.0387022
0	HG00409	224016	224016	-0.0023481	0.0213108	0.03235	0.0158793	0.026655	0.00324455-0.0107152	0.0317714	-0.00764455	0.0155973
0	HG00410	224016	224016	0.000926147	0.0198139	0.0475798	0.00314974	0.0275373	0.041886	-0.0133896	0.0184717	-0.0143644	0.0291036
0	HG00419	224016	224016	0.00580767	0.0369208	-0.00907507	0.00903163	-0.00649345	-0.000472359	-0.00327011	0.0160456	-0.005133	0.0141021
0	HG00421	224016	224016	0.000987901	0.0336895	-0.00697814	0.00557199	-0.0210537	0.00700968	0.00319921	-0.0215999	0.00127686	0.0350116
0	HG00422	224016	224016	0.00440288	0.0335901	-0.0125043	0.0135621	-0.0228428	0.00492741	0.00445856	-0.00911147	-0.00312742	-0.00784459
```

## Testing

Please check https://www.cog-genomics.org/plink/2.0/assoc for more details.

We will perform a logistic regression with firth correction for a simulated binary trait using 1KG East Asian individuals.

Sample code:

```
genotypeFile="../01_Dataset/1KG.EAS.auto.snp.norm.nodup.split.maf005.thinp020"  #!please set this to your own path
phenotypeFile="../01_Dataset/1kgeas_binary.txt" #!please set this to your own path
covariateFile="../05_PCA/plink_results_projected.sscore"

covariateCols=6-10
colName="B1"
threadnum=2

plink2 \
	--bfile ${genotypeFile} \
	--pheno ${phenotypeFile} \
	--pheno-name ${colName} \
	--maf 0.01 \
	--covar ${covariateFile} \
	--covar-col-nums ${covariateCols} \
	--glm hide-covar firth \
	--threads ${threadnum} \
	--out 1kgeas
```

You will see a similar log like:

```
PLINK v2.00a3LM 64-bit Intel (12 Dec 2020)     www.cog-genomics.org/plink/2.0/
(C) 2005-2020 Shaun Purcell, Christopher Chang   GNU General Public License v3
Logging to 1kgeas.log.
Options in effect:
  --bfile ../01_Dataset/1KG.EAS.auto.snp.norm.nodup.split.maf005.thinp020
  --covar ../05_PCA/plink_results_projected.sscore
  --covar-col-nums 6-10
  --glm hide-covar firth
  --maf 0.01
  --out 1kgeas
  --pheno ../01_Dataset/1kgeas_binary.txt
  --pheno-name B1
  --threads 2

Start time: Tue Dec 27 23:02:52 2022
15957 MiB RAM detected; reserving 7978 MiB for main workspace.
Using up to 2 compute threads.
504 samples (0 females, 0 males, 504 ambiguous; 504 founders) loaded from
../01_Dataset/1KG.EAS.auto.snp.norm.nodup.split.maf005.thinp020.fam.
1122299 variants loaded from
../01_Dataset/1KG.EAS.auto.snp.norm.nodup.split.maf005.thinp020.bim.
1 binary phenotype loaded (201 cases, 302 controls).
5 covariates loaded from ../05_PCA/plink_results_projected.sscore.
Calculating allele frequencies... done.
0 variants removed due to allele frequency threshold(s)
(--maf/--max-maf/--mac/--max-mac).
1122299 variants remaining after main filters.
--glm Firth regression on phenotype 'B1': done.
Results written to 1kgeas.B1.glm.firth .
End time: Tue Dec 27 23:04:40 2022
```

Lest check the first lines of the output:
```
#CHROM	POS	ID	REF	ALT	A1	TEST	OBS_CT	OR	LOG(OR)_SE	Z_STAT	P	ERRCODE
1	13273	1:13273:G:C	G	C	C	ADD	503	0.746149	0.282904	-1.03509	0.300628	.
1	14599	1:14599:T:A	T	A	A	ADD	503	1.67693	0.240899	2.14598	0.0318742.
1	14604	1:14604:A:G	A	G	G	ADD	503	1.67693	0.240899	2.14598	0.0318742.
1	14930	1:14930:A:G	A	G	G	ADD	503	1.64359	0.242872	2.04585	0.0407708.
1	69897	1:69897:T:C	T	C	T	ADD	503	1.69142	0.200238	2.62471	0.00867216.
1	86331	1:86331:A:G	A	G	G	ADD	503	1.41887	0.238055	1.46968	0.141649	.
1	91581	1:91581:G:A	G	A	A	ADD	503	0.931304	0.123644	-0.5755980.564887	.
1	122872	1:122872:T:G	T	G	G	ADD	503	1.04828	0.182036	0.259034	0.795609	.
1	135163	1:135163:C:T	C	T	T	ADD	503	0.676666	0.242611	-1.60989	0.107422	.
```

# Visualization
To visualize the result, we will create manhattan plot, QQ plot and regional plot.

Please check [Visualization using gwaslab](https://cloufield.github.io/GWASTutorial/Visualization/)