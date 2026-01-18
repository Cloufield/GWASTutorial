# Relatedness and sample structure

Relatedness and sample structure can inflate test statistics and bias effect estimates if not handled properly. Proper identification and handling of related individuals is crucial for valid GWAS inference.

---

## Why it matters

- **Violation of independence**: Closely related individuals violate the independence assumptions underlying standard association tests
- **Inflated test statistics**: Cryptic relatedness can lead to inflated test statistics and false positive associations
- **Hidden structure**: Unrecognized familial relationships can mimic association signals
- **Population stratification**: Family structure can confound with population structure
- **Different models required**: Family-based designs require specialized statistical models

---

## Key concepts

### Kinship coefficient

The **kinship coefficient** (φ) measures the probability that two alleles sampled at random from two individuals are identical by descent (IBD). It ranges from 0 (unrelated) to 0.5 (identical).

For a pair of individuals, the kinship coefficient can be calculated as:

$$\phi_{ij} = \frac{1}{2}\mathbb{P}(\text{IBD}_1) + \mathbb{P}(\text{IBD}_2)$$

where:

- $\mathbb{P}(\text{IBD}_0)$: probability of sharing 0 alleles IBD
- $\mathbb{P}(\text{IBD}_1)$: probability of sharing 1 allele IBD  
- $\mathbb{P}(\text{IBD}_2)$: probability of sharing 2 alleles IBD

### Relatedness coefficient

The **relatedness coefficient** ($r$) is a scaled version of kinship:

$$r_{ij} = 2\phi_{ij}$$

It is often used as an intuitive measure of how closely related two individuals are (e.g., $r \approx 0.5$ for first-degree relatives).

### Inbreeding coefficient

The **inbreeding coefficient** ($F$) measures the probability that the two alleles at a locus within an individual are IBD due to shared ancestry of the parents. It can be interpreted as self-relatedness beyond the baseline:

$$F_i = 2\phi_{ii} - 1$$

where $\phi_{ii}$ is the diagonal of the kinship matrix (self-kinship).

**Self-kinship** ($\phi_{ii}$) is the kinship coefficient of an individual with themselves. It measures the probability that two alleles sampled at random from the same individual are identical by descent (IBD). 

- For an **outbred individual** (no inbreeding): $\phi_{ii} = 0.5$, meaning the two alleles have a 50% chance of being IBD simply because they come from the same individual. This is the baseline self-kinship.
- For an **inbred individual**: $\phi_{ii} > 0.5$, because the two alleles have an increased probability of being IBD due to shared ancestry of the parents (e.g., if the parents are related).

For an outbred individual, $\phi_{ii} \approx 0.5$, so $F \approx 0$. As inbreeding increases, $\phi_{ii}$ exceeds 0.5 and $F$ becomes positive, linking inbreeding directly to elevated self-kinship.

### Identity by Descent (IBD)

**Identity by Descent (IBD)** refers to alleles that are identical because they were inherited from a common ancestor. Two alleles can be:

- **IBD = 0**: No alleles shared IBD
- **IBD = 1**: One allele shared IBD
- **IBD = 2**: Both alleles shared IBD (homozygous for the same allele from common ancestor)

### IBD vs IBS

**Identity by State (IBS)** refers to alleles that are the same in observed sequence or genotype, regardless of ancestry. IBS can occur without shared ancestry, especially for common alleles.

**Comparison**

- **IBD**: same because of inheritance from a recent common ancestor
- **IBS**: same in observed state, ancestry may be unrelated
- **Use in practice**: IBS is observed directly; IBD is inferred from IBS patterns across many markers

### Genetic relationship matrix (GRM)

The **genetic relationship matrix** (also called kinship matrix) is an $n \times n$ symmetric matrix where element $(i,j)$ contains the kinship coefficient between individuals $i$ and $j$. The diagonal elements represent self-kinship (typically $0.5 + F_i/2$).

---

## Interpreting coefficients

### Typical kinship thresholds

!!! note "KING scaling convention"
    **KING kinship coefficients are scaled such that duplicate samples have kinship 0.5, not 1.** This scaling is used by both KING and PLINK2 (via `--make-king-table`). In KING/PLINK2:

    - Duplicate samples: kinship = 0.5
    - First-degree relations: kinship ≈ 0.25
    - Second-degree relations: kinship ≈ 0.125
    - Third-degree relations: kinship ≈ 0.0625
    
    Conventional KING/PLINK2 cutoffs:

    - **~0.354** (geometric mean of 0.5 and 0.25): screen for monozygotic twins and duplicate samples
    - **~0.177** (geometric mean of 0.25 and 0.125): identify first-degree relations
    - **~0.088** (geometric mean of 0.125 and 0.0625): identify second-degree relations
    
    **PLINK2 commands:**
    - `plink2 --bfile data --make-king-table`: generates KING kinship estimates
    - `plink2 --bfile data --king-cutoff <threshold>`: filters related individuals based on KING kinship threshold

---

## Duplicate handling

Duplicate samples (same individual genotyped multiple times) and monozygotic (MZ) twins must be identified and handled before analysis. Both have identical genotypes and can cause similar issues in GWAS.

**Types to identify:**

- **Duplicate samples**: The same individual genotyped multiple times (technical duplicates)
- **Monozygotic (MZ) twins**: Genetically identical twins (share 100% of their DNA)
- **Dizygotic (DZ) twins**: Fraternal twins (genetically like full siblings, kinship ≈ 0.25)

!!! note "MZ twins vs duplicates"
    MZ twins are genetically identical and should be treated similarly to duplicates in population-based GWAS. However, they are different individuals and may be intentionally included in family-based designs. DZ twins are first-degree relatives and should be handled according to your relatedness filtering strategy.

### Detection

- **General tools**: Kinship coefficient > 0.45 (or relatedness > 0.9)
- **KING**: Kinship coefficient > 0.354 (conventional cutoff for duplicates/MZ twins)
- High concordance rate (> 99%) across all SNPs
- Same or very similar sample IDs

---

## Handling related individuals

### Population GWAS (unrelated samples)

**Option 1: Remove close relatives**

- Remove one individual from each related pair
- Typically remove individuals with kinship > 0.088 (second-degree) or > 0.044 (more stringent; between third- and fourth-degree), depending on design
- Keep the individual with higher call rate or more complete phenotype data
- Simplest approach, but reduces sample size

**Option 2: Use Linear Mixed Models (LMMs)**

- Model relatedness through genetic relationship matrix
- Accounts for covariance structure
- Can include all individuals
- More complex but preserves sample size

**Option 3: Stratified analysis**

- Analyze related and unrelated samples separately
- Combine results using meta-analysis

### Family-based GWAS

Family-based designs explicitly recruit related individuals and use specialized methods:

**Advantages**

- Robust to population stratification
- Clearer causal interpretation (within-family comparisons)
- Can detect parent-of-origin effects

**Methods**

- **TDT (Transmission Disequilibrium Test)**: Tests for association using transmission from heterozygous parents
- **Family-based association tests (FBAT)**: General framework for family-based association
- **Family-based LMM**: Extends LMM to account for family structure
- **Conditional analysis**: Conditions on parental genotypes

**Considerations**

- Lower power than population-based GWAS (fewer independent tests)
- Requires family structure information
- More complex analysis pipeline
