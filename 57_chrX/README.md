

# chrX, chrY and chrMT

Sex chromosomes require special handling in GWAS because **ploidy differs by sex and by genomic region**. This section summarizes notation, PAR regions, sex checks, and dosage scaling, with a focus on PLINK / regenie workflows.

## Table of Contents

- [PAR and Non-PAR](#par-and-non-par)
- [Chromosome encoding](#chromosome-encoding)
- [Check sex by X chromosome inbreeding coefficients](#check-sex-by-x-chromosome-inbreeding-coefficients)
- [Dosage rescaling for GWAS](#dosage-rescaling-for-gwas)

---



## PAR and Non-PAR

### What is PAR?

**PAR (Pseudoautosomal Regions)** are homologous regions shared between **chrX and chrY**:
- Recombine during meiosis
- Behave like autosomes
- **Diploid in both males and females**

**Non-PAR regions**:
- X-specific or Y-specific
- **Different ploidy between sexes**

![chrX/chrY PAR regions](../docs/images/chrXY_PAR_regions.png)

---

### Genomic coordinates

#### hg19

| Region | Coordinates |
|------|------------|
| PAR1 | chrX: 60,001 – 2,699,520 |
| PAR2 | chrX: 154,931,044 – 155,260,560 |

#### hg38

| Region | Coordinates |
|------|------------|
| PAR1 | chrX: 10,001 – 2,781,479 |
| PAR2 | chrX: 155,701,383 – 156,030,895 |

Everything **outside PAR1 + PAR2** is **Non-PAR chrX**.

---

### Practical implications

| Region | Male ploidy | Female ploidy | Treat as |
|------|-------------|---------------|----------|
| PAR | 2 | 2 | Autosomal |
| Non-PAR chrX | 1 | 2 | Sex-specific |
| chrY | 1 | 0 | Male-only |
| chrMT | variable | variable | Special |

---

### Splitting and merging PAR in PLINK 2

PLINK 2 represents PAR as **PAR1** and **PAR2** chromosome codes (instead of PLINK 1.x's `XY`). Use `--split-par` to split chrX variants in PAR regions:

```bash
# Using build code (recommended)
plink2 --bfile data --split-par hg38 --make-bed --out data_split

# Or specify boundaries manually
plink2 --bfile data --split-par 2781479 155701383 --make-bed --out data_split
```

**Supported build codes:**

| Build | PAR1 end | PAR2 start |
|-------|----------|------------|
| b36 / hg18 | 2,709,521 | 154,584,237 |
| b37 / hg19 | 2,699,520 | 154,931,044 |
| b38 / hg38 | 2,781,479 | 155,701,383 |
| chm13 | 2,394,410 | 153,925,835 |

**Related commands:**

| Command | Description |
|---------|-------------|
| `--split-par <build>` | Split chrX into PAR1/PAR2 + non-PAR |
| `--merge-par` | Merge PAR1/PAR2 back to chrX |
| `--merge-x` | Convert PLINK 1.x `XY` codes back to `X` (use with `--sort-vars`) |

Reference: [PLINK 2.0 --split-par](https://www.cog-genomics.org/plink/2.0/data#split_par)

---

## Chromosome encoding

Different standards use **different numeric chromosome codes** for sex chromosomes and mitochondrial DNA.  
It is important to distinguish **GWAS summary statistics conventions** from **PLINK’s internal chromosome numbering**, as they are *not identical*.

| Chromosome (concept) | GWAS-SSF | PLINK 1.9 |
|---------------------|----------|-----------|
| X (non-PAR)         | 23       | 23 or X   |
| Y                  | 24        | 24 or Y   |
| PAR (X/Y regions)  | 23 or 24  | 25 or XY  |
| MT                 | 25        | 26 or MT  |

### Explanation

- **GWAS-SSF**
  - The `chromosome` field must be an **integer**
  - Uses a fixed convention:
    - X = 23
    - Y = 24
    - MT = 25
  - There is **no separate XY/PAR chromosome code** in GWAS-SSF
  - Summary statistics should always be exported using these numeric values

- **PLINK 1.9**
  - Supports both **string labels** (`X`, `Y`, `XY`, `MT`) and **numeric codes**
  - Numeric codes depend on the number of autosomes (`n`)
    - For humans, `n = 22`
    - Therefore:
      - X = 22 + 1 = 23
      - Y = 22 + 2 = 24
      - XY (PAR) = 22 + 3 = 25
      - MT = 22 + 4 = 26
  - The `XY` chromosome represents **pseudo-autosomal regions (PAR)**, which PLINK treats as autosomal-like

⚠️ Because PLINK and GWAS-SSF use **different numeric codes for MT**, numeric chromosome values should **never be copied blindly** from PLINK files into GWAS summary statistics.

---

### Recommended practice

- In **PLINK commands**, prefer **string-based chromosome names** (`X`, `Y`, `XY`, `MT`) for clarity and portability
- In **GWAS summary statistics**, always convert to **GWAS-SSF numeric encoding**
- Treat **XY/PAR variants** explicitly when splitting chrX into PAR vs non-PAR regions

---

### PLINK example

```bash
plink --bfile data --chr 1-22,X,Y,XY,MT
```

This command selects:

- Autosomes (1–22)
- Non-PAR chrX (`X`)
- chrY (`Y`)
- Pseudo-autosomal regions (`XY`)
- Mitochondrial DNA (`MT`)


## Check sex by X chromosome inbreeding coefficients

Sex inference is typically done via **X-chromosome heterozygosity**.

### plink --check-sex

plink --bfile data --check-sex

- Computes **X-chromosome inbreeding coefficient (F)**

The typical pattern is:

- Genetic male (XY): F close to 1 (because X is effectively hemizygous → almost no heterozygosity)
- Genetic female (XX): F close to 0 (normal diploid heterozygosity)


Note that it’s not exactly “male=1, female=0” in real data:

- boundaries are usually threshold-based (e.g., PLINK uses cutoffs like ~0.8 / ~0.2 by default in many setups; exact defaults can vary by PLINK version/options).
- values can drift due to genotyping errors, low call rate, aneuploidy (XXY, XO), sex chromosome mosaicism, or population structure / unusual X heterozygosity.

---

### plink --impute-sex

plink --bfile data --impute-sex

- Infers sex from chrX genotypes
- Writes inferred sex into `.fam` / `.psam`

---

## Dosage rescaling for GWAS

### Core question

Should chrX dosages be on **0–1** or **0–2** scale?

**Answer:** PLINK-style genotype storage uses **0–2 encoding**, even for haploid males.

---

### PLINK encoding rules

`.bed` and `.pgen` files use **0/2 encoding for haploid genotypes**.

| Sample | True ploidy | Stored values |
|------|-------------|---------------|
| Female (XX) | Diploid | 0, 1, 2 |
| Male (X) | Haploid | 0 or 2 |

!!! qoute
    https://groups.google.com/g/plink2-users/c/hPCgYtpCy0M/m/xwZifVK5AQAJ?pli=1




# Reference

- **GWAS-SSF (GWAS Summary Statistics Format)**: [https://github.com/EBISPOT/gwas-summary-statistics-standard](https://github.com/EBISPOT/gwas-summary-statistics-standard)
- **PLINK 1.9 --check-sex**: [https://www.cog-genomics.org/plink/1.9/basic_stats#check_sex](https://www.cog-genomics.org/plink/1.9/basic_stats#check_sex)
- **PLINK 2.0 --check-sex**: [https://www.cog-genomics.org/plink/2.0/basic_stats#check_sex](https://www.cog-genomics.org/plink/2.0/basic_stats#check_sex)
- **UCSC chrX**: [https://genome.ucsc.edu/cgi-bin/hgTracks?db=hg38&position=chrX](https://genome.ucsc.edu/cgi-bin/hgTracks?db=hg38&position=chrX)
- **UCSC chrY**: [https://genome.ucsc.edu/cgi-bin/hgTracks?db=hg38&position=chrY](https://genome.ucsc.edu/cgi-bin/hgTracks?db=hg38&position=chrY)
- **Ensembl Human chrX**: [https://www.ensembl.org/Homo_sapiens/Location/Chromosome?r=X](https://www.ensembl.org/Homo_sapiens/Location/Chromosome?r=X)
- **Ensembl Human chrY**: [https://www.ensembl.org/Homo_sapiens/Location/Chromosome?r=Y](https://www.ensembl.org/Homo_sapiens/Location/Chromosome?r=Y)
