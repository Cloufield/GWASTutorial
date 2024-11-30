# Meta-analysis

## Aims

Meta-analysis is one of the most commonly used statistical methods to combine the evidence from multiple studies into a single result. 

!!! note "Potential problems for small-scale genome-wide association studies"
    - Low coverage of markers and genetic variability
    - Less accurate effect size estimation
    - Low statistical power

To address these problems, meta-analysis is a powerful approach to integrate multiple GWAS summary statistics, especially when more and more summary statistics are publicly available.
. This method allows us to obtain increases in statistical power as sample size increases. 

!!! note "What we could achieve by conducting meta-analysis"
    
    - [x] Increase the statistical power for GWASs. 
    - [x] Improve the effect size estimations, which could facilitate downstream analyses. (For example, PRS or MR).
    - [x] Provide opportunities to study the less prevalent or understudied diseases. 
    - [x] Cross-validate findings across different studies. 

## A typical workflow of meta-analysis

<img width="450" alt="image" src="https://user-images.githubusercontent.com/40289485/218293217-d6a50f73-98f7-4957-82a3-d10a85bed8dc.png">


## Harmonization and QC for GWA meta-analysis

Before performing any type of meta-analysis, we need to make sure our datasets contain sufficient information and the datasets are QCed and harmonized. It is important to perform this step to avoid any unexpected errors and heterogeneity.

!!! info "Key points for Dataset selection"
    - [] **Minimal requirements for data** (CHR,POS,BETA,SE,P,N,EA,NEA,EAF... )
    - [] **Phenotype definition** 
    - [] Study design 
    - [] **Sample overlap** (independent population)
    - [] Proper citations (we can obtain sufficient information on study design, phenotype definition and QC)
    - [] Data integrity (md5sum check)
    - [] Ancestry (population with the same ancestry)
    - [] Downloading from the source (preferably not second-hand datasets)

!!! info "Key points for Quality control"
    - [] Remove variants with minor allele frequency being too low
    - [] Remove Multi-allelic Variants
    - [] Remove Duplicated variants
    - [] Remove Copy number variation
    - [] Normalize Indels
    - [] Standardize notations
    - [] Removed variants with extreme effect sizes
    - [] Filter out variants with low imputation accuracy

!!! info "Key points for Harmonization"
    - [] On the genomic coordinate 
    - [] On the same strand (mostly forward)
    - [] Be cautious for palindromic SNPs

## Fixed effects meta-analysis

Simply speaking, the fixed effects we mentioned here mean that the between-study variance is zero. Under the fixed effect model, we assume a common effect size across studies for a certain SNP.

!!! info "Fixed effect model"
    $$ \bar{\beta_{ij}} = {{\sum_{i=1}^{k} {w_{ij} \beta_{ij}}}\over{\sum_{i=1}^{k} {w_{ij}}}} $$

    - $w_{ij} = 1 / Var(\beta_{ij})$

### Heterogeneity test

!!! info "Cochran's Q test and $I^2$ "

    $$ Q = \sum_{i=1}^{k} {w_i (\beta_i - \bar{\beta})^2} $$

    $$ I_j^2 =  {{Q_j - df_j}\over{Q_j}}\times 100% =  {{Q - (k - 1)}\over{Q}}\times 100% $$

### METAL

