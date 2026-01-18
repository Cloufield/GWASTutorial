# Imputation

Genotype imputation is a statistical method used to infer unobserved genotypes in a study sample by leveraging haplotype information from a reference panel with high-coverage sequencing data (typically whole-genome sequenced, WGS). While missing data imputation is not specific to genetic studies, genotype imputation has unique properties that make specialized methods necessary.

!!! info "Why genotype imputation?"
    Genotyping arrays typically assay 500k–1M markers across the genome, while reference panels contain millions of variants from whole-genome sequencing. Imputation allows researchers to:
    - Increase statistical power by testing more variants
    - Perform meta-analyses across studies with different arrays
    - Compare results with published GWAS that used different platforms

!!! example "Imputation example"
    Suppose you have a target sample genotyped at only a few positions, and a reference panel with complete sequence information:
    
    **Reference haplotypes:**
    ```
    Ref1:  A  T  G  C  A  T  G  C
    Ref2:  A  T  A  C  A  T  A  C
    Ref3:  G  T  G  C  G  T  G  C
    Ref4:  A  C  G  T  A  C  G  T
    ```
    
    **Target sample (genotyped positions marked, missing positions shown as ?):**
    ```
    Target: A  ?  G  ?  A  ?  G  ?
    ```
    
    The imputation algorithm finds that the target matches Ref1 at positions 1, 3, and 5 (A, G, A). Based on this matching pattern and the HMM model, it infers that the target is most likely copying from Ref1, and imputes the missing positions:
    
    **Imputed result:**
    ```
    Target: A  T  G  C  A  T  G  C
    ```
    
    In practice, the algorithm considers all possible paths through reference haplotypes, accounts for recombination events, and provides probability-weighted imputations rather than hard calls.

## Concepts

### Why HMM-based methods?

While tabular data imputation methods could theoretically be used for genotype data, haplotypes have unique biological properties that make specialized methods more effective:

- **Haplotype structure**: Haplotypes are coalesced from ancestors, and recombination events during gametogenesis create mosaics
- **Population genetics**: Each individual's haplotype is a mosaic of reference-panel haplotypes that approximate the population
- **Linkage disequilibrium**: Nearby variants are correlated due to shared ancestry and limited recombination

Given these properties, hidden Markov model (HMM) based methods usually outperform tabular data-based approaches.

!!! quote
    Li, N., & Stephens, M. (2003). Modeling linkage disequilibrium and identifying recombination hotspots using single-nucleotide polymorphism data. Genetics, 165(4), 2213-2233.
    
    The HMM framework for genotype imputation was first described in this foundational paper.

### Hidden Markov Model formulation

The Li & Stephens HMM models an individual's haplotype as a mosaic of reference haplotypes. The model has two key components:

1. **Emission probabilities**: The probability of observing a particular allele given the reference haplotype state
2. **Transition probabilities**: The probability of switching between different reference haplotypes (modeling recombination)

For a target haplotype $h$ and a set of $K$ reference haplotypes $H = \{h_1, h_2, ..., h_K\}$, the probability of the target haplotype given the reference panel is:

$$P(h | H) = \sum_{z} P(h, z | H)$$

where $z = (z_1, z_2, ..., z_L)$ represents the hidden state sequence (which reference haplotype is copied at each position) across $L$ markers.

The joint probability can be decomposed as:

$$P(h, z | H) = P(z_1) \prod_{l=2}^{L} P(z_l | z_{l-1}) \prod_{l=1}^{L} P(h_l | z_l, H)$$

where:

- **Initial state probability**: $P(z_1 = k) = \frac{1}{K}$ (uniform prior over reference haplotypes)

- **Transition probability**: Models recombination between markers $l-1$ and $l$:

  If $k' = k$: $P(z_l = k' | z_{l-1} = k) = e^{-\rho_l} + (1 - e^{-\rho_l}) \frac{1}{K}$
  
  If $k' \neq k$: $P(z_l = k' | z_{l-1} = k) = (1 - e^{-\rho_l}) \frac{1}{K}$
  
  where $\rho_l = 4N_e r_l / K$ is the Li–Stephens 2003 per-step recombination rate parameter between markers $l-1$ and $l$, $N_e$ is the effective population size, $r_l$ is the genetic distance, and $K$ is the number of reference haplotypes.

