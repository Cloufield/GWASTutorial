# Variant Databases

Variant databases are essential resources for GWAS and genetic research, providing comprehensive information about genetic variants, their frequencies, functional consequences, and associations with traits and diseases. This document provides an overview of major variant databases commonly used in GWAS and post-GWAS analyses.

## dbSNP

**Website**: https://www.ncbi.nlm.nih.gov/snp/

**Full name**: Database of Single Nucleotide Polymorphisms

dbSNP is the National Center for Biotechnology Information (NCBI)'s database of genetic variation, primarily focusing on single nucleotide polymorphisms (SNPs) but also including other types of genetic variants such as insertions, deletions, and microsatellites.

### Key Features

- **Comprehensive variant catalog**: Contains millions of genetic variants from multiple species, with human variants being the most extensively cataloged
- **Variant identifiers**: Provides unique reference SNP (rs) IDs for variants (e.g., rs123456)
- **Population frequency data**: Includes allele frequency information from various populations and studies
- **Functional annotations**: Links variants to genes, transcripts, and functional consequences
- **Clinical associations**: Integrates with ClinVar for clinical significance information
- **Validation status**: Indicates whether variants have been validated by multiple independent studies

### Common Uses in GWAS

- **Variant identification**: Looking up rs IDs for variants identified in GWAS
- **Frequency lookup**: Checking population frequencies of variants
- **Annotation**: Obtaining basic functional information about variants
- **Data integration**: Standardizing variant identifiers across different datasets

### Access Methods

- **Web interface**: Search by rs ID, gene name, or genomic coordinates
- **FTP download**: Bulk downloads of variant data
- **API access**: Programmatic access via NCBI's Entrez Programming Utilities
- **Integration with tools**: Many annotation tools (ANNOVAR, VEP) include dbSNP data

!!! info "dbSNP versions"
    dbSNP is regularly updated with new variants and annotations. Different builds correspond to different reference genome assemblies (e.g., dbSNP build 151 for GRCh37/hg19, build 155 for GRCh38/hg38).

## GWAS Catalog

**Website**: https://www.ebi.ac.uk/gwas/

**Full name**: The NHGRI-EBI GWAS Catalog

The GWAS Catalog is a curated database of published genome-wide association studies, providing standardized information about trait-variant associations from GWAS publications.

### Key Features

- **Curated associations**: Manually curated associations between genetic variants and traits/diseases from published GWAS
- **Standardized data format**: Consistent representation of variants, traits, and associations across studies
- **Comprehensive coverage**: Includes associations from thousands of GWAS publications
- **Trait ontology**: Uses Experimental Factor Ontology (EFO) for standardized trait names
- **Effect sizes and p-values**: Provides beta coefficients, odds ratios, and p-values for associations
- **Population information**: Includes ancestry and sample size information for each study

### Common Uses in GWAS

- **Literature review**: Finding previously reported associations for a trait of interest
- **Replication**: Checking if variants from your GWAS have been reported in other studies
- **Pleiotropy analysis**: Identifying variants associated with multiple traits
- **Prioritization**: Using known associations to prioritize variants for follow-up
- **Meta-analysis**: Gathering data from multiple studies for meta-analysis

### Access Methods

- **Web interface**: Search by trait, variant, gene, or study
- **FTP download**: Bulk downloads of all associations
- **REST API**: Programmatic access to the catalog
- **R package**: `gwasrapidd` package for R users

!!! tip "GWAS Catalog search tips"
    - Use EFO terms for more comprehensive trait searches
    - Filter by p-value threshold to focus on significant associations
    - Use genomic region search to find all associations in a locus of interest
    - Export results in various formats (TSV, JSON, VCF)

## Open Targets

**Website**: https://www.opentargets.org/

**Full name**: Open Targets Platform

Open Targets is a platform that integrates evidence from multiple sources to identify and prioritize drug targets associated with diseases. While not exclusively a variant database, it integrates GWAS data with other evidence types to support target identification.

### Key Features

