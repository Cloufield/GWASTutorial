Co-localization
---


# Coloc assuming single causal variant


[`Coloc`](https://journals.plos.org/plosgenetics/article?id=10.1371/journal.pgen.1004383) uses the assumption of 0 or 1 causal variant in each trait, 
and tests for whether they share the same causal variant.


Datasets used:
* For binary traits, `coloc` requires "beta", "varbeta", and "snp". For quantitative traits, 
the trait standard deviation "sdY" is required to estimate the scale of estimated beta.
* LD matrix will be a square numeric matrix of dimension equal to the number of SNPs, with dimnames corresponding to the SNP ids.


Two fuctions were parsed in `coloc`, `ABF` (fine-mapping by converting z-score to Bayes factor) and `coloc` (use a similar strategy to convert BF, and calculated a posterior probability of both traits are associated and share a single causal variant).

It didn't assume the lead variant was the only putative causal variant. So it was possible that the coloc signal was from other variants.
The follow options could extract the credible set:

```R
o <- order(my.res$results$SNP.PP.H4,decreasing=TRUE)
cs <- cumsum(my.res$results$SNP.PP.H4[o])
w <- which(cs > 0.95)[1]
my.res$results[o,][1:w,]$snp
```



References:
>[Coloc: a package for colocalisation analyses](https://chr1swallace.github.io/coloc/articles/a01_intro.html)


# Coloc assuming multiple causal variants

When the single-causal variant assumption is violeted, several ways could be used to relieve it.

1. Assuming multiple causal variants in [Coloc-SuSiE](https://chr1swallace.github.io/coloc/articles/a06_SuSiE.html).
  x
2. Conditioning analysis using GCTA-COJO-Coloc pipeline.
  Actually 


