# GWASTutorial

[<img width="600" alt="image" src="https://github.com/Cloufield/GWASTutorial/assets/40289485/3a188b0f-b693-4cd1-819f-50c4e9ebf816">](https://sites.google.com/edu.k.u-tokyo.ac.jp/kamatanilab/)

Note: this tutorial is being updated to Version 2024

This Github page aims to provide a hands-on tutorial on common analysis in Complex Trait Genomics. This tutorial is designed for the course `Fundamental Exercise II` provided by [The Laboratory of Complex Trait Genomics](https://sites.google.com/edu.k.u-tokyo.ac.jp/kamatanilab/) at the University of Tokyo. For more information, please see [About](https://cloufield.github.io/GWASTutorial/99_About/).

This tutorial covers the minimum skills and knowledge required to perform a typical genome-wide association study (GWAS). The contents are categorized into the following groups. Additionally, for absolute beginners, we also prepared a section on command lines in Linux.

If you have any questions or suggestions, please feel free to let us know in the [Issue section of this repository](https://github.com/Cloufield/GWASTutorial/issues).

<img width="755" alt="image" src="https://github.com/Cloufield/GWASTutorial/assets/40289485/13609a79-2e2d-41f3-af9b-912fc47d57a9">

## Contents

### Command lines
- [Linux command line basics (optional)](https://cloufield.github.io/GWASTutorial/02_Linux_basics/) : For those who haven't used the command line, we will first introduce the basics of the Linux system and commonly used commands.

### Pre-GWAS

- [Data formats](https://cloufield.github.io/GWASTutorial/03_Data_formats/) : Before any analysis, the first thing is always to get familiar with your data. In this section, we will introduce some basic formats used to store sequence, genotype and dosage data.
- [Data QC](https://cloufield.github.io/GWASTutorial/04_Data_QC/) : Usually the raw genotype data is "dirty". This means that there are usually errors, invalid or missing values. In this section, we will learn how to perform quality control for the raw genotype data using PLINK. 
- [Principal component analysis (PCA)](https://cloufield.github.io/GWASTutorial/05_PCA/) : In this section, we will cover how to perform Principal Component Analysis (PCA) to analyze the population structure.  

### GWAS

- [Association tests](https://cloufield.github.io/GWASTutorial/06_Association_tests/): After QC, we will perform the very first association tests for a simulated binary trait (case-control trait) with a logistic regression model using PLINK.
- [Visualization](https://cloufield.github.io/GWASTutorial/Visualization/): To visualize the summary statistics generated from association tests, we will use a python package called gwaslab to create Manhattan plots, Quantitle-Quantile plots and Regional plots.

### Post-GWAS

In these sections, we will briefly introduce the Post-GWAS analyses, which will dig deeper into the GWAS summary statistics.  

- [Variant Annotation by ANNOVAR/VEP](https://cloufield.github.io/GWASTutorial/07_Annotation/)
- [Heritability Concepts](https://cloufield.github.io/GWASTutorial/13_heritability/)
- [SNP-Heritability estimation by GCTA-GREML](https://cloufield.github.io/GWASTutorial/14_gcta_greml/)
- [LD score regression (univariate, cross-trait and partitioned) by LDSC](https://cloufield.github.io/GWASTutorial/08_LDSC/)
- [Gene / Gene-set analysis by MAGMA](https://cloufield.github.io/GWASTutorial/09_Gene_based_analysis/)
- [Fine-mapping by SUSIE](https://cloufield.github.io/GWASTutorial/12_fine_mapping/)
- [Polygenic risk scores](https://cloufield.github.io/GWASTutorial/10_PRS/)
- [Colocalization](https://cloufield.github.io/GWASTutorial/17_colocalization/)
- [TWAS](https://cloufield.github.io/GWASTutorial/21_twas/)

### Topics

Introductions on GWAS-related issues

- [Linkage disequilibrium (LD) ](https://cloufield.github.io/GWASTutorial/19_ld/)
- [Heritability](https://cloufield.github.io/GWASTutorial/13_heritability/)
- [Power analysis for GWAS](https://cloufield.github.io/GWASTutorial/20_power_analysis/)
- [Winner's curse](https://cloufield.github.io/GWASTutorial/15_winners_curse/)
- [Measure of effect](https://cloufield.github.io/GWASTutorial/55_measure_of_effect/)

### Others
- [Recommended reading](https://cloufield.github.io/GWASTutorial/90_Recommended_Reading/)

[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2FCloufield%2FGWASTutorial&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=Views&edge_flat=false)](https://hits.seeyoufarm.com)
