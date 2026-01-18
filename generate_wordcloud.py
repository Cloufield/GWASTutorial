#!/usr/bin/env python3
"""
Generate a word cloud from all markdown files in the repository.
"""

import os
import re
import numpy as np
from collections import Counter
from pathlib import Path
from wordcloud import WordCloud
from PIL import Image, ImageDraw, ImageFont

# Key terms to extract from README files (domain-specific keywords)
KEY_TERMS = {
    # Core GWAS terms
    'GWAS', 'gwas', 'genome-wide', 'genome', 'genomics', 'genetic', 'genetics',
    # Methods and tools
    'PLINK', 'plink', 'GCTA', 'gcta', 'LDSC', 'ldsc', 'MAGMA', 'magma', 
    'SUSIE', 'susie', 'SuSiE', 'susie', 'TWAS', 'twas', 'PRS', 'prs', 'PGS', 'pgs',
    'REGENIE', 'regenie', 'SAIGE', 'saige', 'SKAT', 'skat',
    'coloc', 'dbSNP', 'dbsnp',
    # Statistical methods
    'LOCO', 'loco', 'Firth', 'firth', 'GLM', 'glm', 'LMM', 'lmm',
    # Statistical terms
    'regression', 'association', 'heritability', 'heritable', 'PCA', 'pca',
    'meta-analysis', 'meta', 'META', 'imputation', 'phasing',
    'liability', 'power', 'inbreeding',
    # Genetic terms
    'LD', 'ld', 'linkage', 'disequilibrium', 'MAF', 'maf', 'allele', 'alleles',
    'SNP', 'snp', 'SNPs', 'snps', 'variant', 'variants', 'genotype', 'genotypes',
    'haplotype', 'haplotypes', 'chromosome', 'chromosomes',
    # Analysis terms
    'annotation', 'colocalization', 'fine-mapping', 'finemapping', 'fine', 'mapping',
    'mendelian', 'randomization', 'MR', 'mr', 'causal', 'causality',
    'winners', 'curse', "winner's", "winner's curse",
    'relatedness', 'population structure', 'population', 'populations',
    'analysis', 'statistical', 'statistics',
    'conditional', 'beta shrinkage', 'beta', 'shrinkage', 'P+T', 'P+T', 'P and T',
    # Data formats
    'VCF', 'vcf', 'BCF', 'bcf', 'BED', 'bed', 'BIM', 'bim', 'FAM', 'fam',
    # Quality control
    'QC', 'qc', 'quality', 'control', 'HWE', 'hwe', 'hardy', 'weinberg',
    # Databases and catalogs
    '1000 Genomes', '1000 genome', '1000 genomes', 'HapMap3', 'hapmap3', 'HapMap',
    'GWAS Catalog', 'gwas catalog', 'GWAS catalog', 'PGS Catalog', 'pgs catalog', 'PGS catalog',
    # Biobanks and cohorts
    'UKB', 'ukb', 'UK Biobank', 'uk biobank', 'BBJ', 'bbj', 'BioBank Japan', 'biobank japan',
    'CKB', 'ckb', 'China Kadoorie', 'FinnGen', 'finngen', 'FinnGen',
    # Other important terms
    'trait', 'traits', 'phenotype', 'phenotypes', 'cohort', 'cohorts',
    'sample', 'samples', 'effect', 'effects',
    'rare', 'common', 'distribution', 'p-value', 'pvalue', 'significance',
    'biobanks', 'biobank'
}

