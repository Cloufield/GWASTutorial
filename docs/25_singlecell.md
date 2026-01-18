# Beyond Genomics: Single-Cell Genomics

Single-cell genomics (scRNA-seq, scATAC-seq, spatial transcriptomics, and multiome assays)
resolves molecular variation at the level of individual cells. When integrated with GWAS,
these data enable a conceptual shift from "locus discovery" to "cellular mechanism
inference", linking genetic risk to specific cell types, states, regulatory programs,
and spatial contexts.

This section presents a refined framework for GWAS–single-cell integration, organized
by the *biological question being asked* and the *resolution of inference*.

---

## Why Integrate GWAS with Single-Cell Data?

GWAS robustly identifies trait-associated loci, but typically leaves some key questions
unanswered:

1. **Which cell types mediate genetic risk?**
2. **Which cellular states or programs are involved?**
3. **Where in tissue architecture does risk manifest?**

Single-cell datasets address these gaps by enabling:

- Cell-type and cell-state resolution of GWAS signals
- Gene and regulatory program prioritization in relevant cells
- Dissection of heterogeneous tissues (immune system, brain, tumor microenvironment)
- Cell-type-specific genetic architectures (e.g. sc-eQTL, scATAC-QTL, state-dependent effects)

---

## Framework for GWAS–Single-Cell Methods

Methods can be organized along two orthogonal axes:

### Genetic abstraction level

- Variant / heritability-based
- Gene-based
- Cell-based
- Spatial / tissue-context-based

### Biological resolution

- Cell type
- Cell state / program
- Regulatory mechanism
- Spatial niche

---

## Approaches

### 1. Cell-type heritability and gene-set enrichment
*(Variant-level or gene-level; population-wide signal)*

