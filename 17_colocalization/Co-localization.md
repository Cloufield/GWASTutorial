Co-localization

---

# Coloc assuming single causal variant


[`Coloc`](https://journals.plos.org/plosgenetics/article?id=10.1371/journal.pgen.1004383) uses the assumption of 0 or 1 causal variant in each trait, 
and tests for whether they share the same causal variant.


Datasets used:
* For binary traits, `coloc` requires "beta", "varbeta", and "snp". For quantitative traits, 
the trait standard deviation is required to estimate the scale of estimated beta.
* LD matrix will be a square numeric matrix of dimension equal to the number of SNPs, with dimnames corresponding to the SNP ids.


References:
>[Coloc: a package for colocalisation analyses](https://chr1swallace.github.io/coloc/articles/a01_intro.html)


# Coloc assuming multiple causal variants

When the single-causal variant assumption is violeted, several ways could be used to relieve it.

1. Assuming multiple causal variants in [Coloc-SuSiE](https://chr1swallace.github.io/coloc/articles/a06_SuSiE.html).
2. Conditioning analysis using GCTA-COJO-Coloc pipeline.
