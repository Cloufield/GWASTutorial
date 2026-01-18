# GWAS Workflow Overview

This section provides a comprehensive overview of the complete GWAS workflow, from study design and sample collection to functional validation.

## Complete GWAS Workflow

The following diagram illustrates the full workflow of a genome-wide association study, from study design and sample collection through data generation, quality control, association testing, post-GWAS analysis, and functional validation.

!!! note "Study Design"
    - Study Type Selection (Case-control, Cohort, Population-based)
    - Sample Size Calculation & Power Analysis
    - Inclusion/Exclusion Criteria Definition
    - Phenotype Definition & Diagnostic Criteria
    - Covariate Strategy Planning
    - Ethical Approval & Protocol Development
    
    Planning the study design before data collection: selecting the appropriate study type based on research questions, calculating required sample sizes for adequate statistical power, defining clear inclusion and exclusion criteria, establishing standardized phenotype definitions and diagnostic criteria, planning covariate strategies, and obtaining ethical approval and developing study protocols.

<div style="text-align: center; font-size: 2em;">↓</div>

!!! note "Sample Collection"
    - Cohort Recruitment (Disease-oriented, Population-based, Case-control)
    - Informed Consent & Ethical Approval
    - Biological Sample Collection (DNA, Serum, etc.)
    - Clinical Information Collection (Phenotypes, Demographics)
    - Sample Storage & Management
    
    Recruiting participants, collecting biological samples (DNA, serum) and clinical information from patients or population cohorts. Example: [BioBank Japan (BBJ)](https://biobankjp.org/en/) collects samples from 270,000 patients across 51 diseases through cooperative medical institutions nationwide.

<div style="text-align: center; font-size: 2em;">↓</div>

!!! note "Sequencing / Genotyping (WGS, WES, SNP Arrays)"
    Determining genetic variants using whole genome sequencing (WGS), whole exome sequencing (WES), or genotyping arrays. SNP arrays are cost-effective for large-scale studies (500K-5M variants), while WGS provides complete genome coverage for rare variant discovery.

<div style="text-align: center; font-size: 2em;">↓</div>

!!! note "Raw Data Generation (FASTQ, BAM, VCF, Genotype Calls)"
    - Format Conversion (FASTQ, BAM, VCF, Genotype Calls)
    - Data Harmonization (Multi-platform, Multi-cohort Standardization)
    
    Converting sequencing reads or array data into standardized formats: FASTQ (raw reads), BAM (aligned sequences), VCF (variant calls), or genotype files (PLINK, BED/BIM/FAM formats) for downstream analysis. Harmonizing data across different platforms, arrays, or cohorts to ensure consistent variant calling, coordinate systems (GRCh37/GRCh38), and allele coding for multi-cohort or multi-platform studies.

<div style="text-align: center; font-size: 2em;">↓</div>

!!! note "Data Quality Control (QC)"
    - Sample QC (Missingness, Sex Check, Heterozygosity)
    - Variant QC (MAF, HWE, Call Rate)
    - Relatedness Check (Duplicate Detection, IBD)
    - Population Structure (PCA)
    
    Filtering low-quality samples and variants: removing samples with high missingness or sex mismatches, filtering variants by minor allele frequency (MAF) and Hardy-Weinberg equilibrium (HWE), detecting duplicates and related individuals, and assessing population structure using principal component analysis (PCA).

<div style="text-align: center; font-size: 2em;">↓</div>

!!! note "Pre-GWAS Processing"
    - Phasing (Haplotype Reconstruction)
    - Imputation (Infer Ungenotyped Variants)
    - Population Structure (PCA, Ancestry)
    - Covariate Preparation
    
    Preparing data for association testing: phasing haplotypes (determining parental chromosome origin), imputing ungenotyped variants using reference panels (1000 Genomes, TOPMed), correcting for population structure, and preparing covariates (age, sex, principal components).

<div style="text-align: center; font-size: 2em;">↓</div>

!!! note "Phenotype Preparation"
    - Phenotype QC (Outlier Detection, Range Validation)
    - Normalization/Transformation (INT, Log Transform, Z-score)
    - Covariate Adjustment (Age, Sex, Medication Effects)
    - Case/Control Definition (Binary Traits)
    - Missingness Handling
    
    Preparing phenotype data for association testing: performing quality control to detect outliers and validate ranges, applying appropriate transformations (rank-based inverse normal transformation for quantitative traits, log transforms for skewed data), adjusting for covariates and medication effects, defining cases and controls for binary traits, and handling missing phenotype data appropriately.

<div style="text-align: center; font-size: 2em;">↓</div>

!!! note "GWAS Association Testing"
    - Association Testing (Linear/Logistic Regression, LMM)
    - Multiple Testing Correction (Genome-wide Significance)
    - Summary Statistics (Effect Sizes, P-values)
    
    Testing associations between each genetic variant and the trait using linear regression (quantitative traits) or logistic regression (binary traits), with linear mixed models (LMM) to account for relatedness. Applying multiple testing correction (genome-wide significance threshold p < 5×10⁻⁸) and generating summary statistics (effect sizes, p-values).

<div style="text-align: center; font-size: 2em;">↓</div>

!!! note "Replication"
    - Independent Cohort Validation
    - Cross-population Replication
    - Effect Size Consistency
    - Directional Consistency Check
    
    Validating significant associations in independent cohorts or populations to confirm findings and reduce false positives. Replication studies test whether associations discovered in the discovery cohort can be reproduced in different samples, often with more stringent significance thresholds. Successful replication strengthens confidence in the association and its generalizability across populations.

<div style="text-align: center; font-size: 2em;">↓</div>

!!! note "Post-GWAS Analysis"
    - Variant Annotation (Functional Consequences)
    - Heritability Estimation (SNP Heritability)
    - Fine-mapping (Causal Variant Identification)
    - Gene/Pathway Analysis (MAGMA, Enrichment)
    - Colocalization (eQTL, pQTL Integration)
    - Polygenic Risk Scores (PRS Construction)
    - Mendelian Randomization (Causal Inference)
    - Meta-analysis (Multi-cohort Integration)
    - Genetic Correlation (Cross-trait Analysis)
    
    Interpreting GWAS results: annotating variants with functional consequences, estimating heritability, fine-mapping causal variants, analyzing gene and pathway enrichment, integrating with molecular QTL data (eQTL, pQTL), constructing polygenic risk scores, performing Mendelian randomization for causal inference, meta-analyzing across cohorts, and estimating genetic correlations between traits.

<div style="text-align: center; font-size: 2em;">↓</div>

!!! note "Functional Validation"
    - Functional Genomics (eQTL, CRISPR, Epigenomics)
    - Cell Culture Models (In Vitro Validation)
    - Animal Models (In Vivo Studies)
    - Drug Target Validation (Therapeutic Development)
    
    Experimental validation of GWAS findings: functional genomics studies (eQTL analysis, CRISPR editing, epigenomic profiling), in vitro validation using cell culture models, in vivo studies using animal models, and drug target validation for therapeutic development.

## Key Considerations

!!! tip "Iterative Process"
    The GWAS workflow is often iterative. Findings from post-GWAS analysis may inform additional QC steps, re-analysis with different models, or collection of additional data (e.g., multi-omics data).

!!! warning "Quality is Critical"
    Rigorous QC at each stage is essential. Poor quality data or inadequate QC can lead to false associations, reduced power, and incorrect biological interpretations.

!!! info "Integration is Key"
    Modern GWAS increasingly integrates multiple data types (genomics, transcriptomics, proteomics, epigenomics) and leverages large-scale biobanks and consortia for increased power and generalizability.