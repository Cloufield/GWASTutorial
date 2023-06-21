# Phasing

Human genome is diploid. Distribution of variants between homologous chromosomes can affect the interpretation of genotype data, such as allele specific expression, 
context-informed annotation, loss-of-function compound heterozygous events. 

<img width="270" alt="image" src="https://github.com/Cloufield/GWASTutorial/assets/84720165/7e18a7e1-0c17-4cce-9e74-d387294ba702">

( [SHAPEIT5](https://www.biorxiv.org/content/10.1101/2022.10.19.512867v2.full) )

*In the above illustration, when LoF variants are on both copies of a gene, the gene is thought knocked out*


Trio data and long read sequencing can solve the haplotyping problem. That is not always possible. Statistical phasing is based on the [Li & Stephens]() Markov model. 
The haploid version of this model (see Imputation) is easier to understand. Because the maternal and paternal haplotypes are independent, 
unphased genotype could be constructed by the addition of two haplotypes.

Recent methods had incopoorates long IBD sharing, local haplotypes, etc, to make it tractable for large datasets. 
You could read the following methods if you are interested.

- [PHASE](https://linkinghub.elsevier.com/retrieve/pii/S0002929707633412)
- [MaCH](https://onlinelibrary.wiley.com/doi/full/10.1002/gepi.20533)
- [EAGLE2](https://www.nature.com/articles/ng.3679)
- [SHAPEIT5](https://www.biorxiv.org/content/10.1101/2022.10.19.512867v2.full)
- [BEAGLE3](http://www.cell.com/article/S0002929709000123/fulltext)


# How to do phasing


In most of the cases, phasing is just a pre-step of imputation, and we do not care about how the phasing goes. 
But there are several considerations, like reference-based or reference-free, large and small sample size, rare variants cutoff. 
There is no single method that could best fit all cases.

Here I show one example using EAGLE2.

```sh
eagle \
	--vcf=target.vcf.gz \
	--geneticMapFile=genetic_map_hg19_withX.txt.gz \
	--chrom=19 \
	--outPrefix=target.eagle \
	--numThreads=10
```












