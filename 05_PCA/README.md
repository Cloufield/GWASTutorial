# 5.Principle conponent analysis
PCA is by far the most commonly used dimension reduction approach used in population genetics which could identify the diffenrence in ancestry among the sample individuals.
For GWAS we also need to include top PCs to adjust for the population stratification.

Please read the following paper on how we apply PCA to genetic data:
Price, A., Patterson, N., Plenge, R. et al. Principal components analysis corrects for stratification in genome-wide association studies. Nat Genet 38, 904–909 (2006). https://doi.org/10.1038/ng1847 https://www.nature.com/articles/ng1847

Simply speaking, GRM (genetic relationship matrix) is first estimated and then PCA is applied to this matrix to generate PCs for each individual.

So before association analysis, we will learn how to run PCA analysis first.

---------

## 5.1 Preparation:  excluding SNPs in high-LD or HLA regions. 

Please check https://genome.sph.umich.edu/wiki/Regions_of_high_linkage_disequilibrium_(LD)
- 0.1 simply copy the list of high-LD or HLA regions in Genome build version(.bed format) to a text file `high-ld.txt`.
- 0.2 use `high-ld.txt` to extract all SNPs which are located in the regions described in the file using the code as follows:
```
plink --file ${plinkFile} --make-set high-ld.txt --write-set --out hild
```
- 0.3 exclude these SNPs using `--exclude` when pruning.

Note: the reason why we want to exclude such high-LD or HLA regions ->Price, A. L., Weale, M. E., Patterson, N., Myers, S. R., Need, A. C., Shianna, K. V., Ge, D., Rotter, J. I., Torres, E., Taylor, K. D., Goldstein, D. B., & Reich, D. (2008). Long-range LD can confound genome scans in admixed populations. American journal of human genetics, 83(1), 132–139. https://doi.org/10.1016/j.ajhg.2008.06.005 

(Since we are using simulated data, this step could be skipped for now.)

---------
## 5.2 PCA steps: 

- 1.Pruning (https://www.cog-genomics.org/plink/2.0/ld#indep)
- 2.Removing relatives (usually 2-degree) (https://www.cog-genomics.org/plink/2.0/distance#king_cutoff)
- 3.Run PCA using un-related samples and independent SNPs (https://www.cog-genomics.org/plink/2.0/strat#pca)
- 4.Project to all samples (https://www.cog-genomics.org/plink/2.0/score#pca_project)

---------
## 5.3 Sample codes:
```
plinkFile="" #please set this to your own path
outPrefix="plink_results"
threadnum=2
hildset = hild # change to file of SNPs located in HLA and high ld region 

# pruning
plink2 \
        --bfile ${plinkFile} \
	--threads ${threadnum} \
	--exclude ${hildset} \.    #(Since we are using simulated data, this option could be skipped for this tutorial.)
	--indep-pairwise 500 50 0.2 \
        --out ${outPrefix}

# remove related samples using knig-cuttoff
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

After running, we get the `plink_results.eigenvec.allele` file, which will be used to project onto all samples along with a allele count `plink_results.acount` file.
```
head plink_results.eigenvec.allele


head plink_results.acount


```
Please check https://www.cog-genomics.org/plink/2.0/score#pca_project for more details on projection.
Eventually, we will get the PCA results for all samples.
```
head plink_results_projected.sscore


## Plot the PCs
Please check the following jupyter notebook for the codes to plot PCs.

Requrements:
- python>3
- numpy,pandas,seaborn,matplotlib

## (optional) UMAP
We can apply another non-linear dimension reduction algorithm called UMAP to the PCs to further identfy the local structures. (PCA-UMAP)

For more details, please check the following papers and urls:
- https://umap-learn.readthedocs.io/en/latest/index.html
- McInnes, L., Healy, J., & Melville, J. (2018). Umap: Uniform manifold approximation and projection for dimension reduction. arXiv preprint arXiv:1802.03426. https://doi.org/10.48550/arXiv.1802.03426
- Diaz-Papkovich, A., Anderson-Trocmé, L. & Gravel, S. A review of UMAP in population genetics. J Hum Genet 66, 85–91 (2021). https://doi.org/10.1038/s10038-020-00851-4 https://www.nature.com/articles/s10038-020-00851-4
