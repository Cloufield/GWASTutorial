#!/usr/bin/env python3
"""
Extract chr1 positions from BIM file and run liftover analysis to find examples for each issue.
"""

import subprocess
import os
import argparse
import gzip
from collections import defaultdict

# Paths
LIFTOVER_BIN = "/home/yunye/tools/bin/liftOver"
CHAIN_FILE = "/home/yunye/.liftover/hg19ToHg38.over.chain.gz"
OUTPUT_DIR = "/home/yunye/work/github/GWASTutorial/37_liftover"
BIM_FILE = "/home/yunye/work/github/GWASTutorial/01_Dataset/1KG.EAS.auto.snp.norm.nodup.split.rare002.common015.missing.bim"

# Centromere positions for chr1 (hg19)
CENTROMERE_START = 121535434
CENTROMERE_END = 124535434
CHR1_LENGTH = 249250621

# Regions of interest based on previous analysis results
# These regions contain examples of various liftover issues
REGIONS_OF_INTEREST = [
    # Centromere region (Issue #2)
    (120000000, 125000000),
    # Segmental duplication region (Issue #3)
    (1500000, 2000000),
    # Cross-chromosome mapping regions
    (13000000, 13200000),  # chr1_KI270766v1_alt
    (142500000, 142600000),  # chr4_GL000008v2_random
    (142700000, 142900000),  # chrUn_KI270742v1
    (143000000, 143500000),  # chr1_KI270706v1_random, chr14_GL000009v2_random, chr21
    (148700000, 148800000),  # chr1_KI270711v1_random
    (223700000, 223800000),  # chr9
    (249000000, 249100000),  # chr12
    # Many-to-one mapping regions
    (144600000, 144700000),
    (148300000, 148400000),
]


def is_in_region_of_interest(pos):
    """Check if position is in any region of interest."""
    for start, end in REGIONS_OF_INTEREST:
        if start <= pos <= end:
            return True
    return False


def extract_chr1_positions(bim_file, filter_regions=True):
    """Extract chr1 positions from BIM file, optionally filtering to regions of interest."""
    positions = []
    snp_info = {}  # Store SNP ID and alleles for reference
    total_read = 0
    filtered_count = 0
    
    print(f"Reading positions from {bim_file}...")
    with open(bim_file, 'r') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) >= 4:
                chrom = parts[0]
                if chrom == '1':  # chr1
                    total_read += 1
                    snp_id = parts[1]
                    pos = int(parts[3])  # Position is 1-based in BIM
                    
                    # Filter: keep if in region of interest OR every 1000th position (for normal mappings)
                    if not filter_regions or is_in_region_of_interest(pos) or (total_read % 1000 == 0):
                        allele1 = parts[4] if len(parts) > 4 else 'N'
                        allele2 = parts[5] if len(parts) > 5 else 'N'
                        
                        positions.append(('chr1', pos, pos + 1))
                        snp_info[('chr1', pos)] = {
                            'snp_id': snp_id,
                            'allele1': allele1,
                            'allele2': allele2
                        }
                    else:
                        filtered_count += 1
    
    print(f"Read {total_read} chr1 positions from BIM file")
    if filter_regions:
        print(f"Filtered to {len(positions)} positions in regions of interest + sample positions")
        print(f"  (Filtered out {filtered_count} positions)")
    else:
        print(f"Extracted {len(positions)} chr1 positions (no filtering)")
    return positions, snp_info


def write_bed_file(positions, filename, snp_info=None):
    """Write positions to BED file (0-based, half-open) with IDs for matching."""
    with open(filename, 'w') as f:
        for i, (chr_name, start, end) in enumerate(positions):
            # Add ID as 4th column for matching
            if snp_info and (chr_name, start) in snp_info:
                snp_id = snp_info[(chr_name, start)]['snp_id']
                f.write(f"{chr_name}\t{start-1}\t{end-1}\t{snp_id}\n")
            else:
                # Use index as ID if no SNP info
                f.write(f"{chr_name}\t{start-1}\t{end-1}\tpos_{i}\n")


