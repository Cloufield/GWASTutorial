

# Whole-genome regression : REGENIE

## Concepts

### Overview

!!! quote "Overview of REGENIE"
    REGENIE is a computationally efficient C++ program for whole-genome regression modeling of large genome-wide association studies. It is designed to handle quantitative and binary traits, including binary traits with unbalanced case-control ratios. REGENIE can process multiple phenotypes efficiently, handle population structure and relatedness, and perform various gene/region-based tests. The method uses a two-step approach: Step 1 fits a whole-genome regression model to capture polygenic effects, and Step 2 performs single-variant association tests using predictions from Step 1 to adjust for polygenic background.
    
    Reference: https://rgcgithub.github.io/regenie/overview/

### Whole genome model

REGENIE uses a whole-genome regression approach to model polygenic effects across the entire genome. In **Step 1**, the method:

1. **Partitions the genome into blocks**: The genome is divided into blocks of SNPs (specified by `--bsize`, e.g., 1000 SNPs per block).

!!! example "Genome partitioning example"
    Suppose you have 500,000 SNPs across 22 autosomes. With `--bsize 1000`:

    - Block 1: SNPs 1-1000
    - Block 2: SNPs 1001-2000
    - Block 3: SNPs 2001-3000
    - ... (500 blocks total)
    
    Each block is processed independently in Level 0 regression.

2. **Level 0 regression**: Within each block, ridge regression is performed with multiple shrinkage parameters to create block-level predictors. This captures local polygenic effects within each genomic region.

!!! example "Level 0 regression example"
    For Block 1 (SNPs 1-1000):

    - Fit ridge regression: $y = X_1\beta_1 + X_2\beta_2 + ... + X_{1000}\beta_{1000} + \epsilon$ with shrinkage parameter $\lambda_1$
    - Fit ridge regression with different shrinkage parameter $\lambda_2$
    - ... (repeat for multiple $\lambda$ values, e.g., 5-10 different values)
    - Each combination produces a block-level predictor $P_{1,\lambda}$ for each sample
    
    This creates multiple predictors per block (one for each shrinkage parameter).

3. **Level 1 regression**: The block-level predictors are combined using ridge regression (for quantitative traits) or logistic ridge regression (for binary traits) with cross-validation to select optimal shrinkage parameters. This creates genome-wide polygenic predictions.

!!! example "Level 1 regression example"
    After Level 0, you have predictors from all blocks:

    - $P_{1,\lambda_1}, P_{1,\lambda_2}, ..., P_{1,\lambda_k}$ from Block 1
    - $P_{2,\lambda_1}, P_{2,\lambda_2}, ..., P_{2,\lambda_k}$ from Block 2
    - ... (predictors from all 500 blocks)
    
    Level 1 combines these:
    - For quantitative traits: $y = \alpha_1 P_{1,\lambda_1} + \alpha_2 P_{1,\lambda_2} + ... + \alpha_n P_{500,\lambda_k} + \epsilon$
    - Cross-validation selects the optimal combination and shrinkage
    - Produces final genome-wide polygenic score for each sample

4. **LOCO (Leave-One-Chromosome-Out) predictions**: For each chromosome, predictions are generated using all other chromosomes, which helps avoid overfitting when testing variants in Step 2.

!!! example "LOCO predictions example"
    When testing variants on chromosome 1 in Step 2:

    - Use predictions built from chromosomes 2, 3, 4, ..., 22
    - Exclude all variants from chromosome 1 when building the polygenic score
    
    When testing variants on chromosome 2:
    - Use predictions built from chromosomes 1, 3, 4, ..., 22
    - Exclude all variants from chromosome 2
    
    This ensures that when testing a variant, the polygenic adjustment doesn't include that variant's chromosome, preventing overfitting and inflated test statistics.

!!! info "Why whole-genome regression?"
    Traditional GWAS methods test each variant independently, which can lead to false positives due to population structure and cryptic relatedness. By first fitting a whole-genome model that captures **polygenic background effects**, REGENIE can better control for these confounders and improve the accuracy of association tests.

