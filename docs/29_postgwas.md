# Post-GWAS analysis

Post-GWAS analyses are a set of computational and statistical approaches that use summary statistics from GWAS, which capture variant–trait associations, to **move beyond association mapping** and translate statistical signals into **biological interpretation** by identifying causal variants, genes, tissues, pathways, and underlying disease mechanisms.

!!! info "Why Post-GWAS Analysis?"
    Although GWAS has been highly successful in identifying genomic loci associated with complex traits and diseases, GWAS alone is insufficient for biological interpretation and clinical translation. 

    - GWAS signals typically represent associations rather than causation, as lead variants are often proxies for the true causal variants due to linkage disequilibrium. 
    - Most GWAS-identified variants lie in non-coding regions, making it difficult to infer the affected genes, tissues, or regulatory mechanisms directly from association results.
    - The effect sizes of individual variants are generally small, and GWAS does not explain how multiple variants act together within biological pathways or networks.  
    - GWAS provides limited insight into context-specific effects, such as cell-type specificity, environmental interactions, or downstream molecular consequences.

Post-GWAS analyses address these limitations by prioritizing likely causal variants and genes, integrating GWAS results with functional genomic and multi-omic data (e.g., eQTL, chromatin accessibility, and epigenomic annotations), and identifying relevant tissues, cell types, and biological pathways. By moving beyond association to mechanism, post-GWAS approaches enable a deeper understanding of disease biology and support translational applications, including drug target identification, functional validation, and improved genetic risk prediction.

---

## Overview

After identifying genome-wide significant associations, **post-GWAS analyses** address key biological and translational questions by leveraging GWAS summary statistics and integrating them with functional and multi-omic data:

- **What proportion of trait variation is genetic?** SNP heritability estimation  
- **What are the causal variants?** Fine-mapping and colocalization  
- **Which genes and pathways are involved?** Functional annotation and pathway enrichment  
- **How do variants affect molecular function?** Regulatory annotation and QTL integration  
- **Where do genetic effects act?** Tissue- and cell-type enrichment  
- **Are traits genetically related?** Genetic correlation and shared architecture  
- **What are the causal relationships?** Mendelian randomization  
- **Can we predict disease risk?** Polygenic risk scores  
- **Are effects shared across traits?** Pleiotropy and cross-trait analysis  
- **How can findings be translated?** Drug target identification and prioritization  

---

## [Heritability estimation and genetic architecture](../13_heritability/)

**Biological questions answered:**

- How much phenotypic variance is explained by common genetic variants?
- Is the trait highly polygenic or driven by fewer loci?
- How is heritability distributed across genomic annotations?

**Common approaches:**

- SNP heritability estimation (LD score regression, GREML)
- Partitioned heritability by functional annotations
- Stratified LD score regression
- Polygenicity and effect-size distribution modeling

---

## [Functional annotation](../07_Annotation/)

**Biological questions answered:**

- Which genes are most likely to mediate GWAS associations?
- What functional elements are enriched among associated variants?
- Do variants affect coding sequences, regulatory elements, or both?

**Common approaches:**

- Variant-to-gene mapping (positional, eQTL, chromatin interaction–based)
- Functional annotation (CADD, SIFT, PolyPhen, RegulomeDB)
- Gene-level association methods (MAGMA, Pascal)
- Gene set and pathway enrichment (GO, KEGG, Reactome, MSigDB)
- Tissue-specific expression enrichment (GTEx, single-cell atlases)

---

## [Fine-mapping](../12_fine_mapping/)

**Biological questions answered:**

- Which specific variants are most likely to be causal?
- What is the minimal credible set explaining the association?
- Are there multiple independent signals within a locus?

**Common approaches:**

- Bayesian fine-mapping (FINEMAP, SuSiE, CAVIAR)
- Conditional and joint analysis
- Annotation-informed fine-mapping
- Multi-trait fine-mapping

---

## [Colocalization analysis](../17_colocalization/)

**Biological questions answered:**

- Do GWAS and molecular QTL signals share a causal variant?
- Which genes or proteins mediate trait associations?
- In which tissues or cell types do these effects occur?

**Common approaches:**

- eQTL and sQTL colocalization (GTEx, eQTLGen)
- pQTL and metabolite QTL colocalization
- Chromatin interaction data (Hi-C, promoter capture Hi-C)
- Statistical tests (COLOC, eCAVIAR, HyPrColoc)

---

## [Pathway and network analysis](../09_Gene_based_analysis/)

**Biological questions answered:**

- What biological processes and pathways are perturbed?
- How do associated genes interact in molecular networks?
- Are specific network modules enriched for associations?

**Common approaches:**

- Gene set enrichment analysis (GSEA, MAGMA, PASCAL)
- Pathway databases (KEGG, Reactome, WikiPathways)
- Protein–protein interaction and regulatory networks
- Network propagation and module detection

---

## [Tissue and cell-type enrichment](../25_singlecell/)

**Biological questions answered:**

- In which tissues or cell types do genetic effects manifest?
- Are effects cell-type–specific or context-dependent?
- Do regulatory mechanisms differ across developmental stages?

**Common approaches:**

- Tissue-specific eQTL enrichment
- Single-cell RNA-seq and ATAC-seq integration
- Cell-type–specific heritability partitioning
- Chromatin accessibility and epigenomic enrichment

---

## [Genetic correlation and cross-trait architecture](../08_LDSC/)

**Biological questions answered:**

- Do traits share a common genetic basis?
- What proportion of genetic effects is shared between traits?
- Are shared associations driven by pleiotropy or causality?

**Common approaches:**

- Genetic correlation estimation (LD score regression)
- Cross-trait meta-analysis
- Multivariate GWAS
- Shared heritability partitioning

---

## [Mendelian randomization](../16_mendelian_randomization/)

**Biological questions answered:**

- Is the relationship between exposure and outcome causal?
- What is the direction and magnitude of the effect?
- Are observed associations confounded by pleiotropy?

**Common approaches:**

- Two-sample MR using GWAS summary statistics
- Multivariable MR
- Robust methods (MR-Egger, weighted median)
- Sensitivity and reverse causality analyses

---

## [Polygenic risk scores](../10_PRS/)

**Biological questions answered:**

- Can aggregate genetic risk predict disease susceptibility?
- How do thousands of small-effect variants combine?
- Can PRS inform stratification or prevention strategies?

**Common approaches:**

- PRS construction (clumping + thresholding, LDpred, PRS-CS)
- Cross-ancestry PRS evaluation
- Independent cohort validation
- PRS × environment interaction analysis

---

## Pleiotropy and cross-trait analysis
**Biological questions answered:**

- Do variants influence multiple traits?
- Are effects mediated by shared biological pathways?
- Can pleiotropy explain comorbidity patterns?

**Common approaches:**

- Pleiotropy detection and modeling
- Multivariate association tests
- Cross-phenotype risk prediction
- Trait clustering based on shared genetics

---

## Drug target identification and translation

**Biological questions answered:**

- Which genes represent actionable therapeutic targets?
- Can existing drugs be repurposed?
- How can genetic evidence guide drug development?

**Common approaches:**

- Integration with drug–gene interaction databases
- Target prioritization using genetic evidence
- Pathway-based drug repurposing
- Clinical trial and pharmacogenomic evidence integration