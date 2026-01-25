# 0-based vs 1-based Genome Coordinate Systems

Genomic coordinates specify **positions along a chromosome**.  
Different tools use different conventions, which is a common source of **off-by-one errors**.

This guide explains:

- what **0-based** and **1-based** coordinates mean  
- where each system is used  
- how to **convert safely** between them  

---

## What are Genomic Coordinates?

Genomic coordinates are typically specified as a set of:

- **Chromosome name** (e.g., `chr1`, `chr2`, `chrX`)
- **Start position** (the beginning of the feature)
- **End position** (the end of the feature)
- **Strand** (`+` for forward strand, `-` for reverse strand, `.` for unstranded features)

!!! note "Start and End Coordinates"
    In the vast majority of annotation formats, the **start coordinate refers to the lowest-numbered (leftmost) coordinate relative to the genome**, not relative to the feature itself. This means:

    - For **forward-strand features**: start is the 5' end, end is the 3' end
    - For **reverse-strand features**: start is actually the 3' end (leftmost on the chromosome), end is the 5' end (rightmost on the chromosome)


## 1-based Coordinates (Human-friendly)

**Definition**

- First nucleotide is **1**
- Both **start and end are included** → `[start, end]`

!!! example "Example"
    ```
    chr1:1-10
    ```
    
    - Includes bases **1 through 10**  
    - Length = **10 bases**

Common formats:

- VCF
- GFF / GTF
- Ensembl
- UCSC web interface
- **GWAS Sumstats**

!!! note "GWAS Summary Statistics"
    GWAS summary statistics are typically **1-based** because they are derived from genotype data stored in VCF files (which use 1-based coordinates) or related formats like PGEN/BGEN/BED.


---

## 0-based Coordinates (Computer-friendly)

**Definition**

- First nucleotide is **0**
- Start included, end excluded → `[start, end)`

!!! example "Example"
    ```
    chr1 0 10
    ```
    
    - Includes bases **0 through 9** (which correspond to bases 1-10 in 1-based)  
    - Length = `10 − 0 = 10`

!!! note ""
    **Format notation varies by coordinate system:**
    
    - **1-based formats** typically use colon-dash notation: `chr1:1-10` (represents bases 1-10)
    - **0-based formats** often use space-separated notation (e.g., UCSC BED format): `chr1 0 10` (represents bases 1-10, positions 0-9 in 0-based)
    
    While the notation differs, both examples above describe the same 10-base genomic region. The key is understanding which coordinate system (0-based or 1-based) is being used by the format, as this determines how to interpret the coordinates.



Common formats:

- BED (not Plink bed format)
- BAM
- UCSC tables
- UCSC chain files


!!! info "Four Possible Coordinate Representations"
    Because coordinate systems can be **0-indexed or 1-indexed**, and **half-open or fully-closed**, genomic features can be represented in **four possible ways**:

    | **Half-open** | **Fully-closed** |
    |---------------|------------------|
    | **0-indexed** | start: 11, end: 17 | start: 11, end: 16 |
    | **1-indexed** | start: 12, end: 18 | start: 12, end: 17 |

    For example, a 6-base feature starting at the 12th nucleotide:
    - **0-indexed, half-open**: `[11, 17)` → length = 17 - 11 = 6
    - **0-indexed, fully-closed**: `[11, 16]` → length = 16 - 11 + 1 = 6
    - **1-indexed, half-open**: `[12, 18)` → length = 18 - 12 = 6
    - **1-indexed, fully-closed**: `[12, 17]` → length = 17 - 12 + 1 = 6

    All four representations describe the same biological feature, just using different counting conventions.

---


## Comparison between **1-based** and **0-based**

The following table summarizes the key differences between 1-based and 0-based coordinate systems:

| Aspect | **1-based** | **0-based** |
|--------|-------------|-------------|
| First base | 1 | 0 |
| Interval type | Fully closed `[start, end]` | Half-open `[start, end)` |
| Start included | Yes | Yes |
| End included | Yes | No |
| Length formula | `end − start + 1` | `end − start` |
| Mental model | Counting bases | Array indices / gaps |


**1-based coordinates** label the <span style="color: #1E90FF; font-weight: bold;">nucleotides themselves</span>, while **0-based coordinates** label the <span style="color: #8B0000; font-weight: bold;">positions between nucleotides (gaps)</span>.

**Key insights:**

- Every base is flanked by two gaps
- There is a gap before the first base and after the last base
- This is why 0-based intervals exclude the end position and are written as **half-open** `[start, end)`

---

### Representations with a Concrete Sequence

