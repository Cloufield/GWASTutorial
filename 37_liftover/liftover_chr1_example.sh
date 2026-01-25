#!/bin/bash
# Simple example script for lifting over chr1 positions from BIM file
# Converts hg19 coordinates to hg38 using UCSC liftOver tool

set -e  # Exit on error

# Configuration
BIM_FILE="../01_Dataset/1KG.EAS.auto.snp.norm.nodup.split.rare002.common015.missing.bim"
CHAIN_FILE="hg19ToHg38.over.chain.gz"
LIFTOVER_BIN="liftOver"  # Adjust path if needed

# Output files
INPUT_BED="chr1_hg19.bed"
OUTPUT_BED="chr1_hg38.bed"
UNMAPPED_BED="chr1_unmapped.bed"

# Check if BIM file exists
if [ ! -f "$BIM_FILE" ]; then
    echo "Error: BIM file not found: $BIM_FILE"
    exit 1
fi

# Check if chain file exists
if [ ! -f "$CHAIN_FILE" ]; then
    echo "Error: Chain file not found: $CHAIN_FILE"
    echo "Download it with: wget http://hgdownload.soe.ucsc.edu/goldenPath/hg19/liftOver/hg19ToHg38.over.chain.gz"
    exit 1
fi

# Check if liftOver is available
if ! command -v "$LIFTOVER_BIN" &> /dev/null; then
    echo "Error: liftOver not found. Please install it first."
    echo "Download from: http://hgdownload.soe.ucsc.edu/admin/exe/linux.x86_64/liftOver"
    exit 1
fi

echo "=========================================="
echo "Liftover Example: chr1 from BIM file"
echo "=========================================="
echo ""

# Step 1: Extract chr1 positions from BIM file and convert to BED format
echo "Step 1: Extracting chr1 positions from BIM file..."
echo "  Input: $BIM_FILE"
echo "  Converting 1-based BIM coordinates to 0-based BED format..."

# BIM format: chr variant_id genetic_distance position(1-based) allele1 allele2
# BED format: chr start(0-based) end(0-based) variant_id
awk '$1==1 {print "chr1\t" ($4-1) "\t" $4 "\t" $2}' "$BIM_FILE" > "$INPUT_BED"

TOTAL_POSITIONS=$(wc -l < "$INPUT_BED")
echo "  Extracted $TOTAL_POSITIONS chr1 positions"
echo "  Output: $INPUT_BED"
echo ""

# Step 2: Run liftover
echo "Step 2: Running liftover (hg19 → hg38)..."
echo "  Chain file: $CHAIN_FILE"
echo "  This may take a few minutes..."

"$LIFTOVER_BIN" "$INPUT_BED" "$CHAIN_FILE" "$OUTPUT_BED" "$UNMAPPED_BED"

echo "  Liftover completed"
echo ""

# Step 3: Check results
echo "Step 3: Results summary"
echo "=========================================="
echo "Total input positions:    $TOTAL_POSITIONS"

if [ -f "$OUTPUT_BED" ]; then
    SUCCESS_COUNT=$(wc -l < "$OUTPUT_BED")
    echo "Successfully lifted:      $SUCCESS_COUNT"
    SUCCESS_RATE=$(awk "BEGIN {printf \"%.2f\", ($SUCCESS_COUNT/$TOTAL_POSITIONS)*100}")
    echo "Success rate:             ${SUCCESS_RATE}%"
else
    echo "Successfully lifted:      0"
fi

if [ -f "$UNMAPPED_BED" ]; then
    FAILED_COUNT=$(wc -l < "$UNMAPPED_BED")
    echo "Failed:                   $FAILED_COUNT"
    if [ "$FAILED_COUNT" -gt 0 ]; then
        echo ""
        echo "First 5 failed positions:"
        head -5 "$UNMAPPED_BED" | sed 's/^/  /'
    fi
else
    echo "Failed:                   0"
fi

echo "=========================================="
echo ""

# Step 4: Show examples
if [ -f "$OUTPUT_BED" ] && [ -s "$OUTPUT_BED" ]; then
    echo "Step 4: Example lifted positions (first 5):"
    echo "  Format: chr start(0-based) end(0-based) variant_id"
    head -5 "$OUTPUT_BED" | sed 's/^/  /'
    echo ""
fi

echo "Output files:"
echo "  Input BED (hg19):     $INPUT_BED"
echo "  Output BED (hg38):    $OUTPUT_BED"
echo "  Unmapped positions:   $UNMAPPED_BED"
echo ""
echo "Done!"