def parse_chain_file(chain_file):
    """Parse chain file and return a list of chain records with alignment blocks."""
    chains = []
    
    print(f"Parsing chain file: {chain_file}")
    with gzip.open(chain_file, 'rt') as f:
        current_chain = None
        alignment_blocks = []
        
        for line in f:
            line = line.strip()
            if not line:
                # Blank line ends a chain
                if current_chain:
                    current_chain['blocks'] = alignment_blocks
                    chains.append(current_chain)
                    current_chain = None
                    alignment_blocks = []
                continue
            
            if line.startswith('chain'):
                # Save previous chain if exists
                if current_chain:
                    current_chain['blocks'] = alignment_blocks
                    chains.append(current_chain)
                    alignment_blocks = []
                
                # Parse chain header
                # Format: chain score tName tSize tStrand tStart tEnd qName qSize qStrand qStart qEnd id
                # For hg19ToHg38.over.chain.gz: tName=hg19 (source), qName=hg38 (target)
                # Note: This is reversed from the typical interpretation!
                parts = line.split()
                if len(parts) >= 13:
                    current_chain = {
                        'score': int(parts[1]),
                        'tName': parts[2],  # source (hg19) chromosome
                        'tSize': int(parts[3]),
                        'tStrand': parts[4],
                        'tStart': int(parts[5]),  # source start (0-based)
                        'tEnd': int(parts[6]),     # source end (0-based, exclusive)
                        'qName': parts[7],  # target (hg38) chromosome
                        'qSize': int(parts[8]),
                        'qStrand': parts[9],
                        'qStart': int(parts[10]),  # target start (0-based)
                        'qEnd': int(parts[11]),    # target end (0-based, exclusive)
                        'id': parts[12],
                        'header': line
                    }
                    # Note: Some chains may have swapped tName/qName, we'll handle both cases
            elif current_chain and line:
                # Parse alignment data lines: size dt dq (or just size for last line)
                parts = line.split()
                if len(parts) >= 1:
                    size = int(parts[0])
                    dt = int(parts[1]) if len(parts) > 1 else 0
                    dq = int(parts[2]) if len(parts) > 2 else 0
                    alignment_blocks.append({'size': size, 'dt': dt, 'dq': dq})
                # Note: last line has only size, no dt/dq
        
        # Save last chain if file doesn't end with blank line
        if current_chain:
            current_chain['blocks'] = alignment_blocks
            chains.append(current_chain)
    
    # Sort chains by chromosome and start position for efficient lookup
    # Sort by tName (source chromosome), then tStart (source start position)
    chains.sort(key=lambda c: (c['tName'], c['tStart']))
    
    print(f"Parsed {len(chains)} chain records")
    return chains


def find_chains_for_position(chains, chr_name, pos, is_hg19=True):
    """Find chain records that cover a given position.
    
    Args:
        chains: List of chain records
        chr_name: Chromosome name (e.g., 'chr1')
        pos: Position (1-based)
        is_hg19: If True, search in query (hg19) coordinates; if False, search in target (hg38)
    
    Returns:
        List of matching chain records
    """
    matches = []
    pos_0based = pos - 1  # Convert to 0-based for chain file coordinates
    
    for chain in chains:
        if is_hg19:
            # Check if position is in query (hg19) range
            if chain['qName'] == chr_name:
                if chain['qStart'] <= pos_0based < chain['qEnd']:
                    matches.append(chain)
        else:
            # Check if position is in target (hg38) range
            if chain['tName'] == chr_name:
                if chain['tStart'] <= pos_0based < chain['tEnd']:
                    matches.append(chain)
    
    return matches


def format_chain_record(chain):
    """Format a chain record for display."""
    return (f"chain {chain['score']} {chain['tName']} {chain['tSize']} {chain['tStrand']} "
            f"{chain['tStart']} {chain['tEnd']} {chain['qName']} {chain['qSize']} {chain['qStrand']} "
            f"{chain['qStart']} {chain['qEnd']} {chain['id']}")