METAL is one of the most commonly used tools for GWA meta-analysis. Its official documentation can be found [here](https://genome.sph.umich.edu/wiki/METAL_Documentation). METAL supports two models: (1) Sample size based approach and (2) Inverse variance based approach.


!!! example "A minimal example of meta-analysis using the IVW method" 
    
    ```bash
    cd 11_meta_analysis/GlucoseExample

    metal meta_input.txt
    ```

## Random effects meta-analysis

On the other hand, random effects mean that we need to model the between-study variance, which is not zero in this case. Under the random effect model, we assume the true effect size for a certain SNP varies across studies.

If heterogeneity of effects exists across studies, we need to model the between-study variance to correct for the deflation of variance in fixed-effect estimates.  

### GWAMA

!!! quote "Random effect model"
    The random effect variance component can be estimated by:
    
    $$ r_j^2 = max\left(0, {{Q_j - (N_j -1)}\over{\sum_iw_{ij} - ({{\sum_iw_{ij}^2} \over {\sum_iw_    {ij}}})}}\right)$$
    
    Then the effect size for SNP j can be obtained by:
    
    $$ \bar{\beta_j}^* = {{\sum_{i=1}^{k} {w_{ij}^* \beta_i}}\over{\sum_{i=1}^{k} {w_{ij}^*}}} $$
    
    The weights are estimated by:
    
    $$w_{ij}^* = {{1}\over{r_j^2 + Var(\beta_{ij})}} $$

The random effect model was implemented in GWAMA, which is another very popular GWA meta-analysis tool. Its official documentation can be found [here](https://genomics.ut.ee/en/tools).

!!! example "A minimal example of random effect meta-analysis using GWAMA" 
    
    The input file for GWAMA contains the path to each sumstats. Column names need to be standardized.
    
    ```txt title="GWAMA_script.in"
    Pop1.txt
    Pop2.txt
    Pop3.txt
    ```

    ```bash
    GWAMA \
        -i GWAMA_script.in \
        --random \
        -o myresults
    ```
## Cross-ancestry meta-analysis

### MANTRA

MANTRA (Meta-ANalysis of Transethnic Association studies) is one of the early efforts to address the heterogeneity for cross-ancestry meta-analysis.

MANTRA implements a Bayesian partition model where GWASs were clustered into ancestry clusters based on a prior model of similarity between them. MANTRA then uses Markov chain Monte Carlo (MCMC) algorithms to approximate the posterior distribution of parameters (which might be quite computationally intensive). MANTRA has been shown to increase power and mapping resolution over random-effects meta-analysis over a range of models of heterogeneity situations.

### MR-MEGA

MR-MEGA employs meta-regression to model the heterogeneity in effect sizes across ancestries. Its official documentation can be found [here](https://genomics.ut.ee/en/tools) (The same first author as GWAMA).


!!! quote "Meta-regression implemented in MR-MEGA"
    It will first construct a matrix $D$ of pairwise Euclidean distances between GWAS across autosomal     variants. The elements of D , $d_{k'k} $ for a pair of studies can be expressed as the following.     For each variant $j$, $p_{kj}$ is the allele frequency of j in study k, then:
    
    $$d_{k'k} = {{\sum_jI_j(p_{kj}-p_{k'j})^2}\over{\sum_jI_j}}$$
    
    - $I$ : an indicator of the inclusion of the $j$th variant 
    
    Then multi-dimensional scaling (MDS) will be performed to derive T axes of genetic variation ($x_k$     for study k)
    
    For each variant j, the effect size of the reference allele can be modeled in a linear regression     model as :
    
    $$E[\beta_{kj}] = \beta_j + \sum_{t=1}^T\beta_{tj}x_{kj}$$
    
    - $\beta_j$ : intercept
    - $\beta_{tj}$ : the effect size of the $t$ th axis of genetic variation for the $j$ th variant

!!! example "A minimal example of meta-analysis using MR-MEGA" 
    
    The input file for MR-MEGA contains the path to each sumstats. Column names need to be standardized like GWAMA.
    
    ```txt title="MRMEGA_script.in"
    Pop1.txt.gz
    Pop2.txt.gz
    Pop3.txt.gz
    Pop4.txt.gz
    Pop5.txt.gz
    Pop6.txt.gz
    Pop7.txt.gz
    Pop8.txt.gz
    ```

    ```bash
    MR-MEGA \
        -i MRMEGA_script.in \
        --pc 4 \
        -o myresults
    ```

## Global Biobank Meta-analysis Initiative (GBMI)

As a recent success achieved by meta-analysis, GBMI showed an example of the improvement of our understanding of diseases by taking advantage of large-scale meta-analyses.

For more details, you check check [here](https://www.globalbiobankmeta.org/).

## Reference

- **review** : Zeggini, E., & Ioannidis, J. P. (2009). Meta-analysis in genome-wide association studies.
- **review** : Evangelou, E., & Ioannidis, J. P. (2013). Meta-analysis methods for genome-wide association studies and beyond. Nature Reviews Genetics, 14(6), 379-389.
- **metal** : Willer, C. J., Li, Y., & Abecasis, G. R. (2010). METAL: fast and efficient meta-analysis of genomewide association scans. Bioinformatics, 26(17), 2190-2191.
- **gwama** : Mägi, R., & Morris, A. P. (2010). GWAMA: software for genome-wide association meta-analysis. BMC bioinformatics, 11, 1-6.
- **mantra**: Morris, A. P. (2011). Transethnic meta‐analysis of genomewide association studies. Genetic epidemiology, 35(8), 809-822.
- **mr-mega** :Mägi, R., Horikoshi, M., Sofer, T., Mahajan, A., Kitajima, H., Franceschini, N., ... & Morris, A. P. (2017). Trans-ethnic meta-regression of genome-wide association studies accounting for ancestry increases power for discovery and improves fine-mapping resolution. Human molecular genetics, 26(18), 3639-3650.
- **GBMI** : Zhou, W., Kanai, M., Wu, K. H. H., Rasheed, H., Tsuo, K., Hirbo, J. B., ... & Study, C. O. H. (2022). Global Biobank Meta-analysis Initiative: Powering genetic discovery across human disease. Cell Genomics, 2(10), 100192.
