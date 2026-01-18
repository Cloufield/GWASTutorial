# Colocalization

Colocalization analysis aims to determine whether two traits share the same causal variant(s) in a genomic region. This is particularly useful for understanding the relationship between molecular traits (e.g., gene expression, protein levels) and complex diseases.

## Coloc assuming a single causal variant

[`Coloc`](https://journals.plos.org/plosgenetics/article?id=10.1371/journal.pgen.1004383) uses the assumption of 0 or 1 causal variant in each trait, and tests for whether they share the same causal variant.

!!! note "Colocalization vs. Fine-mapping"
    The assumption in colocalization is different from fine-mapping. In fine-mapping, the aim is to find the putative causal variants, which are determined at birth. In colocalization, the aim is to find the "signal overlapping" to support the causality inference, like eQTL → A trait. It is possible that the causal variants are different in two traits.

### Datasets used

* For binary traits, `coloc` requires "beta", "varbeta", and "snp". For quantitative traits, the trait standard deviation "sdY" is required to estimate the scale of estimated beta.
* LD matrix will be a square numeric matrix of dimension equal to the number of SNPs, with dimnames corresponding to the SNP ids.

### Result interpretation

Basically, five configurations are calculated:

```
## PP.H0.abf PP.H1.abf PP.H2.abf PP.H3.abf PP.H4.abf 
##  1.73e-08  7.16e-07  2.61e-05  8.20e-05  1.00e+00 
## [1] "PP abf for shared variant: 100%"
```

- **$H_0$**: neither trait has a genetic association in the region
- **$H_1$**: only trait 1 has a genetic association in the region
- **$H_2$**: only trait 2 has a genetic association in the region
- **$H_3$**: both traits are associated, but with different causal variants
- **$H_4$**: both traits are associated and share a single causal variant

`PP.H4.abf` is the posterior probability that two traits share a same causal variant.

Then based on `H4` being true, a 95% credible set could be constructed (as a shared causal variant does not necessarily mean a specific variant).

!!! example "Constructing a 95% credible set"
    ```R
    o <- order(my.res$results$SNP.PP.H4,decreasing=TRUE)
    cs <- cumsum(my.res$results$SNP.PP.H4[o])
    w <- which(cs > 0.95)[1]
    my.res$results[o,][1:w,]$snp
    ```

## Coloc assuming multiple causal variants or multiple signals

When the single-causal variant assumption is violated, several ways could be used to relieve it.

1. **Assuming multiple causal variants** in [SuSiE-Coloc pipeline](https://chr1swallace.github.io/coloc/articles/a06_SuSiE.html).
   In this pipeline, putative causal variants are fine-mapped, then each signal is passed to the coloc engine.
   
2. **Conditioning analysis** using [GCTA-COJO-Coloc pipeline](https://www.biorxiv.org/content/10.1101/2022.08.08.503158v1.abstract).
   In this pipeline, signals are segregated, then passed to the coloc engine.

## Other pipelines

Many other strategies and pipelines are available for colocalization and prioritize the variants/genes/traits. For example:

* [HyPrColoc](https://www.nature.com/articles/s41467-020-20885-8): Hypothesis prioritization for colocalization analysis
* [OpenTargets](https://www.nature.com/articles/s41588-021-00945-5): Systematic integration of genomic data for target identification

## References

- [Coloc: a package for colocalisation analyses](https://chr1swallace.github.io/coloc/articles/a01_intro.html)
- Giambartolomei, C., Vukcevic, D., Schadt, E. E., Franke, L., Hingorani, A. D., Wallace, C., & Plagnol, V. (2014). Bayesian test for colocalisation between pairs of genetic association studies using summary statistics. *PLoS genetics*, 10(5), e1004383.