- **Target-disease associations**: Integrates genetic, genomic, and chemical evidence linking targets to diseases
- **GWAS integration**: Incorporates GWAS associations from the GWAS Catalog and other sources
- **Evidence scoring**: Provides association scores based on multiple evidence types
- **Target prioritization**: Ranks potential drug targets based on genetic and functional evidence
- **Visualization tools**: Interactive visualizations of target-disease networks
- **API access**: RESTful API for programmatic access

### Common Uses in GWAS

- **Target identification**: Identifying potential drug targets from GWAS findings
- **Evidence integration**: Combining GWAS signals with other functional evidence
- **Disease mechanism**: Understanding how genetic associations relate to disease mechanisms
- **Drug discovery**: Prioritizing targets for drug development

### Evidence Types

Open Targets integrates multiple evidence types:

- **Genetic associations**: GWAS and genetic association studies
- **Somatic mutations**: Cancer mutation data
- **Drugs**: Known drug-target interactions
- **Pathways**: Pathway and systems biology data
- **Expression**: Gene expression and regulation data
- **Text mining**: Literature-based evidence

!!! note "Open Targets vs. GWAS Catalog"
    While GWAS Catalog focuses on variant-trait associations, Open Targets focuses on target-disease relationships, integrating GWAS data with other evidence types to support drug target identification.

## gnomAD

**Website**: https://gnomad.broadinstitute.org/

**Full name**: Genome Aggregation Database

gnomAD is a resource developed by the Broad Institute that aggregates and harmonizes exome and genome sequencing data from large-scale sequencing projects, providing comprehensive allele frequency data across diverse populations.

### Key Features

- **Large sample sizes**: Contains data from hundreds of thousands of individuals
- **Population diversity**: Includes frequency data for multiple populations (European, African, Asian, Latino, etc.)
- **Comprehensive variant catalog**: Both exome and genome sequencing data
- **Quality metrics**: Provides quality scores and filtering recommendations
- **Constraint scores**: Includes metrics of mutational constraint (pLI, LOEUF) to identify genes under selection
- **Allele frequency spectra**: Detailed frequency distributions across populations

### Common Uses in GWAS

- **Frequency lookup**: Checking population frequencies of variants, especially rare variants
- **Quality control**: Using gnomAD frequencies to filter variants
- **Rare variant analysis**: Identifying rare variants for association testing
- **Population-specific analysis**: Comparing frequencies across different populations
- **Constraint analysis**: Using constraint scores to prioritize functional variants

### Key Metrics

- **Allele frequency (AF)**: Frequency of the alternate allele in each population
- **Allele count (AC)**: Number of alternate alleles observed
- **Allele number (AN)**: Total number of alleles genotyped
- **Homozygote count**: Number of individuals homozygous for the alternate allele
- **pLI (probability of Loss-of-function Intolerance)**: Probability that a gene is intolerant to loss-of-function variants
- **LOEUF (Loss-of-function Observed/Expected Upper bound Fraction)**: Upper bound of the confidence interval for the observed/expected ratio of loss-of-function variants

!!! warning "gnomAD version differences"
    gnomAD has multiple versions (v2, v3, v4) with different sample sizes and populations. Always check which version you're using and ensure consistency across analyses.

!!! tip "Using gnomAD for QC"
    - Filter variants with very low frequency in gnomAD that appear common in your data (likely genotyping errors)
    - Use population-matched frequencies when available
    - Consider using gnomAD's quality filters (PASS variants) for high-confidence variants

## Other Notable Variant Databases

### ClinVar

**Website**: https://www.ncbi.nlm.nih.gov/clinvar/

ClinVar aggregates information about genetic variants and their relationships to human health, providing clinical significance classifications (pathogenic, benign, uncertain significance, etc.).

### ExAC

**Website**: https://exac.broadinstitute.org/

The Exome Aggregation Consortium (ExAC) was the predecessor to gnomAD, providing exome sequencing data from ~60,000 individuals. Now superseded by gnomAD but still useful for historical reference.