<table style="border-collapse: collapse; font-size: 14px;">
<tr>
<td style="border: 1px solid #ddd; padding: 4px 8px; text-align: center;"><b>Sequence</b></td>
<td style="border: 1px solid #ddd; padding: 4px 8px; text-align: center;"></td>
<td style="border: 1px solid #ddd; padding: 4px 8px; text-align: center; color: black; font-weight: bold;">A</td>
<td style="border: 1px solid #ddd; padding: 4px 8px; text-align: center;"></td>
<td style="border: 1px solid #ddd; padding: 4px 8px; text-align: center; color: black; font-weight: bold;">T</td>
<td style="border: 1px solid #ddd; padding: 4px 8px; text-align: center;"></td>
<td style="border: 1px solid #ddd; padding: 4px 8px; text-align: center; color: black; font-weight: bold;">G</td>
<td style="border: 1px solid #ddd; padding: 4px 8px; text-align: center;"></td>
<td style="border: 1px solid #ddd; padding: 4px 8px; text-align: center; color: black; font-weight: bold;">C</td>
<td style="border: 1px solid #ddd; padding: 4px 8px; text-align: center;"></td>
<td style="border: 1px solid #ddd; padding: 4px 8px; text-align: center; color: black; font-weight: bold;">A</td>
<td style="border: 1px solid #ddd; padding: 4px 8px; text-align: center;"></td>
</tr>
<tr>
<td style="border: 1px solid #ddd; padding: 4px 8px; text-align: center;"><b>Type</b></td>
<td style="border: 1px solid #ddd; padding: 4px 8px; text-align: center; color: #8B0000; font-weight: bold;">Gap</td>
<td style="border: 1px solid #ddd; padding: 4px 8px; text-align: center; color: #1E90FF; font-weight: bold;">Base</td>
<td style="border: 1px solid #ddd; padding: 4px 8px; text-align: center; color: #8B0000; font-weight: bold;">Gap</td>
<td style="border: 1px solid #ddd; padding: 4px 8px; text-align: center; color: #1E90FF; font-weight: bold;">Base</td>
<td style="border: 1px solid #ddd; padding: 4px 8px; text-align: center; color: #8B0000; font-weight: bold;">Gap</td>
<td style="border: 1px solid #ddd; padding: 4px 8px; text-align: center; color: #1E90FF; font-weight: bold;">Base</td>
<td style="border: 1px solid #ddd; padding: 4px 8px; text-align: center; color: #8B0000; font-weight: bold;">Gap</td>
<td style="border: 1px solid #ddd; padding: 4px 8px; text-align: center; color: #1E90FF; font-weight: bold;">Base</td>
<td style="border: 1px solid #ddd; padding: 4px 8px; text-align: center; color: #8B0000; font-weight: bold;">Gap</td>
<td style="border: 1px solid #ddd; padding: 4px 8px; text-align: center; color: #1E90FF; font-weight: bold;">Base</td>
<td style="border: 1px solid #ddd; padding: 4px 8px; text-align: center; color: #8B0000; font-weight: bold;">Gap</td>
</tr>
<tr>
<td style="border: 1px solid #ddd; padding: 4px 8px; text-align: center;"><b><span style="color: #1E90FF;">1-based</span></b></td>
<td style="border: 1px solid #ddd; padding: 4px 8px; text-align: center;"></td>
<td style="border: 1px solid #ddd; padding: 4px 8px; text-align: center; color: #1E90FF; font-weight: bold;">1</td>
<td style="border: 1px solid #ddd; padding: 4px 8px; text-align: center;"></td>
<td style="border: 1px solid #ddd; padding: 4px 8px; text-align: center; color: #1E90FF; font-weight: bold;">2</td>
<td style="border: 1px solid #ddd; padding: 4px 8px; text-align: center;"></td>
<td style="border: 1px solid #ddd; padding: 4px 8px; text-align: center; color: #1E90FF; font-weight: bold;">3</td>
<td style="border: 1px solid #ddd; padding: 4px 8px; text-align: center;"></td>
<td style="border: 1px solid #ddd; padding: 4px 8px; text-align: center; color: #1E90FF; font-weight: bold;">4</td>
<td style="border: 1px solid #ddd; padding: 4px 8px; text-align: center;"></td>
<td style="border: 1px solid #ddd; padding: 4px 8px; text-align: center; color: #1E90FF; font-weight: bold;">5</td>
<td style="border: 1px solid #ddd; padding: 4px 8px; text-align: center;"></td>
</tr>
<tr>
<td style="border: 1px solid #ddd; padding: 4px 8px; text-align: center;"><b><span style="color: #8B0000;">0-based</span></b></td>
<td style="border: 1px solid #ddd; padding: 4px 8px; text-align: center; color: #8B0000; font-weight: bold;">0</td>
<td style="border: 1px solid #ddd; padding: 4px 8px; text-align: center;"></td>
<td style="border: 1px solid #ddd; padding: 4px 8px; text-align: center; color: #8B0000; font-weight: bold;">1</td>
<td style="border: 1px solid #ddd; padding: 4px 8px; text-align: center;"></td>
<td style="border: 1px solid #ddd; padding: 4px 8px; text-align: center; color: #8B0000; font-weight: bold;">2</td>
<td style="border: 1px solid #ddd; padding: 4px 8px; text-align: center;"></td>
<td style="border: 1px solid #ddd; padding: 4px 8px; text-align: center; color: #8B0000; font-weight: bold;">3</td>
<td style="border: 1px solid #ddd; padding: 4px 8px; text-align: center;"></td>
<td style="border: 1px solid #ddd; padding: 4px 8px; text-align: center; color: #8B0000; font-weight: bold;">4</td>
<td style="border: 1px solid #ddd; padding: 4px 8px; text-align: center;"></td>
<td style="border: 1px solid #ddd; padding: 4px 8px; text-align: center; color: #8B0000; font-weight: bold;">5</td>
</tr>
</table>


