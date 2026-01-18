# Introduction

Welcome to the GWAS Tutorial! This introduction provides essential background knowledge for understanding genome-wide association studies (GWAS) and complex trait genomics.

---

## What is Statistical Genetics

Statistical genetics is a field that combines **genetics**, **statistics**, and computational methods to understand how **genetic variation** contributes to **phenotypic variation** in populations. It bridges the gap between molecular genetics and **population genetics**, using statistical models to:

- Identify **genetic variants** associated with **traits**
- Estimate the contribution of **genetic factors** to **trait variation** (**heritability**)
- Understand the **genetic architecture** of **complex traits**
- Predict disease risk based on **genetic information**

!!! info "Key concepts in statistical genetics"

    - **Genetic variation**: Differences in DNA sequences among individuals
    - **Phenotype**: Observable characteristics or **traits** (e.g., height, disease status)
    - **Genotype**: The **genetic constitution** of an individual at specific **loci**
    - **Allele frequency**: The proportion of a particular **allele** in a **population**
    - **Linkage disequilibrium (LD)**: Non-random association of **alleles** at different **loci**

---

## Key questions and essential components 

In GWAS and statistical genetics, we seek to answer fundamental questions about how **genetic variation** contributes to **phenotypic variation**. For example:

- Which **genetic variants** are associated with increased risk of type 2 diabetes?
- How much of the variation in height is explained by **genetic factors**?
- Are there **genetic variants** that influence both blood pressure and cardiovascular disease risk?
- Which genes and pathways are involved in the development of autoimmune diseases?
- Can we predict an individual's disease risk based on their **genetic profile**?
- How do **genetic variants** affect gene expression and protein levels?
- What is the causal relationship between cholesterol levels and heart disease? 

To address these questions, we need to understand several key components:

