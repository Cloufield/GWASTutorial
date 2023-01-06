# GWASTutorial (under construction)

[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2FCloufield%2FGWASTutorial&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=Views&edge_flat=false)](https://hits.seeyoufarm.com)

This is a repository aimming to provide a hands-on tutorial of common analysis in Complex Trait Genomics. 

This tutorial covers the minimum skills and knowledge to perform a typical genome-wide association study (GWAS).    

The contents are categorized into the following groups. Additionally, for absolute beginners, we also prepare a section on command lines in Linux.

<img width="686" alt="image" src="https://user-images.githubusercontent.com/40289485/209779725-73b62b15-b044-46a4-98ae-ce5db06f93b3.png">

## Contents

### Command lines 
- [Linux command line basics (optional)](https://cloufield.github.io/GWASTutorial/02_Linux_basics/) : For those who haven't used command line, we will first introduce the basics of Linux system and commonly used commands.

### Pre-GWAS

- [Data formats](https://cloufield.github.io/GWASTutorial/03_Data_formats/) : Before any analysis, the first thing is always to get familiar with your data. In this section, we will introduce some basic formats used to store sequence, genotype and dosage data.
- [Data QC](https://cloufield.github.io/GWASTutorial/04_Data_QC/) : Usually the raw genotype data is "dirty". This means that there are usually errors, invalid or missing values. In this section, we will learn how to perform quiality control for the raw genotype data using PLINK. 
- [Principal component analysis (PCA)](https://cloufield.github.io/GWASTutorial/05_PCA/) : In this section, we will cover how to perform Principal Component Analysis (PCA) to analyze the population structure.  

### GWAS

- [Association tests](https://cloufield.github.io/GWASTutorial/06_Association_tests/): After QC, we will perform the very first association tests for a simulated binary trait (case-control trait) with a logistic regression model using PLINK.
- [Visualization](https://cloufield.github.io/GWASTutorial/Visualization/): To visualize the summary statistics generated from association tests, we will use a python pakage called gwaslab to create mahattan plots, Quantitle-Quantile plots and Regional plots.

### Post-GWAS

In these sections, we will briefly introduce the Post-GWAS analyese, which will dig deeper into the GWAS summary statistics.  

- [Variant Annotation](https://cloufield.github.io/GWASTutorial/07_Annotation/)
- [LD score regression (univariate, cross-trait and partitioned)](https://cloufield.github.io/GWASTutorial/08_LDSC/)
- [Gene / Gene-set analysis](https://cloufield.github.io/GWASTutorial/09_Gene_based_analysis/)
- [Polygenic risk scores](https://cloufield.github.io/GWASTutorial/10_PRS/)

## Contact
This repository is maintained by [Yunye He](https://github.com/Cloufield). If you have any questions or suggestions, please feel free to contact [gwaslab@gmail.com](gwaslab@gmail.com).

<img width="686" alt="image" src="https://user-images.githubusercontent.com/40289485/209780549-54a24fdd-485b-4875-8f40-d6812eb644fe.png">

A real "Manhattan plot"!