### Comparison: Linear Mixed Models vs. Whole Genome Regression

Both Linear Mixed Models (LMM) and Whole Genome Regression (WGR) are methods designed to account for polygenic background effects in GWAS, but they differ in their modeling approaches.

!!! info "Theoretical connection"
    REGENIE's whole-genome regression model has close ties to a linear mixed model (LMM) based on an infinitesimal model. In the LMM, polygenic effects are integrated out so the model only involves the Genetic Relatedness Matrix (GRM) $K$ through a variance component in the covariance matrix. In REGENIE, polygenic effects are **directly estimated** using ridge regression (linear regression with L2 penalty), which bypasses the need for a GRM and uses the polygenic effect estimates to control for population structure when testing variants.

| Aspect | Linear Mixed Models (LMM) | Whole Genome Regression (WGR) |
|--------|---------------------------|------------------------------|
| **Model formulation** | $y = X\beta + Wu + e$ where $u \sim N(0, \sigma^2_g I)$<br>$Var(y) = A\sigma^2_g + I\sigma^2_e$ where $A = WW'/N$ (GRM) | $y = X\beta + W\beta + e$ with L2 penalty<br>Directly estimates polygenic effects via ridge regression |
| **Genetic Relatedness Matrix (GRM)** | **Required**: Must compute and store $N \times N$ GRM matrix | **Not required**: Bypasses GRM by directly estimating polygenic effects |
| **Handling relatedness** | Explicitly models genetic relationships via GRM | Implicitly accounts for relatedness through polygenic predictions |
    
    Reference: https://rgcgithub.github.io/regenie/faq/

### Stacked regressions

The "stacked" regression approach refers to the two-level (Level 0 and Level 1) regression framework used in REGENIE Step 1:

- **Level 0**: Multiple ridge regression models are fit within each genomic block with different shrinkage parameters. This creates a set of block-level predictors.

- **Level 1**: These block-level predictors are then combined using another ridge regression model to create final genome-wide predictions.

!!! example "Stacked regression workflow"
    **Step 1 - Level 0 (within each block):**
    ```
    Block 1 (1000 SNPs) → Ridge regression (λ=0.1) → Predictor P₁₀.₁
                        → Ridge regression (λ=0.5) → Predictor P₁₀.₅
                        → Ridge regression (λ=1.0) → Predictor P₁₁.₀
                        → ... (5-10 predictors per block)
    
    Block 2 (1000 SNPs) → Similar process → Predictors P₂₀.₁, P₂₀.₅, P₂₁.₀, ...
    
    ... (repeat for all blocks)
    ```
    
    **Step 2 - Level 1 (combine all block predictors):**
    ```
    All predictors from Level 0 → Ridge regression → Final polygenic score
    
    For sample i: Score_i = α₁P₁₀.₁ + α₂P₁₀.₅ + ... + αₙP₅₀₀₁.₀
    ```
    
    This two-stage approach is computationally efficient because:
    - Level 0: Each block is processed independently (can be parallelized)
    - Level 1: Only combines ~500-5000 predictors (one per block × shrinkage parameter) instead of 500,000 SNPs directly

This stacking approach allows REGENIE to:
- Capture both local (within-block) and global (across-block) polygenic effects
- Handle the high-dimensional nature of genome-wide data efficiently
- Reduce computational burden compared to fitting a single genome-wide model with all variants

!!! note "Memory efficiency"
    The `--lowmem` option in Step 1 writes Level 0 predictions to disk, allowing REGENIE to process very large datasets without excessive memory usage.

### Firth correction

For binary traits, especially those with unbalanced case-control ratios or when testing rare variants, standard logistic regression can produce biased effect estimates and inflated test statistics. **Firth correction** is a penalized likelihood method that addresses this issue.

In REGENIE Step 2, Firth correction can be applied using the `--firth` flag:

- **`--firth`**: Enables Firth logistic regression for variants with p-values below a threshold
- **`--approx`**: Uses approximate Firth correction for faster computation
- **`--pThresh`**: Sets the p-value threshold (e.g., 0.01) below which Firth correction is applied