def map_position_through_chain(chain, hg19_pos_0based):
    """Map an hg19 position through a chain to get hg38 position.
    
    For hg19ToHg38.over.chain.gz: tName=hg19 (source), qName=hg38 (target)
    
    Args:
        chain: Chain record with alignment blocks
        hg19_pos_0based: hg19 position (0-based)
    
    Returns:
        hg38 position (0-based) or None if position doesn't map through this chain
    """
    # Check if position is within chain source (hg19) range
    if hg19_pos_0based < chain['tStart'] or hg19_pos_0based >= chain['tEnd']:
        return None
    
    # Handle reverse strand for source (hg19)
    if chain['tStrand'] == '-':
        hg19_pos_forward = chain['tSize'] - hg19_pos_0based
    else:
        hg19_pos_forward = hg19_pos_0based
    
    # Walk through alignment blocks
    # Start positions in forward strand coordinates
    hg38_pos = chain['qStart']
    hg19_pos = chain['tStart']
    
    blocks = chain.get('blocks', [])
    if not blocks:
        # No blocks - use simple linear mapping
        offset = hg19_pos_forward - chain['tStart']
        hg38_mapped = chain['qStart'] + offset
        # Handle reverse strand for target (hg38)
        if chain['qStrand'] == '-':
            hg38_mapped = chain['qSize'] - hg38_mapped
        return hg38_mapped
    
    # Traverse blocks to find which block contains the position
    for i, block in enumerate(blocks):
        size = block['size']
        dt = block.get('dt', 0)  # gap in target (hg38)
        dq = block.get('dq', 0)  # gap in source (hg19)
        
        # Check if position is in this aligned block
        if hg19_pos <= hg19_pos_forward < hg19_pos + size:
            # Position is in this aligned block
            offset = hg19_pos_forward - hg19_pos
            hg38_mapped = hg38_pos + offset
            
            # Handle reverse strand for target (hg38)
            if chain['qStrand'] == '-':
                hg38_mapped = chain['qSize'] - hg38_mapped
            
            return hg38_mapped
        
        # Move to next block
        hg38_pos += size + dt
        hg19_pos += size + dq
    
    # Position not found in any block (shouldn't happen if in range)
    return None


def find_chains_for_mapping(chains, hg19_chr, hg19_pos, hg38_chr=None, hg38_pos=None):
    """Find chain records that map hg19 position to hg38 position.
    
    For hg19ToHg38.over.chain.gz: tName=hg19 (source), qName=hg38 (target)
    
    Args:
        chains: List of chain records
        hg19_chr: hg19 chromosome name
        hg19_pos: hg19 position (1-based)
        hg38_chr: hg38 chromosome name (required for exact matching)
        hg38_pos: hg38 position (1-based, required for exact matching)
    
    Returns:
        List of matching chain records
    """
    matches = []
    hg19_pos_0based = hg19_pos - 1
    
    if hg38_chr is None or hg38_pos is None:
        # If no hg38 position provided, just find chains covering hg19 position
        for chain in chains:
            if chain['tName'] == hg19_chr:
                if chain['tStart'] <= hg19_pos_0based < chain['tEnd']:
                    matches.append(chain)
        return matches
    
    # Find chains that actually map to the correct hg38 position
    for chain in chains:
        # For hg19ToHg38: tName should be hg19, qName should be hg38
        if chain['tName'] != hg19_chr:
            continue
        
        # Check if hg19 position is in chain range
        if hg19_pos_0based < chain['tStart'] or hg19_pos_0based >= chain['tEnd']:
            continue
        
        # Map position through chain
        mapped_hg38_pos = map_position_through_chain(chain, hg19_pos_0based)
        if mapped_hg38_pos is None:
            continue
        
        # Convert to 1-based for comparison
        mapped_hg38_pos_1based = mapped_hg38_pos + 1
        
        # Verify it maps to the correct hg38 chromosome and position
        if chain['qName'] == hg38_chr:
            # Allow small tolerance (within 1bp) due to rounding
            if abs(mapped_hg38_pos_1based - hg38_pos) <= 1:
                matches.append(chain)
    
    return matches


def find_chains_for_failed_position(chains, hg19_chr, hg19_pos):
    """Find chain records before and after a failed hg19 position.
    
    For hg19ToHg38.over.chain.gz: tName=hg19 (source), qName=hg38 (target)
    
    Args:
        chains: List of chain records
        hg19_chr: hg19 chromosome name
        hg19_pos: hg19 position (1-based)
    
    Returns:
        Tuple of (chain_before, chain_after) where chain_before is the last chain
        that ends before this position, and chain_after is the first chain that
        starts after this position. Either can be None.
    """
    hg19_pos_0based = hg19_pos - 1
    chain_before = None
    chain_after = None
    max_before_end = -1
    min_after_start = float('inf')
    
    for chain in chains:
        if chain['tName'] != hg19_chr:
            continue
        
        # Chain that ends before this position
        if chain['tEnd'] <= hg19_pos_0based:
            if chain['tEnd'] > max_before_end:
                max_before_end = chain['tEnd']
                chain_before = chain
        
        # Chain that starts after this position
        if chain['tStart'] > hg19_pos_0based:
            if chain['tStart'] < min_after_start:
                min_after_start = chain['tStart']
                chain_after = chain
    
    return (chain_before, chain_after)


