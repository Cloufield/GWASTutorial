# R Basics

## Introduction

This section provides a minimum introduction to R programming for handling genomic data and conducting GWAS analyses. R is a powerful statistical programming language that is widely used in bioinformatics, statistical genetics, and data analysis.

If you are a beginner with no background in programming, this tutorial will help you learn the fundamental concepts needed to work with genomic data in R.

!!! note "For beginners"
    This tutorial assumes no prior programming experience. We'll start with the basics and gradually build up to more complex concepts relevant to genomic data analysis.

!!! tip "Why R for genomics?"
    - **Statistical power**: R was designed for statistical analysis and has extensive statistical functions
    - **Rich ecosystem**: Thousands of packages for genomics (Bioconductor, CRAN)
    - **Data visualization**: Excellent plotting capabilities (ggplot2, base R graphics)
    - **Reproducibility**: R Markdown for creating reproducible reports
    - **Community**: Large bioinformatics and statistics community
    - **GWAS tools**: Many GWAS-specific packages available

## Table of Contents

- [Getting Started](#getting-started)
    - Installation and setup
    - Running R code
- [Basic Data Types](#basic-data-types)
    - Numbers, strings, logicals
- [Variables and Operators](#variables-and-operators)
- [Data Structures](#data-structures)
    - Vectors, matrices, lists, data frames
- [Subsetting](#subsetting)
    - Accessing elements from data structures
- [Control Flow](#control-flow)
    - Conditional statements, loops
- [Functions](#functions)
    - Defining and using functions
- [File Input/Output](#file-inputoutput)
    - Reading and writing files
- [Working with Packages](#working-with-packages)
    - Installing and using R packages
- [Examples for Genomics](#examples-for-genomics)
    - Practical genomics examples
- [Statistical Functions](#statistical-functions)
    - Common statistical operations

## Getting Started

### Installation

R can be installed from CRAN (The Comprehensive R Archive Network) or using package managers.

!!! info "CRAN"
    [https://cran.r-project.org/](https://cran.r-project.org/)

!!! example "Check R version"
    ```r
    > R.version.string
    [1] "R version 4.3.0 (2023-04-21)"
    ```

### Install R using conda

It is convenient to use conda to manage your R environment.

!!! example "Install R with conda"
    ```bash
    conda install -c conda-forge r-base=4.x.x
    ```

### IDE for R: Posit (RStudio)

Posit (formerly RStudio) is one of the most commonly used Integrated Development Environment (IDE) for R.

!!! info "Posit (RStudio)"
    [https://posit.co/](https://posit.co/)

RStudio provides:
- Syntax highlighting
- Integrated help system
- Package management
- R Markdown support
- Debugging tools
- Git integration

### Running R Code

There are several ways to run R code:

1. **Interactive R (REPL)**: Type `R` in terminal
2. **R scripts**: Save code in `.R` files and run with `Rscript script.R`
3. **RStudio**: Use the integrated console or run scripts
4. **R Markdown**: Create reproducible reports with embedded R code

!!! example "Interactive R session"
    ```r
    $ R
    
    R version 4.3.0 (2023-04-21) -- "Already Tomorrow"
    Copyright (C) 2023 The R Foundation for Statistical Computing
    ...
    
    > print("Hello, World!")
    [1] "Hello, World!"
    > q()  # or quit()
    ```

!!! example "R script"
    Create a file `hello.R`:
    ```r
    # hello.R
    print("Hello, World!")
    ```
    
    Run it:
    ```bash
    $ Rscript hello.R
    [1] "Hello, World!"
    ```

### Comments

Comments help document your code. Use `#` for single-line comments:

!!! example "Comments in R"
    ```r
    # This is a comment
    x <- 5  # This is also a comment
    
    # Multi-line comments require # on each line
    # This is line 1 of a comment
    # This is line 2 of a comment
    ```

## Basic Data Types

R has several atomic (basic) data types. The most common ones are:

### Numbers

R supports integers and floating-point numbers (numeric):

!!! example "Numbers"
    ```r
    # Numeric (floating-point)
    x <- 42
    y <- 3.14159
    height <- 175.5
    
    # Integer (specify with L)
    count <- 100L
    
    # Basic arithmetic
    sum_result <- 10 + 5        # 15
    product <- 3 * 4            # 12
    division <- 10 / 3          # 3.333...
    power <- 2 ^ 3              # 8 (or 2 ** 3)
    remainder <- 10 %% 3        # 1 (modulo)
    integer_division <- 10 %/% 3 # 3
    ```

### Strings (Characters)

Strings are sequences of characters, enclosed in single or double quotes:

!!! example "Strings"
    ```r
    # String creation
    name <- "Alice"
    chromosome <- 'chr1'
    variant_id <- "rs123456"
    
    # String operations
    full_name <- paste(name, "Smith")              # "Alice Smith"
    full_name2 <- paste(name, "Smith", sep = "")   # "AliceSmith"
    repeated <- paste(rep("AT", 3), collapse = "") # "ATATAT"
    length <- nchar(name)                          # 5
    
    # String functions
    text <- "  hello world  "
    trimws(text)                                    # "hello world"
    toupper(text)                                   # "  HELLO WORLD  "
    tolower(text)                                   # "  hello world  "
    
    # String formatting (using sprintf or paste)
    variant <- "rs123456"
    p_value <- 0.0001
    message <- paste("Variant", variant, "has p-value", p_value)
    # "Variant rs123456 has p-value 0.0001"
    
    # Or using sprintf
    message2 <- sprintf("Variant %s has p-value %.4f", variant, p_value)
    # "Variant rs123456 has p-value 0.0001"
    ```

!!! example "Working with genomic sequences"
    ```r
    # DNA sequence
    sequence <- "ATGCGATCG"
    sequence_length <- nchar(sequence)              # 9
    
    # Count GC content
    gc_count <- sum(strsplit(sequence, "")[[1]] %in% c("G", "C"))
    gc_content <- gc_count / sequence_length       # 0.444...
    
    # Using stringr package (if installed)
    # library(stringr)
    # gc_count <- str_count(sequence, "[GC]")
    ```

### Logical (Booleans)

Logicals represent truth values: `TRUE` or `FALSE` (can be abbreviated as `T` or `F`):

!!! example "Logicals"
    ```r
    is_significant <- TRUE
    is_rare <- FALSE
    
    # Logical operations
    result1 <- TRUE & FALSE    # FALSE (AND)
    result2 <- TRUE | FALSE    # TRUE (OR)
    result3 <- !TRUE           # FALSE (NOT)
    
    # Comparisons return logicals
    p_value <- 0.0001
    is_significant <- p_value < 0.05  # TRUE
    ```

!!! tip "TRUE/FALSE vs T/F"
    While `T` and `F` can be used as abbreviations, it's better practice to use `TRUE` and `FALSE` because `T` and `F` can be overwritten as variables.

## Variables and Operators

### Variables

Variables store values. In R, use `<-` or `=` for assignment (though `<-` is preferred):

!!! example "Variables"
    ```r
    # Variable assignment
    variant_id <- "rs123456"
    chromosome <- 1
    position <- 12345
    p_value <- 0.0001
    is_significant <- p_value < 5e-8
    
    # Variable names should be descriptive
    sample_size <- 10000
    allele_frequency <- 0.25
    effect_size <- 0.15
    
    # Check variable type
    class(variant_id)    # "character"
    class(chromosome)     # "numeric"
    class(is_significant) # "logical"
    ```

!!! tip "Variable naming conventions"
    - Use lowercase with dots or underscores: `variant_id`, `p.value`
    - Be descriptive: `chr` is better than `c`, `p_value` is better than `p`
    - Avoid R keywords: `if`, `for`, `function`, `TRUE`, `FALSE`, etc.

### Operators

R supports various operators:

!!! info "Common operators"
    | Operator | Description | Example |
    |----------|-------------|---------|
    | `+` | Addition | `3 + 5` → `8` |
    | `-` | Subtraction | `10 - 3` → `7` |
    | `*` | Multiplication | `4 * 5` → `20` |
    | `/` | Division | `10 / 3` → `3.333...` |
    | `^` or `**` | Exponentiation | `2 ^ 3` → `8` |
    | `%%` | Modulo (remainder) | `10 %% 3` → `1` |
    | `%/%` | Integer division | `10 %/% 3` → `3` |
    | `==` | Equality | `5 == 5` → `TRUE` |
    | `!=` | Inequality | `5 != 3` → `TRUE` |
    | `<` | Less than | `3 < 5` → `TRUE` |
    | `>` | Greater than | `5 > 3` → `TRUE` |
    | `<=` | Less than or equal | `3 <= 3` → `TRUE` |
    | `>=` | Greater than or equal | `5 >= 3` → `TRUE` |
    | `&` | Logical AND | `TRUE & FALSE` → `FALSE` |
    | `\|` | Logical OR | `TRUE \| FALSE` → `TRUE` |
    | `!` | Logical NOT | `!TRUE` → `FALSE` |

!!! example "Operators in genomics context"
    ```r
    # Calculate odds ratio from beta
    beta <- 0.2
    odds_ratio <- exp(beta)  # e^beta
    
    # Check if variant passes QC filters
    maf <- 0.01
    call_rate <- 0.98
    hwe_p <- 0.001
    
    passes_qc <- (maf > 0.01) & (call_rate > 0.95) & (hwe_p > 0.0001)
    
    # Check genome-wide significance
    p_value <- 1e-8
    is_gws <- p_value < 5e-8  # TRUE
    ```

## Data Structures

R provides several data structures for organizing data:

### Vectors

Vectors are one-dimensional arrays that can hold numeric, character, or logical data. All elements must be of the same type:

!!! example "Vectors"
    ```r
    # Create vectors using c() (combine)
    chromosomes <- c(1, 2, 3, 4, 5)
    variants <- c("rs123", "rs456", "rs789")
    p_values <- c(0.1, 0.05, 0.01, 0.001)
    logicals <- c(TRUE, FALSE, TRUE)
    
    # Create sequences
    numbers <- 1:10           # 1 2 3 4 5 6 7 8 9 10
    even <- seq(2, 10, by = 2) # 2 4 6 8 10
    
    # Vector operations
    length(chromosomes)        # 5
    sum(p_values)             # 0.161
    mean(p_values)            # 0.04025
    min(p_values)             # 0.001
    max(p_values)             # 0.1
    
    # Element-wise operations
    p_values * 2              # 0.2 0.1 0.02 0.002
    p_values + 0.01           # 0.11 0.06 0.02 0.011
    -log10(p_values)          # 1.0 1.301 2.0 3.0
    ```

!!! example "Working with variant data in vectors"
    ```r
    # Store variant information
    variant_ids <- c("rs123456", "rs234567", "rs345678")
    chromosomes <- c(1, 1, 2)
    positions <- c(12345, 23456, 34567)
    p_values <- c(0.05, 1e-8, 0.001)
    
    # Find significant variants
    is_significant <- p_values < 5e-8
    sig_variants <- variant_ids[is_significant]
    
    # Count significant variants
    sum(is_significant)  # 1
    ```

### Matrices

Matrices are two-dimensional arrays with rows and columns. All elements must be of the same type:

!!! example "Matrices"
    ```r
    # Create a matrix
    mymatrix <- matrix(1:6, nrow = 2, ncol = 3)
    #      [,1] [,2] [,3]
    # [1,]    1    3    5
    # [2,]    2    4    6
    
    # Matrix properties
    ncol(mymatrix)        # 3 (number of columns)
    nrow(mymatrix)        # 2 (number of rows)
    dim(mymatrix)         # 2 3 (dimensions)
    length(mymatrix)      # 6 (total elements)
    
    # Matrix operations
    t(mymatrix)           # Transpose
    mymatrix * 2          # Element-wise multiplication
    mymatrix %*% t(mymatrix)  # Matrix multiplication
    ```

!!! example "Genotype matrix"
    ```r
    # Create a simple genotype matrix (samples x variants)
    # 0 = homozygous reference, 1 = heterozygous, 2 = homozygous alternate
    genotypes <- matrix(c(0, 1, 2, 1, 0, 1, 2, 1, 0), nrow = 3, ncol = 3)
    rownames(genotypes) <- c("Sample1", "Sample2", "Sample3")
    colnames(genotypes) <- c("rs123", "rs456", "rs789")
    
    # Calculate allele frequencies
    colMeans(genotypes) / 2  # Allele frequency for alternate allele
    ```

### Lists

Lists are special vectors that can contain elements of different types, including other lists:

!!! example "Lists"
    ```r
    # Create a list
    mylist <- list(1, 0.02, "a", FALSE, c(1, 2, 3), matrix(1:6, nrow = 2, ncol = 3))
    
    # Named list
    variant_info <- list(
        rsid = "rs123456",
        chromosome = 1,
        position = 12345,
        p_value = 0.0001,
        effect_size = 0.15
    )
    
    # Access elements
    variant_info$rsid           # "rs123456"
    variant_info[["chromosome"]] # 1
    variant_info[[1]]           # "rs123456" (by position)
    
    # Add elements
    variant_info$maf <- 0.25
    ```

!!! example "Storing multiple variants"
    ```r
    # List of variant information
    variants <- list(
        rs123456 = list(chr = 1, pos = 12345, p = 1e-8, beta = 0.15),
        rs234567 = list(chr = 2, pos = 23456, p = 0.05, beta = 0.08)
    )
    
    # Access nested list
    variants$rs123456$chr  # 1
    variants$rs123456$p    # 1e-8
    ```

### Data Frames

Data frames are like tables (similar to Excel spreadsheets). They are lists of vectors of equal length, but each column can be a different type:

!!! example "Data Frames"
    ```r
    # Create a data frame
    df <- data.frame(
        rsid = c("rs123", "rs456", "rs789"),
        chromosome = c(1, 1, 2),
        position = c(12345, 23456, 34567),
        p_value = c(0.05, 1e-8, 0.001),
        stringsAsFactors = FALSE  # Important: keep strings as character
    )
    
    # View data frame
    df
    #    rsid chromosome position   p_value
    # 1 rs123          1    12345 5.00e-02
    # 2 rs456          1    23456 1.00e-08
    # 3 rs789          2    34567 1.00e-03
    
    # Data frame properties
    nrow(df)           # 3 (number of rows)
    ncol(df)           # 4 (number of columns)
    dim(df)            # 3 4
    names(df)          # "rsid" "chromosome" "position" "p_value"
    str(df)            # Structure of data frame
    summary(df)        # Summary statistics
    ```

!!! example "Working with GWAS summary statistics"
    ```r
    # Create a data frame with GWAS results
    gwas_results <- data.frame(
        rsid = c("rs123456", "rs234567", "rs345678"),
        chr = c(1, 1, 2),
        pos = c(12345, 23456, 34567),
        ref = c("A", "G", "T"),
        alt = c("G", "A", "C"),
        beta = c(0.15, 0.08, -0.12),
        se = c(0.03, 0.02, 0.04),
        p = c(1e-8, 0.05, 0.001),
        stringsAsFactors = FALSE
    )
    
    # Add calculated columns
    gwas_results$or <- exp(gwas_results$beta)  # Odds ratio
    gwas_results$mlog10p <- -log10(gwas_results$p)  # -log10(p)
    
    # Filter for significant variants
    significant <- gwas_results[gwas_results$p < 5e-8, ]
    ```

## Subsetting

Subsetting allows you to access specific elements from data structures:

### Vector Subsetting

!!! example "Vector subsetting"
    ```r
    myvector <- c(1, 2, 3, 4, 5)
    
    myvector[1]        # 1 (R uses 1-based indexing!)
    myvector[1:3]      # 1 2 3
    myvector[c(1, 3, 5)]  # 1 3 5
    myvector[-1]      # 2 3 4 5 (exclude first element)
    myvector[-c(1, 2)] # 3 4 5
    
    # Logical indexing
    myvector[myvector > 3]  # 4 5
    myvector[myvector %% 2 == 0]  # 2 4 (even numbers)
    ```

### Matrix Subsetting

!!! example "Matrix subsetting"
    ```r
    mymatrix <- matrix(1:6, nrow = 2, ncol = 3)
    #      [,1] [,2] [,3]
    # [1,]    1    3    5
    # [2,]    2    4    6
    
    mymatrix[1, 2]     # 3 (row 1, column 2)
    mymatrix[1, ]     # 1 3 5 (entire first row)
    mymatrix[, 2]      # 3 4 (entire second column)
    mymatrix[1:2, 2:3] # Submatrix
    mymatrix[, -1]     # All rows, exclude first column
    ```

### Data Frame Subsetting

!!! example "Data frame subsetting"
    ```r
    df <- data.frame(
        rsid = c("rs123", "rs456", "rs789"),
        chr = c(1, 1, 2),
        p = c(0.05, 1e-8, 0.001),
        stringsAsFactors = FALSE
    )
    
    # Access columns
    df$rsid            # "rs123" "rs456" "rs789"
    df[["rsid"]]       # Same as above
    df[, "rsid"]       # Same as above
    df["rsid"]         # Returns data frame with one column
    
    # Access rows
    df[1, ]            # First row
    df[1:2, ]          # First two rows
    
    # Access specific cell
    df[1, "rsid"]      # "rs123"
    df[1, 1]           # "rs123"
    
    # Multiple columns
    df[, c("rsid", "p")]
    
    # Logical subsetting (filtering)
    df[df$p < 0.05, ]  # Rows where p < 0.05
    df[df$chr == 1, ]  # Rows where chromosome is 1
    df[df$p < 5e-8 & df$chr == 1, ]  # Multiple conditions
    ```

!!! example "Filtering GWAS results"
    ```r
    # Filter for genome-wide significant variants
    gws <- df[df$p < 5e-8, ]
    
    # Filter for chromosome 1
    chr1_variants <- df[df$chr == 1, ]
    
    # Filter with multiple conditions
    filtered <- df[df$p < 0.05 & df$chr == 1, ]
    
    # Order by p-value
    df_ordered <- df[order(df$p), ]
    
    # Top 10 most significant
    top10 <- head(df_ordered, 10)
    ```

## Control Flow

Control flow statements allow you to execute code conditionally or repeatedly.

### Conditional Statements

Use `if`, `else if`, and `else` for conditional execution:

!!! example "If statements"
    ```r
    # Basic if statement
    p_value <- 0.0001
    
    if (p_value < 5e-8) {
        print("Genome-wide significant!")
    } else if (p_value < 0.05) {
        print("Nominally significant")
    } else {
        print("Not significant")
    }
    
    # Multiple conditions
    maf <- 0.01
    call_rate <- 0.98
    
    if (maf > 0.01 & call_rate > 0.95) {
        print("Passes QC")
    } else {
        print("Fails QC")
    }
    ```

!!! example "ifelse() for vectorized conditionals"
    ```r
    # ifelse() works on vectors
    p_values <- c(0.1, 0.05, 1e-8, 0.001)
    significance <- ifelse(p_values < 5e-8, "GWS", 
                          ifelse(p_values < 0.05, "Nominal", "NS"))
    # "NS" "Nominal" "GWS" "Nominal"
    ```

### Loops

Loops allow you to repeat code. R has `for` and `while` loops:

!!! example "For loops"
    ```r
    # Iterate over a vector
    chromosomes <- c(1, 2, 3, 4, 5)
    for (chr in chromosomes) {
        print(paste("Processing chromosome", chr))
    }
    
    # Iterate with index
    variants <- c("rs123", "rs456", "rs789")
    for (i in 1:length(variants)) {
        print(paste("Index", i, ":", variants[i]))
    }
    
    # Iterate over data frame rows (usually not recommended - use vectorized operations)
    df <- data.frame(rsid = c("rs123", "rs456"), p = c(0.05, 1e-8))
    for (i in 1:nrow(df)) {
        if (df$p[i] < 5e-8) {
            print(paste(df$rsid[i], "is significant"))
        }
    }
    ```

!!! example "While loops"
    ```r
    # While loop
    count <- 0
    while (count < 5) {
        print(count)
        count <- count + 1
    }
    
    # Process until condition is met
    p_value <- 1.0
    iterations <- 0
    while (p_value > 0.05 & iterations < 100) {
        # Some calculation that updates p_value
        p_value <- p_value * 0.9
        iterations <- iterations + 1
    }
    ```

!!! tip "Vectorization in R"
    R is designed for vectorized operations. Instead of loops, try to use vectorized functions:
    
    ```r
    # Instead of this (slow):
    result <- numeric(length(p_values))
    for (i in 1:length(p_values)) {
        result[i] <- -log10(p_values[i])
    }
    
    # Do this (fast):
    result <- -log10(p_values)
    ```

## Functions

Functions allow you to organize code into reusable blocks:

!!! example "Defining functions"
    ```r
    # Simple function
    greet <- function(name) {
        return(paste("Hello,", name, "!"))
    }
    
    result <- greet("Alice")
    print(result)  # "Hello, Alice !"
    
    # Function with multiple parameters
    calculate_odds_ratio <- function(beta) {
        return(exp(beta))
    }
    
    or_value <- calculate_odds_ratio(0.2)
    print(or_value)  # ~1.22
    ```

!!! example "Function with default parameters"
    ```r
    check_significance <- function(p_value, threshold = 5e-8) {
        return(p_value < threshold)
    }
    
    # Use default threshold
    is_sig1 <- check_significance(1e-8)  # TRUE (uses 5e-8)
    
    # Use custom threshold
    is_sig2 <- check_significance(0.01, threshold = 0.05)  # TRUE
    ```

!!! example "Genomics-related functions"
    ```r
    # Calculate GC content
    calculate_gc_content <- function(sequence) {
        sequence <- toupper(sequence)
        bases <- strsplit(sequence, "")[[1]]
        gc_count <- sum(bases %in% c("G", "C"))
        return(gc_count / nchar(sequence))
    }
    
    # Filter variants
    filter_variants <- function(variants, min_maf = 0.01, max_p = 0.05) {
        filtered <- variants[variants$maf >= min_maf & variants$p <= max_p, ]
        return(filtered)
    }
    
    # Usage
    seq <- "ATGCGATCG"
    gc <- calculate_gc_content(seq)
    print(paste("GC content:", round(gc * 100, 2), "%"))  # "GC content: 44.44 %"
    
    variants <- data.frame(
        rsid = c("rs123", "rs456", "rs789"),
        maf = c(0.05, 0.005, 0.02),
        p = c(0.01, 0.03, 0.1),
        stringsAsFactors = FALSE
    )
    filtered <- filter_variants(variants, min_maf = 0.01, max_p = 0.05)
    print(filtered$rsid)  # "rs123"
    ```

## File Input/Output

Reading from and writing to files is essential for working with genomic data:

!!! example "Reading files"
    ```r
    # Read tab-separated file
    data <- read.table("variants.txt", header = TRUE, sep = "\t", stringsAsFactors = FALSE)
    
    # Read comma-separated file
    data <- read.csv("variants.csv", stringsAsFactors = FALSE)
    
    # Read with more control
    data <- read.table("sumstats.txt", 
                      header = TRUE,
                      sep = "\t",
                      stringsAsFactors = FALSE,
                      na.strings = c("NA", ".", ""))
    ```

!!! example "Writing files"
    ```r
    # Write tab-separated file
    write.table(data, "output.txt", sep = "\t", row.names = FALSE, quote = FALSE)
    
    # Write comma-separated file
    write.csv(data, "output.csv", row.names = FALSE)
    
    # Write with more control
    write.table(data, "output.txt",
               sep = "\t",
               row.names = FALSE,
               col.names = TRUE,
               quote = FALSE)
    ```

!!! example "Processing GWAS summary statistics"
    ```r
    # Read sumstats file
    sumstats <- read.table("sumstats.txt", 
                          header = TRUE,
                          sep = "\t",
                          stringsAsFactors = FALSE)
    
    # Filter for significant variants
    significant <- sumstats[sumstats$P < 5e-8, ]
    
    # Add calculated column
    significant$MLOG10P <- -log10(significant$P)
    
    # Write results
    write.table(significant, 
               "significant_variants.txt",
               sep = "\t",
               row.names = FALSE,
               quote = FALSE)
    ```

!!! tip "Reading large files"
    For very large files, consider:
    - `data.table::fread()` - Much faster for large files
    - `readr::read_tsv()` - Part of tidyverse, faster than base R
    - Reading in chunks if memory is limited

## Working with Packages

R's power comes from its extensive package ecosystem. For genomics, key packages include:

### Installing Packages

!!! example "Installing packages"
    ```r
    # Install from CRAN
    install.packages("ggplot2")
    
    # Install from Bioconductor (for genomics)
    if (!require("BiocManager", quietly = TRUE))
        install.packages("BiocManager")
    BiocManager::install("GenomicRanges")
    
    # Install from GitHub
    # install.packages("devtools")
    # devtools::install_github("user/package")
    ```

### Loading Packages

!!! example "Loading packages"
    ```r
    # Load a package
    library(ggplot2)
    
    # Or use package::function() without loading
    ggplot2::ggplot(data, aes(x = x, y = y))
    ```

### Useful Packages for Genomics

!!! info "Essential R packages for genomics"
    | Package | Purpose | Installation |
    |---------|---------|--------------|
    | **data.table** | Fast data manipulation | `install.packages("data.table")` |
    | **dplyr** | Data manipulation (tidyverse) | `install.packages("dplyr")` |
    | **ggplot2** | Data visualization | `install.packages("ggplot2")` |
    | **Bioconductor** | Genomics packages | See Bioconductor website |
    | **GenomicRanges** | Genomic interval operations | Bioconductor |
    | **VariantAnnotation** | VCF file handling | Bioconductor |
    | **rtracklayer** | Import/export genomic data | Bioconductor |

!!! example "Using dplyr for data manipulation"
    ```r
    library(dplyr)
    
    # Read data
    sumstats <- read.table("sumstats.txt", header = TRUE, sep = "\t", stringsAsFactors = FALSE)
    
    # Filter, mutate, and arrange
    results <- sumstats %>%
        filter(P < 5e-8) %>%
        mutate(MLOG10P = -log10(P)) %>%
        arrange(P) %>%
        select(RSID, CHR, POS, P, MLOG10P)
    
    # Group by chromosome and summarize
    by_chr <- sumstats %>%
        group_by(CHR) %>%
        summarize(
            n_variants = n(),
            n_significant = sum(P < 5e-8),
            mean_p = mean(P)
        )
    ```

## Examples for Genomics

Here are some practical examples combining the concepts above:

!!! example "Parse and filter GWAS results"
    ```r
    # Function to process GWAS summary statistics
    process_gwas_results <- function(filename, p_threshold = 5e-8) {
        # Read file
        data <- read.table(filename, 
                          header = TRUE,
                          sep = "\t",
                          stringsAsFactors = FALSE)
        
        # Filter for significant variants
        significant <- data[data$P < p_threshold, ]
        
        # Calculate -log10(p)
        significant$MLOG10P <- -log10(significant$P)
        
        # Summary statistics
        results <- list(
            total = nrow(data),
            significant = nrow(significant),
            by_chromosome = table(significant$CHR)
        )
        
        return(list(data = significant, summary = results))
    }
    
    # Usage
    gwas_output <- process_gwas_results("sumstats.txt")
    print(gwas_output$summary)
    ```

!!! example "Calculate allele frequencies"
    ```r
    # Calculate minor allele frequency from genotype counts
    calculate_maf <- function(genotype_counts) {
        # genotype_counts should be a named vector: c(AA = 100, Aa = 50, aa = 10)
        total <- sum(genotype_counts)
        if (total == 0) return(0.0)
        
        # Count alleles
        a_count <- 2 * genotype_counts["AA"] + genotype_counts["Aa"]
        total_alleles <- 2 * total
        
        maf <- a_count / total_alleles
        # Return the minor (less frequent) allele frequency
        return(min(maf, 1 - maf))
    }
    
    # Example usage
    counts <- c(AA = 100, Aa = 50, aa = 10)
    maf <- calculate_maf(counts)
    print(paste("Minor allele frequency:", round(maf, 3)))
    ```

!!! example "Manhattan plot data preparation"
    ```r
    # Prepare data for Manhattan plot
    prepare_manhattan_data <- function(sumstats) {
        # Add -log10(p)
        sumstats$MLOG10P <- -log10(sumstats$P)
        
        # Calculate cumulative positions for plotting
        sumstats <- sumstats[order(sumstats$CHR, sumstats$POS), ]
        
        cumulative_pos <- 0
        chr_breaks <- numeric()
        
        for (chr in unique(sumstats$CHR)) {
            chr_data <- sumstats[sumstats$CHR == chr, ]
            max_pos <- max(chr_data$POS)
            
            sumstats$cumulative_pos[sumstats$CHR == chr] <- 
                cumulative_pos + sumstats$POS[sumstats$CHR == chr]
            
            cumulative_pos <- cumulative_pos + max_pos
            chr_breaks <- c(chr_breaks, cumulative_pos)
        }
        
        return(sumstats)
    }
    ```

## Statistical Functions

R has extensive built-in statistical functions:

### Normal Distribution

!!! example "Normal distribution functions"
    ```r
    # Probability density function
    dnorm(1.96)                    # 0.05844094
    
    # Cumulative distribution function
    pnorm(1.96)                     # 0.9750021
    pnorm(1.96, lower.tail = FALSE)  # 0.0249979
    
    # Quantile function
    qnorm(0.975)                    # 1.959964
    
    # Generate random values
    rnorm(10, mean = 0, sd = 1)
    ```

### Chi-square Distribution

!!! example "Chi-square distribution functions"
    ```r
    # Probability density function
    dchisq(5, df = 3)
    
    # Cumulative distribution function
    pchisq(5, df = 3)
    
    # Quantile function
    qchisq(0.95, df = 3)
    
    # Generate random values
    rchisq(10, df = 3)
    ```

### Regression

!!! example "Linear and logistic regression"
    ```r
    # Linear regression
    # y ~ x1 + x2 means: y is modeled as a function of x1 and x2
    model <- lm(formula = phenotype ~ genotype + age + sex, data = mydata)
    
    # View results
    summary(model)
    coefficients(model)
    
    # Logistic regression
    logistic_model <- glm(formula = disease ~ genotype + age + sex,
                         family = binomial(link = "logit"),
                         data = mydata)
    
    summary(logistic_model)
    ```

!!! example "GWAS association test"
    ```r
    # Simple GWAS association test
    # Assuming you have phenotype and genotype data
    perform_gwas <- function(phenotype, genotype, covariates = NULL) {
        if (is.null(covariates)) {
            model <- lm(phenotype ~ genotype)
        } else {
            # Include covariates
            formula_str <- "phenotype ~ genotype"
            for (cov in names(covariates)) {
                formula_str <- paste(formula_str, "+", cov)
            }
            model <- lm(as.formula(formula_str), 
                       data = cbind(phenotype, genotype, covariates))
        }
        
        results <- summary(model)$coefficients
        return(list(
            beta = results["genotype", "Estimate"],
            se = results["genotype", "Std. Error"],
            p = results["genotype", "Pr(>|t|)"]
        ))
    }
    ```

## Best Practices

!!! tip "Code organization"
    - Use meaningful variable names
    - Add comments for complex logic
    - Break code into functions
    - Keep functions focused on one task
    - Use consistent style (consider `styler` package)

!!! tip "Performance"
    - Prefer vectorized operations over loops
    - Use `data.table` or `dplyr` for large data frames
    - Consider parallel processing for intensive computations
    - Profile code to identify bottlenecks

!!! tip "Reproducibility"
    - Set random seeds: `set.seed(123)`
    - Use `sessionInfo()` to record package versions
    - Consider using `renv` for package management
    - Use R Markdown for reproducible reports

!!! tip "Error handling"
    ```r
    # Use tryCatch for error handling
    result <- tryCatch({
        read.table("file.txt", header = TRUE)
    }, error = function(e) {
        print(paste("Error reading file:", e$message))
        return(NULL)
    })
    ```

## Next Steps

Now that you understand R basics, you can:

1. **Learn tidyverse**: Modern R packages for data manipulation (dplyr, tidyr, ggplot2)
2. **Explore Bioconductor**: Genomics-specific packages and workflows
3. **Practice with real data**: Work with actual GWAS summary statistics
4. **Learn visualization**: ggplot2 for publication-quality plots
5. **Advanced topics**: Object-oriented programming, package development, Shiny apps

## References

- **Official R documentation**: https://www.r-project.org/
- **R for Data Science** (book by Hadley Wickham): https://r4ds.hadley.nz/
- **Bioconductor**: https://bioconductor.org/
- **CRAN**: https://cran.r-project.org/
- **RStudio Cheat Sheets**: https://posit.co/resources/cheatsheets/