!!! info "When to use Firth correction?"
    Firth correction is particularly important for:
    - Binary traits with highly unbalanced case-control ratios (e.g., 1:10 or more extreme)
    - Rare variants (MAF < 0.01) where standard logistic regression may fail
    - Small sample sizes where maximum likelihood estimates may be biased
    
    The correction adds a penalty term to the likelihood function, which prevents the estimates from becoming infinite and produces more reliable p-values.

## Tutorial

### Installation

Please check [here](https://rgcgithub.github.io/regenie/install/)

### Step1

In Step 1, REGENIE fits a whole-genome regression model to capture polygenic background effects. This step:
- Uses a subset of variants (typically LD-pruned variants) to reduce computational burden
- Creates LOCO (Leave-One-Chromosome-Out) predictions for each chromosome
- Generates prediction files that will be used in Step 2 to adjust for polygenic effects

!!! example "Sample codes for running step 1"
    ```
    plinkFile=../01_Dataset/1KG.EAS.auto.snp.norm.nodup.split.rare002.common015.missing
    phenoFile=../01_Dataset/1kgeas_binary_regenie.txt
    covarFile=../05_PCA/plink_results_projected.sscore
    covarList="PC1_AVG,PC2_AVG,PC3_AVG,PC4_AVG,PC5_AVG,PC6_AVG,PC7_AVG,PC8_AVG,PC9_AVG,PC10_AVG"
    extract=../05_PCA/plink_results.prune.in
    
    # revise the header of covariate file
    sed -i 's/#FID/FID/' ../05_PCA/plink_results_projected.sscore
    mkdir tmpdir
    
    regenie \
      --step 1 \
      --bed ${plinkFile} \
      --extract ${extract} \
      --phenoFile ${phenoFile} \
      --covarFile ${covarFile} \
      --covarColList ${covarList} \
      --bt \
      --bsize 1000 \
      --lowmem \
      --lowmem-prefix tmpdir/regenie_tmp_preds \
      --out 1kg_eas_step1_BT
    ```


### Step2

In Step 2, REGENIE performs single-variant association tests while adjusting for polygenic background using the predictions from Step 1. This step:
- Tests each variant across the genome for association with the phenotype
- Uses LOCO predictions to avoid overfitting (when testing variants on chromosome X, predictions exclude chromosome X)
- For binary traits, can apply Firth correction for rare variants or unbalanced case-control ratios

!!! info "Key parameters in Step 2"

    - `--pred`: Points to the prediction file list generated in Step 1 (e.g., `*_pred.list`)
    - `--firth --approx --pThresh 0.01`: Applies Firth correction to variants with p < 0.01
    - `--bsize 400`: Block size for processing (can be different from Step 1)
    - `--ref-first`: Uses the first allele in the genotype file as the reference allele

!!! example "Sample codes for running step 2"
    ```
    plinkFile=../01_Dataset/1KG.EAS.auto.snp.norm.nodup.split.rare002.common015.missing
    phenoFile=../01_Dataset/1kgeas_binary_regenie.txt
    covarFile=../05_PCA/plink_results_projected.sscore
    covarList="PC1_AVG,PC2_AVG,PC3_AVG,PC4_AVG,PC5_AVG,PC6_AVG,PC7_AVG,PC8_AVG,PC9_AVG,PC10_AVG"
    extract=../05_PCA/plink_results.prune.in
    
    sed -i 's/#FID/FID/' ../05_PCA/plink_results_projected.sscore
    mkdir tmpdir
    
    regenie \
      --step 2 \
      --bed ${plinkFile} \
      --ref-first \
      --phenoFile ${phenoFile} \
      --covarFile ${covarFile} \
      --covarColList ${covarList} \
      --bt \
      --bsize 400 \
      --firth --approx --pThresh 0.01 \
      --pred 1kg_eas_step1_BT_pred.list \
      --out 1kg_eas_step1_BT
    ```


After running REGENIE Step 2, you will obtain summary statistics files (typically with `.regenie` extension) containing association test results. These results can be visualized using standard GWAS visualization tools.

!!! info "REGENIE output format"
    The Step 2 output file contains columns such as:
    
    - `CHROM`: Chromosome
    - `GENPOS`: Genomic position
    - `ID`: Variant ID
    - `A1`: Effect allele
    - `A2`: Reference allele
    - `A1FREQ`: Effect allele frequency
    - `N`: Sample size
    - `TEST`: Test type (e.g., ADD for additive model)
    - `BETA`: Effect size estimate
    - `SE`: Standard error
    - `CHISQ`: Chi-square test statistic
    - `LOG10P`: -log10(p-value)
    - `P`: P-value
    - Additional columns for Firth correction if used (e.g., `EXTRA`)

## Other Applications

Beyond single-variant association testing, REGENIE supports several advanced analyses that extend its functionality:

### Gene-based and region-based tests

REGENIE can perform gene/region-based association tests that aggregate information across multiple variants within a gene or genomic region. This is particularly useful for detecting associations with rare variants that may have weak individual effects but collectively contribute to disease risk.

**Available tests:**
- **Burden tests**: Aggregate variants into a single burden score (e.g., count of rare alleles)
- **SKAT/SKATO**: Sequence Kernel Association Test (SKAT) and its optimal version (SKATO) that combines burden and variance-component tests
- **ACATV/ACATO**: Aggregated Cauchy Association Test for variants (ACATV) and optimal version (ACATO)
- **SBAT**: Step-up Burden Association Test

!!! info "Gene-based testing workflow"
    Gene-based tests in REGENIE require:
    1. Annotation files defining gene boundaries and variant annotations
    2. Mask definitions specifying which variants to include (e.g., by functional annotation, MAF threshold)
    3. Running Step 2 with `--anno-file`, `--set-list`, and test-specific options (e.g., `--burden`, `--skat`, `--acat`)
    
    Reference: https://rgcgithub.github.io/regenie/options/#gene-based-testing

### Interaction testing

REGENIE supports testing for gene-environment (G×E) and gene-gene (G×G) interactions, which can reveal context-dependent genetic effects.

- **G×E interactions**: Test whether genetic effects vary across environmental exposures (e.g., BMI, smoking status)
- **G×G interactions**: Test for epistatic effects between pairs of genetic variants

!!! example "G×E interaction example"
    ```bash
    regenie \
      --step 2 \
      --bed ${plinkFile} \
      --phenoFile ${phenoFile} \
      --covarFile ${covarFile} \
      --interaction BMI \
      --pred step1_pred.list \
      --out gxe_results
    ```
    
    This tests whether genetic effects differ across BMI categories.

### Conditional analyses

Starting from REGENIE v3.0, you can perform conditional analyses by specifying variants to include as covariates. This is useful for:
- Identifying independent signals at a locus
- Fine-mapping by conditioning on known associations
- Testing for secondary signals after accounting for the primary association

!!! info "Conditional analysis"
    Use `--condition-list` to specify variants to condition on. REGENIE will automatically exclude these variants from the analysis and include them as covariates in the association model.
    
    Reference: https://rgcgithub.github.io/regenie/options/#conditional-analyses

### Survival/time-to-event analyses

Starting from REGENIE v4.0, survival analysis for time-to-event data is supported using Cox proportional hazards models. This is useful for:
- Disease onset time
- Time to treatment response
- Other time-to-event phenotypes

!!! example "Survival analysis example"
    ```bash
    regenie \
      --step 2 \
      --bed ${plinkFile} \
      --t2e \
      --phenoColList Time \
      --eventColList Event \
      --pred step1_pred.list \
      --out survival_results
    ```
    
    The phenotype file should contain time-to-event and event indicator columns (0=no event, 1=event, NA=missing).


For detailed documentation on all REGENIE features and options, see: https://rgcgithub.github.io/regenie/options/

## References
- Mbatchou, J., Barnard, L., Backman, J., Marcketta, A., Kosmicki, J. A., Ziyatdinov, A., ... & Marchini, J. (2021). Computationally efficient whole-genome regression for quantitative and binary traits. Nature genetics, 53(7), 1097-1103.