def run_liftover(input_bed, output_bed, unmapped_bed):
    """Run liftOver command."""
    cmd = [LIFTOVER_BIN, input_bed, CHAIN_FILE, output_bed, unmapped_bed]
    print(f"\nRunning: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Warning: liftOver returned code {result.returncode}")
    return result


def analyze_results(input_bed, output_bed, unmapped_bed, snp_info, chains=None):
    """Analyze liftover results and categorize by issue type."""
    # Read input positions in order with their IDs
    input_positions_list = []  # List of (chr, pos) in input order
    position_to_snp = {}  # (chr, pos) -> snp_id
    
    with open(input_bed, 'r') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) >= 3:
                chr_name = parts[0]
                start = int(parts[1]) + 1  # Convert to 1-based
                hg19_key = (chr_name, start)
                input_positions_list.append(hg19_key)
                
                # Store SNP ID if available
                if len(parts) >= 4:
                    snp_id = parts[3]
                    position_to_snp[hg19_key] = snp_id
    
    # Create reverse lookup: snp_id -> hg19_key (for fast matching)
    snp_to_position = {snp_id: pos for pos, snp_id in position_to_snp.items()}
    
    # Read successful mappings
    successful = {}  # hg19_key -> list of hg38_pos
    successful_indices = set()
    
    with open(output_bed, 'r') as f:
        idx = 0
        for line in f:
            if line.startswith('#'):
                continue
            parts = line.strip().split('\t')
            if len(parts) >= 3:
                hg38_chr = parts[0]
                hg38_pos = int(parts[1]) + 1
                hg38_pos_tuple = (hg38_chr, hg38_pos)
                
                hg19_key = None
                # Try to get ID from 4th column if available
                if len(parts) >= 4 and parts[3]:
                    snp_id = parts[3]
                    # Fast lookup using dictionary
                    hg19_key = snp_to_position.get(snp_id)
                
                # Fallback: match by order if no ID match
                if hg19_key is None and idx < len(input_positions_list):
                    hg19_key = input_positions_list[idx]
                
                if hg19_key:
                    if hg19_key not in successful:
                        successful[hg19_key] = []
                    successful[hg19_key].append(hg38_pos_tuple)
                    # Track index for this position
                    try:
                        pos_idx = input_positions_list.index(hg19_key)
                        successful_indices.add(pos_idx)
                    except ValueError:
                        successful_indices.add(idx)
                idx += 1
    
    # Convert to single mapping for backward compatibility (use first mapping if multiple)
    successful_single = {k: v[0] if v else None for k, v in successful.items() if v}
    
    # Read failed mappings - match by position and ID if available
    failed = []
    failed_positions_set = set()
    
    with open(unmapped_bed, 'r') as f:
        current_hg19 = None
        current_snp_id = None
        for line in f:
            if line.startswith('#Deleted in new'):
                if current_hg19:
                    failed.append(('deleted', current_hg19))
                    failed_positions_set.add(current_hg19)
            elif line.startswith('#Partially deleted'):
                if current_hg19:
                    failed.append(('partially_deleted', current_hg19))
                    failed_positions_set.add(current_hg19)
            else:
                parts = line.strip().split('\t')
                if len(parts) >= 3:
                    chr_name = parts[0]
                    start = int(parts[1]) + 1
                    current_hg19 = (chr_name, start)
                    # Get ID if available
                    if len(parts) >= 4:
                        current_snp_id = parts[3]
    
    # Also check for positions that are in input but not in successful (they failed)
    for i, hg19_key in enumerate(input_positions_list):
        if i not in successful_indices and hg19_key not in failed_positions_set:
            # This position failed but wasn't in unmapped file (shouldn't happen, but be safe)
            failed.append(('unknown', hg19_key))
            failed_positions_set.add(hg19_key)
    
    # Categorize by issue type
    issue2_centromere = []  # Centromere and gap redefinition
    issue3_segmental_dup = []  # Ambiguous mapping (segmental duplications)
    issue4_other = []  # Other failures
    
    # Categorize failures
    for failure_type, (chr_name, pos) in failed:
        if CENTROMERE_START - 1000000 <= pos <= CENTROMERE_END + 1000000:
            issue2_centromere.append((chr_name, pos, failure_type))
        elif 1000000 <= pos <= 2000000:  # Olfactory receptor region (segmental dup)
            issue3_segmental_dup.append((chr_name, pos, failure_type))
        else:
            issue4_other.append((chr_name, pos, failure_type))
    
    # Find many-to-one mappings (multiple hg19 -> one hg38)
    # Use first mapping for each hg19 position for this analysis
    hg38_positions = defaultdict(list)
    for hg19_key, hg38_pos_list in successful.items():
        if hg38_pos_list:
            # Use first mapping
            hg38_pos = hg38_pos_list[0]
            hg38_positions[hg38_pos].append(hg19_key)
    
    many_to_one = {k: v for k, v in hg38_positions.items() if len(v) > 1}
    
    # Find cross-chromosome mappings (use first mapping for each)
    cross_chr = []
    for hg19_key, hg38_pos_list in successful.items():
        if hg38_pos_list:
            hg19_chr, hg19_pos = hg19_key
            # Check all mappings for cross-chromosome
            for hg38_pos in hg38_pos_list:
                hg38_chr, hg38_pos_val = hg38_pos
                if hg19_chr != hg38_chr:
                    cross_chr.append({
                        'hg19': hg19_key,
                        'hg38': hg38_pos
                    })
    
    return {
        'total': len(input_positions_list),
        'successful': len(successful),
        'failed': len(failed),
        'issue2_centromere': issue2_centromere,
        'issue3_segmental_dup': issue3_segmental_dup,
        'issue4_other': issue4_other,
        'many_to_one': many_to_one,
        'cross_chromosome': cross_chr,
        'successful_mappings': successful_single,
        'snp_info': snp_info,
        'chains': chains  # Pass chains for report generation
    }