### 1000 Genomes Project

**Website**: https://www.internationalgenome.org/

Provides comprehensive catalog of human genetic variation from ~2,500 individuals across 26 populations. Useful for population genetics and as a reference panel for imputation.

### TOPMed

**Website**: https://www.nhlbiwgs.org/

The Trans-Omics for Precision Medicine (TOPMed) program provides whole-genome sequencing data from diverse populations, useful for rare variant analysis and as an imputation reference panel.

## Choosing the Right Database

Different databases serve different purposes in GWAS research:

| Database | Primary Use | Best For |
|----------|-------------|----------|
| **dbSNP** | Variant identification and basic annotation | Looking up rs IDs, basic frequency data |
| **GWAS Catalog** | Literature review and replication | Finding previously reported associations |
| **gnomAD** | Population frequency data | QC, rare variant analysis, population-specific frequencies |
| **Open Targets** | Target identification | Drug discovery, integrating multiple evidence types |
| **ClinVar** | Clinical significance | Interpreting variants in clinical context |

## References

### dbSNP

- **Sherry, S. T., Ward, M. H., Kholodov, M., Baker, J., Phan, L., Smigielski, E. M., & Sirotkin, K.** (2001). dbSNP: the NCBI database of genetic variation. *Nucleic Acids Research*, 29(1), 308-311. doi: [10.1093/nar/29.1.308](https://doi.org/10.1093/nar/29.1.308)

- **Sayers, E. W., et al.** (2022). Database resources of the National Center for Biotechnology Information. *Nucleic Acids Research*, 50(D1), D20-D26. doi: [10.1093/nar/gkab1112](https://doi.org/10.1093/nar/gkab1112)

### GWAS Catalog

- **Buniello, A., et al.** (2019). The NHGRI-EBI GWAS Catalog of published genome-wide association studies, targeted arrays and summary statistics 2019. *Nucleic Acids Research*, 47(D1), D1005-D1012. doi: [10.1093/nar/gky1120](https://doi.org/10.1093/nar/gky1120)

- **Sollis, E., et al.** (2023). The NHGRI-EBI GWAS Catalog: knowledgebase and deposition resource. *Nucleic Acids Research*, 51(D1), D977-D985. doi: [10.1093/nar/gkac1010](https://doi.org/10.1093/nar/gkac1010)

### Open Targets

- **Koscielny, G., et al.** (2017). Open Targets: a platform for therapeutic target identification and validation. *Nucleic Acids Research*, 45(D1), D985-D994. doi: [10.1093/nar/gkw1055](https://doi.org/10.1093/nar/gkw1055)

- **Ochoa, D., et al.** (2021). Open Targets Platform: supporting systematic drug-target identification and prioritisation. *Nucleic Acids Research*, 49(D1), D1302-D1310. doi: [10.1093/nar/gkaa1027](https://doi.org/10.1093/nar/gkaa1027)

### gnomAD

- **Karczewski, K. J., et al.** (2020). The mutational constraint spectrum quantified from variation in 141,456 humans. *Nature*, 581(7809), 434-443. doi: [10.1038/s41586-020-2308-7](https://doi.org/10.1038/s41586-020-2308-7)

- **Chen, S., et al.** (2023). A genomic mutational constraint map using variation in 76,156 human genomes. *Nature*, 625(7993), 92-100. doi: [10.1038/s41586-023-06045-0](https://doi.org/10.1038/s41586-023-06045-0)

### Other Resources

- **ClinVar**: Landrum, M. J., et al. (2018). ClinVar: improving access to variant interpretations and supporting evidence. *Nucleic Acids Research*, 46(D1), D1062-D1067. doi: [10.1093/nar/gkx1153](https://doi.org/10.1093/nar/gkx1153)

- **1000 Genomes Project**: The 1000 Genomes Project Consortium. (2015). A global reference for human genetic variation. *Nature*, 526(7571), 68-74. doi: [10.1038/nature15393](https://doi.org/10.1038/nature15393)