**Representative methods:**
- LDSC-seg (stratified LD Score Regression) - [GitHub](https://github.com/bulik/ldsc)
- MAGMA (gene-property and gene-set analysis) - [Software](https://ctg.cncr.nl/software/magma)

**Core question:**
"Are GWAS signals enriched in genes or annotations specific to certain cell types?"

**Core idea:**
- Derive cell-type-specific annotations from expression or chromatin data
- Partition GWAS heritability (LDSC-seg) or gene-level association (MAGMA)
- Test enrichment while accounting for LD and baseline genomic features

**Typical inputs:**
- GWAS summary statistics
- Cell-type aggregated expression or accessibility profiles
- LD reference panels

**Typical outputs:**
- Enrichment statistics per cell type or tissue

**Strengths:**
- Robust, LD-aware, interpretable
- Ideal as a first-pass prioritization step

**Limitations:**
- Limited resolution (cell type rather than individual cells)
- Sensitive to gene-to-SNP mapping choices

**Workflow:**
```
GWAS Summary Statistics
         ↓
    LD Reference Panels
         ↓
Cell-type Aggregated Expression/Accessibility Profiles
         ↓
    [LDSC-seg: Stratified LD Score Regression]
    [MAGMA: Gene-property Analysis]
         ↓
    Enrichment Statistics per Cell Type
```

---

### 2. Per-cell and per-state disease relevance scoring
*(Cell-level resolution; heterogeneity-aware)*

**Representative methods:**
- scDRS - [GitHub](https://github.com/martinjzhang/scDRS)

**Core question:**
"Which individual cells or cellular states are most relevant to a given disease?"

**Core idea:**
- Convert GWAS summary statistics into gene-level disease scores
- Score each cell by coordinated expression of disease-associated genes
- Use matched control gene sets for calibration and statistical testing

**Typical inputs:**
- scRNA-seq data (cell-by-gene expression matrix)
- GWAS summary statistics or derived gene scores

**Typical outputs:**
- Disease relevance score per cell
- Cluster- or state-level summaries

**Strengths:**
- Captures within–cell-type heterogeneity
- Highlights rare, transient, or activated states

**Limitations:**
- Expression-based (does not directly model regulatory variants)
- Interpretation is correlational rather than causal

**Workflow:**
```
GWAS Summary Statistics
         ↓
    Gene-level Disease Scores
         ↓
    scRNA-seq Data (Cell × Gene Matrix)
         ↓
    [scDRS: Score Each Cell]
         ↓
    Disease Relevance Score per Cell
         ↓
    Cluster/State-level Summaries
```

---

### 3. Variant-to-gene-to-cell-type linking
*(Mechanistic and regulatory interpretation)*

**Representative methods:**
- sc-linker - [GitHub](https://github.com/karthikj89/scgenetics)

**Core question:**
"Which genes mediate GWAS loci, and in which cell types do they act?"

**Core idea:**
- Integrate GWAS loci with single-cell chromatin accessibility and expression
- Link non-coding variants to regulatory elements
- Connect regulatory elements to target genes in a cell-type-specific manner

**Typical inputs:**
- GWAS summary statistics or fine-mapped loci
- scATAC-seq / multiome data
- Single-cell gene expression

**Typical outputs:**
- Prioritized causal genes per locus
- Cell-type-specific regulatory links

**Strengths:**
- Moves toward causal interpretation
- Explicitly models regulatory context

**Limitations:**
- Requires high-quality regulatory maps
- Peak-to-gene linking remains noisy

**Workflow:**
```
GWAS Summary Statistics / Fine-mapped Loci
         ↓
    scATAC-seq / Multiome Data
         ↓
    Single-cell Gene Expression
         ↓
    [sc-linker: Link Variants → Regulatory Elements → Genes]
         ↓
    Prioritized Causal Genes per Locus
         ↓
    Cell-type-specific Regulatory Links
```

---

### 4. Spatial mapping of genetic risk
*(Tissue architecture and microenvironment context)*

**Representative methods:**
- gsMap - [GitHub](https://github.com/JianYang-Lab/gsMap)

**Core question:**
"Where in the tissue does genetic risk manifest?"

**Core idea:**
- Use Graph Neural Network (GNN) to identify homogeneous spots (microdomains) based on gene expression patterns and spatial coordinates
- Compute gene specificity scores (GSS) for each spot by comparing gene expression ranks within microdomains versus the entire section
- Map GSS to SNPs via distance-based windows (±50 kb from transcription start sites) and SNP-to-gene linking maps
- Apply stratified LD Score Regression (S-LDSC) to test whether SNPs with higher GSS are enriched for trait heritability
- Aggregate spot-level associations to spatial regions using the Cauchy combination test

**Typical inputs:**
- Spatial transcriptomics data (with spatial coordinates and gene expression profiles)
- GWAS summary statistics
- LD reference panels
- SNP-to-gene linking maps (e.g., from epigenomic data)
- Optional: cell type annotation priors

**Typical outputs:**
- Enrichment statistics and P-values per spatial spot
- Spatial maps of trait-associated cells or regions
- Region-level aggregated associations

**Strengths:**
- Addresses sparsity and technical noise in ST data through microdomain aggregation
- Provides spatially resolved mapping at cellular resolution
- Adds anatomical and microenvironmental context
- Essential for brain, cancer, and developmental studies

**Limitations:**
- Resolution depends on spatial technology (spot-level in high-resolution platforms, cluster-level in conventional platforms)
- Requires high-quality SNP-to-gene linking maps
- Computational intensity increases with spatial resolution

**Workflow:**
```
Spatial Transcriptomics Data (Expression + Coordinates)
         ↓
    [GNN: Identify Homogeneous Spots / Microdomains]
         ↓
    [Compute Gene Specificity Scores (GSS) per Spot]
         ↓
    [Map GSS to SNPs via Distance & SNP-to-Gene Links]
         ↓
    GWAS Summary Statistics + LD Reference Panels
         ↓
    [S-LDSC: Test Heritability Enrichment per Spot]
         ↓
    [Cauchy Combination Test: Aggregate to Regions]
         ↓
    Spatial Maps of Trait-associated Spots/Regions
```

---

## Conceptual Summary Table

| Method class | Resolution | Primary question |
|--------------|------------|------------------|
| LDSC-seg / MAGMA | Cell type | Which cell types are enriched? |
| scDRS | Individual cells | Which cells or states matter? |
| sc-linker | Gene + cell type | Which genes mediate risk? |
| gsMap | Spatial regions | Where does risk manifest? |

---

## References

### Review papers

- **Cuomo, A. S. E., Nathan, A., Raychaudhuri, S., MacArthur, D. G., & Powell, J. E.** (2023). Single-cell genomics meets human genetics. *Nature Reviews Genetics*, 24(8), 535–549. https://doi.org/10.1038/s41576-023-00598-6

### Method papers

- **Finucane, H. K., Reshef, Y. A., Anttila, V., Slowikowski, K., Gusev, A., Byrnes, A., et al.** (2018). Heritability enrichment of specifically expressed genes identifies disease-relevant tissues and cell types. *Nature Genetics*, 50(4), 621–629. https://doi.org/10.1038/s41588-018-0081-4

- **de Leeuw, C. A., Mooij, J. M., Heskes, T., & Posthuma, D.** (2015). MAGMA: generalized gene-set analysis of GWAS data. *PLoS Computational Biology*, 11(4), e1004219. https://doi.org/10.1371/journal.pcbi.1004219

- **Zhang, M. J., Hou, K., Dey, K. K., et al.** (2022). Polygenic enrichment distinguishes disease associations of individual cells in single-cell RNA-seq data. *Nature Genetics*, 54(9), 1344–1350. https://doi.org/10.1038/s41588-022-01167-z (scDRS)

- **Jagadeesh, K. A., Dey, K. K., Montoro, D. T., Mohan, R., Gazal, S., Engreitz, J. M., Xavier, R. J., Price, A. L., Regev, A., et al.** (2022). Identifying disease-critical cell types and cellular processes by integrating single-cell RNA-sequencing and human genetics. *Nature Genetics*, 54(10), 1479–1492. https://doi.org/10.1038/s41588-022-01187-9 (sc-linker)

- **Song, L., Chen, W., Hou, J., Guo, M., & Yang, J.** (2025). Spatially resolved mapping of cells associated with human complex traits. *Nature*, 641, 932–941. https://doi.org/10.1038/s41586-025-08757-x (gsMap)
