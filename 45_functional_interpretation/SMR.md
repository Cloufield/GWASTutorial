# SMR: Summary-data-based Mendelian Randomization

## Table of Contents

- [Introduction](#introduction)
    - [SMR & HEIDI overview](#smr--heidi-overview)
    - [Key concepts](#key-concepts)
- [Workflow](#workflow)
- [Installation](#installation)
- [Data preparation](#data-preparation)
    - [GWAS summary statistics](#gwas-summary-statistics)
    - [eQTL summary data in BESD format](#eqtl-summary-data-in-besd-format)
    - [LD reference panel](#ld-reference-panel)
- [SMR & HEIDI analysis](#smr--heidi-analysis)
    - [Run SMR and HEIDI test](#run-smr-and-heidi-test)
    - [Interpret the results](#interpret-the-results)
    - [Key parameters](#key-parameters)
- [Multi-SNP-based SMR test](#multi-snp-based-smr-test)
- [SMR in trans regions](#smr-in-trans-regions)
- [SMR analysis of two molecular traits](#smr-analysis-of-two-molecular-traits)
- [Data management](#data-management)
    - [BESD format](#besd-format)
    - [Make a BESD file from eQTL summary data](#make-a-besd-file-from-eqtl-summary-data)
    - [Query eQTL results](#query-eqtl-results)
- [SMR locus plot](#smr-locus-plot)
- [SMR Portal](#smr-portal)
- [Available xQTL data resources](#available-xqtl-data-resources)
    - [eQTL data](#eqtl-data)
    - [mQTL data](#mqtl-data)
    - [sQTL data](#sqtl-data)
- [References](#references)

## Introduction

### SMR & HEIDI overview

GWAS can identify SNPs associated with complex traits, but it often remains unclear **which gene** a significant SNP acts through. SMR (Summary-data-based Mendelian Randomization) helps answer this question by combining GWAS results with eQTL data to **prioritize genes whose expression levels are associated with the trait** (Zhu et al. 2016 Nature Genetics).

The basic logic is:

- From a GWAS, we know a SNP is associated with a trait.
- From an eQTL study, we know the same SNP is associated with the expression of a specific gene.
- If both associations are driven by the same underlying causal variant, this gene is likely involved in the trait.

Although the method is named after eQTLs, it works with any type of molecular QTL (xQTL):

- Expression QTL (eQTL) — gene expression levels
- DNA methylation QTL (mQTL) — methylation sites
- Protein abundance QTL (pQTL) — protein levels
- Splicing QTL (sQTL) — RNA splicing events
- Chromatin accessibility QTL (caQTL) — open chromatin regions

!!! info "SMR vs. standard Mendelian Randomization"
    Standard MR uses genetic variants as instruments to infer **causal** relationships between an exposure and an outcome (e.g. does cholesterol cause heart disease?). SMR borrows this idea but uses it to link molecular traits (like gene expression) to complex traits via shared genetic variants. The goal is gene prioritization rather than formal causal inference.

!!! warning "Pleiotropy vs. causality — an important limitation"
    SMR uses a single SNP as the instrument, so it **cannot tell apart** two scenarios:

    - **Causality**: SNP $\rightarrow$ gene expression $\rightarrow$ trait (the SNP affects the trait *through* the gene)
    - **Pleiotropy**: SNP $\rightarrow$ gene expression *and* SNP $\rightarrow$ trait (the SNP affects both independently)

    Both look identical in summary statistics. Zhu et al. (2016) confirmed this by simulation. For this reason, the authors use the term **"pleiotropic association"** broadly to cover both possibilities, and SMR results should not be interpreted as proof of causality.

### Key concepts

**SMR test**: If a SNP ($z$) affects both gene expression ($x$) and a trait ($y$), we can estimate the effect of expression on the trait as a simple ratio:

$$\hat{b}_{xy} = \hat{b}_{zy} / \hat{b}_{zx}$$

where $\hat{b}_{zy}$ is the SNP-trait effect from GWAS and $\hat{b}_{zx}$ is the SNP-expression effect from the eQTL study. This is known as a **Wald ratio** estimator.

To test whether $\hat{b}_{xy}$ is significantly different from zero, we need its variance. Using the delta method:

$$\text{Var}(\hat{b}_{xy}) \approx \frac{b_{zy}^2}{b_{zx}^2} \left( \frac{\text{Var}(\hat{b}_{zy})}{b_{zy}^2} + \frac{\text{Var}(\hat{b}_{zx})}{b_{zx}^2} - 2 \frac{\text{Cov}(\hat{b}_{zy}, \hat{b}_{zx})}{b_{zy} \cdot b_{zx}} \right)$$

In practice, the GWAS and eQTL summary statistics come from **two independent studies** with non-overlapping samples. Because the estimates are from different individuals, $\text{Cov}(\hat{b}_{zy}, \hat{b}_{zx}) = 0$, and the variance simplifies to:

$$\text{Var}(\hat{b}_{xy}) \approx \frac{b_{zy}^2}{b_{zx}^2} \left( \frac{\text{Var}(\hat{b}_{zy})}{b_{zy}^2} + \frac{\text{Var}(\hat{b}_{zx})}{b_{zx}^2} \right)$$

The test statistic $T_{SMR} = \hat{b}_{xy}^2 / \text{Var}(\hat{b}_{xy}) \sim \chi^2_1$ can also be written as:

$$T_{SMR} \approx \frac{ \chi^2_{zy} \cdot \chi^2_{zx} }{ \chi^2_{zy} + \chi^2_{zx} }$$

where $\chi^2_{zy}$ and $\chi^2_{zx}$ are the chi-squared statistics from the GWAS and eQTL studies, respectively. Intuitively, $T_{SMR}$ will only be large when a SNP is strongly associated with **both** the trait and gene expression.

**HEIDI test**: The SMR test tells us *whether* a gene is associated with the trait, but not *why*. The association could be due to:

- **Pleiotropy**: a single causal variant affecting both expression and the trait
- **Linkage**: two distinct causal variants that happen to be in LD

The HEIDI (HEterogeneity In Dependent Instruments) test distinguishes between these two scenarios. The key idea is simple: if a single shared variant drives both signals, then the ratio $\hat{b}_{zy} / \hat{b}_{zx}$ should be **the same** no matter which nearby SNP we use to compute it. If two different variants are responsible, the ratio will vary across SNPs.

HEIDI tests this by comparing the SMR estimate at each nearby SNP $i$ to that at the top eQTL:

$$d_i = \hat{b}_{xy}(i) - \hat{b}_{xy}(\text{top})$$

If pleiotropy is true, all $d_i$ should be close to zero. HEIDI combines these differences into a single test statistic ($T_{HEIDI} \sim \chi^2_{m-1}$, where $m$ is the number of SNPs) that accounts for LD between SNPs. A significant result ($p_{HEIDI} < 0.05$) rejects the pleiotropy model in favor of linkage.

!!! info "Interpreting SMR and HEIDI results together"

    | SMR p-value | HEIDI p-value | Interpretation |
    |---|---|---|
    | Significant | Not significant ($\geq 0.05$) | Pleiotropic association (gene likely involved) |
    | Significant | Significant ($< 0.05$) | Likely due to linkage (two distinct causal variants) |
    | Not significant | — | No association detected |

## Workflow

1. **Prepare input data**: GWAS summary statistics (GCTA-COJO format), xQTL summary data (BESD format), and an LD reference panel (PLINK binary format).
2. **Run SMR test**: Identify genes whose expression is associated with the trait using the top cis-eQTL as the instrument.
3. **Run HEIDI test**: Distinguish pleiotropy (shared causal variant) from linkage (distinct causal variants in LD).
4. **Filter results**: Select genes passing the SMR significance threshold ($p_{SMR} < 0.05/n_{probes}$) and not rejected by HEIDI ($p_{HEIDI} \geq 0.05$).
5. **Visualize**: Generate SMR locus plots or explore results via the SMR Portal.

## Installation

SMR can be downloaded from the Yang Lab website: [https://yanglab.westlake.edu.cn/software/smr/](https://yanglab.westlake.edu.cn/software/smr/)

## Data preparation

Three types of input data are required for SMR analysis:

1. **GWAS summary statistics** in GCTA-COJO format
2. **eQTL (or other xQTL) summary data** in BESD format
3. **LD reference panel** in PLINK binary format (for LD estimation in the HEIDI test)

### GWAS summary statistics

GWAS summary statistics must follow the GCTA-COJO format:

```txt title="mygwas.ma"
SNP    A1  A2  freq    b   se  p   n
rs1001    A   G   0.8493  0.0024  0.0055  0.6653  129850
rs1002    C   G   0.03606 0.0034  0.0115  0.7659  129799
rs1003    A   C   0.5128  0.045   0.038   0.2319  129830
```

The columns are:

| Column | Description |
|--------|-------------|
| `SNP` | SNP rs ID |
| `A1` | Effect allele (coded allele) |
| `A2` | The other allele |
| `freq` | Frequency of the effect allele |
| `b` | Effect size (log(OR) for case-control studies) |
| `se` | Standard error |
| `p` | P-value |
| `n` | Sample size (can be `NA` if not available; not used in SMR/HEIDI) |

!!! warning
    - `A1` must be the effect allele with `A2` being the other allele.
    - `freq` must be the frequency of `A1`.
    - For case-control studies, the effect size should be $\log(\text{OR})$.
    - The allele frequency information is used in a QC step to remove SNPs with discrepant allele frequencies between datasets.

### eQTL summary data in BESD format

SMR reads eQTL summary data in its own efficient binary format called **BESD** (Binary Effect Size Distribution). The data are stored in three files:

- `.esi` — SNP information (similar to PLINK `.bim`)
- `.epi` — Probe/gene information
- `.besd` — Summary statistics in binary format

Pre-compiled eQTL/xQTL datasets in BESD format are available for download (see [Available xQTL data resources](#available-xqtl-data-resources) below).

If your eQTL data are in other formats (e.g. Matrix eQTL, FastQTL, QTLtools, PLINK, GEMMA, BOLT-LMM), you can convert them to BESD format using SMR's data management options (see [Data management](#data-management)).

### LD reference panel

A reference panel in PLINK binary format (`.bed`, `.bim`, `.fam`) is required for LD estimation in the HEIDI test. The reference sample should be from the same ancestry as the GWAS and eQTL studies.

## SMR & HEIDI analysis

### Run SMR and HEIDI test

!!! example "Basic SMR and HEIDI analysis"
    ```bash
    smr \
        --bfile ../01_Dataset/1KG.EAS.auto.snp.norm.nodup.split.rare002.common015.missing \
        --gwas-summary mygwas.ma \
        --beqtl-summary myeqtl \
        --out mysmr \
        --thread-num 10
    ```

**Flags:**

- `--bfile` reads individual-level SNP genotype data (PLINK binary format) as the LD reference.
- `--gwas-summary` reads GWAS summary statistics in GCTA-COJO format.
- `--beqtl-summary` reads xQTL summary data in BESD format.
- `--out` specifies the output filename prefix.
- `--thread-num` specifies the number of threads for parallel computing (default: 1).

### Interpret the results

The output file `mysmr.smr` contains the following columns:

```txt title="mysmr.smr"
ProbeID  Probe_Chr  Gene  Probe_bp  SNP  SNP_Chr  SNP_bp  A1  A2  Freq  b_GWAS  se_GWAS  p_GWAS  b_eQTL  se_eQTL  p_eQTL  b_SMR  se_SMR  p_SMR  p_HEIDI  nsnp_HEIDI
```

| Column | Description |
|--------|-------------|
| `ProbeID` | Probe ID |
| `Probe_Chr` | Probe chromosome |
| `Gene` | Gene name |
| `Probe_bp` | Probe position |
| `SNP` | Top associated cis-eQTL |
| `A1` / `A2` | Effect allele / other allele |
| `Freq` | Frequency of effect allele (from reference) |
| `b_GWAS` / `se_GWAS` / `p_GWAS` | Effect size, SE, and p-value from GWAS |
| `b_eQTL` / `se_eQTL` / `p_eQTL` | Effect size, SE, and p-value from eQTL study |
| `b_SMR` / `se_SMR` / `p_SMR` | Effect size, SE, and p-value from SMR test |
| `p_HEIDI` | P-value from the HEIDI test |
| `nsnp_HEIDI` | Number of SNPs used in the HEIDI test |

!!! note "Filtering the results"
    A common filtering strategy is:

    1. Select probes with $p_{SMR}$ below a Bonferroni-corrected threshold (e.g. $0.05 / n_{probes}$).
    2. Among these, retain probes with $p_{HEIDI} \geq 0.05$ (not rejected by the HEIDI test), indicating pleiotropy rather than linkage.
    3. Probes with `NA` for `p_HEIDI` indicate too few SNPs for the HEIDI test; interpret with caution.

### Key parameters

!!! example "SMR with customized parameters"
    ```bash
    smr \
        --bfile mydata \
        --gwas-summary mygwas.ma \
        --beqtl-summary myeqtl \
        --peqtl-smr 5e-8 \
        --ld-upper-limit 0.9 \
        --ld-lower-limit 0.05 \
        --peqtl-heidi 1.57e-3 \
        --heidi-min-m 3 \
        --heidi-max-m 20 \
        --cis-wind 2000 \
        --maf 0.01 \
        --diff-freq 0.2 \
        --thread-num 10 \
        --out mysmr
    ```

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--peqtl-smr` | `5e-8` | P-value threshold for selecting the top cis-eQTL for SMR test |
| `--peqtl-heidi` | `1.57e-3` | P-value threshold for selecting eQTLs for HEIDI test |
| `--ld-upper-limit` | `0.9` | LD $r^2$ upper threshold for pruning SNPs in HEIDI test |
| `--ld-lower-limit` | `0.05` | LD $r^2$ lower threshold for pruning SNPs in HEIDI test |
| `--heidi-min-m` | `3` | Minimum number of cis-SNPs for HEIDI test |
| `--heidi-max-m` | `20` | Maximum number of eQTLs for HEIDI test |
| `--cis-wind` | `2000` | Window size (Kb) around the probe for cis-eQTL selection |
| `--maf` | — | MAF threshold for SNP filtering in the reference sample |
| `--diff-freq` | `0.2` | Max allele frequency difference between datasets |
| `--heidi-mtd` | `1` | HEIDI method: `0` for original, `1` for new (uses top 20 SNPs) |

!!! example "Turn off the HEIDI test"
    ```bash
    smr \
        --bfile mydata \
        --gwas-summary mygwas.ma \
        --beqtl-summary myeqtl \
        --heidi-off \
        --out mysmr
    ```

!!! example "Specify a target SNP for SMR and HEIDI tests"
    ```bash
    smr \
        --bfile mydata \
        --gwas-summary mygwas.ma \
        --beqtl-summary myeqtl \
        --target-snp rs12345 \
        --out mysmr
    ```

## Multi-SNP-based SMR test

The multi-SNP-based SMR test combines information from all cis-SNPs passing a p-value threshold (default: `5e-8`) to increase statistical power (Wu et al. 2018 Nature Communications). SNPs are pruned for LD using a weighted vertex coverage algorithm.

!!! example "Multi-SNP-based SMR test"
    ```bash
    smr \
        --bfile mydata \
        --gwas-summary mygwas.ma \
        --beqtl-summary myeqtl \
        --smr-multi \
        --out mymulti
    ```

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--smr-multi` | — | Turns on the multi-SNP-based SMR test |
| `--set-wind` | all cis | Window (Kb) around top cis-eQTL for SNP selection |
| `--ld-multi-snp` | `0.1` | LD $r^2$ threshold for pruning SNPs in multi-SNP SMR |

## SMR in trans regions

Trans-eQTLs are defined as eQTLs more than 5 Mb away from the probe. SMR and HEIDI tests can also be applied in trans regions.

!!! example "SMR and HEIDI tests in trans regions"
    ```bash
    smr \
        --bfile mydata \
        --gwas-summary mygwas.ma \
        --beqtl-summary myeqtl \
        --trans \
        --trans-wind 1000 \
        --out mytrans
    ```

- `--trans` turns on SMR/HEIDI tests in trans regions.
- `--trans-wind` defines the window size (Kb) around the top trans-eQTL (default: 1000 Kb, i.e. a whole region of 2000 Kb).

## SMR analysis of two molecular traits

SMR can also test the pleiotropic association between two molecular traits (e.g. DNA methylation and gene expression) using summary data.

!!! example "SMR analysis of mQTL (exposure) and eQTL (outcome)"
    ```bash
    smr \
        --bfile mydata \
        --beqtl-summary myexposure \
        --beqtl-summary myoutcome \
        --out myomics
    ```

The first `--beqtl-summary` specifies the exposure (e.g. mQTL) and the second specifies the outcome (e.g. eQTL). The analysis focuses on the cis region, testing for associations between molecular sites within $\pm$ 1 Mb of each target gene.

Useful flags for subsetting probes:

| Flag | Description |
|------|-------------|
| `--extract-exposure-probe` | Extract a subset of exposure probes |
| `--extract-outcome-probe` | Extract a subset of outcome probes |
| `--exclude-exposure-probe` | Exclude a subset of exposure probes |
| `--exclude-outcome-probe` | Exclude a subset of outcome probes |
| `--extract-single-exposure-probe` | Extract a single exposure probe |
| `--extract-single-outcome-probe` | Extract a single outcome probe |

## Data management

### BESD format

eQTL summary data in BESD format consist of three files:

```txt title="myeqtl.esi (SNP information)"
1    rs1001  0   744055  A   G   0.23
1    rs1002  0   765522  C   G   0.06
1    rs1003  0   995669  T   C   0.11
```

Columns: chromosome, SNP, genetic distance, bp position, effect allele, other allele, frequency of effect allele.

```txt title="myeqtl.epi (Probe information)"
1    probe1001   0   924243  Gene01  +
1    probe1002   0   939564  Gene02  -
1    probe1003   0   1130681 Gene03  -
```

Columns: chromosome, probe ID, genetic distance, physical position, gene ID, gene orientation.

The `.besd` file stores the summary statistics (effect size and SE) in binary format.

!!! info "Sparse BESD format"
    By default, SMR uses the **sparse BESD format**, which only stores data for SNPs within 2 Mb of a probe, SNPs within 1 Mb of any trans-eQTL, and SNPs with $p < 10^{-5}$ elsewhere. This dramatically reduces file size compared to the dense format.

### Make a BESD file from eQTL summary data

SMR supports conversion from multiple formats:

!!! example "1. From ESD format (text-based eQTL summary data)"
    ```bash
    smr --eqtl-flist my.flist --make-besd --out mybesd
    ```
    The `.flist` file provides probe information and paths to individual `.esd` files:

    ```txt title="my.flist"
    Chr    ProbeID GeneticDistance ProbeBp Gene    Orientation PathOfEsd
    9    cg00000658  0   139997924   MAN1B1  -   path/my01.esd
    20    cg26036652  0   33735834    NA  NA  path/my02.esd
    ```

    Each `.esd` file contains:

    ```txt title="my01.esd"
    Chr    SNP Bp  A1  A2  Freq    Beta    se  p
    9    rs12349815  150048  T   A   0.968   0.019   0.016   0.2434
    20    rs141129176 62955484    G   A   0.89    0.012   0.009   0.2156
    ```

!!! example "2. From Matrix eQTL output"
    ```bash
    smr --eqtl-summary mateQTL.txt --matrix-eqtl-format --make-besd --out mybesd
    ```

!!! example "3. From FastQTL output"
    ```bash
    smr --eqtl-summary fastqtlnomi.txt --fastqtl-nominal-format --make-besd --out mybesd
    ```

!!! example "4. From QTLtools output"
    ```bash
    smr --eqtl-summary qtltoolsnomi.txt --qtltools-nominal-format --make-besd --out mybesd
    ```

!!! example "5. From PLINK, GEMMA, or BOLT-LMM output"
    ```bash
    # PLINK qassoc format
    smr --eqtl-flist my.flist --plink-qassoc-format --make-besd --out mybesd

    # GEMMA format
    smr --eqtl-flist my.flist --gemma-format --make-besd --out mybesd

    # BOLT-LMM format
    smr --eqtl-flist my.flist --bolt-assoc-format --make-besd --out mybesd
    ```

!!! example "6. Merge or convert existing BESD files"
    ```bash
    # Convert dense BESD to sparse BESD
    smr --beqtl-summary my_beqtl --make-besd --out my_sparse

    # Merge multiple BESD files
    smr --besd-flist my_file.list --make-besd --out my_merged
    ```

!!! tip "Customizing sparse BESD parameters"
    ```bash
    smr --eqtl-flist my.flist --make-besd \
        --cis-wind 2000 \
        --trans-wind 1000 \
        --peqtl-trans 5.0e-8 \
        --peqtl-other 1.0e-5 \
        --out mybesd
    ```

### Query eQTL results

Since the eQTL data are stored in binary format, SMR provides options to query subsets of the data.

!!! example "Query by SNP"
    ```bash
    # Single SNP
    smr --beqtl-summary myeqtl --query 5.0e-8 --snp rs123 --out myquery

    # All SNPs on a chromosome
    smr --beqtl-summary myeqtl --query 5.0e-8 --snp-chr 1 --out myquery

    # SNPs in a genomic region
    smr --beqtl-summary myeqtl --query 5.0e-8 --snp-chr 1 \
        --from-snp-kb 100 --to-snp-kb 200 --out myquery

    # SNPs in a window around a target SNP
    smr --beqtl-summary myeqtl --query 5.0e-8 --snp rs123 \
        --snp-wind 50 --out myquery
    ```

!!! example "Query by probe or gene"
    ```bash
    # Single probe
    smr --beqtl-summary myeqtl --query 5.0e-8 --probe cg123 --out myquery

    # By gene name
    smr --beqtl-summary myeqtl --query 5.0e-8 --gene BRCA1 --out myquery

    # All probes on a chromosome
    smr --beqtl-summary myeqtl --query 5.0e-8 --probe-chr 1 --out myquery
    ```

## SMR locus plot

SMR provides an R script to visualize results in a locus plot. First, generate the data file for plotting:

!!! example "Generate plot data"
    ```bash
    smr \
        --bfile mydata \
        --gwas-summary mygwas.ma \
        --beqtl-summary myeqtl \
        --out myplot \
        --plot \
        --probe ILMN_123 \
        --probe-wind 500 \
        --gene-list glist-hg19
    ```

- `--plot` generates a text file for plotting.
- `--probe` specifies the probe to plot.
- `--probe-wind` defines the window size (Kb) around the probe.
- `--gene-list` specifies a gene annotation file (available for hg18, hg19, and hg38).

!!! example "R commands for SMR locus plot"
    ```R
    source("plot_SMR.r")

    SMRData <- ReadSMRData("myplot.ILMN_123.txt")

    # Locus plot
    SMRLocusPlot(
      data = SMRData,
      smr_thresh = 8.4e-6,
      heidi_thresh = 0.05,
      plotWindow = 1000,
      max_anno_probe = 16
    )

    # Effect size plot (GWAS vs eQTL)
    SMREffectPlot(data = SMRData, trait_name = "BMI")
    ```

## SMR Portal

The [SMR Portal](https://yanglab.westlake.edu.cn/smr-portal/) is an online platform that allows users to explore SMR results without running the software locally (Guo et al. 2025 *Nature Methods*).

- **Pre-computed SMR results** for hundreds of complex traits integrated with large-scale xQTL datasets (eQTL, mQTL, sQTL, pQTL), allowing users to browse gene-trait associations directly.
- **Online SMR analysis** where users can upload their own GWAS summary statistics and run SMR against available xQTL databases through the web interface.
- **Interactive locus plots** for visualizing SMR and HEIDI results alongside GWAS signals, eQTL associations, and gene annotations in a genomic region.
- **Cross-omics integration** to explore how genetic variants affect multiple molecular layers (expression, methylation, splicing, protein levels) and their downstream effects on complex traits.

## Available xQTL data resources

Pre-compiled xQTL datasets in BESD format are available for download from the [SMR website](https://yanglab.westlake.edu.cn/software/smr/#DataResource):

### eQTL data

- BrainMeta v2 cis-eQTL (Qi et al. 2022) — brain cortex, n = 2,865, hg19, 2.6 GB
- Westra et al. (2013) — blood, n = 3,511, hg18/hg19, 10.3 MB
- CAGE (Lloyd-Jones et al. 2017) — blood, n = 2,765, hg19, 3.8 GB
- GTEx V8 cis-eQTL (2020) — 49 tissues, n = 73–670, hg19, 48 GB
- PsychENCODE (Wang et al. 2018) — prefrontal cortex, n = 1,387, hg19, 33–65 MB
- Geuvadis (Lappalainen et al. 2013) — lymphoblastoid cell lines, n = 373 EUR, hg19, 650.5 MB

### mQTL data

- Hatton et al. (2024) EAS — blood, n = 2,099, 2.5 GB
- Hatton et al. (2024) EUR — blood, n = 3,701, 3.7 GB
- McRae et al. (2018) — blood, n = 1,980, hg19, 7.5 GB
- Brain-mMeta (Qi et al. 2018) — brain, n ≈ 1,160, hg19, 893 MB

### sQTL data

- BrainMeta v2 cis-sQTL (Qi et al. 2022) — brain cortex, n = 2,865, hg19, 9.0 GB
- GTEx V8 cis-sQTL (2020) — 49 tissues, n = 73–670, hg19, 190 GB

!!! note "Lite versions"
    For many datasets, lite versions (containing only SNPs with $p < 10^{-5}$) are available, which are much smaller and sufficient for most SMR analyses.

## References

- Zhu Z, Zhang F, Hu H, et al. (2016) Integration of summary data from GWAS and eQTL studies predicts complex trait gene targets. *Nature Genetics*, 48:481-487. [doi:10.1038/ng.3538](https://doi.org/10.1038/ng.3538)

- Wu Y, Zeng J, Zhang F, et al. (2018) Integrative analysis of omics summary data reveals putative mechanisms underlying complex traits. *Nature Communications*, 9:918. [doi:10.1038/s41467-018-03371-0](https://doi.org/10.1038/s41467-018-03371-0)

- Qi T, Wu Y, Zeng J, et al. (2018) Identifying gene targets for brain-related traits using transcriptomic and methylomic data from blood. *Nature Communications*, 9:2282. [doi:10.1038/s41467-018-04558-1](https://doi.org/10.1038/s41467-018-04558-1)

- Guo Y, Xu T, Luo J, et al. (2025) SMR-Portal: an online platform for integrative analysis of GWAS and xQTL data to identify complex trait genes. *Nature Methods*, 22:220-222. [doi:10.1038/s41592-024-02530-4](https://doi.org/10.1038/s41592-024-02530-4)

- SMR software and documentation: [https://yanglab.westlake.edu.cn/software/smr/](https://yanglab.westlake.edu.cn/software/smr/)

- SMR Portal (online tool and database): [https://yanglab.westlake.edu.cn/smr-portal/](https://yanglab.westlake.edu.cn/smr-portal/)