- **Emission probability**: The probability of observing allele $h_l$ given we're copying from reference haplotype $k$:

  If $h_l = h_{k,l}$: $P(h_l | z_l = k, H) = 1 - \theta$
  
  If $h_l \neq h_{k,l}$: $P(h_l | z_l = k, H) = \theta$
  
  where $\theta$ is a mutation/error parameter (typically small, e.g., 0.001), and $h_{k,l}$ is the allele at position $l$ in reference haplotype $k$.

!!! info "Key parameters"
    - **$\rho_l$ (recombination rate)**: Controls how often the model switches between reference haplotypes. Higher values allow more frequent switching (more recombination).
    - **$\theta$ (mutation parameter)**: Allows for mismatches between target and reference, accounting for genotyping errors, mutations, or missing reference haplotypes.
    - **$K$ (number of reference haplotypes)**: Larger reference panels provide more haplotype diversity and generally improve imputation accuracy.

The forward-backward algorithm is used to efficiently compute the posterior probabilities $P(z_l = k | h, H)$ for all positions and reference haplotypes, which are then used to impute missing genotypes as probability-weighted averages.

### Minimac

[Minimac](https://www.nature.com/articles/ng.3656) is a widely used imputation tool that implements the Li & Stephens HMM model. It is computationally efficient and can handle large reference panels.

!!! quote
    Das, S., et al. (2016). Next-generation genotype imputation service and methods. Nature genetics, 48(10), 1284-1287.

## Figure illustration

<img width="490" alt="image" src="https://github.com/Cloufield/GWASTutorial/assets/84720165/afff6f31-6a97-4ed2-975e-6f795a39b440">

!!! example "Understanding the imputation process"
    In the figure above:
    - **Top panel**: Each row represents a reference haplotype from the reference panel
    - **Middle panel**: Shows the genotyping array data. Genotyped markers are squared and WGS-only markers (to be imputed) are circled
    - **Colors**: Represent the ref and alt alleles, or different haplotype fragments
    - **Red triangles**: Indicate recombination hotspots where crossovers between reference haplotypes are more likely to occur

The imputation process works as follows:

1. **Path probability calculation**: Given the genotyped markers, matching probabilities are calculated for all potential paths through reference haplotypes
2. **Recombination modeling**: At each recombination hotspot, the model allows transitions between different reference haplotypes (in this simplified example, we assume free recombination at hotspots)
3. **Weighted imputation**: Missing markers are filled with probability-weighted alleles from all possible paths

!!! example "Example calculation"
    In the figure, paths chained by dark blue match 2 of the 4 genotyped markers. These paths have equal probability. For the left three circles (missing markers), two paths are cyan and one path is orange, so the imputation result will be 1/3 orange and 2/3 cyan.

## How to do imputation

### Option 1: Imputation servers

The simplest way is to use public imputation servers if you don't have access to WGS reference data:

- **[Michigan Imputation Server](https://imputationserver.sph.umich.edu/index.html#!)**: Provides access to various reference panels including 1000 Genomes, HRC, and TOPMed
- **[TOPMed Imputation Server](https://imputation.biodatacatalyst.nhlbi.nih.gov/#!)**: Uses the NHLBI TOPMed reference panel

!!! warning "Ethics and data privacy"
    Before uploading data to public imputation servers, ensure compliance with informed consent, IRB approval, and data protection regulations (GDPR, HIPAA, etc.).

!!! tip "Server workflow"
    The typical workflow is:
    1. Prepare your VCF file
    2. Submit it to the server
    3. Select the appropriate reference panel
    4. Download the imputed results

!!! warning "Important considerations"
    Although imputation servers can automatically handle phasing, liftover, and quality control, **it is strongly recommended** to perform these preprocessing steps locally for better control, reproducibility, and the ability to reuse phased data with different reference panels:
    
    - **Liftover**: Convert between hg19 and hg38, properly flip alleles, and exclude ambiguous variants (A/T and G/C SNPs)
    - **Phasing**: Phase your data locally and store it. Phased data can be reused for imputation against any reference panel
    - **Ancestry matching**: Check ancestry information and select the proper reference panel that matches your study population

### Option 2: Local imputation

Recent imputation tools are memory and computationally efficient, allowing you to run imputation on a small in-house server or even a personal computer.

!!! warning "Imputation runtime"
    Imputation often takes a very long time to complete, especially for large datasets. The runtime depends on several factors:
    - **Sample size**: Larger cohorts take proportionally longer
    - **Reference panel size**: Larger reference panels (e.g., TOPMed with >90k samples) require more computation
    - **Number of variants**: More variants to impute increases runtime
    - **Hardware**: CPU cores and memory availability affect speed
    
    For large-scale studies (thousands of samples), imputation can take hours to days even on powerful servers. Plan accordingly and consider running imputation in batches or using high-performance computing resources.

#### Minimac workflow

A typical workflow using Minimac consists of two steps:

**Step 1: Parameter estimation** (creates an [m3vcf](https://genome.sph.umich.edu/wiki/M3VCF_Files) reference panel file)

This step preprocesses the reference panel to create a compressed format that speeds up imputation:

```sh
minimac3 \
  --refHaps ./phased_reference.vcf.gz \
  --processReference \
  --prefix ./phased_reference \
  --log
```

**Step 2: Imputation**

This step performs the actual imputation of your target dataset:

```sh
minimac4 \
  --refHaps ./phased_reference.m3vcf \
  --haps ./phased_target.vcf.gz \
  --prefix ./result \
  --format GT,DS,HDS,GP,SD \
  --meta \
  --log \
  --cpus 10
```

!!! info "Output format options"
    The `--format` parameter specifies which genotype representations to include:
    - `GT`: Best-guess genotypes (0/0, 0/1, 1/1)
    - `DS`: Allelic dosage (expected number of alternate alleles, 0-2)
    - `HDS`: Haplotype dosages (separate dosages for each chromosome)
    - `GP`: Genotype probabilities (posterior probabilities for each genotype)
    - `SD`: Standard deviation of dosage

    See the [Minimac4 documentation](https://genome.sph.umich.edu/wiki/Minimac4_Documentation) for details on all options.

## After imputation

### Quality control

The output is a VCF file containing imputed genotypes. Before using imputed data in downstream analyses, it is crucial to examine imputation quality.

!!! info "Imputation quality metrics"
    Two commonly reported metrics are **Rsq** (used by Minimac) and **INFO** (used by IMPUTE). Both aim to summarize imputation certainty but are defined differently:

    - **Rsq**: An estimated squared correlation between the unobserved true dosage and the imputed dosage, typically computed as the ratio of the empirical dosage variance to the expected binomial variance under HWE (i.e., $\mathrm{Var}(\hat{d}) / [2p(1-p)]$).
    - **INFO**: A ratio comparing the observed variance of posterior mean dosages to the expected binomial variance under HWE, often written as $1 - \frac{\mathrm{E}[\mathrm{Var}(G \mid \text{data})]}{2p(1-p)}$ or equivalently $\mathrm{Var}(\hat{d}) / [2p(1-p)]$ depending on the software's exact definition.
    
    In both cases, higher values indicate better imputation quality, but thresholds are not strictly interchangeable across tools or definitions.

!!! tip "Quality thresholds"
    Most of the time, when the following criteria are met:
    - Genotyping array contains > 500k markers
    - Reference panel is 1000 Genomes or ancestry-matched, or at least the major ancestry in the panel matches the target population
    
    The Rsq metric efficiently discriminates well-imputed variants at a threshold of **0.7**. You may loosen this to **0.3** to allow more variants in GWAS, but be aware that lower-quality imputations may introduce noise.

!!! warning "Quality assessment"
    Imputation quality assessment can be complex and depends on many factors including:
    - Reference panel size and ancestry match
    - Variant frequency (rare variants are harder to impute)
    - Local LD structure
    - Genotyping array density
    
    For detailed discussion, see: [A comprehensive evaluation of imputation quality](https://www.biorxiv.org/content/10.1101/2023.05.30.542466v1)

### Filtering imputed variants

After quality assessment, filter variants based on quality metrics:

```sh
# Example: Filter variants with R2 >= 0.7
bcftools filter -i 'INFO/R2>=0.7' imputed.vcf.gz -Oz -o imputed.filtered.vcf.gz
```

## Before GWAS

### Genotype representations

Three types of genotype representations are widely used in GWAS:

1. **Best-guess genotypes (GT)**: Hard calls (0/0, 0/1, 1/1) representing the most likely genotype
2. **Allelic dosage (DS)**: Expected number of alternate alleles (continuous value from 0 to 2)
3. **Genotype probability (GP)**: Posterior probabilities for each genotype state

!!! tip "Choosing a representation"

    - **Dosage (DS)** is often preferred because:
        - It preserves uncertainty information (unlike hard calls)
        - It keeps the dataset smaller than genotype probabilities
        - Most association test software (PLINK, REGENIE, etc.) can use dosage directly
        - It provides better power for rare variants compared to hard calls
    - **Best-guess genotypes** may be used when:
        - Software requires discrete genotypes
        - For visualization or quality checks
        - When imputation quality is very high (Rsq > 0.9)
    - **Genotype probabilities** are useful for:
        - Methods that explicitly model uncertainty
        - Rare variant analysis where uncertainty is important
        - Fine-mapping applications

### Converting to PLINK format

If you need to convert imputed VCF to PLINK format for association testing:

```sh
# Using dosage (recommended)
plink2 \
  --vcf imputed.vcf.gz \
  --dosage DS \
  --make-pgen \
  --out imputed.dosage

# Or using best-guess genotypes
plink2 \
  --vcf imputed.vcf.gz \
  --make-bed \
  --out imputed.hardcall
```

!!! note
    When using dosage, PLINK2 will create a `.pgen` file with dosage values. Some older software may require hard calls, but dosage is generally preferred for better statistical power.

## Specialized imputation applications

While standard genome-wide imputation is primarily used for GWAS, imputation methods have been adapted for specialized applications that require different approaches or reference panels.

### HLA imputation

The Human Leukocyte Antigen (HLA) region on chromosome 6 is one of the most polymorphic regions in the human genome, with thousands of alleles across multiple genes (HLA-A, HLA-B, HLA-C, HLA-DRB1, HLA-DQA1, HLA-DQB1, etc.). HLA typing is critical for:

- **Organ transplantation**: Matching donors and recipients
- **Autoimmune disease research**: Many autoimmune conditions show strong HLA associations
- **Pharmacogenomics**: Drug hypersensitivity reactions (e.g., HLA-B*57:01 and abacavir)
- **Infectious disease**: HIV progression, hepatitis B/C outcomes

!!! info "Why specialized HLA imputation?"
    Standard imputation methods struggle with the HLA region because:

    - **Extreme polymorphism**: Hundreds to thousands of alleles per gene
    - **Linkage disequilibrium**: Complex LD patterns that differ from the rest of the genome
    - **Structural variation**: Large insertions/deletions and gene duplications
    - **Population-specific diversity**: Different allele frequencies across populations

Specialized HLA imputation tools use HLA-specific reference panels and methods:

- **[HIBAG](https://www.bioconductor.org/packages/release/bioc/html/HIBAG.html)**: HLA Genotype Imputation with Attribute Bagging
- **[HLA*IMP](https://www.ucl.ac.uk/cancer/research-groups/genetic-epidemiology-research-group/hla-imp)**: HLA imputation using population-specific reference panels
- **[CookHLA](https://github.com/WansonChoi/CookHLA)**: Fast and accurate HLA imputation from SNP data
- **[HLA-HD](https://www.genome.med.kyoto-u.ac.jp/HLA-HD/)**: High-resolution HLA typing from sequencing data

!!! tip "HLA imputation workflow"
    The typical workflow for HLA imputation:

    1. Extract SNPs in the HLA region (chr6:25-35 Mb; specify the genome build, e.g., GRCh37/GRCh38) from your genotyped data
    2. Use population-matched HLA reference panels (e.g., 1000 Genomes HLA-typed samples)
    3. Run HLA-specific imputation software
    4. Validate imputed HLA types against known types when available
    5. Report HLA alleles at 2-field (e.g., HLA-B*57:01) or 4-field resolution

### Ancient genome imputation

Imputing genotypes in ancient DNA (aDNA) samples presents unique challenges due to DNA degradation, contamination, and limited reference data from ancient populations.

!!! info "Challenges in ancient DNA imputation"

    - **Low coverage**: Ancient samples often have very low sequencing depth (<1x)
    - **DNA damage**: Post-mortem damage patterns (C→T deamination) that can be mistaken for variants
    - **Contamination**: Modern human DNA contamination from handling
    - **Population structure**: Ancient populations may not be well-represented in modern reference panels
    - **Temporal distance**: Large time gaps between ancient samples and modern reference panels

!!! tip "Approaches for ancient DNA imputation"
    Several strategies have been developed:
    
    - **Damage-aware imputation**: Account for post-mortem DNA damage patterns
    - **Ancient reference panels**: Use other ancient genomes as reference when available
    - **Population-specific references**: Use reference panels from populations genetically closest to the ancient sample
    - **Quality filtering**: More stringent filtering of low-quality sites and samples
    
    Tools adapted for ancient DNA:
    - **[GLIMPSE](https://odelaneau.github.io/GLIMPSE/)**: Can handle low-coverage data and is used in ancient DNA studies
    - **[Beagle](http://faculty.washington.edu/browning/beagle/beagle.html)**: Has been adapted for ancient DNA with damage-aware models
    - Custom pipelines that combine damage correction, contamination estimation, and imputation

!!! example "Ancient DNA imputation example"
    A typical workflow might involve:

    1. **Damage correction**: Remove or downweight C→T and G→A transitions at read ends
    2. **Contamination estimation**: Estimate modern human contamination levels
    3. **Reference panel selection**: Choose modern populations genetically closest to the ancient sample (e.g., using PCA or f-statistics)
    4. **Low-coverage imputation**: Use methods that can handle very sparse data
    5. **Validation**: Compare imputed genotypes to high-coverage ancient genomes when available

!!! warning "Considerations for specialized imputation"
    When working with specialized imputation applications:

    - **Reference panel quality**: Ensure reference panels are appropriate for your application (population-matched, high-quality)
    - **Validation**: Always validate imputed results when possible (e.g., compare to gold-standard typing)
    - **Quality metrics**: Use application-specific quality metrics (e.g., HLA imputation confidence scores)
    - **Population matching**: Population ancestry matching is even more critical for specialized applications

## References

- (**Li & Stephens model**) Li, N., & Stephens, M. (2003). Modeling linkage disequilibrium and identifying recombination hotspots using single-nucleotide polymorphism data. Genetics, 165(4), 2213-2233. https://doi.org/10.1093/genetics/165.4.2213

- (**Minimac**) Das, S., Forer, L., Schönherr, S., Sidore, C., Locke, A. E., Kwong, A., ... & Fuchsberger, C. (2016). Next-generation genotype imputation service and methods. Nature Genetics, 48(10), 1284-1287. https://doi.org/10.1038/ng.3656

- (**HIBAG**) Zheng, X., Shen, J., Cox, C., Wakefield, J. C., Ehm, M. G., Nelson, M. R., & Weir, B. S. (2014). HIBAG—HLA genotype imputation with attribute bagging. The Pharmacogenomics Journal, 14(2), 192-200. https://doi.org/10.1038/tpj.2013.18

- (**GLIMPSE**) Rubinacci, S., Ribeiro, D. M., Hofmeister, R. J., & Delaneau, O. (2021). Efficient phasing and imputation of low-coverage sequencing data using large reference panels. Nature Genetics, 53(1), 120-126. https://doi.org/10.1038/s41588-020-00756-0

- (**Ancient DNA imputation**) Margaryan, A., Lawson, D. J., Sikora, M., Racimo, F., Rasmussen, S., Moltke, I., ... & Willerslev, E. (2020). Population genomics of the Viking world. Nature, 585(7825), 390-396. https://doi.org/10.1038/s41586-020-2225-9