- **What genetic variants exist?** Understanding the types and characteristics of **genetic variation** in human **genomes** (see [Sequencing and Human Genomes](#sequencing-and-human-genomes))
- **What traits can we study?** Recognizing the distinction between **Mendelian** and **complex traits**, and identifying suitable **phenotypes** for GWAS (see [Mendelian traits and Complex Traits](#mendelian-traits-and-complex-traits))
- **Who should we study?** Designing appropriate **cohorts** with sufficient **sample sizes** and proper study designs (see [Cohort](#cohort))
- **How do we find associations?** Conducting **genome-wide association studies** to systematically identify **genetic variants** associated with **traits** (see [Genome-Wide Association Study (GWAS)](#genome-wide-association-study-gwas))

Together, these components form the foundation for discovering and understanding the genetic basis of complex traits and diseases.

---

## Sequencing and Human Genomes

The human **genome** consists of approximately **3 billion base** pairs of DNA, organized into 23 pairs of **chromosomes**. Modern **sequencing technologies** have enabled comprehensive characterization of **genetic variation** across the **genome**.

### Sequencing technologies

**Sequencing technologies** are methods used to determine the order of nucleotides (A, T, G, C) in DNA. Different technologies have been developed over time, each with specific advantages for GWAS applications:

| Technology | Description | Key Features | Common Use in GWAS | Advantages | Limitations |
|------------|-------------|--------------|-------------------|------------|-------------|
| **Array-based genotyping** | SNP arrays (e.g., Illumina, Affymetrix) | Hundreds of thousands to millions of variants | Standard GWAS genotyping | High throughput, cost-effective, well-validated | Imputation required for genome-wide coverage |
| **Whole Genome Sequencing (WGS)** | Complete sequencing of entire genome | Reads all ~3 billion base pairs | Discovery of rare variants, fine-mapping | Comprehensive, discovers all variant types | Expensive, requires more computational resources |
| **Whole Exome Sequencing (WES)** | Sequencing of protein-coding regions only | ~1-2% of genome (exons) | Rare variant discovery in coding regions | More affordable than WGS, focuses on functional regions | Misses non-coding variants, regulatory regions |
| **Long-read sequencing** | Sequencing technologies producing long reads (PacBio, Oxford Nanopore) | Reads of thousands to tens of thousands of base pairs | Structural variant detection, complex regions, haplotype phasing | Better resolution of complex regions, structural variants, phasing | Higher error rates, more expensive, lower throughput |

!!! info "Genotyping vs. Sequencing"
    - **Genotyping**: Measures specific known variants (typically SNPs) using arrays or targeted methods. Most GWAS use genotyping arrays followed by **imputation** to infer untyped variants.
    - **Sequencing**: Determines the complete DNA sequence, enabling discovery of novel variants. More expensive but provides comprehensive variant discovery.

!!! tip "Imputation in GWAS"
    Most GWAS use **genotyping arrays** that measure 500K-5M variants, then use **imputation** to infer millions of additional variants based on **linkage disequilibrium (LD)** patterns from reference panels (e.g., 1000 Genomes Project, TOPMed). This approach balances cost and genome-wide coverage.

### Types of genetic variants

**Genetic variants** are differences in DNA sequence between individuals. The main types are summarized in the table below:

| Variant Type | Definition | Size | Frequency | Example | Relevance to GWAS |
|--------------|-----------|------|-----------|---------|-------------------|
| **SNPs** (Single Nucleotide Polymorphisms) | Single base pair changes | 1 bp | Most common (millions in genome) | A→G substitution | Primary focus of most GWAS studies |
| **Indels** (Insertions/Deletions) | Small insertions or deletions | 1-50 bp | Common but less than SNPs | Insertion: "AT", Deletion: "CG" | Challenging to genotype accurately |
| **CNVs** (Copy Number Variants) | Duplications or deletions of DNA segments | >50 bp | Less common | Duplication/deletion of gene | Require specialized genotyping |
| **Inversions** | Reversal of DNA segment orientation | >50 bp | Rare | Chromosomal inversion | Require specialized genotyping |
| **Translocations** | Movement of DNA segments between chromosomes | Variable | Rare | Chromosomal translocation | Rarely studied in GWAS |
| **STRs/Microsatellites** | Repetitive sequences (2-6 bp) repeated multiple times | Variable | Common | (CA)ₙ repeats | Less commonly studied but important |


---

## Mendelian traits and Complex Traits

Understanding the distinction between **Mendelian traits** and **complex traits** is fundamental to GWAS.

### Mendelian vs. Complex traits

Understanding the distinction between **Mendelian traits** and **complex traits** is fundamental to GWAS:

| Characteristic | Mendelian Traits | Complex Traits |
|----------------|------------------|----------------|
| **Alternative name** | Monogenic traits | Polygenic traits |
| **Number of genes** | One or a few genes | Hundreds to thousands of variants |
| **Effect size** | Large (often necessary and sufficient) | Small to moderate per variant |
| **Inheritance pattern** | Clear (dominant, recessive, X-linked) | No clear pattern |
| **Environmental factors** | Minimal role | Important role |
| **Population frequency** | Rare (typically <1%) | Common |
| **Examples** | Cystic fibrosis, Huntington's disease, Sickle cell anemia | Height, BMI, type 2 diabetes, schizophrenia, blood pressure, depression, anxiety, ADHD, autism spectrum disorder, educational attainment, cognitive ability, personality traits, substance use disorders, sleep patterns, eating behaviors, risk-taking behaviors |
| **Suitable for GWAS** | Less suitable (large effects, rare) | Highly suitable (many small effects) |

!!! tip "The polygenic nature of complex traits"
    Most human traits and diseases are complex traits. Even diseases with known Mendelian forms (e.g., breast cancer) often have complex forms influenced by many genetic and environmental factors.

### Types of traits suitable for GWAS

GWAS is most effective for complex traits. The following trait types are commonly studied:

#### Traditional phenotypic traits

| Trait Type | Definition | Analysis Method | Examples | Advantages |
|------------|-----------|-----------------|----------|------------|
| **Quantitative** | Continuous measurements | Linear regression | Height, BMI, blood pressure, lipid levels, educational attainment, cognitive test scores, personality trait scores, sleep duration | More statistical power, can detect smaller effects |
| **Binary** (Case-control) | Dichotomous outcomes | Logistic regression | Type 2 diabetes, coronary artery disease, autoimmune diseases, depression, anxiety disorders, ADHD, autism spectrum disorder, substance use disorders | Clinically relevant, easier to collect |
| **Ordinal** | Categorical with ordered categories | Ordinal regression | Disease severity stages, pain scales | Captures ordered relationships |
| **Time-to-event** (Survival) | Time until an event occurs | Cox proportional hazards | Age at disease onset, survival time | Accounts for censoring |

#### Molecular QTL traits

| QTL Type | Abbreviation | Definition | Measurement | Analysis Method | Key Features |
|----------|--------------|-----------|-------------|-----------------|-------------|
| **Expression QTL** | eQTL | Gene expression levels (mRNA) | RNA-seq, microarrays | Linear regression | cis-eQTL (near gene) vs. trans-eQTL (distant) |
| **Protein QTL** | pQTL | Protein abundance levels | Mass spectrometry, aptamer arrays | Linear regression | More direct functional readout than eQTL |
| **Metabolite QTL** | mQTL | Metabolite concentrations | Mass spectrometry, NMR | Linear regression | Captures downstream metabolic effects |
| **Single-cell eQTL** | sc-eQTL | Gene expression in individual cells | Single-cell RNA-seq | Specialized models (accounting for cell types) | Cell-type-specific effects, context-dependent |
| **Splicing QTL** | sQTL | Alternative splicing patterns | RNA-seq | Linear regression | Variants affecting isoform usage |
| **Methylation QTL** | meQTL | DNA methylation levels | Bisulfite sequencing, arrays | Linear regression | Epigenetic regulation |
| **Histone QTL** | hQTL | Histone modification levels | ChIP-seq | Linear regression | Chromatin state regulation |
| **Accessibility QTL** | aQTL | Chromatin accessibility | ATAC-seq | Linear regression | Regulatory element activity |
| **Chromatin interaction QTL** | caQTL | 3D chromatin structure | Hi-C, ChIA-PET | Specialized models | Long-range regulatory interactions |

!!! warning "Considerations for trait selection"
    - **Sample size**: Larger **sample sizes** provide more **power** to detect **associations**
    - **Trait heritability**: Higher **heritability** **traits** are more likely to yield significant findings
    - **Phenotype quality**: Accurate and consistent **phenotype** measurement is crucial
    - **Population homogeneity**: More homogeneous **populations** may have higher **power**

---

## Cohort

A **cohort** in GWAS refers to a group of individuals who are studied together, typically sharing **genetic data** and **phenotypic measurements**. The choice and design of **cohorts** are fundamental to the success of GWAS, as they determine the **statistical power**, **generalizability**, and validity of findings.

#### Types of study designs

GWAS can be conducted using different cohort designs, each with specific advantages and considerations:

| Study Design | Description | Advantages | Limitations | Examples |
|--------------|-------------|------------|-------------|----------|
| **Population-based cohort** | Random or representative sample from a population | Generalizable, can study multiple traits, longitudinal follow-up possible | May have lower case numbers for rare diseases | UK Biobank, FinnGen, Estonian Biobank |
| **Case-control** | Cases (with disease) and controls (without disease) matched on key characteristics | Efficient for rare diseases, high power for binary traits | Potential for selection bias, limited to one trait | Disease-specific case-control studies |
| **Family-based** | Related individuals (families, trios, siblings) | Controls for population structure, can detect rare variants | Lower power, more complex analysis, recruitment challenges | Family-based association studies |
| **Multi-ethnic/Multi-ancestry** | Diverse populations from different genetic ancestries | Improved generalizability, better fine-mapping, discovery of ancestry-specific effects | Population stratification concerns, requires careful analysis | PAGE, TOPMed, All of Us |

#### Major cohorts in GWAS

Several large-scale cohorts have been instrumental in advancing GWAS research:

| Cohort | Sample Size | Population | Key Features |
|--------|-------------|------------|--------------|
| **UK Biobank** | ~500,000 | British | Comprehensive phenotyping, longitudinal follow-up, imaging, multi-omics |
| **FinnGen** | ~500,000 | Finnish | Population isolate, extensive health registry data, high-quality phenotypes |
| **23andMe** | Millions | Multi-ancestry | Consumer genetics, self-reported phenotypes, large sample sizes |
| **TOPMed** | ~100,000+ | Multi-ancestry | Whole genome sequencing, diverse populations, deep phenotyping |
| **All of Us** | 1M+ (target) | Multi-ancestry | Diverse US population, comprehensive health data, precision medicine focus |
| **Estonian Biobank** | ~200,000 | Estonian | Population-based, extensive health records, longitudinal data |
| **deCODE** | ~300,000 | Icelandic | Population isolate, extensive genealogical records, high-quality data |

!!! success "Meta-analysis and consortium studies"
    Many GWAS combine data from multiple cohorts through meta-analysis or consortium efforts, which:
    - Increase statistical power by pooling samples
    - Enable replication across independent cohorts
    - Improve generalizability across populations
    - Require careful harmonization of phenotypes and genotypes

---

## Genome-Wide Association Study (GWAS)

A **Genome-Wide Association Study (GWAS)** is a research approach that investigates the association between **genetic variants** (typically **SNPs**) and **traits** across the entire **genome**. GWAS represents a powerful hypothesis-free method for discovering genetic factors that contribute to complex traits and diseases. Unlike candidate gene studies that focus on specific genes, GWAS systematically scans the entire genome without prior assumptions about which variants might be important.

### Description of GWAS

GWAS is a **population-based** study design that examines **genetic variation** across the genome to identify **loci** (genomic regions) associated with **phenotypes** of interest. The fundamental principle is to compare the **allele frequencies** of **genetic variants** between individuals with different **phenotypic** values (e.g., cases vs. controls, or high vs. low trait values). 

Key characteristics of GWAS:

- **Hypothesis-free discovery**: Unlike candidate gene studies, GWAS does not require prior knowledge about which genes or pathways are involved
- **Genome-wide coverage**: Tests millions of **genetic variants** simultaneously across all chromosomes
- **Population-based**: Typically studies unrelated individuals from a population rather than families
- **Statistical association**: Identifies correlations between **genotypes** and **phenotypes**, not necessarily causal relationships
- **Polygenic architecture**: Most complex traits are influenced by many variants with small individual effects

The typical GWAS workflow involves:
1. **Genotyping** or **sequencing** a large number of individuals to obtain **genotype** data
2. Measuring **phenotypes** (traits) of interest in the same individuals
3. Performing **association testing** between each **genetic variant** and the **phenotype**
4. Applying **multiple testing correction** to account for the millions of tests performed
5. Identifying **genome-wide significant** associations that pass stringent significance thresholds
6. Replicating findings in independent **cohorts** to validate associations

### What GWAS does

GWAS systematically tests millions of **genetic variants** to identify those associated with a **trait** of interest. The basic approach is:

1. **Genotype individuals**: Measure **genetic variants** across the **genome**
2. **Measure phenotypes**: Collect **trait** data for the same individuals
3. **Test associations**: For each **variant**, test if **genotype** is associated with **phenotype**
4. **Identify significant associations**: **Variants** that pass **significance thresholds** are considered associated with the **trait**

!!! info "The GWAS workflow"
    ```
    Genotype Data + Phenotype Data
           ↓
    Association Testing (millions of tests)
           ↓
    Summary Statistics (effect sizes, p-values)
           ↓
    Significance Filtering (e.g., p < 5×10⁻⁸)
           ↓
    Associated Variants
    ```

### Key concepts in GWAS

| Concept | Description | Details |
|---------|-------------|---------|
| **Effect size** | Magnitude of **association** between **variant** and **trait** | **Quantitative traits**: beta (β) or change per **allele**<br>**Binary traits**: **odds ratio (OR)** or relative risk<br>Small effects common (e.g., 0.1-0.5 cm height change per **allele**) |
| **P-value** | Probability of observing **association** by chance alone | Lower **p-value** = stronger evidence against null hypothesis |
| **Genome-wide significance** | Standard **threshold** accounting for **multiple testing** | Typically **p < 5×10⁻⁸** (~1 million independent tests) |
| **Multiple testing correction** | Methods to control **false positives** | **Bonferroni**: Divide **threshold** by number of tests<br>**FDR**: Controls proportion of **false positives**<br>**Permutation**: Empirical **threshold** establishment |

!!! tip "What GWAS can and cannot tell us"
    **What GWAS can do:**
    - Identify **genetic variants** associated with **traits**
    - Estimate **effect sizes** of **associations**
    - Discover novel **biological pathways**
    - Enable **polygenic risk prediction**
    - Provide targets for drug development
    
    **What GWAS cannot do:**
    - Establish **causality** (correlation ≠ causation)
    - Identify the **causal variant** when multiple **variants** are in **LD**
    - Explain the **biological mechanism** (requires functional studies)
    - Account for all **genetic contribution** (**missing heritability**)

### Applications of GWAS

GWAS has revolutionized our understanding of complex traits, but it is important to recognize that **GWAS is not the end goal**—it is a starting point for discovery. The associations identified by GWAS require **post-GWAS analysis** and **functional experiments** to translate statistical associations into biological insights and clinical applications.

| Application Area | GWAS Role | Post-GWAS Analysis Needed | Examples |
|------------------|-----------|---------------------------|----------|
| **Disease genetics** | Identifies genetic risk factors for common diseases | Fine-mapping causal variants, functional validation, pathway analysis | Type 2 diabetes, coronary artery disease, autoimmune diseases |
| **Drug discovery** | Suggests potential drug targets based on genetic associations | Target validation, mechanism studies, clinical trials | PCSK9 inhibitors for cholesterol, IL-23 pathway for autoimmune diseases |
| **Personalized medicine** | Provides variants for polygenic risk scores | Validation in diverse populations, clinical utility studies | PRS for cardiovascular disease, cancer risk prediction |
| **Biological insights** | Identifies associated genomic regions | Functional genomics (eQTL, CRISPR), mechanistic studies, pathway enrichment | Novel pathways, gene function, regulatory networks |
| **Causal inference** | Provides genetic instruments for causal inference | **Mendelian Randomization (MR)**, colocalization analysis, causal variant identification | Establishing causal relationships between exposures and outcomes (e.g., cholesterol → heart disease) |
| **Population genetics** | Reveals population structure and selection patterns | Evolutionary analysis, demographic modeling, comparative genomics | Population structure, selection signatures, migration patterns |

---

## Skills you may need

To successfully conduct and interpret GWAS, you will benefit from knowledge and skills in several areas:

| Skill Category | Key Topics | Importance | Tutorial Sections |
|----------------|------------|------------|-------------------|
| **Biology & Medicine** | Molecular biology, genetics, genomics, disease biology, functional genomics | Essential for understanding biological context | Throughout tutorial |
| **Statistics** | Regression analysis, hypothesis testing, multiple testing correction, population genetics, heritability, meta-analysis | Core to GWAS methodology | Throughout tutorial |
| **Programming** | Command line (Linux/Unix), Python, R, Bash, data manipulation, version control (Git) | Essential for data analysis | [Section 02](https://cloufield.github.io/GWASTutorial/02_Linux_basics/), [70](https://cloufield.github.io/GWASTutorial/70_python_basics/), [75](https://cloufield.github.io/GWASTutorial/75_R_basics/) |

### Detailed skill breakdown

#### Biology and Medicine

| Topic | Description | Examples |
|-------|-------------|----------|
| **Molecular biology** | DNA structure, transcription, translation, gene regulation | Understanding how variants affect gene function |
| **Genetics** | Mendelian inheritance, genetic variation, inheritance patterns | Understanding how traits are inherited |
| **Population genetics** | Allele frequencies, Hardy-Weinberg equilibrium, linkage disequilibrium, genetic drift, selection | Understanding genetic structure, population stratification, evolutionary processes |
| **Genomics** | Genome structure, sequencing technologies, variant types | Understanding data generation and variant classification |
| **Disease biology** | Understanding the traits/diseases being studied | Context for interpreting associations |
| **Functional genomics** | How genetic variants affect gene function | Interpreting biological mechanisms |

#### Statistics

| Topic | Description | Application in GWAS |
|-------|-------------|---------------------|
| **Regression analysis** | Linear and logistic regression | Fundamental to association testing |
| **Hypothesis testing** | P-values, confidence intervals, type I/II errors | Evaluating statistical significance |
| **Multiple testing** | Correction methods, false discovery rate | Accounting for millions of tests |
| **Bayesian statistics** | Prior distributions, posterior inference, Bayesian model selection | Fine-mapping, polygenic risk scores, uncertainty quantification, causal inference |
| **Linear algebra** | Matrix operations, eigenvalues, eigenvectors, matrix decomposition | Principal component analysis (PCA), mixed models, genomic relationship matrices, dimension reduction |
| **Machine learning** | Supervised and unsupervised learning, feature selection, model training | Polygenic risk scores, phenotype prediction, dimensionality reduction, variant prioritization, pattern recognition in genetic data |
| **Meta-analysis** | Combining results from multiple studies | Increasing power and replication |

#### Programming

| Tool/Language | Primary Use | Key Applications |
|---------------|------------|-----------------|
| **Linux/Unix command line** | Essential for most GWAS tools | Running PLINK, GCTA, and other command-line tools |
| **Python** | Data manipulation, visualization, statistical analysis | Data processing, plotting, downstream analysis |
| **R** | Statistical analysis, visualization, specialized genetics packages | Statistical modeling, visualization, genetics packages |
| **Bash** | Automating workflows, file processing | Pipeline automation, batch processing |
| **Git** | Version control | Managing code and tracking changes |


!!! success "Ready to start?"
    Now that you have the foundational knowledge, you're ready to dive into the hands-on tutorials! We recommend starting with:
    1. [Linux basics](https://cloufield.github.io/GWASTutorial/02_Linux_basics/) (if needed)
    2. [Data formats](https://cloufield.github.io/GWASTutorial/03_Data_formats/)
    3. [Data QC](https://cloufield.github.io/GWASTutorial/04_Data_QC/)

### Recommended reading

For a comprehensive list of recommended reading materials, see [Section 90: Recommended Reading](https://cloufield.github.io/GWASTutorial/90_Recommended_Reading/).

