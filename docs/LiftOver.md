# UCSC LiftOver Tool

UCSC `liftOver` is a command-line tool for converting genomic coordinates between different genome assemblies using chain files.

## Online Version

UCSC also provides a **web-based liftOver tool** for quick conversions without installation:

- **Online liftOver tool**: https://genome.ucsc.edu/cgi-bin/hgLiftOver
- Upload a BED file or paste coordinates directly
- Select source and target genome assemblies
- Download results immediately

The online tool is convenient for small-scale conversions, while the command-line tool is recommended for batch processing and automation.

## Installation

Download the `liftOver` binary from UCSC:

- **Linux**: http://hgdownload.soe.ucsc.edu/admin/exe/linux.x86_64/liftOver
- **macOS**: http://hgdownload.soe.ucsc.edu/admin/exe/macOSX.x86_64/liftOver

Make it executable:
```bash
chmod +x liftOver
```

## Download Chain Files

Download chain files from UCSC for your desired conversion (e.g., hg19 → hg38):

```bash
wget http://hgdownload.soe.ucsc.edu/goldenPath/hg19/liftOver/hg19ToHg38.over.chain.gz
```

Common chain files:

- `hg19ToHg38.over.chain.gz` (hg19 → hg38)
- `hg38ToHg19.over.chain.gz` (hg38 → hg19)
- `hg18ToHg19.over.chain.gz` (hg18 → hg19)

## Basic Usage

```bash
liftOver input.bed chain_file.chain.gz output.bed unmapped.bed
```

**Arguments:**

- `input.bed`: Input file in BED format (0-based, half-open intervals)
- `chain_file.chain.gz`: Chain file for the conversion
- `output.bed`: Successfully lifted coordinates
- `unmapped.bed`: Failed coordinates with failure reasons

## Input Format (BED)

BED format uses **0-based, half-open intervals**:

```text
chr1    1000    1001    rs123
chr1    2000    2001    rs456
chr2    5000    5001    rs789
```

Columns:
1. Chromosome name
2. Start position (0-based)
3. End position (0-based, exclusive)
4. Name/ID (optional, but useful for tracking)

!!! warning "Coordinate System"
    BED format is **0-based**. If your coordinates are **1-based** (e.g., from VCF or sumstats), convert them first:
    - 1-based position `N` → BED start: `N-1`, BED end: `N`

## Common Options

```bash
liftOver -minMatch=0.95 input.bed chain_file.chain.gz output.bed unmapped.bed
```

- `-minMatch=0.95`: Minimum match ratio for intervals (default: 0.95)
- `-multiple`: Allow multiple mappings (default: drop ambiguous mappings)

!!! example "Example"
    Convert SNP positions from hg19 to hg38:

    ```bash
    # Create input BED file (0-based)
    cat > snps_hg19.bed << EOF
    chr1    1000000    1000001    rs123
    chr1    2000000    2000001    rs456
    chr2    5000000    5000001    rs789
    EOF

    # Run liftover
    liftOver snps_hg19.bed hg19ToHg38.over.chain.gz snps_hg38.bed snps_unmapped.bed

    # Check results
    echo "Successfully lifted:"
    wc -l snps_hg38.bed

    echo "Failed:"
    wc -l snps_unmapped.bed
    ```

!!! example "Simple Example: Liftover chr1 from BIM File"
    This example demonstrates how to extract chromosome 1 positions from a PLINK BIM file and convert them from hg19 to hg38:

    ```bash
    # Extract chr1 positions from BIM file and convert to BED format
    # BIM format: chr variant_id genetic_distance position(1-based) allele1 allele2
    # BED format: chr start(0-based) end(0-based) variant_id

    awk '$1==1 {print "chr1\t" ($4-1) "\t" $4 "\t" $2}' \
        01_Dataset/1KG.EAS.auto.snp.norm.nodup.split.rare002.common015.missing.bim \
        > chr1_hg19.bed

    # Run liftover
    liftOver chr1_hg19.bed hg19ToHg38.over.chain.gz chr1_hg38.bed chr1_unmapped.bed

    # Check results
    echo "Total input positions:"
    wc -l chr1_hg19.bed

    echo "Successfully lifted:"
    wc -l chr1_hg38.bed

    echo "Failed:"
    wc -l chr1_unmapped.bed

    # View first few successfully lifted positions
    echo "First 5 lifted positions:"
    head -5 chr1_hg38.bed
    ```

    ```
    ==========================================
    Liftover Example: chr1 from BIM file
    ==========================================

    Step 1: Extracting chr1 positions from BIM file...
      Input: ../01_Dataset/1KG.EAS.auto.snp.norm.nodup.split.rare002.common015.missing.bim
      Converting 1-based BIM coordinates to 0-based BED format...
      Extracted 97655 chr1 positions
      Output: chr1_hg19.bed

    Step 2: Running liftover (hg19 → hg38)...
      Chain file: hg19ToHg38.over.chain.gz
      This may take a few minutes...
    Reading liftover chains
    Mapping coordinates
      Liftover completed

    Step 3: Results summary
    ==========================================
    Total input positions:    97655
    Successfully lifted:      97526
    Success rate:             99.87%
    Failed:                   258

    First 5 failed positions:
      #Deleted in new
      chr1  1590525 1590526 1:1590526:G:C
      #Deleted in new
      chr1  1590574 1590575 1:1590575:G:A
      #Deleted in new
    ==========================================

    Step 4: Example lifted positions (first 5):
      Format: chr start(0-based) end(0-based) variant_id
      chr1  14929   14930   1:14930:A:G
      chr1  15773   15774   1:15774:G:A
      chr1  15776   15777   1:15777:A:G
      chr1  57291   57292   1:57292:C:T
      chr1  77873   77874   1:77874:G:A

    Output files:
      Input BED (hg19):     chr1_hg19.bed
      Output BED (hg38):    chr1_hg38.bed
      Unmapped positions:   chr1_unmapped.bed
    ```

    **Key points:**

    - BIM files use **1-based coordinates**, so we subtract 1 to convert to 0-based BED format
    - The BED end position is `position` (same as start+1 for single-base variants)
    - The variant ID from column 2 is preserved in the BED file for tracking

    See `liftover_chr1_example.sh` for a complete script that performs this conversion.

## Output Files

- **`output.bed`**: Contains successfully lifted coordinates in the target assembly
- **`unmapped.bed`**: Contains failed coordinates with reasons (e.g., "No chain found", "Multiple mappings")

## Tips

- Always check the `unmapped.bed` file to see which positions failed and why
- For sumstats, convert 1-based positions to 0-based BED format before liftover
- After liftover, convert back to 1-based if needed for downstream analysis
- Some positions may fail due to assembly differences (centromeres, gaps, duplications) — this is expected

## References

- [UCSC LiftOver Tool](https://genome.ucsc.edu/cgi-bin/hgLiftOver) - Tool for converting coordinates between genome assemblies
- UCSC liftOver tool: **Download and documentation**  
  http://hgdownload.soe.ucsc.edu/admin/exe/
- UCSC Genome Browser: **liftOver tool**  
  https://genome.ucsc.edu/cgi-bin/hgLiftOver
