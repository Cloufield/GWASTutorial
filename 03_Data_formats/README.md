# Data format

This section lists some of the most commonly used formats in complex trait genomic analysis. 

## Table of Contents
- [Data formats for general purpose](#data-formats-for-general-purpose)
    - [txt](#txt)
    - [tsv](#tsv)
    - [csv](#csv)
- [Data formats in bioinformatics](#data-formats-in-bioinformatics)
    - [Sequence](#sequence)
        - FASTA
        - FASTQ
    - [Alignment](#alingment)
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
Simple text file

!!! example "`.txt`"
    ```
    cat sample_text.txt 
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. In ut sem congue, tristique tortor et, ullamcorper elit. Nulla elementum, erat ac fringilla mattis, nisi tellus euismod dui, interdum laoreet orci velit vel leo. Vestibulum neque mi, pharetra in tempor id, malesuada at ipsum. Duis tellus enim, suscipit sit amet vestibulum in, ultricies vitae erat. Proin consequat id quam sed sodales. Ut a magna non tellus dictum aliquet vitae nec mi. Suspendisse potenti. Vestibulum mauris sem, viverra ac metus sed, scelerisque ornare arcu. Vivamus consequat, libero vitae aliquet tempor, lorem leo mattis arcu, et viverra erat ligula sit amet tortor. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Praesent ut massa ac tortor lobortis placerat. Pellentesque aliquam tortor augue, at rutrum magna molestie et. Etiam congue nulla in venenatis congue. Nunc ac felis pharetra, cursus leo et, finibus eros.
    ```
    Random texts are generated using - https://www.lipsum.com/

### tsv
Tab-separated values
Tabular data format 


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
Comma-separated values
Tabular data format 


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
text-based format for representing either nucleotide sequences or amino acid (protein) sequences
!!! example "`.fa` or `.fasta`"
   ```
   >SEQ_ID
   GATTTGGGGTTCAAAGCAGTATCGATCAAATAGTAAATCCATTTGTTCAACTCACAGTTT
   ```
   
### fastq
text-based format for storing both a nucleotide sequence and its corresponding quality scores

!!! example "`.fastq`"
    ```
    @SEQ_ID
    GATTTGGGGTTCAAAGCAGTATCGATCAAATAGTAAATCCATTTGTTCAACTCACAGTTT
    +
    !''*((((***+))%%%++)(%%%%).1***-+*''))**55CCF>>>>>>CCCCCCC65
    ```    
    Reference: https://en.wikipedia.org/wiki/FASTQ_format

## Alingment
### SAM/BAM
Sequence Alignment/Map Format is a TAB-delimited text file format consisting of a header section and an alignment section.

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
VCF is a text file format consisting of meta-information lines, a header line, and then data lines. Each data line contains information about a variant in the genome (and the genotype information on samples for each variant). 

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

The figure shows how genotypes are stored in files.

We have 3 parts of information:

1. Individual information
2. Variant information
3. Genotype matrix

And there are different ways (format sets) to represent this information in PLINK1.9 and PLINK2:

1. ped / map
2. fam / bim / bed
3. psam / pvar / pgen


<img width="900" alt="image" src="https://github.com/Cloufield/GWASTutorial/assets/40289485/70dc5c9c-5096-41af-95ee-4f925483a93c">



### ped / map 
`.ped` (PLINK/MERLIN/Haploview text pedigree + genotype table)

Original standard text format for sample pedigree information and genotype calls.Contains no header line, and one line per sample with 2V+6 fields where V is the number of variants. The first six fields are the same as those in a .fam file. The seventh and eighth fields are allele calls for the first variant in the .map file ('0' = no call); the 9th and 10th are allele calls for the second variant; and so on.

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

`.map` (PLINK text fileset variant information file)

Variant information file accompanying a .ped text pedigree + genotype table. A text file with no header line, and one line per variant with the following 3-4 fields:

- Chromosome code. PLINK 1.9 also permits contig names here, but most older programs do not.
- Variant identifier
- Position in morgans or centimorgans (optional; also safe to use dummy value of '0')
- Base-pair coordinate

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
### bed / fam /bim

bed/fam/bim formats are the binary implementation of ped/map formats.
bed/bim/fam files contain the same information as ped/map but are much smaller in size.

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
    "Primary representation of genotype calls at biallelic variants
    The first three bytes should be 0x6c, 0x1b, and 0x01 in that order.
    The rest of the file is a sequence of V blocks of N/4 (rounded up) bytes each, where V is the number of variants and N is the number of samples. The first block corresponds to the first marker in the .bim file, etc."
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
Reference: [https://www.well.ox.ac.uk/~gav/bgen_format/](https://www.well.ox.ac.uk/~gav/bgen_format/)

### pgen,psam,pvar
Reference: [https://www.cog-genomics.org/plink/2.0/formats#pgen](https://www.cog-genomics.org/plink/2.0/formats#pgen)

NOTE: `pgen` only saved the dosage for each individual (a scalar ranged from 0 to 2). It could not been converted back to the genotype probability (a vector of length 3) or allele probability (a matrix of dimension 2 x 2) saved in `bgen`.

## Summary

<img width="746" alt="Screen Shot 2022-03-28 at 16 45 56" src="https://user-images.githubusercontent.com/40289485/160350838-63da9633-2c74-49dd-889e-03392735463f.png">
