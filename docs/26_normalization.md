# Phenotype normalization

Phenotype normalization is a critical preprocessing step in GWAS to ensure valid statistical inference, numerical stability, and comparability across cohorts.

---

## Raw measures

**Definition**

The phenotype is analyzed in its original measurement scale:

$$
Y_i = \text{observed phenotype for individual } i
$$

**When appropriate**
- Binary traits (case–control)
- Approximately normally distributed quantitative traits

**Pros**
- Preserves biological units and interpretability

**Cons**
- Sensitive to skewness and outliers

---

## Residual (covariate and medication adjusted)

**Definition**

The phenotype is adjusted for covariates and medication effects using regression:

$$Y_i = \alpha + \mathbf{C}_i^\top \gamma + \mathbf{M}_i^\top \delta + \varepsilon_i$$

$$
Y_i^{\text{resid}} = \hat{\varepsilon}_i
$$

where  

- $\mathbf{C}_i$: age, sex, PCs, batch, center  
- $\mathbf{M}_i$: medication indicators, dosage, or drug class  

**Medication adjustment strategies**
- Indicator-based covariate (most common)
- Dosage or drug-class covariates
- Pre-correction (phenotype shifting, e.g. +10 mmHg for BP)
- Exclusion of medicated individuals (not recommended)

**Pros**
- Removes systematic non-genetic effects
- Improves power and reduces bias

**Cons**
- Residuals may still be non-normal

---

## Z score

**Definition**

Standardization to zero mean and unit variance:

$$
Z_i = \frac{Y_i - \mu_Y}{\sigma_Y}
\quad \text{or} \quad
Z_i = \frac{Y_i^{\text{resid}} - \mu_{\text{resid}}}{\sigma_{\text{resid}}}
$$

**Pros**
- Comparable effect sizes across cohorts
- Stable regression behavior

**Cons**
- Does not correct skewness
- Sensitive to outliers

---

## Rank-based inverse normal transformation (INT)

**Definition**

Transforms phenotype ranks to a standard normal distribution:

$$
Y_i^{\text{INT}} = \Phi^{-1}\left( \frac{r_i - c}{n + 1 - 2c} \right)
$$

where  

- $r_i$: rank of individual $i$  
- $c = 3/8$ (Blom's transformation, commonly used; $c = 0.5$ is also used in Rankit transformation)

**Pros**
- Enforces normality
- Robust to outliers
- Controls type-I error

**Cons**
- Effect sizes lose original scale
- Alters genetic architecture

---

## Recommended workflows

- Raw → GWAS (binary traits)
- Residual → Z (well-behaved quantitative traits)
- Residual → INT (highly skewed traits)
- Medication correction → Residual → Z / INT (clinical traits)

## References

- Beasley, T. M., Erickson, S., & Allison, D. B. (2009). Rank-based inverse normal transformations are increasingly used, but are they merited? *Behavior Genetics*, 39(5), 580-595. https://doi.org/10.1007/s10519-009-9281-0 https://pubmed.ncbi.nlm.nih.gov/19526352/

