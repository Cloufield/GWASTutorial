# Imputation

The missing data imputation is not a task specific to genetic studies. 
By comparing the genotyping array (generally 500k–1M markers) to the reference panel (WGSed), missing markers on the array are filled. 
The tabular data imputation methods could be used to impute the genotype data.
However, haplotypes are coalesced from the ancestors, and the recombination events during gametogenesis, 
each individual's haplotype is a mosaic of all haplotypes in a population.
Given these properties, hidden Markov model (HMM) based methods usually outperform tabular data-based ones.

This HMM was first described in [Li & Stephens 2003](https://academic.oup.com/genetics/article/165/4/2213/6050566). 
Here we will not go through tools over the past 20 years. 
We will introduce the concept and the usage of [Minimac](https://www.nature.com/articles/ng.3656).

## Figure illustration

<img width="490" alt="image" src="https://github.com/Cloufield/GWASTutorial/assets/84720165/afff6f31-6a97-4ed2-975e-6f795a39b440">

In the figure, each row in the above panel represents a reference haplotype. The middle panel shows the genotyping array. 
Genotyped markers are squared and WGS-only markers are circled. The two colors represent the ref and alt alleles. 
You could also think they represent different haplotype fragments. The red triangles indicate the recombination hot spots, 
which a crossover between the reference haplotypes is more likely to happen.

Given the genotyped marker, matching probabilities are calculated for all potential paths through reference haplotypes. 
Then, in this example (the real case is not this simple), we assumed at each recombination hotspot, there is a free recombination. 
You will see that all paths chained by dark blue match 2 of the 4 genotyped markers. So these paths have equal probability.

Finally, missing markers are filled with the probability-weighted alleles on each path. For the left three circles, 
two paths are cyan and one path is orange, the imputation result will be 1/3 orange and 2/3 cyan.

## How to do imputation

The simplest way is to use the [Michigan](https://imputationserver.sph.umich.edu/index.html#!) or [TOPMed](https://imputation.biodatacatalyst.nhlbi.nih.gov/#!) imputation server, 
if you don't have resources of WGS data.
Just make your vcf, submit it to the server, and select the favored reference panel. There are built-in phasing, liftover, and QC on the server, 
but we would strongly suggest checking the data and doing these steps by yourself. For example:

- Liftover between hg19 and hg38, properly flip the alleles, and exclude the ambiguous variants.
- Phasing the data locally and storing it. The phased data can be used for imputation against any reference panel.
- Check the ancestry information and select the proper reference panel.

Another way is to run the job locally. Recent tools are memory and computation efficient, you may run it in a small in-house server or even PC.

A typical workflow of Minimac is:

Parameter estimation (this step will create a [m3vcf](https://genome.sph.umich.edu/wiki/M3VCF_Files) reference panel file):

```sh
Minimac3 \
  --refHaps ./phased_reference.vcf.gz \
  --processReference \
  --prefix ./phased_reference \
  --log
```

Imputation:

```sh
minimac4 \
  --refHaps ./phased_reference.m3vcf \
  --haps ./phased_target.vcf.gz \
  --prefix ./result \
  --format GT,DS,HDS,GP,SD \
  --meta \
  --log \
  --cpus 10
```

Details of the [options](https://genome.sph.umich.edu/wiki/Minimac4_Documentation).

## After imputation

The output is a vcf file. First, we need to examine the [imputation quality](https://www.biorxiv.org/content/10.1101/2023.05.30.542466v1). 
It can be a long long story and I will not explain it in detail. Most of the time, 
when the following criteria meet, 

- Genotyping array contains > 500k markers
- Reference panel is 1KG or ancestry matched, or at least the major ancestry in the panel matches the target

The standard imputation quality metric, named `Rsq`, efficiently discriminates the well-imputed variants at a threshold 0.7 
(may loosen it to 0.3 to allow more variants in the GWAS).

## Before GWAS

Three types of genotypes are widely used in GWAS -- best-guess genotype, allelic dosage, and genotype probability. 
Using Dosage (DS) keeps the dataset smallest while most association test software only requires this information.












