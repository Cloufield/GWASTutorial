# Self training

## PCA using 1000 Genome Project Dataset

In this self-learning module, we would like you to put your hands on the 1000 Genome Project data and apply the skills you have learned to this mini-project.

!!! note "Aim"
    
    Aim:
    
    1. Download 1000 Genome VCF files. 
    2. Perform PCA using 1000 Genome samples.
    3. Plot the PCs of these individuals.
    4. Interpret the results.

    Here is a brief overview of this mini project.

    ![image](https://user-images.githubusercontent.com/40289485/161699756-13c9f474-f9a2-4514-886f-61022a374bf8.png)

The ultimate goal of this assignment is simple, which is to help you get familiar with the skills and the most commonly used datasets in complex trait genomics.

!!! tip
    Please pay attention to the details of each step. Understanding why and how we do certain steps is much more important than running the sample code itself. 

## 1. Download the publicly available 1000 Genome VCF 


Download the files we need from 1000 Genomes Project FTP site:

1. Autosome VCF files
2. Ancestry information file
3. Reference genome sequence
4. Strict mask

!!! tip
    - Autosome VCF: chr1 - chr22 files: [in this directory](http://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/).
    - Ancestry information file: [download here](http://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/integrated_call_samples_v3.20130502.ALL.panel)
    - Reference genome sequence: [in this directory](https://ftp.1000genomes.ebi.ac.uk/vol1/ftp/technical/reference/).
    - Strict mask: [download here](https://ftp-trace.ncbi.nih.gov/1000genomes/ftp/release/20130502/supporting/accessible_genome_masks/20141020.strict_mask.whole_genome.bed)

!!! Note 
    If it takes too long or if you are using your local laptop, you can just download the files for chr1.

!!! example "Sample shell script for downloading the files"
    ```
    #!/bin/bash
    for chr in $(seq 1 22)  #Note: If it takes too long, you can download just chr1.
    do
    wget https://ftp-trace.ncbi.nih.gov/1000genomes/ftp/release/20130502/ALL.chr${chr}.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz
    wget https://ftp-trace.ncbi.nih.gov/1000genomes/ftp/release/20130502/ALL.chr${chr}.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz.tbi
    done
    
    wget https://ftp.1000genomes.ebi.ac.uk/vol1/ftp/technical/reference/human_g1k_v37.fasta.gz
    wget https://ftp.1000genomes.ebi.ac.uk/vol1/ftp/technical/reference/human_g1k_v37.fasta.fai
    
    wget https://ftp-trace.ncbi.nih.gov/1000genomes/ftp/release/20130502/integrated_call_samples_v3.20130502.ALL.panel
    wget https://ftp-trace.ncbi.nih.gov/1000genomes/ftp/release/20130502/supporting/accessible_genome_masks/20141020.strict_mask.whole_genome.bed
    ```

## 2. Re-align, normalize and remove duplication

We need to use bcftools to process the raw vcf files. 

!!! tip "Install bcftools"
    http://www.htslib.org/download/

Since the variants are not normalized and also have many duplications, we need to clean the vcf files.

- Normalize: https://samtools.github.io/bcftools/bcftools.html#norm
- Remove duplication: https://samtools.github.io/bcftools/bcftools.html#common_options


!!! example "Re-align with the reference genome, normalize variants and remove duplications" 
    ```
    #!/bin/bash
    for chr in $(seq 1 22)
    do
        bcftools norm -m-any --check-ref w -f human_g1k_v37.fasta \
          ALL.chr"${chr}".phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz | \
          bcftools annotate -I +'%CHROM:%POS:%REF:%ALT' | \
            bcftools norm -Ob --rm-dup both \
              > ALL.chr"${chr}".phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.bcf 
        bcftools index ALL.chr"${chr}".phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.bcf
    done
    ```

## 3. Convert VCF files to plink binary format

!!! example    
    ```
    #!/bin/bash
    for chr in $(seq 1 22)
    do
    plink \
          --bcf ALL.chr"${chr}".phase3_shapeit2_mvncall_integrated_v5b.20130502.genotypes.bcf \
          --keep-allele-order \
          --vcf-idspace-to _ \
          --const-fid \
          --allow-extra-chr 0 \
          --split-x b37 no-fail \
          --make-bed \
          --out ALL.chr"${chr}".phase3_shapeit2_mvncall_integrated_v5b.20130502.genotypes
    done
    ```

## 4. Using SNPs only in strict masks

Strict masks are [in this directory](https://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/supporting/accessible_genome_masks/).

!!! quote "Strict mask"
    The overlapped region with this mask is “callable” (or credible variant calls).
    This mask was developed in the 1KG main paper and it is well explained in https://www.biostars.org/p/219634/

!!! tip
    Use `plink --make-set` option with the `BED` files to extract SNPs in the strict mask.

## 5. QC it and prune it to ~ 100K variants.

!!! tip
    Use PLINK.
    
    QC: only SNPs (exclude indels), MAF>0.1

    Pruning: `plink --indep-pariwise`

## 6. Perform PCA 

!!! tip
    `plink --pca`

## 7. Visualization and interpretation.

Draw PC1 - PC2 plot and color each individual by ancestry information (from ALL.panel file). Interpret the result.

!!! tip
    You can use R, python, or any other tools you like (even Excel can do the job.)
    
    (If you are having trouble performing any of the steps, you can also refer to: https://www.biostars.org/p/335605/.)

## Checklist 
- [x] What does variant normalization mean and What are the two principles for variant normalization?
- [x] For chromosome 1, what is the proportion of commom variants(MAF >5%) / low-frequency-variants(1<=MAF <5%) / and rare variants(MAF <1%) ? If possible, please draw a figure showing the distribution of MAF. (plink --freq)
- [x] What pattern did you observe from the 1KG PCA plot? 

## Reference

- https://www.biostars.org/p/335605/
- 1000 Genomes Project Consortium. "A global reference for human genetic variation." Nature 526.7571 (2015): 68.