# Common English stopwords to filter out
STOPWORDS = {
    'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with',
    'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been', 'be', 'have', 'has', 'had',
    'do', 'does', 'did', 'will', 'would', 'should', 'could', 'may', 'might', 'must',
    'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they',
    'what', 'which', 'who', 'when', 'where', 'why', 'how', 'all', 'each', 'every',
    'both', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only',
    'own', 'same', 'so', 'than', 'too', 'very', 'just', 'also', 'about', 'into', 'through',
    'during', 'before', 'after', 'above', 'below', 'up', 'down', 'out', 'off', 'over',
    'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why',
    'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such',
    'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't',
    'can', 'will', 'just', 'don', 'should', 'now', 'one', 'two', 'three', 'first',
    'second', 'third', 'section', 'sections', 'example', 'examples', 'figure', 'figures',
    'table', 'tables', 'see', 'using', 'used', 'use', 'uses', 'page', 'pages',
    'https', 'http', 'www', 'com', 'org', 'edu', 'github', 'io',
    # Additional common words to filter
    'variants', 'variant', 'reference', 'data', 'file', 'files', 'analysis', 'check',
    'input', 'directories', 'directory', 'binary', 'image', 'images', 'wide', 'download',
    'info', 'missing', 'add', 'job', 'need', 'please', 'perform', 'run', 'create',
    'note', 'notes', 'text', 'true', 'options', 'option', 'small',
    # Generic common words
    'test', 'tests', 'testing', 'model', 'models', 'effect', 'effects', 'sample', 'samples',
    'study', 'studies', 'based', 'statistics', 'statistic', 'population', 'populations',
    'gene', 'genes', 'allele', 'alleles', 'snps', 'snp', 'result', 'results', 'value', 'values',
    'method', 'methods', 'methodology', 'different', 'following', 'include', 'includes',
    'including', 'show', 'shows', 'shown', 'make', 'makes', 'made', 'get', 'gets', 'got',
    'give', 'gives', 'given', 'take', 'takes', 'took', 'taken', 'set', 'sets', 'setting',
    'way', 'ways', 'part', 'parts', 'type', 'types', 'kind', 'kinds', 'form', 'forms',
    'time', 'times', 'number', 'numbers', 'many', 'much', 'well', 'way', 'ways',
    'new', 'old', 'large', 'long', 'high', 'low', 'great', 'good', 'bad', 'important',
    'general', 'specific', 'particular', 'certain', 'several', 'various', 'different',
    'similar', 'same', 'another', 'each', 'every', 'both', 'either', 'neither',
    'your', 'their', 'our', 'its', 'his', 'her', 'my', 'command', 'commands',
    'multiple', 'control', 'controls', 'summary', 'summaries', 'nature',
    'between', 'step', 'steps', 'case', 'cases', 'common', 'within', 'without',
    'across', 'along', 'among', 'around', 'behind', 'beside', 'beyond'
}

