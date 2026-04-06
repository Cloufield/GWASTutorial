# Meta-analysis

---


**On this page**

[TOC]

---


## Aims

Meta-analysis is one of the most commonly used statistical methods to combine the evidence from multiple studies into a single result. 

!!! note "Potential problems for small-scale genome-wide association studies"
    - Low coverage of markers and genetic variability
    - Less accurate effect size estimation
    - Low statistical power

To address these problems, meta-analysis is a powerful approach to integrate multiple GWAS summary statistics, especially when more and more summary statistics are publicly available. This method allows us to obtain increases in statistical power as sample size increases. 

!!! note "What we could achieve by conducting meta-analysis"
    
    - [x] Increase the statistical power for GWASs. 
    - [x] Improve the effect size estimations, which could facilitate downstream analyses. (For example, PRS or MR).
    - [x] Provide opportunities to study the less prevalent or understudied diseases. 
    - [x] Cross-validate findings across different studies. 

---


## A typical workflow of meta-analysis

<img width="450" alt="image" src="https://user-images.githubusercontent.com/40289485/218293217-d6a50f73-98f7-4957-82a3-d10a85bed8dc.png">

!!! note "Required data and tools"

    - **GWAS summary statistics** from each cohort — harmonized fields (CHR, POS, BETA, SE, P, N, effect/other allele, EAF, …); see [Harmonization and QC for GWA meta-analysis](#harmonization-and-qc-for-gwa-meta-analysis).
    - **Meta-analysis software** — e.g. **METAL** for the worked example ([METAL](#metal)); other sections mention R/`metafor` for random-effects models.

---


## Harmonization and QC for GWA meta-analysis

Before performing any type of meta-analysis, we need to make sure our datasets contain sufficient information and the datasets are QCed and harmonized. It is important to perform this step to avoid any unexpected errors and heterogeneity.

!!! info "Key points for Dataset selection"
    - [x] **Minimal requirements for data** (CHR,POS,BETA,SE,P,N,EA,NEA,EAF... )
    - [x] **Phenotype definition** 
    - [x] Study design 
    - [x] **Sample overlap** (independent population)
    - [x] Proper citations (we can obtain sufficient information on study design, phenotype definition and QC)
    - [x] Data integrity (md5sum check)
    - [x] Ancestry (population with the same ancestry)
    - [x] Downloading from the source (preferably not second-hand datasets)

!!! info "Key points for Quality control"
    - [x] Remove variants with minor allele frequency being too low
    - [x] Remove Multi-allelic Variants
    - [x] Remove Duplicated variants
    - [x] Remove Copy number variation
    - [x] Normalize Indels
    - [x] Standardize notations
    - [x] Removed variants with extreme effect sizes
    - [x] Filter out variants with low imputation accuracy

!!! info "Key points for Harmonization"
    - [x] On the genomic coordinate 
    - [x] On the same strand (mostly forward)
    - [x] Be cautious for palindromic SNPs

---


## Fixed effects meta-analysis

Simply speaking, the fixed effects we mentioned here mean that the between-study variance is zero. Under the fixed effect model, we assume a common effect size across studies for a certain SNP.

!!! info "Fixed effect model"
    $$ \bar{\beta_{ij}} = {{\sum_{i=1}^{k} {w_{ij} \beta_{ij}}}\over{\sum_{i=1}^{k} {w_{ij}}}} $$

    - $w_{ij} = 1 / Var(\beta_{ij})$

---


### Heterogeneity test

!!! info "Cochran's Q test and $I^2$ "

    $$ Q = \sum_{i=1}^{k} {w_i (\beta_i - \bar{\beta})^2} $$

    $$ I_j^2 =  {{Q_j - df_j}\over{Q_j}}\times 100% =  {{Q - (k - 1)}\over{Q}}\times 100% $$

    When $Q \le (k-1)$, $I^2$ is usually reported as **0%** (no excess heterogeneity relative to sampling error).

---


### METAL

METAL is one of the most commonly used tools for GWA meta-analysis. Its official documentation can be found [here](https://genome.sph.umich.edu/wiki/METAL_Documentation). METAL supports two models: (1) Sample size based approach and (2) Inverse variance based approach.


!!! example "A minimal example of meta-analysis using the IVW method" 
    
    ```bash
    cd 11_meta_analysis/GlucoseExample

    metal meta_input.txt
    ```

---


## Random effects meta-analysis

On the other hand, random effects mean that we need to model the between-study variance, which is not zero in this case. Under the random effect model, we assume the true effect size for a certain SNP varies across studies.

If heterogeneity of effects exists across studies, we need to model the between-study variance to correct for the deflation of variance in fixed-effect estimates.  

---


### GWAMA

!!! quote "Random effect model"
    The random effect variance component can be estimated by:
    
    $$ r_j^2 = max\left(0, {{Q_j - (N_j -1)}\over{\sum_iw_{ij} - ({{\sum_iw_{ij}^2} \over {\sum_iw_{ij}}})}}\right)$$
    
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

---


### Manual calculation in Python (IVW fixed and DL random effects)

The script [`manual_meta_ivw.py`](manual_meta_ivw.py) walks through **inverse-variance fixed effects** (same IVW logic as in [Fixed effects meta-analysis](#fixed-effects-meta-analysis) and METAL), **Cochran’s Q / I²**, and **DerSimonian–Laird random effects** with the same between-study variance structure as $r_j^2$ and $w_{ij}^*$ in GWAMA above. It uses **numpy** and **scipy** only.

The script prints a **toy three-study example** (low heterogeneity, $\tau^2=0$) and a **second example** with more spread across studies so $\tau^2>0$ and the random-effects standard error is wider than the fixed-effects one.

!!! example "Run the educational script"

    ```bash
    cd 11_meta_analysis
    pip install numpy scipy   # if needed
    python3 manual_meta_ivw.py
    ```

    You can change the arrays `beta` and `se` in the `main()` function to try your own harmonized summary statistics for one variant.

!!! note "Genome-wide scale"

    GWAS meta-analysis repeats these calculations **per SNP** (after harmonization). Loops over millions of variants belong in compiled tools (METAL, GWAMA, etc.); this Python file is for **understanding the statistics**, not for production GWAS.

---

## Cross-ancestry meta-analysis

---


### MANTRA

MANTRA (Meta-ANalysis of Transethnic Association studies) is one of the early efforts to address the heterogeneity for cross-ancestry meta-analysis.

MANTRA implements a Bayesian partition model where GWASs were clustered into ancestry clusters based on a prior model of similarity between them. MANTRA then uses Markov chain Monte Carlo (MCMC) algorithms to approximate the posterior distribution of parameters (which might be quite computationally intensive). MANTRA has been shown to increase power and mapping resolution over random-effects meta-analysis over a range of models of heterogeneity situations.

---


### MR-MEGA

MR-MEGA employs meta-regression to model the heterogeneity in effect sizes across ancestries. Its official documentation can be found [here](https://genomics.ut.ee/en/tools) (The same first author as GWAMA).


!!! quote "Meta-regression implemented in MR-MEGA"
    It will first construct a matrix $D$ of pairwise Euclidean distances between GWAS across autosomal variants. The elements of D, $d_{k'k}$ for a pair of studies can be expressed as the following. For each variant $j$, $p_{kj}$ is the allele frequency of j in study k, then:
    
    $$d_{k'k} = {{\sum_jI_j(p_{kj}-p_{k'j})^2}\over{\sum_jI_j}}$$
    
    - $I$ : an indicator of the inclusion of the $j$th variant 
    
    Then multi-dimensional scaling (MDS) will be performed to derive T axes of genetic variation ($x_k$ for study k)
    
    For each variant j, the effect size of the reference allele can be modeled in a linear regression model as:
    
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

---


## Rare variant meta-analysis

Rare-variant association is usually done at the **variant-set, region, or gene level** (burden, SKAT, SKAT-O, ACAT, etc.), not only as one independent SNP test at a time. **Meta-analysis across cohorts** must match that structure: you combine the **same aggregation unit** across studies (same gene/region, same variant mask, same weights, and compatible allele coding) using statistics that are valid for the test you ran. For background on rare-variant *tests within one study*, see the tutorial chapter [Rare-variant association tests](../34_rare_variant/README.md).

!!! info "Key formulas: combining score statistics across cohorts"

    For variant $j$ in a fixed mask, let cohort $k$ contribute a **null-model score** $S_{jk}$ and its **variance** $V_{jk}$ (often after SPA or other calibration for binary traits). Under independence of cohorts, the **meta-analyzed** score and variance are typically formed as

    $$ S_j^* = \sum_{k=1}^{K} S_{jk}, \qquad V_j^* = \sum_{k=1}^{K} V_{jk}. $$

    For a **set** of $m$ variants, write $S^* = (S_1^*,\ldots,S_m^*)^\top$ and $V^* = \mathrm{diag}(V_1^*,\ldots,V_m^*)$. A common **sandwich** covariance uses the correlation of genotypes in the set, $\mathrm{Cor}(G)$ (from LD / cross-products), together with the meta variances:

    $$ \mathrm{Cov}(S^*) \approx V^{*1/2}\, \mathrm{Cor}(G)\, V^{*1/2}. $$

    Software adjusts $V_{jk}$ (e.g. SPA, genotype-count–based SPA in Meta-SAIGE) before summing and before building $\mathrm{Cov}(S^*)$; the exact recipe is implementation-specific.

---


### How it differs from common-variant SNP meta-analysis

| Aspect | Common-variant GWAS meta (e.g. METAL) | Rare-variant meta |
|--------|----------------------------------------|-------------------|
| Unit of analysis | Usually each SNP separately | Often a **gene, region, or variant set** (burden/SKAT window) |
| Per-study output | $\beta$, SE (or $Z$, $N$) per SNP after harmonization | Set-level **score statistics** and, for SKAT-type tests, **score covariances**; sometimes harmonized burden $\beta$/SE |
| Variant alignment | Harmonize EA/NEA, strand, position | Same **aggregation unit**: same mask, same functional filter (e.g. LoF), compatible allele coding, and usually comparable frequency thresholds / weighting rules |
| Heterogeneity | Cochran $Q$, random effects | Still relevant; rare-variant meta is especially sensitive to **mask differences**, ancestry-specific allele-frequency differences, and study-specific variant availability |

!!! note "Why simple SNP meta tools are not enough"

    Standard **per-variant** inverse-variance meta assumes each variant is tested in the same way in every study. **SKAT** and **SKAT-O** instead rely on variant-level score information and its covariance within a set. Combining only final cohort-level gene/set *p*-values with Fisher's method is generally **not equivalent** to proper score-based rare-variant meta-analysis and is often less powerful.

---


### Score-based meta-analysis (RAREMETAL)

**RAREMETAL** implements rare-variant meta-analysis by combining per-study **score statistics** and, for variance-component tests, the **covariance of scores across variants**, rather than using only final set-level *p*-values. Studies must use compatible pipelines that export the statistics expected by the meta-analysis software. This is a standard approach when individual-level genotypes cannot be pooled.

!!! info "Key formulas: burden and SKAT-type tests on combined scores"

    Let $S^* = (S_1^*,\ldots,S_m^*)^\top$ be the **meta-combined** scores for $m$ variants in the tested set, $\Sigma^* = \mathrm{Cov}(S^*)$, and $w = (w_1,\ldots,w_m)^\top$ a **weight vector** (often MAF-based, e.g. Beta weights). Define $W = \mathrm{diag}(w_1^2,\ldots,w_m^2)$.

    **Burden (directional) test statistic** (quadratic form; one degree of freedom under standard approximations):

    $$ Q_{\mathrm{burden}} = \frac{\bigl(w^\top S^*\bigr)^2}{w^\top \Sigma^* w}. $$

    **SKAT (variance-component) statistic:**

    $$ Q_{\mathrm{SKAT}} = S^{*\top} W\, S^*. $$

    Under $H_0$, $Q_{\mathrm{SKAT}}$ is often approximated by a **mixture of $\chi^2_1$** variables determined by the eigenvalues of $W^{1/2} \Sigma^* W^{1/2}$ (Davies-type *p*-values in software).

    **SKAT-O** combines the burden and SKAT components into a single omnibus test by searching over a mixing parameter $\rho \in [0,1]$ (optimal unified approach of Lee et al.).

!!! info "What to read for the statistical framework"

    The key idea is that cohorts contribute **null-model score statistics** that add across studies, while the corresponding variances and covariances determine burden- and SKAT-type meta-analysis. See Feng et al. (Bioinformatics 2014) and Liu et al. (Nature Genetics 2014).

Other software and pipelines (for example **seqMeta** in R) follow similar **score-meta** principles for burden and SKAT-type tests; check each tool's input format and whether **related samples**, **variant correlation**, or **set definition** are handled consistently in your cohort analyses.

---


### Other rare-variant score-meta tools (Meta-SAIGE, MetaSKAT, MetaSTAAR)

[**Meta-SAIGE**](https://www.nature.com/articles/s41588-025-02403-y) extends **SAIGE-GENE+** to pooled **summary statistics**: cohorts contribute per-variant **scores**, variances, and **sparse LD** for gene/set **burden**, **SKAT**, and **SKAT-O**, with ultrarare collapsing, **Cauchy** combination across masks, **SPA** for imbalanced binary traits, and per-cohort LD reusable across phenotypes.

[**MetaSKAT**](https://doi.org/10.1016/j.ajhg.2013.05.010), via the **MetaSKAT** **R** package, is an earlier **general framework** for rare-variant **gene/set** meta-analysis on **sequencing** studies: each cohort exports variant-level **score statistics** and the **covariance of scores within the tested set**, which are combined for meta **burden**, **SKAT**, and **SKAT-O** without individual-level genotypes.

[**MetaSTAAR**](https://www.nature.com/articles/s41588-022-01225-6) is geared to **biobank-scale WGS/WES** meta-analysis, storing study summaries in **sparse** form for scalable cross-cohort combination and using **multiple functional annotations** to weight variants in **coding** and **noncoding** masks; it accommodates **relatedness**, **population structure**, and **quantitative** or **binary** traits.

---


### Inverse-variance meta of harmonized burden summaries

If each study reports a **single effect** and **standard error** for the **same predefined burden** (same variants, same weights, same coding of the burden and effect allele), then the usual inverse-variance fixed- or random-effects formulas can be applied to that scalar outcome. This is most defensible when all cohorts follow the same **analysis plan** for constructing the burden.

!!! info "Key formulas: inverse-variance meta of one harmonized burden (scalar)"

    For $K$ studies with harmonized burden estimates $\beta_k$ and $\mathrm{SE}_k$, let $w_k = 1 / \mathrm{SE}_k^2$. The **fixed-effect** pooled estimate matches [Fixed effects meta-analysis](#fixed-effects-meta-analysis):

    $$ \bar{\beta} = \frac{\sum_{k=1}^{K} w_k\, \beta_k}{\sum_{k=1}^{K} w_k}, \qquad \mathrm{SE}(\bar{\beta}) = \frac{1}{\sqrt{\sum_{k=1}^{K} w_k}}. $$

    **Random-effects** meta (e.g. DerSimonian–Laird $\tau^2$ on the $\beta_k$ with weights $w_k$, then revised weights $w_k^* = 1/(\tau^2 + \mathrm{SE}_k^2)$) uses the same expressions as in [GWAMA](#gwama) / [Manual calculation in Python](#manual-calculation-in-python-ivw-fixed-and-dl-random-effects).

!!! warning "Validity depends on harmonization"

    IVW meta of burden $\beta$ and SE is only appropriate when the **burden construction** is aligned across studies. Do not mix different variant masks, MAF cutoffs, functional annotations, or weighting schemes without reprocessing.

---

## Global Biobank Meta-analysis Initiative (GBMI)

As a recent success achieved by meta-analysis, GBMI showed an example of the improvement of our understanding of diseases by taking advantage of large-scale meta-analyses.

For more details, you can check [here](https://www.globalbiobankmeta.org/).

---


## References

- **review** : Zeggini, E., & Ioannidis, J. P. (2009). Meta-analysis in genome-wide association studies.
- **review** : Evangelou, E., & Ioannidis, J. P. (2013). Meta-analysis methods for genome-wide association studies and beyond. Nature Reviews Genetics, 14(6), 379-389.
- **metal** : Willer, C. J., Li, Y., & Abecasis, G. R. (2010). METAL: fast and efficient meta-analysis of genomewide association scans. Bioinformatics, 26(17), 2190-2191.
- **gwama** : Mägi, R., & Morris, A. P. (2010). GWAMA: software for genome-wide association meta-analysis. BMC bioinformatics, 11, 1-6.
- **mantra**: Morris, A. P. (2011). Transethnic meta‐analysis of genomewide association studies. Genetic epidemiology, 35(8), 809-822.
- **mr-mega** :Mägi, R., Horikoshi, M., Sofer, T., Mahajan, A., Kitajima, H., Franceschini, N., ... & Morris, A. P. (2017). Trans-ethnic meta-regression of genome-wide association studies accounting for ancestry increases power for discovery and improves fine-mapping resolution. Human molecular genetics, 26(18), 3639-3650.
- **GBMI** : Zhou, W., Kanai, M., Wu, K. H. H., Rasheed, H., Tsuo, K., Hirbo, J. B., ... & Study, C. O. H. (2022). Global Biobank Meta-analysis Initiative: Powering genetic discovery across human disease. Cell Genomics, 2(10), 100192.
- **rare-variant meta (framework)** : Liu, D. J., Peloso, G. M., Zhan, X., Holmen, O. L., Zawistowski, M., ... & Abecasis, G. R. (2014). Meta-analysis of gene-level tests for rare variant association. *Nature Genetics*, 46(2), 155–165.
- **raremetal** : Feng, S., Liu, D., Zhan, X., Wing, M. K., & Abecasis, G. R. (2014). RAREMETAL: fast and powerful meta-analysis of rare variants. *Bioinformatics*, 30(19), 2828–2829.
- **meta-saige** : Park, E., Nam, K., Jeong, S., ... Zhou, W., & Lee, S. (2025). Scalable and accurate rare variant meta-analysis with Meta-SAIGE. *Nature Genetics*, 57, 3185–3192. [https://doi.org/10.1038/s41588-025-02403-y](https://www.nature.com/articles/s41588-025-02403-y)
- **metaskat** : Lee, S., Teslovich, T. M., Boehnke, M., & Lin, X. (2013). General framework for meta-analysis of rare variants in sequencing association studies. *American Journal of Human Genetics*, 93(1), 42–53. [https://doi.org/10.1016/j.ajhg.2013.05.010](https://doi.org/10.1016/j.ajhg.2013.05.010)
- **metastaar** : Li, X., Quick, C., Zhou, H., Gaynor, S., Liu, Y., Chen, H., ... & Lin, X. (2022). Powerful, scalable and resource-efficient meta-analysis of rare variant associations in large whole genome sequencing studies. *Nature Genetics*, 55(1), 154–164. [https://doi.org/10.1038/s41588-022-01225-6](https://www.nature.com/articles/s41588-022-01225-6)
- **cauchy-combination** : Liu, Y., & Xie, J. (2020). Cauchy combination test: a powerful test with analytic p-value calculation under arbitrary dependency structures. *Journal of the American Statistical Association*, 115(529), 393–402.
- **skat-o** : Lee, S., Wu, M. C., & Lin, X. (2012). Optimal unified approach for rare-variant association testing with application to small-sample case-control whole-exome sequencing studies. *American Journal of Human Genetics*, 91(2), 224–237.
