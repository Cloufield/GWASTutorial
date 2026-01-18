# Data format

## Overview

This section provides a brief guide to the most commonly used data formats in complex trait genomic analysis and genome-wide association studies (GWAS). Understanding these formats is essential for working with genomic data, as different stages of the analysis pipeline require different file formats, each optimized for specific purposes.

The data formats covered here span the entire workflow from raw sequencing data to analysis-ready genotype files:

- **General-purpose formats** (txt, tsv, csv) for tabular data and results
- **Sequence formats** (FASTA, FASTQ) for storing raw DNA sequences and quality scores
- **Alignment formats** (SAM/BAM) for storing mapped sequencing reads
- **Variant and genotype formats** (VCF, PLINK formats) for storing genetic variants and genotype calls
- **Imputation dosage formats** (bgen, pgen) for storing imputed genotype probabilities

Each format serves a specific role in the genomic data processing pipeline, from initial sequencing through variant calling, quality control, and statistical analysis. This guide includes examples and references to help you understand the structure and usage of each format. 

## Table of Contents
- [Data formats for general purposes](#data-formats-for-general-purposes)
    - [txt](#txt)
    - [tsv](#tsv)
    - [csv](#csv)
- [Data formats in bioinformatics](#data-formats-in-bioinformatics)
    - [Sequence](#sequence)
        - FASTA
        - FASTQ
    - [Alignment](#alignment)
        - SAM/BAM
    - [Variant and genotype](#variant-and-genotype)
        - VCF/BCF
        - ped/map
        - bed/fam/bim
    - [Imputation dosage](#imputation-dosage)
        - bgen
        - pgen

## Data formats for general purposes

### txt
Plain text files are the most basic format for storing unstructured data. In genomic analysis, they are commonly used for storing notes, documentation, log files, or any text-based information that doesn't require a specific structure. While simple, text files are human-readable and can be easily processed with standard command-line tools.

!!! example "`.txt`"
    ```
    cat sample_text.txt 
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. In ut sem congue, tristique tortor et, ullamcorper elit. Nulla elementum, erat ac fringilla mattis, nisi tellus euismod dui, interdum laoreet orci velit vel leo. Vestibulum neque mi, pharetra in tempor id, malesuada at ipsum. Duis tellus enim, suscipit sit amet vestibulum in, ultricies vitae erat. Proin consequat id quam sed sodales. Ut a magna non tellus dictum aliquet vitae nec mi. Suspendisse potenti. Vestibulum mauris sem, viverra ac metus sed, scelerisque ornare arcu. Vivamus consequat, libero vitae aliquet tempor, lorem leo mattis arcu, et viverra erat ligula sit amet tortor. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Praesent ut massa ac tortor lobortis placerat. Pellentesque aliquam tortor augue, at rutrum magna molestie et. Etiam congue nulla in venenatis congue. Nunc ac felis pharetra, cursus leo et, finibus eros.
    ```
    Random texts are generated using - https://www.lipsum.com/

### tsv
Tab-separated values (TSV) is a tabular data format where columns are separated by tab characters. TSV files are commonly used in bioinformatics because tabs are less likely to appear in genomic data compared to commas, making them more reliable for data that may contain commas. TSV files are particularly useful for storing variant annotation data, association test results, and other structured genomic datasets. They can be easily read by spreadsheet applications and processed with command-line tools like `awk` and `cut`. 


!!! example "`.tsv`"
    ```
    head sample_data.tsv
    #CHROM	POS	ID	REF	ALT	A1	FIRTH?	TEST	OBS_CT	OR	LOG(OR)_SE	Z_STAT	P	ERRCODE
    1	13273	1:13273:G:C	G	C	C	N	ADD	503	0.750168	0.280794	-1.02373	0.305961	.
    1	14599	1:14599:T:A	T	A	A	N	ADD	503	1.80972	0.231595	2.56124	0.0104299	.
    1	14604	1:14604:A:G	A	G	G	N	ADD	503	1.80972	0.231595	2.56124	0.0104299	.
    1	14930	1:14930:A:G	A	G	G	N	ADD	503	1.70139	0.240245	2.21209	0.0269602	.
    1	69897	1:69897:T:C	T	C	T	N	ADD	503	1.58002	0.194774	2.34855	0.0188466	.
    1	86331	1:86331:A:G	A	G	G	N	ADD	503	1.47006	0.236102	1.63193	0.102694	.
    1	91581	1:91581:G:A	G	A	A	N	ADD	503	0.924422	0.122991	-0.638963	0.522847	.
    1	122872	1:122872:T:G	T	G	G	N	ADD	503	1.07113	0.180776	0.380121	0.703856	.
    1	135163	1:135163:C:T	C	T	T	N	ADD	503	0.711822	0.23908	-1.42182	0.155079	.
    ```

### csv
Comma-separated values (CSV) is a widely-used tabular data format where columns are separated by commas. CSV files are standard in many data analysis workflows and are easily imported into spreadsheet applications and statistical software. In genomic analysis, CSV files are often used for storing summary statistics, phenotype data, and analysis results. Note that CSV files may require special handling when data values themselves contain commas, which is why TSV is sometimes preferred for genomic data. 


!!! example "`.csv`"
    ```
    head sample_data.csv 
    #CHROM,POS,ID,REF,ALT,A1,FIRTH?,TEST,OBS_CT,OR,LOG(OR)_SE,Z_STAT,P,ERRCODE
    1,13273,1:13273:G:C,G,C,C,N,ADD,503,0.750168,0.280794,-1.02373,0.305961,.
    1,14599,1:14599:T:A,T,A,A,N,ADD,503,1.80972,0.231595,2.56124,0.0104299,.
    1,14604,1:14604:A:G,A,G,G,N,ADD,503,1.80972,0.231595,2.56124,0.0104299,.
    1,14930,1:14930:A:G,A,G,G,N,ADD,503,1.70139,0.240245,2.21209,0.0269602,.
    1,69897,1:69897:T:C,T,C,T,N,ADD,503,1.58002,0.194774,2.34855,0.0188466,.
    1,86331,1:86331:A:G,A,G,G,N,ADD,503,1.47006,0.236102,1.63193,0.102694,.
    1,91581,1:91581:G:A,G,A,A,N,ADD,503,0.924422,0.122991,-0.638963,0.522847,.
    1,122872,1:122872:T:G,T,G,G,N,ADD,503,1.07113,0.180776,0.380121,0.703856,.
    1,135163,1:135163:C:T,C,T,T,N,ADD,503,0.711822,0.23908,-1.42182,0.155079,.
    ```
    
## Data formats in bioinformatics

A typical workflow for generating genotype data for genome-wide association analysis.

<img width="900" alt="image" src="https://github.com/Cloufield/GWASTutorial/assets/40289485/42c1f84a-ccc4-4fbe-96ab-366127fa5059">

## Sequence

### fasta
FASTA is a text-based format for representing biological sequences, including nucleotide sequences (DNA/RNA) or amino acid sequences (proteins). Each sequence entry consists of a header line starting with `>` followed by a sequence identifier and optional description, and one or more lines containing the sequence itself. FASTA files are fundamental in genomics as they store reference genomes, gene sequences, and assembled contigs. The format is simple, human-readable, and widely supported by bioinformatics tools.
!!! example "`.fa` or `.fasta`"
   ```
   >SEQ_ID
   GATTTGGGGTTCAAAGCAGTATCGATCAAATAGTAAATCCATTTGTTCAACTCACAGTTT
   ```
   
### fastq
FASTQ is a text-based format that stores both nucleotide sequences and their corresponding per-base quality scores. Each sequence entry consists of four lines: (1) a sequence identifier starting with `@`, (2) the nucleotide sequence, (3) a separator line starting with `+` (optionally followed by the identifier), and (4) quality scores encoded as ASCII characters. FASTQ files are the standard output format from sequencing instruments and are essential for quality control, read filtering, and downstream alignment. The quality scores allow researchers to assess the reliability of each base call in the sequence.

!!! example "`.fastq`"
    ```
    @SEQ_ID
    GATTTGGGGTTCAAAGCAGTATCGATCAAATAGTAAATCCATTTGTTCAACTCACAGTTT
    +
    !''*((((***+))%%%++)(%%%%).1***-+*''))**55CCF>>>>>>CCCCCCC65
    ```    
    Reference: https://en.wikipedia.org/wiki/FASTQ_format

## Alignment

### SAM/BAM
SAM (Sequence Alignment/Map) is a TAB-delimited text format for storing sequence alignments against a reference genome. It consists of a header section (metadata about the reference, read groups, and program information) and an alignment section (one line per read alignment with information about mapping position, CIGAR string, quality scores, and optional tags). BAM is the binary, compressed version of SAM that is more storage-efficient and faster to process. SAM/BAM files are the standard output from read alignment tools (e.g., BWA, Bowtie2) and are used for variant calling, coverage analysis, and visualization. The BAM format is typically preferred for large-scale analyses due to its smaller file size and faster I/O operations.

!!! example "`.sam`"
    ```
    @HD VN:1.6 SO:coordinate
    @SQ SN:ref LN:45
    r001 99 ref 7 30 8M2I4M1D3M = 37 39 TTAGATAAAGGATACTG *
    r002 0 ref 9 30 3S6M1P1I4M * 0 0 AAAAGATAAGGATA *
    r003 0 ref 9 30 5S6M * 0 0 GCCTAAGCTAA * SA:Z:ref,29,-,6H5M,17,0;
    r004 0 ref 16 30 6M14N5M * 0 0 ATAGCTTCAGC *
    r003 2064 ref 29 17 6H5M * 0 0 TAGGC * SA:Z:ref,9,+,5S6M,30,1;
    r001 147 ref 37 30 9M = 7 -39 CAGCGGCAT * NM:i:1
    ```
    Reference : https://samtools.github.io/hts-specs/SAMv1.pdf

## Variant and genotype

### vcf / vcf.gz / vcf.gz.tbi
VCF (Variant Call Format) is a text file format for storing genetic variants and their associated genotype information. A VCF file consists of: (1) meta-information lines (starting with `##`) that describe the file format, reference genome, and field definitions, (2) a header line (starting with `#CHROM`) that lists column names, and (3) data lines containing variant information including chromosome, position, reference and alternate alleles, quality metrics, and genotype calls for each sample. VCF files are the standard format for variant calling pipelines and are used by most downstream analysis tools. VCF files are often compressed as `.vcf.gz` (gzip-compressed) to save space, and `.tbi` (tabix index) files enable fast random access to specific genomic regions without reading the entire file. 

!!! example "`.vcf`"
    ```
    ##fileformat=VCFv4.2
    ##fileDate=20090805
    ##source=myImputationProgramV3.1
    ##reference=file:///seq/references/1000GenomesPilot-NCBI36.fasta
    ##contig=<ID=20,length=62435964,assembly=B36,md5=f126cdf8a6e0c7f379d618ff66beb2da,species="Homo sapiens",taxonomy=x>
    ##phasing=partial
    ##INFO=<ID=NS,Number=1,Type=Integer,Description="Number of Samples With Data">
    ##INFO=<ID=DP,Number=1,Type=Integer,Description="Total Depth">
    ##INFO=<ID=AF,Number=A,Type=Float,Description="Allele Frequency">
    ##INFO=<ID=AA,Number=1,Type=String,Description="Ancestral Allele">
    ##INFO=<ID=DB,Number=0,Type=Flag,Description="dbSNP membership, build 129">
    ##INFO=<ID=H2,Number=0,Type=Flag,Description="HapMap2 membership">
    ##FILTER=<ID=q10,Description="Quality below 10">
    ##FILTER=<ID=s50,Description="Less than 50% of samples have data">
    ##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">
    ##FORMAT=<ID=GQ,Number=1,Type=Integer,Description="Genotype Quality">
    ##FORMAT=<ID=DP,Number=1,Type=Integer,Description="Read Depth">
    ##FORMAT=<ID=HQ,Number=2,Type=Integer,Description="Haplotype Quality">
    #CHROM POS ID REF ALT QUAL FILTER INFO FORMAT NA00001 NA00002 NA00003
    20 14370 rs6054257 G A 29 PASS NS=3;DP=14;AF=0.5;DB;H2 GT:GQ:DP:HQ 0|0:48:1:51,51 1|0:48:8:51,51 1/1:43:5:.,.
    20 17330 . T A 3 q10 NS=3;DP=11;AF=0.017 GT:GQ:DP:HQ 0|0:49:3:58,50 0|1:3:5:65,3 0/0:41:3
    20 1110696 rs6040355 A G,T 67 PASS NS=2;DP=10;AF=0.333,0.667;AA=T;DB GT:GQ:DP:HQ 1|2:21:6:23,27 2|1:2:0:18,2 2/2:35:4
    20 1230237 . T . 47 PASS NS=3;DP=13;AA=T GT:GQ:DP:HQ 0|0:54:7:56,60 0|0:48:4:51,51 0/0:61:2
    20 1234567 microsat1 GTC G,GTCT 50 PASS NS=3;DP=9;AA=G GT:GQ:DP 0/1:35:4 0/2:17:2 1/1:40:3
    ```
    Reference : https://samtools.github.io/hts-specs/VCFv4.2.pdf 

### PLINK format

PLINK is a widely-used software package for genome-wide association studies (GWAS) and population genetics analyses. PLINK genotype data consists of three essential components:

1. **Individual information**: Sample identifiers, pedigree relationships, sex, and phenotype data
2. **Variant information**: Chromosome, position, variant IDs, and allele information
3. **Genotype matrix**: The actual genotype calls for each sample at each variant

PLINK supports multiple format sets to represent this information, each optimized for different use cases:

1. **ped / map**: Original text-based format (human-readable but large file sizes)
2. **fam / bim / bed**: Binary format for PLINK 1.9 (efficient storage and fast processing)
3. **psam / pvar / pgen**: Native format for PLINK 2.0 (extended metadata support and improved efficiency)

The figure below illustrates how these three components are organized in PLINK files:


<img width="900" alt="image" src="https://github.com/Cloufield/GWASTutorial/assets/40289485/70dc5c9c-5096-41af-95ee-4f925483a93c">



### ped / map 

**`.ped` (PLINK/MERLIN/Haploview text pedigree + genotype table)**

The PED file is the original standard text format for storing sample pedigree information and genotype calls in PLINK. It contains no header line, with one line per sample. Each line has 2V+6 fields where V is the number of variants. The first six fields contain sample information (family ID, individual ID, paternal ID, maternal ID, sex, and phenotype), which are the same as those in a `.fam` file. The remaining fields contain genotype calls: fields 7-8 are the two alleles for the first variant, fields 9-10 for the second variant, and so on. The value '0' indicates a missing genotype call. PED files are human-readable but can become very large for datasets with many variants, which is why the binary BED format is preferred for large-scale analyses.

!!! example "`.ped`"
    ```
    # check the first 16 rows and 16 columns of the ped file
    cut -d " " -f 1-16 1KG.EAS.auto.snp.norm.nodup.split.rare002.common015.missing.ped | head
    0 HG00403 0 0 0 -9 G G T T A A G A C C
    0 HG00404 0 0 0 -9 G G T T A A G A T C
    0 HG00406 0 0 0 -9 G G T T A A G A T C
    0 HG00407 0 0 0 -9 G G T T A A A A C C
    0 HG00409 0 0 0 -9 G G T T A A G A C C
    0 HG00410 0 0 0 -9 G G T T A A G A C C
    0 HG00419 0 0 0 -9 G G T T A A A A T C
    0 HG00421 0 0 0 -9 G G T T A A G A C C
    0 HG00422 0 0 0 -9 G G T T A A G A C C
    0 HG00428 0 0 0 -9 G G T T A A G A C C
    0 HG00436 0 0 0 -9 G G A T G A A A C C
    0 HG00437 0 0 0 -9 C G T T A A G A C C
    0 HG00442 0 0 0 -9 G G T T A A G A C C
    0 HG00443 0 0 0 -9 G G T T A A G A C C
    0 HG00445 0 0 0 -9 G G T T A A G A C C
    0 HG00446 0 0 0 -9 C G T T A A G A T C
    ```

**`.map` (PLINK text fileset variant information file)**

The MAP file contains variant information that accompanies a PED file. It is a text file with no header line, containing one line per variant with 3-4 fields:

- **Chromosome code**: Chromosome number or contig name (PLINK 1.9 supports contig names, but older programs may not)
- **Variant identifier**: SNP ID or variant name (e.g., rs number or chromosome:position:ref:alt)
- **Genetic distance**: Position in morgans or centimorgans (optional; can use dummy value of '0' if unknown)
- **Base-pair coordinate**: Physical position on the chromosome

The MAP file provides the genomic coordinates and identifiers for each variant, while the PED file contains the actual genotype data. Together, they form a complete representation of genotype data in PLINK text format.

!!! example "`.map`"
    ```
    head 1KG.EAS.auto.snp.norm.nodup.split.rare002.common015.missing.map
    1       1:13273:G:C     0       13273
    1       1:14599:T:A     0       14599
    1       1:14604:A:G     0       14604
    1       1:14930:A:G     0       14930
    1       1:69897:T:C     0       69897
    1       1:86331:A:G     0       86331
    1       1:91581:G:A     0       91581
    1       1:122872:T:G    0       122872
    1       1:135163:C:T    0       135163
    1       1:233473:C:G    0       233473
    ```

Reference: [https://www.cog-genomics.org/plink/1.9/formats](https://www.cog-genomics.org/plink/1.9/formats)
### bed / fam / bim

The BED/FAM/BIM format set is the binary implementation of the PED/MAP format, providing the same information in a more storage-efficient and faster-to-process format. These three files work together to store genotype data:

- **`.fam` (family file)**: Contains sample/pedigree information (family ID, individual ID, paternal ID, maternal ID, sex, phenotype) - one line per sample. This is identical to the first six columns of a PED file.

- **`.bim` (bim file)**: Contains variant information (chromosome, variant ID, genetic distance, base-pair position, allele 1, allele 2) - one line per variant. This is similar to a MAP file but includes the two alleles.

- **`.bed` (binary file)**: Contains the actual genotype calls in binary format. It stores genotypes efficiently using 2 bits per genotype, making it much smaller than the text-based PED format. The file starts with a 3-byte magic number (0x6c, 0x1b, 0x01) followed by genotype data blocks.

The BED format is the standard format for PLINK 1.9 analyses due to its significantly smaller file size (often 10-100x smaller than PED files) and faster I/O operations, which is crucial when working with large-scale genomic datasets.

```
-rw-r----- 1 yunye yunye 135M Dec 23 11:45 1KG.EAS.auto.snp.norm.nodup.split.rare002.common015.missing.bed
-rw-r----- 1 yunye yunye  36M Dec 23 11:46 1KG.EAS.auto.snp.norm.nodup.split.rare002.common015.missing.bim
-rw-r----- 1 yunye yunye 9.4K Dec 23 11:46 1KG.EAS.auto.snp.norm.nodup.split.rare002.common015.missing.fam
-rw-r--r-- 1 yunye yunye  32M Dec 27 17:51 1KG.EAS.auto.snp.norm.nodup.split.rare002.common015.missing.map
-rw-r--r-- 1 yunye yunye 2.2G Dec 27 17:51 1KG.EAS.auto.snp.norm.nodup.split.rare002.common015.missing.ped
```

!!! example "`.fam`"
    ```
    head 1KG.EAS.auto.snp.norm.nodup.split.rare002.common015.missing.fam
    0 HG00403 0 0 0 -9
    0 HG00404 0 0 0 -9
    0 HG00406 0 0 0 -9
    0 HG00407 0 0 0 -9
    0 HG00409 0 0 0 -9
    0 HG00410 0 0 0 -9
    0 HG00419 0 0 0 -9
    0 HG00421 0 0 0 -9
    0 HG00422 0 0 0 -9
    0 HG00428 0 0 0 -9
    ```

!!! example "`.bim`"
    ```
    head 1KG.EAS.auto.snp.norm.nodup.split.rare002.common015.missing.bim
    1       1:13273:G:C     0       13273   C       G
    1       1:14599:T:A     0       14599   A       T
    1       1:14604:A:G     0       14604   G       A
    1       1:14930:A:G     0       14930   G       A
    1       1:69897:T:C     0       69897   C       T
    1       1:86331:A:G     0       86331   G       A
    1       1:91581:G:A     0       91581   A       G
    1       1:122872:T:G    0       122872  G       T
    1       1:135163:C:T    0       135163  T       C
    1       1:233473:C:G    0       233473  G       C
    ```

!!! example "`.bed`"
    The BED file is the binary representation of genotype calls at biallelic variants. The first three bytes are a magic number (0x6c, 0x1b, 0x01) that identifies the file format. The rest of the file contains genotype data: a sequence of V blocks (one per variant) of N/4 (rounded up) bytes each, where V is the number of variants and N is the number of samples. Each block stores genotypes for all samples at that variant position, with 2 bits per genotype (00=homozygote for allele 1, 01=heterozygote, 10=homozygote for allele 2, 11=missing).
    ```
    hexdump -C 1KG.EAS.auto.snp.norm.nodup.split.rare002.common015.missing.bed | head
    00000000  6c 1b 01 ff ff bf bf ff  ff ff ef fb ff ff ff fe  |l...............|
    00000010  ff ff ff ff fb ff bb ff  ff fb af ff ff fe fb ff  |................|
    00000020  ff ff ff fe ff ff ff ff  ff bf ff ff ef ff ff ef  |................|
    00000030  bb ff ff ff ff ff ff ff  fa ff ff ff ff ff ff ff  |................|
    00000040  ff ff ff fb ff ff ff ff  ff ff ff ff ff ff ff ef  |................|
    00000050  ff ff ff fb fe ef fe ff  ff ff ff eb ff ff fe fe  |................|
    00000060  ff ff fe ff bf ff fa fb  fb eb be ff ff 3b ff be  |.............;..|
    00000070  fe be bf ef fe ff ef ee  ff ff bf ea fe bf fe ff  |................|
    00000080  bf ff ff ef ff ff ff ff  ff fa ff ff eb ff ff ff  |................|
    00000090  ff ff fb fe af ff bf ff  ff ff ff ff ff ff ff ff  |................|
    ```

Reference: [https://www.cog-genomics.org/plink/1.9/formats](https://www.cog-genomics.org/plink/1.9/formats)
## Imputation dosage

### bgen / bgi

BGEN (Binary GENotype) is a binary format designed for storing imputed genotype data with full probability information. It can store genotype probabilities (probabilities for the three possible genotypes: homozygous reference, heterozygous, and homozygous alternate) or allele dosages (expected number of alternate alleles, ranging from 0 to 2). BGEN files are commonly used for storing imputation results from reference panels (e.g., 1000 Genomes, UK Biobank imputation). The format supports both phased and unphased data and can efficiently store large-scale imputed datasets. The `.bgi` file is the index file that enables fast random access to specific genomic regions in the BGEN file.

Reference: [https://www.well.ox.ac.uk/~gav/bgen_format/](https://www.well.ox.ac.uk/~gav/bgen_format/)

### pgen / psam / pvar

The PGEN/PSAM/PVAR format set is PLINK 2.0's native format for storing genotype data, designed to replace the older BED/FAM/BIM format. These three files work together:

- **`.psam` (sample file)**: Contains sample information (similar to `.fam` but with extended metadata support)
- **`.pvar` (variant file)**: Contains variant information (similar to `.bim` but with extended metadata support)
- **`.pgen` (genotype file)**: Contains the binary genotype data, which can store either hard-called genotypes or imputed dosages

**Important note**: When storing imputed data, `pgen` only saves the dosage value (a scalar ranging from 0 to 2) for each individual. Unlike BGEN, it cannot store the full genotype probability distribution (a vector of length 3) or allele probability matrix (2 x 2). Therefore, `pgen` files cannot be converted back to the full probability information that is stored in `bgen` files. If you need to preserve full probability information, BGEN is the preferred format.

Reference: [https://www.cog-genomics.org/plink/2.0/formats#pgen](https://www.cog-genomics.org/plink/2.0/formats#pgen)

## Summary

<img width="746" alt="Screen Shot 2022-03-28 at 16 45 56" src="https://user-images.githubusercontent.com/40289485/160350838-63da9633-2c74-49dd-889e-03392735463f.png">