def write_report(results, report_file):
    """Write comprehensive analysis report."""
    with open(report_file, 'w') as f:
        f.write("="*80 + "\n")
        f.write("LIFTOVER ANALYSIS FROM REAL DATA\n")
        f.write("Using chr1 positions from 1KG.EAS.auto.snp.norm.nodup.split.rare002.common015.missing.bim\n")
        f.write("="*80 + "\n\n")
        
        f.write(f"Total positions tested: {results['total']:,}\n")
        f.write(f"Successful: {results['successful']:,} ({100*results['successful']/results['total']:.1f}%)\n")
        f.write(f"Failed: {results['failed']:,} ({100*results['failed']/results['total']:.1f}%)\n\n")
        
        # Issue #2: Centromere failures
        f.write("\nISSUE #2: Centromere and gap redefinition in hg38\n")
        f.write("-" * 80 + "\n")
        f.write(f"Found {len(results['issue2_centromere'])} centromere region failures:\n\n")
        chains = results.get('chains', [])
        
        # Group by chain records
        chain_to_examples = defaultdict(list)
        no_chain_examples = []
        
        for chr_name, pos, failure_type in results['issue2_centromere'][:20]:
            distance = min(abs(pos - CENTROMERE_START), abs(pos - CENTROMERE_END))
            snp_info = results['snp_info'].get((chr_name, pos), {})
            snp_id = snp_info.get('snp_id', 'N/A')
            example_info = {
                'chr': chr_name,
                'pos': pos,
                'snp_id': snp_id,
                'distance': distance,
                'failure_type': failure_type
            }
            
            if chains:
                chain_before, chain_after = find_chains_for_failed_position(chains, chr_name, pos)
                # Create a key from both chains
                if chain_before or chain_after:
                    chain_key = f"Before: {format_chain_record(chain_before) if chain_before else 'None'}; After: {format_chain_record(chain_after) if chain_after else 'None'}"
                    example_info['chain_before'] = chain_before
                    example_info['chain_after'] = chain_after
                    chain_to_examples[chain_key].append(example_info)
                else:
                    no_chain_examples.append(example_info)
            else:
                no_chain_examples.append(example_info)
        
        # Write grouped examples
        for chain_str, examples in chain_to_examples.items():
            # Show chain before and after for first example
            if examples:
                ex = examples[0]
                if 'chain_before' in ex or 'chain_after' in ex:
                    f.write(f"Chain record before: {format_chain_record(ex['chain_before']) if ex.get('chain_before') else 'None'}\n")
                    f.write(f"Chain record after: {format_chain_record(ex['chain_after']) if ex.get('chain_after') else 'None'}\n")
            f.write(f"  Examples ({len(examples)} positions):\n")
            for ex in examples[:10]:
                f.write(f"    - hg19 {ex['chr']}:{ex['pos']:,} (SNP: {ex['snp_id']}, distance: ~{ex['distance']:,} bp) → FAILED ({ex['failure_type']})\n")
            if len(examples) > 10:
                f.write(f"    ... and {len(examples) - 10} more\n")
            f.write("\n")
        
        # Write examples without chains
        if no_chain_examples:
            f.write("No chain found (positions not covered):\n")
            for ex in no_chain_examples[:10]:
                f.write(f"  - hg19 {ex['chr']}:{ex['pos']:,} (SNP: {ex['snp_id']}, distance: ~{ex['distance']:,} bp) → FAILED ({ex['failure_type']})\n")
            if len(no_chain_examples) > 10:
                f.write(f"  ... and {len(no_chain_examples) - 10} more\n")
            f.write("\n")
        
        if len(results['issue2_centromere']) > 20:
            f.write(f"  ... and {len(results['issue2_centromere']) - 20} more examples not shown\n")
        f.write("\n")
        
        # Issue #3: Segmental duplications
        f.write("\nISSUE #3: Ambiguous mapping (Segmental duplications)\n")
        f.write("-" * 80 + "\n")
        f.write(f"Found {len(results['issue3_segmental_dup'])} failures in segmental duplication regions:\n\n")
        chains = results.get('chains', [])
        
        # Group by chain records
        chain_to_examples = defaultdict(list)
        no_chain_examples = []
        
        for chr_name, pos, failure_type in results['issue3_segmental_dup'][:20]:
            snp_info = results['snp_info'].get((chr_name, pos), {})
            snp_id = snp_info.get('snp_id', 'N/A')
            example_info = {
                'chr': chr_name,
                'pos': pos,
                'snp_id': snp_id,
                'failure_type': failure_type
            }
            
            if chains:
                chain_before, chain_after = find_chains_for_failed_position(chains, chr_name, pos)
                if chain_before or chain_after:
                    chain_key = f"Before: {format_chain_record(chain_before) if chain_before else 'None'}; After: {format_chain_record(chain_after) if chain_after else 'None'}"
                    example_info['chain_before'] = chain_before
                    example_info['chain_after'] = chain_after
                    chain_to_examples[chain_key].append(example_info)
                else:
                    no_chain_examples.append(example_info)
            else:
                no_chain_examples.append(example_info)
        
        # Write grouped examples
        for chain_str, examples in chain_to_examples.items():
            # Show chain before and after for first example
            if examples:
                ex = examples[0]
                if 'chain_before' in ex or 'chain_after' in ex:
                    f.write(f"Chain record before: {format_chain_record(ex['chain_before']) if ex.get('chain_before') else 'None'}\n")
                    f.write(f"Chain record after: {format_chain_record(ex['chain_after']) if ex.get('chain_after') else 'None'}\n")
            f.write(f"  Examples ({len(examples)} positions):\n")
            for ex in examples:
                f.write(f"    - hg19 {ex['chr']}:{ex['pos']:,} (SNP: {ex['snp_id']}) → FAILED ({ex['failure_type']})\n")
            f.write("\n")
        
        # Write examples without chains
        if no_chain_examples:
            f.write("No chain found (positions not covered):\n")
            for ex in no_chain_examples:
                f.write(f"  - hg19 {ex['chr']}:{ex['pos']:,} (SNP: {ex['snp_id']}) → FAILED ({ex['failure_type']})\n")
            f.write("\n")
        
        if len(results['issue3_segmental_dup']) > 20:
            f.write(f"  ... and {len(results['issue3_segmental_dup']) - 20} more examples not shown\n")
        f.write("\n")
        
        # Many-to-one mappings
        f.write("\nMANY-TO-ONE MAPPINGS\n")
        f.write("-" * 80 + "\n")
        f.write("Multiple hg19 positions that map to the same hg38 position\n\n")
        f.write(f"Found {len(results['many_to_one'])} hg38 positions with multiple hg19 mappings:\n\n")
        chains = results.get('chains', [])
        count = 0
        for hg38_pos, hg19_positions in list(results['many_to_one'].items())[:10]:
            f.write(f"Example {count+1}:\n")
            f.write(f"  hg38 {hg38_pos[0]}:{hg38_pos[1]:,} ← {len(hg19_positions)} hg19 positions:\n")
            
            # Group hg19 positions by their chain records
            hg19_chain_to_positions = defaultdict(list)
            hg19_no_chain = []
            
            for hg19_pos in hg19_positions[:5]:
                snp_info = results['snp_info'].get(hg19_pos, {})
                snp_id = snp_info.get('snp_id', 'N/A')
                pos_info = {'pos': hg19_pos, 'snp_id': snp_id}
                
                if chains:
                    # For many-to-one, we have the hg38 position, so find chains that map hg19 to that hg38
                    # Only use chains that actually map to the correct hg38 chromosome and position
                    matching_chains = find_chains_for_mapping(chains, hg19_pos[0], hg19_pos[1], hg38_pos[0], hg38_pos[1])
                    if matching_chains:
                        primary_chain = format_chain_record(matching_chains[0])
                        hg19_chain_to_positions[primary_chain].append(pos_info)
                    else:
                        # No chain found that maps to the exact hg38 position
                        # Don't use fallback - it would show wrong chains (e.g., chr1_KI270711v1_random instead of chr1)
                        hg19_no_chain.append(pos_info)
                else:
                    hg19_no_chain.append(pos_info)
            
            # Write grouped hg19 positions
            for chain_str, pos_list in hg19_chain_to_positions.items():
                f.write(f"    Chain: {chain_str}\n")
                f.write(f"      hg19 positions ({len(pos_list)}):\n")
                for pos_info in pos_list:
                    f.write(f"        - {pos_info['pos'][0]}:{pos_info['pos'][1]:,} (SNP: {pos_info['snp_id']})\n")
            
            if hg19_no_chain:
                f.write(f"    No chain found:\n")
                for pos_info in hg19_no_chain:
                    f.write(f"      - {pos_info['pos'][0]}:{pos_info['pos'][1]:,} (SNP: {pos_info['snp_id']})\n")
            
            if len(hg19_positions) > 5:
                f.write(f"    - ... and {len(hg19_positions) - 5} more hg19 positions\n")
            
            # Show chain for hg38 position (chains that map to this hg38 position)
            if chains:
                # Find chains where target (qName) is this hg38 position
                hg38_chains = []
                for chain in chains:
                    if chain['qName'] == hg38_pos[0]:
                        q_pos_0based = hg38_pos[1] - 1
                        if chain['qStart'] <= q_pos_0based < chain['qEnd']:
                            hg38_chains.append(chain)
                
                if hg38_chains:
                    f.write(f"  hg38 position chain record(s):\n")
                    for chain in hg38_chains[:2]:
                        f.write(f"    {format_chain_record(chain)}\n")
            f.write("\n")
            count += 1
            if count >= 10:
                break
        
        if len(results['many_to_one']) == 0:
            f.write("  (No many-to-one mappings found in this sample.)\n")
        f.write("\n")
        
        # Cross-chromosome mappings
        f.write("\nCROSS-CHROMOSOME MAPPINGS\n")
        f.write("-" * 80 + "\n")
        f.write(f"Found {len(results['cross_chromosome'])} cross-chromosome mappings:\n\n")
        if results['cross_chromosome']:
            by_pair = defaultdict(list)
            for mapping in results['cross_chromosome']:
                hg19_chr, hg19_pos = mapping['hg19']
                hg38_chr, hg38_pos = mapping['hg38']
                pair = (hg19_chr, hg38_chr)
                by_pair[pair].append(mapping)
            
            chains = results.get('chains', [])
            for (hg19_chr, hg38_chr), mappings in sorted(by_pair.items()):
                f.write(f"{hg19_chr} → {hg38_chr}: {len(mappings)} examples\n")
                
                # Group mappings by chain records
                chain_to_mappings = defaultdict(list)
                no_chain_mappings = []
                
                for mapping in mappings[:20]:  # Process up to 20 for grouping
                    hg19_pos = mapping['hg19'][1]
                    hg38_pos = mapping['hg38'][1]
                    snp_info = results['snp_info'].get(mapping['hg19'], {})
                    snp_id = snp_info.get('snp_id', 'N/A')
                    mapping_info = {
                        'hg19_pos': hg19_pos,
                        'hg38_pos': hg38_pos,
                        'snp_id': snp_id
                    }
                    
                    if chains:
                        # Find chains that map this hg19 position to the hg38 position
                        # Use the actual mapped positions from liftover output
                        hg19_chains = find_chains_for_mapping(chains, hg19_chr, hg19_pos, hg38_chr, hg38_pos)
                        if hg19_chains:
                            # Use the chain that actually maps to the correct position
                            primary_chain = format_chain_record(hg19_chains[0])
                            chain_to_mappings[primary_chain].append(mapping_info)
                        else:
                            # No chain found that maps to this exact position
                            no_chain_mappings.append(mapping_info)
                    else:
                        no_chain_mappings.append(mapping_info)
                
                # Write grouped mappings
                for chain_str, mapping_list in chain_to_mappings.items():
                    f.write(f"  Chain record: {chain_str}\n")
                    f.write(f"    Examples ({len(mapping_list)} positions):\n")
                    for m in mapping_list[:10]:
                        f.write(f"      - hg19 {hg19_chr}:{m['hg19_pos']:,} (SNP: {m['snp_id']}) → hg38 {hg38_chr}:{m['hg38_pos']:,}\n")
                    if len(mapping_list) > 10:
                        f.write(f"      ... and {len(mapping_list) - 10} more\n")
                    f.write("\n")
                
                # Write mappings without chains
                if no_chain_mappings:
                    f.write(f"  No chain found ({len(no_chain_mappings)} positions):\n")
                    for m in no_chain_mappings[:10]:
                        f.write(f"    - hg19 {hg19_chr}:{m['hg19_pos']:,} (SNP: {m['snp_id']}) → hg38 {hg38_chr}:{m['hg38_pos']:,}\n")
                    if len(no_chain_mappings) > 10:
                        f.write(f"    ... and {len(no_chain_mappings) - 10} more\n")
                    f.write("\n")
                
                if len(mappings) > 20:
                    f.write(f"  ... and {len(mappings) - 20} more examples not shown\n")
                f.write("\n")
        else:
            f.write("  (No cross-chromosome mappings found in this sample.)\n")
        f.write("\n")
        
        # Summary
        f.write("\n" + "="*80 + "\n")
        f.write("SUMMARY\n")
        f.write("="*80 + "\n")
        f.write(f"Issue #2 (Centromeres): {len(results['issue2_centromere'])} failures\n")
        f.write(f"Issue #3 (Segmental duplications): {len(results['issue3_segmental_dup'])} failures\n")
        f.write(f"Other failures: {len(results['issue4_other'])} failures\n")
        f.write(f"Many-to-one mappings: {len(results['many_to_one'])} found\n")
        f.write(f"Cross-chromosome mappings: {len(results['cross_chromosome'])} found\n")


