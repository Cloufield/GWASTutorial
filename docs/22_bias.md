# Bias

Bias refers to a **systematic (non-random) deviation** of an estimator's expected value from the true parameter.

For a statistic $T$ estimating a parameter $\theta$:

$$
\text{bias}(T, \theta) = E(T) - \theta
$$

where:
- $T$: statistic used to estimate $\theta$
- $E(T)$: expected value of $T$

---

## Conceptual classification of bias

In genetic epidemiology and GWAS, biases can be broadly grouped into:

1. **Confounding**
2. **Measurement / information bias**
3. **Selection bias**
4. **Analysis-induced bias** (modeling and statistical selection)

---

## 1. Confounding

Confounding occurs when an exposure and outcome share a **common cause**, creating a non-causal association.

### Common confounders in GWAS

- **Population structure**: Systematic differences in allele frequencies across subpopulations that can induce spurious genotype–phenotype associations.

- **Cryptic relatedness**: Unrecognized familial relationships among participants that violate independence assumptions and bias effect estimates.

- **Assortative mating**: Non-random mating based on phenotypes (or correlated traits, such as education or socioeconomic status) can induce correlations between genotypes and shared family environments. This creates **family-level (dynastic) confounding**, leading to biased genotype–phenotype associations, inflated heritability estimates, and distorted genetic correlations.

<img width="700" alt="confounding diagram" src="https://github.com/Cloufield/GWASTutorial/assets/40289485/2e60f785-7486-420a-a52a-ab6929ca19c7">

---

## 2. Measurement / information bias

Measurement (information) bias arises from **errors in measuring exposures, outcomes, or covariates**.

### Examples in GWAS

- **Phenotype misclassification** (e.g. ICD codes, self-reported traits)
- **Batch effects** in genotyping or imputation
- Differential measurement error across cohorts in meta-analysis

---

## 3. Selection bias

Selection bias occurs when inclusion in the study depends on factors related to the exposure, outcome, or their causes, making the analyzed sample **non-representative** of the target population.

### 3.1 Collider bias

Collider bias arises when both the exposure and outcome affect a **common variable** and that variable is conditioned on (e.g. adjusted for or used as a selection criterion).

In other words, **conditioning on a collider can induce a spurious association** between exposure and outcome.

<img width="700" alt="collider bias diagram" src="https://github.com/Cloufield/GWASTutorial/assets/40289485/c763e7d1-de0f-4f3e-a56d-acd5eb12c019">

### 3.2 Participation (ascertainment) bias

Participation (ascertainment) bias is a form of **selection bias** in which inclusion in the study depends on traits that are genetically correlated with the outcome.

In biobank-scale GWAS, this can:
- Distort SNP–trait associations
- Bias heritability estimates
- Affect downstream analyses such as PRS and Mendelian randomization

---

## 4. Analysis-induced bias

These biases arise **after data collection**, due to modeling assumptions or statistical procedures.

### 4.1 Model misspecification bias

Model misspecification bias occurs when the assumed statistical model does not match the true data-generating process.

Examples in GWAS include:
- Ignoring non-additive genetic effects (dominance, epistasis)
- Using linear models for binary traits without appropriate correction
- Incorrect variance assumptions in mixed models

### 4.2 Winner’s curse

Winner’s curse refers to the **upward bias in estimated effect sizes** for variants that pass a significance threshold.

In GWAS, this occurs because:
- Only variants with large observed effects are selected
- Effect sizes are conditional on extreme sampling variation

---

## References

- Holmberg, M. J., & Andersen, L. W. (2022). *Collider bias*. JAMA, 327(13), 1282–1283.
- Schoeler, T., Speed, D., Porcu, E., Pirastu, N., Pingault, J. B., & Kutalik, Z. (2023). *Participation bias in the UK Biobank distorts genetic associations and downstream analyses*. Nature Human Behaviour, 7(7), 1216–1227.
- Griffith, G. J., Morris, T. T., Tudball, M. J., Herbert, A., Mancano, G., Pike, L., et al. (2020). *Collider bias undermines our understanding of COVID-19 disease risk and severity*. Nature Communications, 11(1), 5749.