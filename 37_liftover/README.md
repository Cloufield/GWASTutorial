# Liftover

This tutorial explains the basics of **liftover** and how to liftover **summary statistics (sumstats)** coordinates across different genome builds.

## Table of Contents

- [Liftover](#liftover)
- [Chain file](#chain-file)
  - [Format](#format)
  - [Meaning](#meaning)
  - [Example of a chain file (simplified)](#example-of-a-chain-file-simplified)
- [How chain file is created](#how-chain-file-is-created)
  - [Step 1: BLAT Alignment](#step-1-blat-alignment)
  - [Step 2: Chain/Net Construction](#step-2-chainnet-construction)
  - [Key Tools and Programs](#key-tools-and-programs)
  - [Notes](#notes)
- [How liftover is performed](#how-liftover-is-performed)
- [Liftover sumstats](#liftover-sumstats)
- [Scores](#scores)
- [Common reasons for liftover failures](#common-reasons-for-liftover-failures)
- [Why multiple hg19 positions liftover to the same hg38 position](#why-multiple-hg19-positions-liftover-to-the-same-hg38-position)
- [References](#references)

---

## Liftover

**Liftover** refers to the process of converting genomic coordinates from one reference genome build to another (e.g. **hg19 → hg38**), while preserving the underlying sequence correspondence as much as possible.

Liftover is required when:
- Datasets were generated using different genome builds
- Integrating GWAS summary statistics, annotations, or functional data
- Updating legacy analyses to newer reference genomes

Liftover operates purely at the **sequence-coordinate level**:
- It does **not** preserve gene annotations or biological interpretation
- It relies on precomputed whole-genome alignments between assemblies

---

## Chain file

A **chain file** encodes how two genome assemblies align to each other and is the core input required for liftover.

### Format
- File extension: `.chain` or `.chain.gz`
- Plain text, line-based format
- Produced by UCSC genome alignment pipelines

Each chain contains:
- A header line describing the source and target regions
- Multiple block lines describing aligned segments and gaps

### Meaning
A chain represents:
- A **colinear mapping** between a region in the source genome and a region in the target genome
- Allowing for:
  - Insertions
  - Deletions
  - Inversions
  - Assembly-specific differences


**Colinear mapping**: how two genomic regions correspond to each other while preserving linear order along the chromosome. If two positions A and B appear in a certain order in the source genome, they appear in the same relative order in the target genome (possibly on the opposite strand), with no rearrangement.

Formally:

Source: A → B → C

Target: A′ → B′ → C′
(or C′ → B′ → A′ if on the minus strand)


Key properties:
- One source interval ↔ one target interval
- Includes strand information
- Includes a score reflecting alignment quality

Chain files encode **sequence correspondence only**, not genes, SNP IDs, or annotations.

## Example of a chain file (simplified)

```text
chain 123456 chr1 249250621 + 100000 100700 chr1 248956422 + 100200 100900 950
300 10 15
200 5  0
100
```

| Field       | Meaning                  |
| ----------- | ------------------------ |
| `chain`     | Record type              |
| `123456`    | Chain ID                 |
| `chr1`      | Source chromosome        |
| `249250621` | Source chromosome length |
| `+`         | Source strand            |
| `100000`    | Source start (0-based)   |
| `100700`    | Source end               |
| `chr1`      | Target chromosome        |
| `248956422` | Target chromosome length |
| `+`         | Target strand            |
| `100200`    | Target start (0-based)   |
| `100900`    | Target end               |
| `950`       | Chain score              |

### Block lines

Each block line represents an aligned segment and the gaps following it.

```
chain 123456 chr1 249250621 + 100000 100700 chr1 248956422 + 100200 100900 950
300 10 15  <- this line
200 5  0
100
```
| Value | Meaning                   |
| ----- | ------------------------- |
| `300` | Aligned block size (bp)   |
| `10`  | Gap in source genome (bp) |
| `15`  | Gap in target genome (bp) |


```
chain 123456 chr1 249250621 + 100000 100700 chr1 248956422 + 100200 100900 950
300 10 15  
200 5  0  <- this line
100
```

| Value | Meaning            |
| ----- | ------------------ |
| `200` | Aligned block size |
| `5`   | Gap in source      |
| `0`   | No gap in target   |

```
chain 123456 chr1 249250621 + 100000 100700 chr1 248956422 + 100200 100900 950
300 10 15  
200 5  0  
100 <- this line
```

| Value | Meaning                                 |
| ----- | --------------------------------------- |
| `100` | Final aligned block (no following gaps) |


```
Source: chr1:100000 ──300bp── gap10 ──200bp── gap5 ──100bp──
Target: chr1:100200 ──300bp── gap15 ──200bp── gap0 ──100bp──
```

---

## How chain file is created

The chain file creation process involves two main steps: **BLAT alignment** and **chain/net construction**. The following describes the UCSC same-species liftover procedure:

### Step 1: BLAT Alignment

1. **Genome preparation**
   - Convert source and target genomes to **2bit format** (`.2bit`)
   - Generate chromosome size files using `twoBitInfo`

2. **Genome partitioning**
   - Partition both genomes into chunks (typically ~10 million bases each)
   - For small genomes: each chromosome remains in a single chunk
   - For large genomes: chromosomes may be split into multiple chunks
   - Tools: `partitionSequence.pl` from the kent source tree
   - Output: lists of coordinate ranges (`.lst` files)

3. **BLAT setup**
   - Create an **11.ooc file** (overlap-only count) for the target genome
   - This file helps BLAT skip repetitive regions efficiently
   - Calculated based on genome size and repeat content

4. **Pairwise BLAT alignment**
   - Run BLAT for each query chunk against each target chunk
   - Parameters: `-tileSize=11`, `-minScore=100`, `-minIdentity=98`, `-fastMap`
   - For large query chunks, further subdivide into ~5000 bp pieces for alignment
   - Output: **PSL files** (Pairwise Sequence Alignment format)
   - Each PSL file contains alignments between one query chunk and one target chunk

### Step 2: Chain/Net Construction

5. **Chaining step** (`axtChain`)
   - Convert PSL alignments to **raw chain files**
   - Group **colinear** alignment blocks from PSL files
   - Allow gaps caused by insertions and deletions
   - Preserve strand and order information
   - Parameters: `-linearGap=medium` (or `loose`/`tight` depending on genome similarity)
   - Output: raw chain files (one per chromosome/chunk)

6. **Chain merging and sorting**
   - Merge chains from all chunks using `chainMergeSort`
   - Assign unique chain IDs
   - Split merged chains into manageable files (e.g., 100 chains per file)
   - Output: sorted, merged chain files

7. **Netting step** (`chainNet`)
   - Resolve overlapping chains
   - Select the **best (primary) chain** per genomic region based on score
   - Retain secondary chains for duplications and paralogous regions
   - Requires chromosome size files for both genomes
   - Output: **net files** (`.net`) containing hierarchical chain relationships

8. **Primary chain extraction** (`netChainSubset`)
   - Extract primary chains from nets
   - Stitch chains together with consistent IDs using `chainStitchId`
   - Output: primary chain files ready for liftover

9. **Final chain file assembly**
   - Concatenate all primary chains
   - Compress to `.chain.gz` format
   - Output: **liftover-ready chain file** (e.g., `hg19ToHg38.over.chain.gz`)

### Key Tools and Programs

- **BLAT**: Fast sequence alignment tool for finding similar regions
- **axtChain**: Converts alignments (PSL/AXT) to chain format
- **chainMergeSort**: Merges and sorts chain files
- **chainNet**: Creates nets to resolve chain overlaps
- **netChainSubset**: Extracts primary chains from nets
- **chainStitchId**: Assigns consistent IDs to stitched chains

### Notes

- For **same-species** liftover: uses BLAT with high identity thresholds (98%+)
- For **cross-species** liftover: uses LASTZ or similar tools with different parameters
- The process is computationally intensive and may require cluster computing for large genomes
- Modern alternative: UCSC's `DoSameSpeciesLiftOver.pl` can automate the entire process

### References

- UCSC Genome Browser Wiki: **Chains and Nets**  
  https://genomewiki.ucsc.edu/index.php/Chains_Nets  
- UCSC Genome Browser Wiki: **Same species lift over construction**  
  https://genomewiki.ucsc.edu/index.php?title=Same_species_lift_over_construction  
- UCSC Genome Browser Wiki: **SameSpeciesChainNet.sh** (chain/net construction script)  
  https://genomewiki.ucsc.edu/images/d/d3/SameSpeciesChainNet.sh.txt  
- UCSC Genome Browser Wiki: **SameSpeciesBlatSetup.sh** (BLAT setup script)  
  https://genomewiki.ucsc.edu/images/9/91/SameSpeciesBlatSetup.sh.txt  
- UCSC Genome Browser Wiki: **BlatJob.csh** (BLAT job execution script)  
  https://genomewiki.ucsc.edu/images/f/fa/BlatJob.csh.txt

## How liftover is performed

Given:
- Input coordinates (e.g. SNP positions in sumstats)
- A chain file describing source → target genome alignment

The liftover tool:
1. Locates the chain covering the source coordinate
2. Identifies the aligned block within that chain
3. Applies offsets, strand changes, or inversions if needed
4. Outputs the corresponding coordinate in the target genome

If:
- No suitable chain exists, or
- The coordinate falls into an unaligned region  

→ the position **fails liftover** and should be reported or filtered.

Common tools:
- UCSC `liftOver`
- CrossMap
- Picard `LiftoverVcf`

---

## Liftover sumstats

**Summary statistics (sumstats)** from GWAS and other association studies often need to be lifted over when.


## Scores

Each chain has a **score** that reflects alignment reliability.

Score components typically include:
- Number of aligned bases
- Match/mismatch quality
- Penalties for gaps and rearrangements

Why scores matter:
- A region may appear in multiple chains (e.g. duplications)
- Liftover uses the **highest-scoring compatible chain**
- Lower-scoring chains are treated as secondary mappings

High score ≠ biological correctness  
It only reflects **sequence-level similarity**.

---

## Common reasons for liftover failures

Why Liftover Fails: hg19 → hg38 as an example (Practical Explanation)

Liftover fails when a genomic coordinate or interval cannot be mapped
**uniquely, confidently, and consistently** from hg19 to hg38 using a chain file.
Below are the most common hg19 → hg38-specific causes, especially relevant for GWAS.

---

### 1. No valid alignment chain (missing coverage)

Some hg19 regions do not have a corresponding alignment in hg38 due to:
- Assembly redesigns
- Removed or restructured sequences
- Unresolved regions in either build

Typical locations:
- Pericentromeric regions
- Telomeres
- Assembly gaps

**Result:** No chain → liftover failure.

---

### 2. Centromere and gap redefinition in hg38

hg38 significantly improved:
- Centromere modeling
- Gap placement
- Chromosome continuity

Variants near hg19 centromeres or gaps may:
- Fall into regions that were shifted or removed
- Lose positional correspondence

**Very common cause of failure in GWAS summary statistics.**

---

### 3. Ambiguous mapping due to segmental duplications

hg38 better represents:
- Segmental duplications
- Repetitive and paralogous regions

An hg19 coordinate may map to:
- Multiple hg38 loci
- Different chromosomes or alt loci

Liftover tools may **discard multi-mapping variants**.

Common examples:
- Immune gene clusters
- Olfactory receptor regions
- Subtelomeric segments

---

### 4. ALT contigs and decoy sequences (hg38-specific)

hg38 introduced many:
- ALT contigs (e.g., HLA)
- Fix patches
- Decoy sequences

If:
- The chain file excludes ALT contigs, or
- The tool ignores them by default,

valid mappings may be **dropped**.

hg19 had far fewer ALT loci, making this a hg19 → hg38-specific issue.

### 5. Coordinate system boundary issues (0-based vs 1-based, inclusive vs half-open)

This is a *pipeline/format* failure mode rather than an assembly difference.

Different genomics formats use different coordinate conventions:
- **VCF**: 1-based POS, REF anchored at POS
- **BED**: 0-based start, **half-open** interval `[start, end)`
- Many liftover tools assume BED-like semantics for intervals

If you accidentally liftover VCF-style coordinates as BED (or vice versa),
you can shift positions by 1 bp or move intervals across boundaries.

### Example: off-by-one on a SNP (BED vs VCF)

Suppose the true SNP is:
- VCF (hg19): `chr1:100` (1-based)

Correct BED representation of a single base would be:
- BED (hg19): `chr1 99 100`  (0-based, end-exclusive)

**Common mistake:** using `chr1 100 101` (treating 100 as 0-based)
- This represents hg19 VCF position 101, not 100.

**Consequence after liftover:**
- The position is shifted by +1 bp in hg38
- If you later validate alleles, REF may mismatch and be flagged as “failed”

### Example: boundary crossing causes drop (interval liftover)

A BED interval:
- hg19: `chr1 1000 1100`

If the hg19→hg38 chain has a breakpoint at 1050, the interval might split:
- Part A: 1000–1050 maps
- Part B: 1050–1100 does not map (or maps elsewhere)

Tools that require high fraction mapping (e.g., `minMatch=0.95`) may **drop**
the whole interval because only 50/100 bp could be mapped contiguously.

**Result:** interval liftover failure due to boundary semantics + chain breakpoint.

---

## Why multiple hg19 positions liftover to the same hg38 position

This situation is **expected** and reflects real assembly differences,
not a software bug. Below are the main mechanisms **with concrete toy examples**.

> Notation:
> - hg19 positions are 1-based single-base coordinates.
> - “→” denotes the liftover result in hg38.
> - Examples are schematic (illustrative), not specific loci.

---

### 1. Collapsed or shortened regions in hg38 (assembly correction)

hg38 fixed regions that were:
- Over-expanded
- Redundant
- Misassembled

When hg19 had extra or duplicated bases that were removed in hg38, multiple hg19
coordinates can land on the same hg38 coordinate because hg38 is effectively
"shorter" there.

**Toy example (collapse of a duplicated segment):**

```text
hg19 sequence (misassembled / duplicated):
... A B C [D E F] [D E F] G H ...
        ^ copy1    ^ copy2

hg38 sequence (corrected, only one copy retained):
... A B C [D E F] G H ...
```

Example coordinate behavior (schematic):
- hg19:pos=1000 (D in copy1) → hg38:pos=2000 (D)
- hg19:pos=1003 (D in copy2) → hg38:pos=2000 (D)  ✅ many-to-one

**Effect:** many-to-one mapping because hg19 had “extra” bases/segments that do not
exist as distinct positions in hg38.

---

### 2. Repeat compression and duplication resolution (multi-copy ambiguity → one locus)

hg19 contained:
- Collapsed repeats or inaccurate copy counts
- Hard-to-place duplicated sequence

hg38:
- Improves representation and alignment of repetitive sequence
- May “merge” the best-supported mapping for some chains (or your pipeline may
  later collapse them during normalization/dedup)

This can produce apparent many-to-one outcomes, especially when repeats align
equally well.

**Toy example (two nearly identical repeat copies in hg19 align to one best locus in hg38):**

```text
hg19:
... [ATATATAT] ........ [ATATATAT] ...
    R1                  R2

hg38 (or the chain’s best-supported mapping):
... [ATATATAT] ...
    R
```

Example coordinate behavior:
- hg19:pos=50010 (A in R1) → hg38:pos=80010 (A)
- hg19:pos=90010 (A in R2) → hg38:pos=80010 (A)  ✅ many-to-one

**Practical note:**
- Some liftover tools would instead flag this as **ambiguous** (multi-mapping) and
  drop one/both.
- Many-to-one often appears after **post-liftover dedup/normalization**, even if the
  raw tool output differed.

---

### 3. Indels and coordinate compression (adjacent hg19 bases map onto one hg38 base)

Insertions/deletions between builds can cause:
- Several adjacent hg19 bases to map onto one hg38 base
- Common near indels or low-complexity sequence

This is normal behavior for chain-based alignments because alignments include
gaps; at a gap boundary, multiple source positions may correspond to the same
target anchor.

#### 3.1 Deletion in hg38 (hg19 has extra bases)

```text
hg19:
... A C T [G G G] T A ...
        ^ extra in hg19

hg38 (deletion of "GGG"):
... A C T T A ...
```

Schematic mapping around the deleted block:
- hg19:pos=1200 (last base before deleted block) → hg38:pos=3400
- hg19:pos=1201 (G) → hg38:pos=3400
- hg19:pos=1202 (G) → hg38:pos=3400
- hg19:pos=1203 (G) → hg38:pos=3400
- hg19:pos=1204 (first base after block) → hg38:pos=3401

Here, several hg19 positions “pile up” onto the same hg38 coordinate at the
alignment anchor. ✅ many-to-one

#### 3.2 Different variant representations collapse after normalization

Two hg19 indel representations:
- Variant A: pos=100, REF=AT, ALT=A  (delete T)
- Variant B: pos=101, REF=T,  ALT=-  (same deletion, different representation)

After liftover + left-normalization on hg38:
- Both may become: pos=500, REF=AT, ALT=A

This looks like “two hg19 positions → one hg38 position”, but the real cause is
**representation/normalization**, not necessarily chain compression.

---

### Practical implication (GWAS / VCF)

If you observe many-to-one mappings:
- **Deduplicate after liftover** using a stable key (CHR:POS:REF:ALT after
  normalization).
- **Prefer keeping the record with consistent alleles / highest INFO / smallest SE**
  (project-dependent).
- Optionally **flag** these sites as non-unique to avoid double-counting signals.


### Practical summary (hg19 → hg38)

Most liftover failures in practice come from:

1. Centromeric or repetitive regions
2. Ambiguous mappings in duplicated loci
3. Indels with reference allele mismatch
4. Chromosome naming or build mismatch
5. ALT-contig-related filtering

These failures are expected and should be treated as
**assembly differences, not data errors**.


## References

- Kent WJ et al. *The Human Genome Browser at UCSC*. Genome Research, 2002.  
- Kent WJ et al. *The UCSC Genome Browser Database: update papers*. Nucleic Acids Research.  
- UCSC Genome Browser Wiki: **Chains and Nets**  
  https://genomewiki.ucsc.edu/index.php/Chains_Nets  
- UCSC Genome Browser Wiki: **Same species lift over construction**  
  https://genomewiki.ucsc.edu/index.php?title=Same_species_lift_over_construction  
- UCSC Genome Browser Wiki: **SameSpeciesChainNet.sh** (chain/net construction script)  
  https://genomewiki.ucsc.edu/images/d/d3/SameSpeciesChainNet.sh.txt  
- UCSC Genome Browser Wiki: **SameSpeciesBlatSetup.sh** (BLAT setup script)  
  https://genomewiki.ucsc.edu/images/9/91/SameSpeciesBlatSetup.sh.txt  
- UCSC Genome Browser Wiki: **BlatJob.csh** (BLAT job execution script)  
  https://genomewiki.ucsc.edu/images/f/fa/BlatJob.csh.txt  
- Zhao H et al. *A comprehensive evaluation of genome coordinate liftover tools*. NAR Genomics and Bioinformatics, 2020.