def main():
    """Main function."""
    os.chdir(OUTPUT_DIR)
    
    print("Extracting chr1 positions from BIM file (filtered to regions of interest)...")
    positions, snp_info = extract_chr1_positions(BIM_FILE, filter_regions=True)
    
    if not positions:
        print("Error: No chr1 positions found in BIM file")
        return
    
    # Write input BED file with IDs
    input_bed = "bim_chr1_positions_hg19.bed"
    print(f"\nWriting input BED file: {input_bed}")
    write_bed_file(positions, input_bed, snp_info)
    
    # Run liftover
    output_bed = "bim_chr1_positions_hg38.bed"
    unmapped_bed = "bim_chr1_positions_unmapped.bed"
    
    run_liftover(input_bed, output_bed, unmapped_bed)
    
    # Parse chain file
    print("\nParsing chain file for chain record information...")
    chains = parse_chain_file(CHAIN_FILE)
    
    # Analyze results
    print("\nAnalyzing results...")
    results = analyze_results(input_bed, output_bed, unmapped_bed, snp_info, chains)
    
    # Write report
    report_file = "liftover_bim_analysis.txt"
    print(f"\nWriting analysis report: {report_file}")
    write_report(results, report_file)
    
    # Print summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"Total positions: {results['total']:,}")
    print(f"Successful: {results['successful']:,} ({100*results['successful']/results['total']:.1f}%)")
    print(f"Failed: {results['failed']:,} ({100*results['failed']/results['total']:.1f}%)")
    print(f"\nIssue #2 (Centromeres): {len(results['issue2_centromere'])} failures")
    print(f"Issue #3 (Segmental duplications): {len(results['issue3_segmental_dup'])} failures")
    print(f"Many-to-one mappings: {len(results['many_to_one'])} found")
    print(f"Cross-chromosome mappings: {len(results['cross_chromosome'])} found")
    print(f"\nReport written to: {report_file}")


if __name__ == "__main__":
    main()
