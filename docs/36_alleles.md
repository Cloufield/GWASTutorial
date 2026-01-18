# Allele 

## Definition

An **allele** is one of the alternative forms of a genetic variant (e.g., SNP) at a specific genomic position. For a bi-allelic variant, there are two possible alleles (e.g., A or G). Each individual carries two alleles at each autosomal position (one from each parent), which together form their genotype (e.g., AA, AG, or GG).

In GWAS and genetic analysis, alleles are the fundamental units used to:

- Measure genetic variation within and between populations
- Test associations between genetic variants and phenotypes
- Calculate allele frequencies and genotype distributions
- Estimate effect sizes and odds ratios

The specific nucleotide or sequence variant at a position represents an allele, and different alleles can have different effects on phenotypes, disease risk, or other traits of interest.

## Related concepts

Concepts: Major/Minor/Reference/Alternative/Risk/Effect Allele, Allele0/Allele1, A1/A2, Ancestral/Derived Allele

Understanding allele terminology is crucial in GWAS analysis. These concepts are often confused, leading to errors or misunderstandings.

!!! warning "Allele Naming is Highly Inconsistent"
    **The naming conventions for alleles are quite mixed and inconsistent across different software, databases, and file formats.** The same term (e.g., "reference allele", "A1", "Allele0") can have different meanings depending on the context, software version, or data source. 
    
    **Always check the documentation of your data source, software, or database to determine which allele is which.** Never assume that naming conventions are consistent across different tools or datasets. When in doubt:
    
    - Consult the official documentation
    - Check allele frequency information if available
    - Verify with example data or test cases
    - Cross-reference with known reference genomes when possible
    
    This inconsistency is a common source of errors in GWAS analysis, so extra caution is essential.

## Three Groups of Allele Concepts

### First Group: Major and Minor Allele (Frequency-based)

**Major allele** and **minor allele** are defined relative to **a specific population of a certain size**. The allele with the highest frequency is the major allele, and the one with the second highest frequency is the minor allele. For the most common bi-allelic SNPs, the two alleles have different frequencies - one is major and one is minor. For tri-allelic or quad-allelic SNPs (sites with three or four bases), the minor allele is the **second most frequent allele**.

**Key points:**

- The distinction between major and minor is based on **allele frequency in a specific population of a certain size**
- PLINK1.9 uses major and minor allele concepts. The software automatically calculates frequencies and may reorder alleles when processing raw data
- When using PLINK1.9's `--frq` option, the output shows MAF (minor allele frequency), which **will not exceed 0.5**
- In PLINK1.9, A1 is the minor allele and A2 is the major allele, so MAF refers to the frequency of A1 (minor allele)

**Example PLINK1.9 output:**
```
CHR    SNP    A1   A2          MAF  NCHROBS
1      SNP1    T    C       0.1258    10000
1      SNP2    A    G       0.1258    10000
```

---

### Second Group: Reference (ref) and Alternative (alt) Allele (Reference-genome-based)

**Reference allele** refers to the allele at that position in **a specific reference genome**. All other alleles at that position are called alternative alleles. **Note: reference and alternative alleles are unrelated to frequency - the only determining factor is the chosen reference genome**. While reference genome alleles are often major alleles, this is coincidental and should not be used to equate major and reference alleles. Some reference alleles can be minor alleles in a given population.

Unlike PLINK1.9, PLINK2 uses reference and alternative allele concepts. When processing data, it does not automatically reorder alleles based on frequency. When using PLINK2's `--frq` option, the output shows alternative allele frequency (not MAF), with **values ranging from [0,1]**.

**Example PLINK2 output:**
```
#CHROM	ID	REF	ALT	ALT_FREQS	OBS_CT
1	SNP1    	T	C	0.8742	10000
1	SNP2    	G	A	0.1258	10000
```

In PLINK2, reference and alternative alleles are clearly distinguished. For example, in the above SNPs:

- SNP1: T is the ref allele (from reference genome) but is the minor allele in this population, while C is the alt allele but is the major allele
- SNP2: G is the ref allele and major allele, while A is the alt allele and minor allele

**Tip:** You can align your data's ref and alt alleles with the corresponding reference genome using PLINK2:

```bash
plink2 \
       --bfile testfile \
       --ref-from-fa -fa hg19.fasta \
       --make-bed \
       --out testfile_fa
```

---

### Third Group: Reference and Risk/Effect Allele (Association-test-based)