def extract_text_from_markdown(file_path):
    """Extract text content from a markdown file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove markdown syntax
        # Remove headers
        content = re.sub(r'^#+\s+', '', content, flags=re.MULTILINE)
        # Remove code blocks
        content = re.sub(r'```[\s\S]*?```', '', content)
        content = re.sub(r'`[^`]+`', '', content)
        # Remove images (must be before links, since images are ! followed by link syntax)
        content = re.sub(r'!\[([^\]]*)\]\([^\)]+\)', '', content)
        # Remove links [text](url)
        content = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', content)
        # Remove emphasis
        content = re.sub(r'\*\*([^\*]+)\*\*', r'\1', content)
        content = re.sub(r'\*([^\*]+)\*', r'\1', content)
        # Remove HTML tags
        content = re.sub(r'<[^>]+>', '', content)
        
        return content
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return ""

def extract_key_terms(text):
    """Extract only key domain-specific terms from text."""
    found_terms = []
    
    # Handle multi-word terms first (longer terms first to avoid partial matches)
    multi_word_terms = [
        ("winner's curse", "winner's curse"),
        ("winners curse", "winner's curse"),
        ("population structure", "population structure"),
        ("fine-mapping", "fine-mapping"),
        ("finemapping", "fine-mapping"),
        ("meta-analysis", "meta-analysis"),
        ("genome-wide", "genome-wide"),
        ("linkage disequilibrium", "linkage disequilibrium"),
        ("hardy weinberg", "HWE"),
        ("hardy-weinberg", "HWE"),
        ("1000 Genomes", "1000 Genomes"),
        ("1000 genome", "1000 Genomes"),
        ("1000 genomes", "1000 Genomes"),
        ("HapMap3", "HapMap3"),
        ("hapmap3", "HapMap3"),
        ("HapMap", "HapMap3"),
        ("GWAS Catalog", "GWAS Catalog"),
        ("gwas catalog", "GWAS Catalog"),
        ("GWAS catalog", "GWAS Catalog"),
        ("PGS Catalog", "PGS Catalog"),
        ("pgs catalog", "PGS Catalog"),
        ("PGS catalog", "PGS Catalog"),
        ("UK Biobank", "UK Biobank"),
        ("uk biobank", "UK Biobank"),
        ("BioBank Japan", "BBJ"),
        ("biobank japan", "BBJ"),
        ("China Kadoorie", "CKB"),
        ("beta shrinkage", "beta shrinkage")
    ]
    
    # Search for multi-word terms
    for pattern, output_term in multi_word_terms:
        # Handle P+T specially since + needs special regex handling
        if pattern == "P+T":
            # Try multiple patterns for P+T
            p_t_patterns = [
                r'\bP\+T\b',
                r'\bP\s*\+\s*T\b',
                r'\bP\s+and\s+T\b',
                r'\bP\s*&\s*T\b'
            ]
            for pat in p_t_patterns:
                matches = re.findall(pat, text, re.IGNORECASE)
                found_terms.extend([output_term] * len(matches))
        else:
            matches = re.findall(r'\b' + re.escape(pattern) + r'\b', text, re.IGNORECASE)
            found_terms.extend([output_term] * len(matches))
    
    # Handle P+T specially (can appear as P+T, P and T, P & T, etc.)
    p_t_patterns = [
        r'\bP\+T\b',
        r'\bP\s*\+\s*T\b',
        r'\bP\s+and\s+T\b',
        r'\bP\s*&\s*T\b'
    ]
    for pat in p_t_patterns:
        matches = re.findall(pat, text, re.IGNORECASE)
        found_terms.extend(['P+T'] * len(matches))
    
    # Search for single-word key terms
    for term in KEY_TERMS:
        # Skip if it's part of a multi-word term we already handled
        if term in ["winner's", "winners", "curse", "population", "structure", 
                   "fine", "mapping", "meta", "genome", "wide", "linkage", 
                   "disequilibrium", "hardy", "weinberg", "1000", "genomes",
                   "hapmap", "catalog", "gwas", "pgs", "uk", "biobank", "japan",
                   "china", "kadoorie", "beta", "shrinkage", "p", "t", "and", "&"]:
            continue
            
        # Create a case-insensitive pattern
        pattern = r'\b' + re.escape(term) + r'\b'
        matches = re.findall(pattern, text, re.IGNORECASE)
        
        # Count occurrences and add to list with normalized casing
        for match in matches:
            # Normalize to preferred casing
            if term.isupper():
                found_terms.append(term)
            else:
                # Use preferred casing for acronyms and specific terms
                term_lower = term.lower()
                if term_lower == 'susie':
                    found_terms.append('SuSiE')
                elif term_lower in ['gwas', 'plink', 'gcta', 'ldsc', 'magma', 'twas', 
                                   'prs', 'pgs', 'pca', 'ld', 'maf', 'snp', 'snps',
                                   'vcf', 'bcf', 'bed', 'bim', 'fam', 'qc', 'hwe', 
                                   'mr', 'meta', 'regenie', 'saige', 'skat', 'coloc',
                                   'dbsnp', 'ukb', 'bbj', 'ckb', 'finngen', 'loco',
                                   'glm', 'lmm']:
                    found_terms.append(term.upper())
                elif term_lower == 'firth':
                    # Firth should be capitalized (proper name)
                    found_terms.append('Firth')
                elif term_lower in ['heritability', 'liability', 'relatedness', 
                                   'colocalization', 'finemapping', 'phasing', 
                                   'imputation', 'power', 'inbreeding', 'biobanks',
                                   'biobank', 'conditional', 'beta', 'shrinkage']:
                    # Use lowercase for these terms
                    found_terms.append(term_lower)
                else:
                    found_terms.append(match)
    
    return found_terms

def create_gwas_text_mask(width, height):
    """Create a 'GWAS' text mask image - words will form the letters GWAS."""
    # WordCloud mask: WHITE (255) = masked out (no words), BLACK (0) = allowed (words can go here)
    # So we want: white background (masked), black text (where words appear)
    mask = Image.new('RGB', (width, height), 'white')  # White background = masked out
    draw = ImageDraw.Draw(mask)
    
    # Try to load a bold font for the text - make it much larger to fill the image
    # Use a larger multiplier to fill more of the image
    font_size = int(min(width, height) * 0.75)  # Much larger font size to fill edges
    font = None
    
    # Try to find Arial Bold or similar bold font
    possible_fonts = [
        'C:/Windows/Fonts/arialbd.ttf',  # Arial Bold
        'C:/Windows/Fonts/ARIALBD.TTF',
        '/System/Library/Fonts/Supplemental/Arial Bold.ttf',
        '/usr/share/fonts/truetype/msttcorefonts/arialbd.ttf',
        '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf',
        '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
    ]
    
    for font_path in possible_fonts:
        if os.path.exists(font_path):
            try:
                font = ImageFont.truetype(font_path, font_size)
                break
            except:
                continue
    
    # If no font found, use default (but it might not be bold)
    if font is None:
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
        except:
            font = ImageFont.load_default()
    
    # Draw "GWAS" text in BLACK (where words should appear)
    text = "GWAS"
    
    # Get text bounding box to center it
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Center the text, but allow it to extend closer to edges
    # Add some padding but make it fill more of the space
    x = (width - text_width) // 2 - bbox[0]
    y = (height - text_height) // 2 - bbox[1]
    
    # If text is too small, try increasing font size iteratively
    if text_width < width * 0.8 or text_height < height * 0.6:
        # Try even larger font
        larger_font_size = int(min(width, height) * 0.85)
        for font_path in possible_fonts:
            if os.path.exists(font_path):
                try:
                    font = ImageFont.truetype(font_path, larger_font_size)
                    bbox = draw.textbbox((0, 0), text, font=font)
                    text_width = bbox[2] - bbox[0]
                    text_height = bbox[3] - bbox[1]
                    x = (width - text_width) // 2 - bbox[0]
                    y = (height - text_height) // 2 - bbox[1]
                    break
                except:
                    continue
    
    # Draw the text in black (thick outline for better mask)
    # Draw multiple times with slight offsets to make it thicker/bolder
    for dx in range(-5, 6):
        for dy in range(-5, 6):
            draw.text((x + dx, y + dy), text, fill='black', font=font)
    
    # Convert to numpy array for wordcloud
    # WordCloud: white (255) = masked out, black (0) = words allowed
    # PIL Image is (width, height), numpy array is (height, width)
    mask_array = np.array(mask.convert('L'))  # Convert to grayscale
    
    # Verify dimensions - numpy array should be (height, width)
    # PIL Image.new('RGB', (width, height)) creates width x height image
    # np.array() converts it to (height, width) array
    expected_shape = (height, width)
    if mask_array.shape != expected_shape:
        print(f"Warning: Mask shape {mask_array.shape} doesn't match expected {expected_shape}")
        # If it's transposed, fix it
        if mask_array.shape == (width, height):
            mask_array = mask_array.T
            print(f"Transposed mask to {mask_array.shape}")
    
    return mask_array

def main():
    # Get repository root
    repo_root = Path(__file__).parent
    
    # Find all markdown files
    md_files = []
    for ext in ['*.md', '*.MD']:
        md_files.extend(repo_root.rglob(ext))
    
    print(f"Found {len(md_files)} markdown files")
    
    # Extract key terms from each README
    all_key_terms = []
    for md_file in md_files:
        # Skip files in site/ directory (generated files)
        if 'site/' in str(md_file):
            continue
        text = extract_text_from_markdown(md_file)
        key_terms = extract_key_terms(text)
        all_key_terms.extend(key_terms)
        if len(key_terms) > 0:
            print(f"Processed {md_file.relative_to(repo_root)}: {len(key_terms)} key terms")
    
    # Count key term frequencies
    word_freq = Counter(all_key_terms)
    
    print(f"\nTotal unique words: {len(word_freq)}")
    print(f"Top 20 words:")
    for word, count in word_freq.most_common(20):
        print(f"  {word}: {count}")
    
    # Create GWAS text mask with 6:2 (3:1) aspect ratio to prevent clipping
    # Wider aspect ratio gives more horizontal space for "GWAS" text
    mask_width, mask_height = 2400, 800  # 3:1 ratio (6:2)
    mask = create_gwas_text_mask(mask_width, mask_height)
    
    # Try to find Arial font
    font_path = None
    # Try common Arial font paths
    possible_fonts = [
        'C:/Windows/Fonts/arial.ttf',
        'C:/Windows/Fonts/ARIAL.TTF',
        'C:/Windows/Fonts/arialbd.ttf',  # Arial Bold
        '/System/Library/Fonts/Supplemental/Arial.ttf',
        '/System/Library/Fonts/Supplemental/Arial Bold.ttf',
        '/usr/share/fonts/truetype/msttcorefonts/arial.ttf',
        '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',  # Arial-like fallback
        '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',  # Fallback
    ]
    for font in possible_fonts:
        if os.path.exists(font):
            font_path = font
            print(f"Using font: {font_path}")
            break
    
    if font_path is None:
        print("Warning: Arial font not found, using default font")
    
    # Verify mask dimensions match
    print(f"Mask dimensions: {mask.shape}")
    print(f"Target dimensions: {mask_width}x{mask_height}")
    
    # Create word cloud with single color for all words (blue)
    # Use color_func to assign the same color to all words
    def single_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
        # Return a single blue color for all words (RGB tuple)
        return (70, 130, 180)  # Steel blue color
    
    # Create word cloud with single color and GWAS text mask
    wordcloud = WordCloud(
        width=mask_width,
        height=mask_height,
        background_color='white',
        max_words=200,
        color_func=single_color_func,
        relative_scaling=0.5,
        random_state=42,
        mask=mask,
        font_path=font_path,
        prefer_horizontal=0.7,
        min_font_size=10,
        scale=1.0  # Ensure full scale
    ).generate_from_frequencies(word_freq)
    
    # Save to docs/images
    output_dir = repo_root / 'docs' / 'images'
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / 'wordcloud.png'
    
    # Save directly using wordcloud's to_image method
    image = wordcloud.to_image()
    print(f"Generated image size: {image.size}")
    
    # Ensure we save the full image without cropping
    # Save without DPI to avoid display issues, or use standard DPI
    image.save(output_path, 'PNG')
    
    # Verify the saved image
    saved_img = Image.open(output_path)
    print(f"Saved image size: {saved_img.size}, mode: {saved_img.mode}")
    
    print(f"\nWord cloud saved to: {output_path}")

if __name__ == '__main__':
    main()
