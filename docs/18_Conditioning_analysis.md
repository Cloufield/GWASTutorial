# Conditioning analysis

Multiple association signals could exist in one locus, especially when observing complex LD structures in the regional plot.
Conditioning on one signal allows the separation of independent signals.

## Statistical Model

In a standard GWAS association test, we model the phenotype $Y$ as:

$$ Y = \mu + \beta_1 G_1 + \epsilon $$

where $G_1$ is the genotype of the variant of interest, $\beta_1$ is its effect size, and $\epsilon$ is the error term.

When conditioning on a lead variant $G_2$, we include it as a covariate in the regression model:

$$ Y = \mu + \beta_1 G_1 + \beta_2 G_2 + \epsilon $$

This allows us to test the association of $G_1$ with $Y$ while controlling for the effect of $G_2$, effectively removing the effect of $G_2$ and revealing independent association signals.

Several ways to perform the conditioning analysis:

- Adding the lead variant to the covariates step-wisely and rerun the association test.
- [Conditional & joint association analysis using GWAS summary statistics (GCTA-COJO)](https://www.nature.com/articles/ng.2213).

## Adding the lead variant to the covariates

First, extract the individual genotype (dosage) to the text file. Then add it to covariates.

```sh
plink2 \
  --pfile chr1.dose.Rsq0.3 vzs \
  --extract chr1.list \
  --threads 1 \
  --export A \
  --out genotype/chr1
```

The exported format could be found in [Export non-PLINK 2 fileset](https://www.cog-genomics.org/plink/2.0/data#export).

!!! note
    Major allele dosage would be outputted. If adding `ref-first`, REF allele would be outputted. It does not matter as a covariate.

Then just paste it to the covariates table and run the association test.

!!! note
    Some association test software will also provide options for condition analysis. For example, in PLINK, you can use `--condition <variant ID> ` for condition analysis. You can simply provide a list of variant IDs to run the condition analysis.

## GCTA-COJO

If raw genotypes and phenotypes are not available, GCTA-COJO performs conditioning analysis using sumstats and external LD reference.

`cojo-top-SNPs 10` will perform a step-wise model selection to select 10 independently associated SNPs (including non-significant ones).

```
gcta \
  --bfile chr1 \
  --chr 1 \
  --maf 0.001 \
  --cojo-file chr1_cojo.input \
  --cojo-top-SNPs 10 \
  --extract-region-bp 1 152383617 5000 \
  --out chr1_cojo.output
```

!!! note
    `bfile` is used to generate LD. A size of [> 4000 unrelated samples](https://yanglab.westlake.edu.cn/software/gcta/#COJO) is suggested. Estimation of LD in GCTA is based on the hard-call genotype.

Input file format `less chr1_cojo.input`:
```
ID      ALLELE1 ALLELE0 A1FREQ  BETA    SE      P       N
chr1:11171:CCTTG:C      C       CCTTG   0.0831407       -0.0459889      0.0710074       0.5172  180590
chr1:13024:G:A  A       G       1.63957e-05     -3.2714 3.26302 0.3161  180590
```
Here `A1` is the effect allele. 

Then `--cojo-cond` could be used to generate new sumstats conditioned on the above-selected variant(s).


## Conditional Analysis vs. Fine-mapping

While both conditional analysis and fine-mapping are used to dissect association signals in a locus, they address different questions and use different approaches:

| Aspect | Conditional Analysis | Fine-mapping |
|--------|---------------------|--------------|
| **Primary Goal** | Identify **independent association signals** in a locus | Identify **causal variant(s)** within a locus |
| **Question Asked** | "Are there multiple independent signals after controlling for the lead variant?" | "Which specific variant(s) are likely to be causal?" |
| **Method** | Regression-based: add variants as covariates and test remaining associations | Bayesian methods: estimate posterior inclusion probabilities (PIPs) |
| **Output** | P-values for independent associations | PIPs and credible sets for causal variants |
| **Focus** | **Signal separation**: Distinguishes independent signals from correlated ones | **Causal inference**: Distinguishes causal variants from tag variants (in LD) |
| **When to Use** | When you want to identify all independent association signals | When you want to pinpoint the most likely causal variant(s) |

!!! tip "Complementary Approaches"
    - **Conditional analysis** is often used as a first step to identify how many independent signals exist in a region
    - **Fine-mapping** is then applied to each independent signal to identify the causal variant(s) within that signal
    - Together, they provide a comprehensive understanding of the genetic architecture of a locus



## References

- https://www.cog-genomics.org/plink/1.9/assoc
- Yang, J., Ferreira, T., Morris, A. P., Medland, S. E., Genetic Investigation of ANthropometric Traits (GIANT) Consortium, DIAbetes Genetics Replication And Meta-analysis (DIAGRAM) Consortium, ... & Visscher, P. M. (2012). Conditional and joint multiple-SNP analysis of GWAS summary statistics identifies additional variants influencing complex traits. Nature genetics, 44(4), 369-375.