---

### Comparison Table (Using the Same Sequence)

| Feature Type | Example | 1-based Representation | 0-based Representation | Selected Bases |
|--------------|---------|------------------------|------------------------|----------------|
| Single nucleotide | Base at position 3 | `chr1:3-3` | `chr1 2 3` | G |
| Range | Bases 2–4 | `chr1:2-4` | `chr1 1 4` | T G C |
| SNP | G→A at position 3 | `chr1:3-3` | `chr1 2 3` | Position 3 |
| Deletion | Delete positions 2–3 | `chr1:2-3` | `chr1 1 3` | Remove TG |
| Insertion | Insert T after position 3 | `chr1:3-3` | `chr1 2 3` | Insert after G |

**Key points**

- In **1-based**, the end coordinate is **included**.
- In **0-based**, the end coordinate is **excluded**.
- A single-base interval `N-N` (1-based) corresponds to `(N-1, N)` in 0-based.
- Both systems describe the same biological locations using different counting conventions.

## Conversion Rules

!!! warning "Always Check Format Documentation"
    Always check the format description first, as some formats may not completely follow these conversion rules. Different tools and file formats may have specific conventions or exceptions that deviate from the general rules shown below.

| Scenario | 1-based Representation | 0-based Representation | Conversion Rule | Example (1-based → 0-based) | Example (0-based → 1-based) |
|--------|------------------------|------------------------|-----------------|-----------------------------|-----------------------------|
| Single base | `N` | `N − 1` | `0-based = 1-based − 1`; `1-based = 0-based + 1` | `N=5` → `4` | `4` → `5` |
| Single-base interval | `[N, N]` | `[N−1, N)` | shift start only | `[5,5]` → `[4,5)` | `[4,5)` → `[5,5]` |
| Interval | `[start, end]` | `[start−1, end)` | start −1, end same | `[2,4]` → `[1,4)` | `[1,4)` → `[2,4]` |
| BED one base | `chr1:N-N` | `chr1 (N−1) N` | shift start only | `chr1:101-101` → `chr1 100 101` | `chr1 100 101` → `chr1:101-101` |
| Deletion (length L) | deletes `POS..POS+L−1` | `[POS−1, POS+L−1)` | `start=POS−1`, `end=POS+L−1` | `POS=2,L=2` deletes 2–3 → `[1,3)` | `[1,3)` → deletes 2–3 (`POS=2,L=2`) |
| Insertion (between bases) | between `POS` and `POS+1` | `[POS, POS)` | `start` same; `end` ± 1 | `POS=3` → `[3,3)` | `[3,3)` → `POS=3-4` |

Notes:

- For most intervals, **only the start changes**; insertions are the exception (start stays the same, end shifts).
- 1-based intervals are inclusive; 0-based intervals are half-open.
- For insertions, BED cannot represent inserted sequence; it can only mark the insertion point.

## References

- [UCSC File Format FAQ - BED Format](https://genome.ucsc.edu/FAQ/FAQformat.html#format1) - Detailed description of BED format and coordinate systems
- [Biostars: Understanding 0-based vs 1-based coordinates](https://www.biostars.org/p/84686/) - Community discussion on coordinate systems
- [UCSC Genome Browser Blog: Coordinate Counting Systems](https://genome-blog.gi.ucsc.edu/blog/2016/12/12/the-ucsc-genome-browser-coordinate-counting-systems/) - Explanation of UCSC's coordinate counting systems
- [Plastid Documentation: Coordinate Systems](https://plastid.readthedocs.io/en/latest/concepts/coordinates.html) - Comprehensive guide to coordinate systems used in genomics