This concept changes again. When "reference allele" is used alongside "risk/effect allele", it refers to the **reference allele in GWAS association testing (non-risk or non-effect allele)**, which is the reference group for estimating effect sizes (beta or odds ratio). However, some software may also use "reference allele" as the effect allele. This concept is independent of the ref/alt combination above, but for consistency, recent studies often align the reference allele in association testing with the reference genome to avoid confusion. **(Note: Early studies often used minor allele as the reference allele in association testing, which is a source of confusion.)** The concept of "reference allele" is very confusing - when distinguishing, don't focus on the name, but rather on what the effect size refers to.

**Risk allele** is straightforward - it's the allele that contributes to disease occurrence. In complex disease research, risk alleles are often minor alleles, but exceptions exist. The concept of **effect allele** is similar - it's the allele whose effect on disease or phenotype we want to study, so it's usually the allele that contributes to the phenotype or disease. The "effect" column in association test results refers to the effect of the effect allele.

---

## Additional Allele Naming Conventions

### Allele0 and Allele1

**Allele0** and **Allele1** use 0-indexed numbering:

- **Allele0**: Typically refers to the reference allele
- **Allele1**: Typically refers to the alternative allele

**Caveats:**

- The numbering is 0-indexed, where the reference allele is always index 0
- Alternative alleles are numbered sequentially (1, 2, 3... for multi-allelic sites)
- This convention does not indicate frequency - Allele0 may be major or minor depending on the population
- Always verify what Allele0 and Allele1 represent in your specific dataset or software

### Allele1 and Allele2 (A1/A2)

**A1** and **A2** are numeric designations for the two alleles at a bi-allelic site:

- **A1**: Often refers to the minor allele (lower frequency) in frequency-based systems
- **A2**: Often refers to the major allele (higher frequency) in frequency-based systems

**Caveats:**

- A1/A2 designation is often frequency-based and may differ from reference/alternative alleles
- Some software may automatically reorder alleles based on frequency, so A1/A2 do not necessarily correspond to reference/alternative alleles in the reference genome
- The meaning of A1/A2 can vary between software and datasets - always check the documentation or frequency information to understand which is which
- A1 is not always the minor allele - it depends on the convention used by the specific software or dataset

### Derived Allele

**Derived allele** is an evolutionary concept:

- **Derived allele**: The allele that arose from a mutation from the ancestral state
- **Ancestral allele**: The allele that was present in the common ancestor (often inferred from outgroup species)

**Caveats:**

- Derived alleles are not necessarily minor alleles - they can be major alleles in some populations
- The derived allele frequency (DAF) can range from 0 to 1, unlike MAF which is capped at 0.5
- The ancestral allele is often used as a proxy for the reference allele in some contexts, but they are distinct concepts - the reference genome may not always match the ancestral state
- Ancestral/derived information requires phylogenetic inference and may have uncertainty, especially for older mutations or when outgroup information is limited
- The same allele can be ancestral in one population but derived in another, depending on the evolutionary history

---

## Summary

Understanding these three groups of concepts will help you navigate allele terminology with confidence:

| Concept Group | Definition | Basis | Key Caveat |
|--------------|------------|-------|------------|
| **Major/Minor** | Major: highest frequency allele<br>Minor: second highest frequency allele | Frequency in a specific population | Population-specific; may differ from reference/alternative |
| **Reference/Alternative** | Reference: allele in reference genome<br>Alternative: other alleles at that position | Reference genome | Unrelated to frequency; reference may be minor in some populations |
| **Reference/Risk/Effect** | Reference: non-risk/non-effect allele (baseline)<br>Risk/Effect: allele with effect on phenotype | GWAS association testing context | Meaning varies by software; check effect size interpretation |

**Important reminders:**

| Common Misconception | Reality |
|---------------------|---------|
| Major = Reference | They can differ - reference is genome-based, major is frequency-based |
| Minor = Risk/Effect | They can differ - risk/effect is context-dependent |
| Reference allele meaning is consistent | Always check what effect size refers to in your software |
| Naming conventions are standardized | **Allele naming is highly inconsistent - always check source documentation** |
| - | Modern best practice: align reference allele in association testing with reference genome for consistency |

!!! warning "Critical Reminder"
    Due to the inconsistent naming conventions across software and databases, **always verify allele designations by checking the documentation of your specific data source or software**. Do not assume naming conventions are universal.
