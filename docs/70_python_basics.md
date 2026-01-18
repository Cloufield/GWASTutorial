# Python Basics

## Introduction

This section provides a minimum introduction to Python programming for handling genomic data and conducting GWAS analyses. Python is a versatile, high-level programming language that is widely used in bioinformatics, data science, and statistical genetics.

If you are a beginner with no background in programming, this tutorial will help you learn the fundamental concepts needed to work with genomic data in Python.

!!! note "For beginners"
    This tutorial assumes no prior programming experience. We'll start with the basics and gradually build up to more complex concepts relevant to genomic data analysis.

!!! tip "Why Python for genomics?"
    - **Readability**: Python code is easy to read and write
    - **Rich ecosystem**: Extensive libraries for data analysis (pandas, numpy, scipy)
    - **Bioinformatics tools**: Many genomics tools have Python interfaces
    - **Integration**: Works well with command-line tools and other languages
    - **Community**: Large community and extensive documentation

## Table of Contents

- [Getting Started](#getting-started)
    - Installation and setup
    - Running Python code
- [Basic Data Types](#basic-data-types)
    - Numbers, strings, booleans
- [Variables and Operators](#variables-and-operators)
- [Data Structures](#data-structures)
    - Lists, dictionaries, tuples, sets
- [Control Flow](#control-flow)
    - Conditional statements, loops
- [Functions](#functions)
    - Defining and using functions
- [File Input/Output](#file-inputoutput)
    - Reading and writing files
- [Working with Libraries](#working-with-libraries)
    - NumPy, pandas basics
- [Examples for Genomics](#examples-for-genomics)
    - Practical genomics examples

## Getting Started

### Installation

Python is typically pre-installed on Linux and Mac systems. You can check if Python is installed:

!!! example "Check Python version"
    ```bash
    $ python --version
    Python 3.9.5
    
    # Or try python3
    $ python3 --version
    Python 3.9.5
    ```

!!! tip "Python 2 vs Python 3"
    Python 2 is deprecated. Always use Python 3 (3.9 or higher recommended). Most systems use `python3` command for Python 3.

### Running Python Code

There are several ways to run Python code:

1. **Interactive Python (REPL)**: Type `python` or `python3` in terminal
2. **Python scripts**: Save code in `.py` files and run with `python script.py`
3. **Jupyter notebooks**: Interactive environment for data analysis

!!! example "Interactive Python session"
    ```python
    $ python3
    Python 3.9.5 (default, ...)
    Type "help", "copyright", "credits" or "license" for more information.
    >>> print("Hello, World!")
    Hello, World!
    >>> exit()
    ```

!!! example "Python script"
    Create a file `hello.py`:
    ```python
    # hello.py
    print("Hello, World!")
    ```
    
    Run it:
    ```bash
    $ python3 hello.py
    Hello, World!
    ```

### Comments

Comments help document your code. Use `#` for single-line comments:

!!! example "Comments in Python"
    ```python
    # This is a comment
    print("Hello")  # This is also a comment
    
    """
    This is a multi-line comment
    (actually a docstring)
    """
    ```

## Basic Data Types

Python has several built-in data types. The most common ones are:

### Numbers

Python supports integers and floating-point numbers:

!!! example "Numbers"
    ```python
    # Integers
    x = 42
    y = -10
    
    # Floating-point numbers
    pi = 3.14159
    height = 175.5
    
    # Basic arithmetic
    sum_result = 10 + 5        # 15
    product = 3 * 4            # 12
    division = 10 / 3          # 3.333...
    floor_division = 10 // 3   # 3 (integer division)
    remainder = 10 % 3         # 1 (modulo)
    power = 2 ** 3             # 8 (2 to the power of 3)
    ```

### Strings

Strings are sequences of characters, enclosed in single or double quotes:

!!! example "Strings"
    ```python
    # String creation
    name = "Alice"
    chromosome = 'chr1'
    variant_id = "rs123456"
    
    # String operations
    full_name = name + " Smith"           # Concatenation: "Alice Smith"
    repeated = "AT" * 3                    # "ATATAT"
    length = len(name)                     # 5
    
    # String methods
    text = "  hello world  "
    text.strip()                           # "hello world" (remove whitespace)
    text.upper()                           # "  HELLO WORLD  "
    text.lower()                           # "  hello world  "
    text.replace("world", "Python")        # "  hello Python  "
    
    # String formatting (f-strings, Python 3.6+)
    variant = "rs123456"
    p_value = 0.0001
    message = f"Variant {variant} has p-value {p_value}"
    # "Variant rs123456 has p-value 0.0001"
    ```

!!! example "Working with genomic sequences"
    ```python
    # DNA sequence
    sequence = "ATGCGATCG"
    sequence_length = len(sequence)       # 9
    gc_count = sequence.count("G") + sequence.count("C")  # 4
    gc_content = gc_count / sequence_length  # 0.444...
    
    # Reverse complement (simple example)
    complement = sequence.replace("A", "t").replace("T", "a").replace("G", "c").replace("C", "g")
    reverse_complement = complement.upper()[::-1]
    ```

### Booleans

Booleans represent truth values: `True` or `False`:

!!! example "Booleans"
    ```python
    is_significant = True
    is_rare = False
    
    # Boolean operations
    result1 = True and False    # False
    result2 = True or False     # True
    result3 = not True          # False
    
    # Comparisons return booleans
    p_value = 0.0001
    is_significant = p_value < 0.05  # True
    ```

## Variables and Operators

### Variables

Variables store values. In Python, you don't need to declare variable types:

!!! example "Variables"
    ```python
    # Variable assignment
    variant_id = "rs123456"
    chromosome = 1
    position = 12345
    p_value = 0.0001
    is_significant = p_value < 5e-8
    
    # Variable names should be descriptive
    sample_size = 10000
    allele_frequency = 0.25
    effect_size = 0.15
    ```

!!! tip "Variable naming conventions"
    - Use lowercase with underscores: `variant_id`, `p_value`
    - Be descriptive: `chr` is better than `c`, `p_value` is better than `p`
    - Avoid Python keywords: `if`, `for`, `def`, `class`, etc.

### Operators

Python supports various operators:

!!! info "Common operators"
    | Operator | Description | Example |
    |----------|-------------|---------|
    | `+` | Addition | `3 + 5` → `8` |
    | `-` | Subtraction | `10 - 3` → `7` |
    | `*` | Multiplication | `4 * 5` → `20` |
    | `/` | Division | `10 / 3` → `3.333...` |
    | `//` | Floor division | `10 // 3` → `3` |
    | `%` | Modulo (remainder) | `10 % 3` → `1` |
    | `**` | Exponentiation | `2 ** 3` → `8` |
    | `==` | Equality | `5 == 5` → `True` |
    | `!=` | Inequality | `5 != 3` → `True` |
    | `<` | Less than | `3 < 5` → `True` |
    | `>` | Greater than | `5 > 3` → `True` |
    | `<=` | Less than or equal | `3 <= 3` → `True` |
    | `>=` | Greater than or equal | `5 >= 3` → `True` |
    | `and` | Logical AND | `True and False` → `False` |
    | `or` | Logical OR | `True or False` → `True` |
    | `not` | Logical NOT | `not True` → `False` |

!!! example "Operators in genomics context"
    ```python
    # Calculate odds ratio from beta
    beta = 0.2
    odds_ratio = 2.718 ** beta  # e^beta
    
    # Check if variant passes QC filters
    maf = 0.01
    call_rate = 0.98
    hwe_p = 0.001
    
    passes_qc = (maf > 0.01) and (call_rate > 0.95) and (hwe_p > 0.0001)
    
    # Check genome-wide significance
    p_value = 1e-8
    is_gws = p_value < 5e-8  # True
    ```

## Data Structures

Python provides several built-in data structures for organizing data:

### Lists

Lists are ordered, mutable sequences of items:

!!! example "Lists"
    ```python
    # Create a list
    chromosomes = [1, 2, 3, 4, 5]
    variants = ["rs123", "rs456", "rs789"]
    mixed = [1, "rs123", 0.05, True]
    
    # Access elements (indexing starts at 0)
    first_chr = chromosomes[0]        # 1
    last_variant = variants[-1]        # "rs789" (negative index from end)
    
    # Modify elements
    variants[0] = "rs111"             # Change first element
    
    # List operations
    len(chromosomes)                   # 5
    chromosomes.append(6)              # Add element: [1, 2, 3, 4, 5, 6]
    chromosomes.extend([7, 8])        # Add multiple: [1, 2, 3, 4, 5, 6, 7, 8]
    
    # Slicing
    first_three = chromosomes[0:3]     # [1, 2, 3]
    last_two = chromosomes[-2:]       # [7, 8]
    
    # List methods
    p_values = [0.1, 0.05, 0.01, 0.001]
    p_values.sort()                    # Sort in place: [0.001, 0.01, 0.05, 0.1]
    min_p = min(p_values)              # 0.001
    max_p = max(p_values)              # 0.1
    ```

!!! example "Working with variant data in lists"
    ```python
    # Store variant information
    variant_ids = ["rs123456", "rs234567", "rs345678"]
    chromosomes = [1, 1, 2]
    positions = [12345, 23456, 34567]
    p_values = [0.05, 1e-8, 0.001]
    
    # Find significant variants
    significant_indices = []
    for i, p in enumerate(p_values):
        if p < 5e-8:
            significant_indices.append(i)
    
    # Get significant variant IDs
    sig_variants = [variant_ids[i] for i in significant_indices]
    ```

### Dictionaries

Dictionaries store key-value pairs. They're very useful for organizing data:

!!! example "Dictionaries"
    ```python
    # Create a dictionary
    variant_info = {
        "rsid": "rs123456",
        "chromosome": 1,
        "position": 12345,
        "p_value": 0.0001,
        "effect_size": 0.15
    }
    
    # Access values
    rsid = variant_info["rsid"]                    # "rs123456"
    pval = variant_info.get("p_value", 1.0)      # 0.0001 (with default)
    
    # Modify values
    variant_info["p_value"] = 1e-8
    variant_info["maf"] = 0.25                    # Add new key-value pair
    
    # Dictionary methods
    keys = variant_info.keys()                     # dict_keys(['rsid', 'chromosome', ...])
    values = variant_info.values()                 # dict_values(['rs123456', 1, ...])
    items = variant_info.items()                   # dict_items([('rsid', 'rs123456'), ...])
    
    # Check if key exists
    if "rsid" in variant_info:
        print(variant_info["rsid"])
    ```

!!! example "Storing multiple variants"
    ```python
    # Dictionary of variants
    variants = {
        "rs123456": {
            "chr": 1,
            "pos": 12345,
            "p": 1e-8,
            "beta": 0.15
        },
        "rs234567": {
            "chr": 2,
            "pos": 23456,
            "p": 0.05,
            "beta": 0.08
        }
    }
    
    # Access nested dictionary
    rs123_chr = variants["rs123456"]["chr"]        # 1
    rs123_p = variants["rs123456"]["p"]            # 1e-8
    ```

### Tuples

Tuples are ordered, immutable sequences. Use them when you need a fixed collection:

!!! example "Tuples"
    ```python
    # Create a tuple
    coordinates = (1, 12345)                       # (chromosome, position)
    variant = ("rs123456", 1, 12345, 0.0001)       # (rsid, chr, pos, p)
    
    # Access elements
    chromosome = coordinates[0]                    # 1
    position = coordinates[1]                      # 12345
    
    # Tuples are immutable (cannot be changed)
    # coordinates[0] = 2  # This would cause an error
    
    # Unpacking
    rsid, chr, pos, p = variant
    ```

!!! tip "When to use tuples vs lists"
    - **Tuples**: Use when the collection shouldn't change (e.g., coordinates, fixed parameters)
    - **Lists**: Use when you need to modify the collection (e.g., adding/removing variants)

### Sets

Sets are unordered collections of unique elements:

!!! example "Sets"
    ```python
    # Create a set
    chromosomes = {1, 2, 3, 4, 5}
    unique_variants = {"rs123", "rs456", "rs789"}
    
    # Set operations
    chromosomes.add(6)                             # Add element
    chromosomes.remove(1)                          # Remove element
    len(chromosomes)                               # Get size
    
    # Set operations (union, intersection, difference)
    set1 = {1, 2, 3, 4}
    set2 = {3, 4, 5, 6}
    union = set1 | set2                            # {1, 2, 3, 4, 5, 6}
    intersection = set1 & set2                     # {3, 4}
    difference = set1 - set2                       # {1, 2}
    ```

!!! example "Finding unique variants"
    ```python
    # Remove duplicates from a list
    variant_list = ["rs123", "rs456", "rs123", "rs789", "rs456"]
    unique_variants = set(variant_list)            # {"rs123", "rs456", "rs789"}
    unique_list = list(unique_variants)            # Convert back to list
    ```

## Control Flow

Control flow statements allow you to execute code conditionally or repeatedly.

### Conditional Statements

Use `if`, `elif`, and `else` for conditional execution:

!!! example "If statements"
    ```python
    # Basic if statement
    p_value = 0.0001
    
    if p_value < 5e-8:
        print("Genome-wide significant!")
    elif p_value < 0.05:
        print("Nominally significant")
    else:
        print("Not significant")
    
    # Multiple conditions
    maf = 0.01
    call_rate = 0.98
    
    if maf > 0.01 and call_rate > 0.95:
        print("Passes QC")
    else:
        print("Fails QC")
    ```

!!! example "Filtering variants by significance"
    ```python
    variants = [
        {"rsid": "rs123", "p": 1e-8, "chr": 1},
        {"rsid": "rs456", "p": 0.05, "chr": 2},
        {"rsid": "rs789", "p": 1e-9, "chr": 3}
    ]
    
    significant_variants = []
    for variant in variants:
        if variant["p"] < 5e-8:
            significant_variants.append(variant["rsid"])
    
    print(significant_variants)  # ["rs123", "rs789"]
    ```

### Loops

Loops allow you to repeat code. Python has `for` and `while` loops:

!!! example "For loops"
    ```python
    # Iterate over a list
    chromosomes = [1, 2, 3, 4, 5]
    for chr in chromosomes:
        print(f"Processing chromosome {chr}")
    
    # Iterate with index
    variants = ["rs123", "rs456", "rs789"]
    for i, variant in enumerate(variants):
        print(f"Index {i}: {variant}")
    
    # Iterate over dictionary
    variant_info = {"rsid": "rs123", "chr": 1, "pos": 12345}
    for key, value in variant_info.items():
        print(f"{key}: {value}")
    
    # Range function
    for i in range(5):              # 0, 1, 2, 3, 4
        print(i)
    
    for i in range(1, 6):            # 1, 2, 3, 4, 5
        print(i)
    ```

!!! example "While loops"
    ```python
    # While loop
    count = 0
    while count < 5:
        print(count)
        count += 1
    
    # Process until condition is met
    p_value = 1.0
    iterations = 0
    while p_value > 0.05 and iterations < 100:
        # Some calculation that updates p_value
        p_value = p_value * 0.9
        iterations += 1
    ```

!!! example "List comprehensions"
    ```python
    # List comprehension (concise way to create lists)
    p_values = [0.1, 0.05, 0.01, 1e-8, 0.001]
    
    # Traditional approach
    significant = []
    for p in p_values:
        if p < 5e-8:
            significant.append(p)
    
    # List comprehension (more Pythonic)
    significant = [p for p in p_values if p < 5e-8]
    
    # More complex example
    variants = ["rs123", "rs456", "rs789"]
    variant_lengths = [len(v) for v in variants]  # [5, 5, 5]
    
    # With transformation
    chromosomes = [1, 2, 3]
    chr_strings = [f"chr{chr}" for chr in chromosomes]  # ["chr1", "chr2", "chr3"]
    ```

!!! example "Processing genomic data with loops"
    ```python
    # Process variants from a file-like structure
    variant_data = [
        ("rs123", 1, 12345, 0.05),
        ("rs456", 1, 23456, 1e-8),
        ("rs789", 2, 34567, 0.001)
    ]
    
    # Count significant variants per chromosome
    chr_counts = {}
    for rsid, chr, pos, p in variant_data:
        if p < 5e-8:
            if chr in chr_counts:
                chr_counts[chr] += 1
            else:
                chr_counts[chr] = 1
    
    print(chr_counts)  # {1: 1}
    ```

## Functions

Functions allow you to organize code into reusable blocks:

!!! example "Defining functions"
    ```python
    # Simple function
    def greet(name):
        return f"Hello, {name}!"
    
    result = greet("Alice")
    print(result)  # "Hello, Alice!"
    
    # Function with multiple parameters
    def calculate_odds_ratio(beta):
        """Calculate odds ratio from beta coefficient."""
        import math
        return math.exp(beta)
    
    or_value = calculate_odds_ratio(0.2)
    print(or_value)  # ~1.22
    ```

!!! example "Function with default parameters"
    ```python
    def check_significance(p_value, threshold=5e-8):
        """Check if p-value is significant."""
        return p_value < threshold
    
    # Use default threshold
    is_sig1 = check_significance(1e-8)  # True (uses 5e-8)
    
    # Use custom threshold
    is_sig2 = check_significance(0.01, threshold=0.05)  # True
    ```

!!! example "Genomics-related functions"
    ```python
    def calculate_gc_content(sequence):
        """Calculate GC content of a DNA sequence."""
        sequence = sequence.upper()
        gc_count = sequence.count("G") + sequence.count("C")
        return gc_count / len(sequence) if len(sequence) > 0 else 0
    
    def filter_variants(variants, min_maf=0.01, max_p=0.05):
        """Filter variants by MAF and p-value."""
        filtered = []
        for variant in variants:
            if variant["maf"] >= min_maf and variant["p"] <= max_p:
                filtered.append(variant)
        return filtered
    
    # Usage
    seq = "ATGCGATCG"
    gc = calculate_gc_content(seq)
    print(f"GC content: {gc:.2%}")  # GC content: 44.44%
    
    variants = [
        {"rsid": "rs123", "maf": 0.05, "p": 0.01},
        {"rsid": "rs456", "maf": 0.005, "p": 0.03},
        {"rsid": "rs789", "maf": 0.02, "p": 0.1}
    ]
    filtered = filter_variants(variants, min_maf=0.01, max_p=0.05)
    print([v["rsid"] for v in filtered])  # ["rs123"]
    ```

## File Input/Output

Reading from and writing to files is essential for working with genomic data:

!!! example "Reading files"
    ```python
    # Read entire file
    with open("variants.txt", "r") as f:
        content = f.read()
    
    # Read line by line
    with open("variants.txt", "r") as f:
        for line in f:
            print(line.strip())  # strip() removes newline
    
    # Read all lines into a list
    with open("variants.txt", "r") as f:
        lines = f.readlines()
    
    # More Pythonic: read lines directly
    with open("variants.txt", "r") as f:
        lines = [line.strip() for line in f]
    ```

!!! example "Writing files"
    ```python
    # Write to file
    variants = ["rs123", "rs456", "rs789"]
    with open("output.txt", "w") as f:
        for variant in variants:
            f.write(f"{variant}\n")
    
    # Write multiple lines at once
    data = ["rs123\t1\t12345", "rs456\t2\t23456"]
    with open("output.txt", "w") as f:
        f.write("\n".join(data))
    ```

!!! example "Processing tab-separated files (common in genomics)"
    ```python
    # Read TSV file (like sumstats)
    significant_variants = []
    
    with open("sumstats.txt", "r") as f:
        header = f.readline().strip().split("\t")
        print(f"Columns: {header}")
        
        for line in f:
            fields = line.strip().split("\t")
            variant_dict = dict(zip(header, fields))
            
            # Convert p-value to float and check significance
            p_value = float(variant_dict["P"])
            if p_value < 5e-8:
                significant_variants.append(variant_dict)
    
    print(f"Found {len(significant_variants)} significant variants")
    ```

!!! example "Writing TSV files"
    ```python
    # Write variant data to TSV
    variants = [
        {"rsid": "rs123", "chr": 1, "pos": 12345, "p": 1e-8},
        {"rsid": "rs456", "chr": 2, "pos": 23456, "p": 1e-9}
    ]
    
    with open("significant_variants.txt", "w") as f:
        # Write header
        f.write("RSID\tCHR\tPOS\tP\n")
        
        # Write data
        for variant in variants:
            f.write(f"{variant['rsid']}\t{variant['chr']}\t{variant['pos']}\t{variant['p']}\n")
    ```

!!! tip "File modes"
    - `"r"`: Read mode (default)
    - `"w"`: Write mode (overwrites existing file)
    - `"a"`: Append mode (adds to end of file)
    - `"r+"`: Read and write mode

## Working with Libraries

Python's power comes from its extensive library ecosystem. For genomics and data analysis, key libraries include:

### NumPy

NumPy provides arrays and numerical operations:

!!! example "NumPy basics"
    ```python
    import numpy as np
    
    # Create arrays
    p_values = np.array([0.1, 0.05, 0.01, 1e-8, 0.001])
    
    # Array operations
    log_p = -np.log10(p_values)           # -log10(p)
    significant = p_values < 5e-8          # Boolean array
    sig_count = np.sum(significant)        # Count of True values
    
    # Statistical functions
    mean_p = np.mean(p_values)
    min_p = np.min(p_values)
    max_p = np.max(p_values)
    
    # Array indexing
    first_three = p_values[0:3]            # [0.1, 0.05, 0.01]
    significant_p = p_values[significant]   # Get only significant p-values
    ```

### Pandas

Pandas provides DataFrames for working with tabular data (like Excel spreadsheets):

!!! example "Pandas basics"
    ```python
    import pandas as pd
    
    # Read TSV file into DataFrame
    df = pd.read_csv("sumstats.txt", sep="\t")
    
    # Basic operations
    print(df.head())                       # First 5 rows
    print(df.shape)                        # (rows, columns)
    print(df.columns)                     # Column names
    print(df.dtypes)                       # Data types
    
    # Access columns
    p_values = df["P"]
    chromosomes = df["CHROM"]
    
    # Filtering
    significant = df[df["P"] < 5e-8]
    chr1_variants = df[df["CHROM"] == 1]
    
    # Multiple conditions
    filtered = df[(df["P"] < 5e-8) & (df["CHROM"] == 1)]
    
    # Add new column
    df["MLOG10P"] = -np.log10(df["P"])
    
    # Group operations
    chr_counts = df.groupby("CHROM").size()
    mean_p_by_chr = df.groupby("CHROM")["P"].mean()
    
    # Write to file
    significant.to_csv("significant.txt", sep="\t", index=False)
    ```

!!! example "Common pandas operations for GWAS"
    ```python
    import pandas as pd
    import numpy as np
    
    # Read sumstats
    df = pd.read_csv("sumstats.txt", sep="\t")
    
    # Basic QC filters
    qc_passed = df[
        (df["MAF"] > 0.01) &           # Minor allele frequency > 1%
        (df["INFO"] > 0.8) &           # Imputation quality > 0.8
        (df["P"] > 0) &                # Valid p-values
        (df["P"] <= 1)
    ]
    
    # Calculate -log10(p)
    qc_passed["MLOG10P"] = -np.log10(qc_passed["P"])
    
    # Find genome-wide significant variants
    gws = qc_passed[qc_passed["P"] < 5e-8]
    
    # Summary statistics
    print(f"Total variants: {len(df)}")
    print(f"After QC: {len(qc_passed)}")
    print(f"Genome-wide significant: {len(gws)}")
    print(f"Mean p-value: {qc_passed['P'].mean():.2e}")
    
    # Save results
    gws.to_csv("gws_variants.txt", sep="\t", index=False)
    ```

!!! tip "Installing libraries"
    Use `pip` to install Python packages:
    ```bash
    pip install numpy pandas
    # or
    pip3 install numpy pandas
    ```

## Examples for Genomics

Here are some practical examples combining the concepts above:

!!! example "Parse VCF-like data"
    ```python
    def parse_vcf_line(line):
        """Parse a line from a VCF file."""
        fields = line.strip().split("\t")
        if len(fields) < 8:
            return None
        
        return {
            "chr": fields[0],
            "pos": int(fields[1]),
            "id": fields[2],
            "ref": fields[3],
            "alt": fields[4],
            "qual": fields[5],
            "filter": fields[6],
            "info": fields[7]
        }
    
    # Read and parse VCF
    variants = []
    with open("variants.vcf", "r") as f:
        for line in f:
            if line.startswith("#"):
                continue  # Skip header lines
            variant = parse_vcf_line(line)
            if variant:
                variants.append(variant)
    
    print(f"Found {len(variants)} variants")
    ```

!!! example "Calculate allele frequencies"
    ```python
    def calculate_maf(genotype_counts):
        """
        Calculate minor allele frequency from genotype counts.
        genotype_counts: dict with keys 'AA', 'Aa', 'aa' and counts as values
        """
        total = sum(genotype_counts.values())
        if total == 0:
            return 0.0
        
        # Count alleles
        a_count = 2 * genotype_counts.get('AA', 0) + genotype_counts.get('Aa', 0)
        total_alleles = 2 * total
        
        maf = a_count / total_alleles
        # Return the minor (less frequent) allele frequency
        return min(maf, 1 - maf)
    
    # Example usage
    counts = {'AA': 100, 'Aa': 50, 'aa': 10}
    maf = calculate_maf(counts)
    print(f"Minor allele frequency: {maf:.3f}")
    ```

!!! example "Filter and summarize GWAS results"
    ```python
    def process_gwas_results(filename, p_threshold=5e-8):
        """Process GWAS summary statistics."""
        results = {
            "total": 0,
            "significant": 0,
            "by_chromosome": {}
        }
        
        with open(filename, "r") as f:
            header = f.readline().strip().split("\t")
            chr_idx = header.index("CHROM")
            p_idx = header.index("P")
            
            for line in f:
                fields = line.strip().split("\t")
                if len(fields) <= max(chr_idx, p_idx):
                    continue
                
                results["total"] += 1
                chromosome = fields[chr_idx]
                p_value = float(fields[p_idx])
                
                if p_value < p_threshold:
                    results["significant"] += 1
                    if chromosome not in results["by_chromosome"]:
                        results["by_chromosome"][chromosome] = 0
                    results["by_chromosome"][chromosome] += 1
        
        return results
    
    # Usage
    results = process_gwas_results("sumstats.txt")
    print(f"Total variants: {results['total']}")
    print(f"Genome-wide significant: {results['significant']}")
    print("By chromosome:")
    for chr, count in sorted(results["by_chromosome"].items()):
        print(f"  Chr {chr}: {count}")
    ```

!!! example "Convert between data formats"
    ```python
    def convert_sumstats_to_bed(sumstats_file, output_file):
        """Convert sumstats to BED format (chr, start, end, name)."""
        with open(sumstats_file, "r") as infile, open(output_file, "w") as outfile:
            header = infile.readline().strip().split("\t")
            chr_idx = header.index("CHROM")
            pos_idx = header.index("POS")
            id_idx = header.index("ID")
            
            # BED format: chr, start, end, name
            outfile.write("chr\tstart\tend\tname\n")
            
            for line in infile:
                fields = line.strip().split("\t")
                if len(fields) <= max(chr_idx, pos_idx, id_idx):
                    continue
                
                chromosome = fields[chr_idx]
                position = int(fields[pos_idx])
                variant_id = fields[id_idx]
                
                # BED uses 0-based coordinates, end is exclusive
                # For point variants, use position-1 as start, position as end
                outfile.write(f"{chromosome}\t{position-1}\t{position}\t{variant_id}\n")
    
    # Usage
    convert_sumstats_to_bed("sumstats.txt", "variants.bed")
    ```

## Best Practices

!!! tip "Code organization"
    - Use meaningful variable names
    - Add comments for complex logic
    - Break code into functions
    - Keep functions focused on one task

!!! tip "Error handling"
    ```python
    # Use try-except for error handling
    try:
        p_value = float(variant["P"])
    except (KeyError, ValueError) as e:
        print(f"Error processing variant: {e}")
        p_value = None
    ```

!!! tip "Code style"
    - Follow PEP 8 style guide
    - Use 4 spaces for indentation (not tabs)
    - Keep lines under 79-99 characters
    - Use descriptive function and variable names

## Next Steps

Now that you understand Python basics, you can:

1. **Learn pandas in depth**: Essential for working with genomic data tables
2. **Explore bioinformatics libraries**: Biopython, pysam, pyvcf
3. **Practice with real data**: Work with actual GWAS summary statistics
4. **Learn visualization**: Matplotlib, seaborn for plotting
5. **Advanced topics**: Object-oriented programming, modules, packages

## References

- **Official Python documentation**: https://docs.python.org/3/
- **Pandas documentation**: https://pandas.pydata.org/docs/
- **NumPy documentation**: https://numpy.org/doc/
- **Python for Data Analysis** (book by Wes McKinney)
