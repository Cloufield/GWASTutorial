# Study design and phenotype definition

Careful study design and clean phenotype definition reduce bias, improve power, and make results interpretable across cohorts.

---

## Ascertainment bias

Ascertainment bias happens when sample selection depends on the trait or related factors.

**Common sources**
- Clinic-based recruitment for disease studies
- Enrichment of extreme phenotypes
- Volunteer or biobank participation bias

**Mitigation**
- Document inclusion criteria and recruitment pathways
- Include sampling weights or covariates that capture selection
- Perform sensitivity analyses with alternative inclusion rules

---

## Case/control selection

**Principles**
- Use consistent diagnostic criteria across sites
- Exclude ambiguous cases or controls with related conditions
- Avoid "super controls" that are not representative of the source population

**Matching and balance**
- Match or adjust for age, sex, ancestry, and study site
- Track case/control ratio for power and calibration

---

## Covariate strategy

**Typical covariates**
- Age, sex, study site or batch
- Genetic ancestry PCs
- Technical variables (array, center, processing date)

**Guidelines**
- Use a prespecified covariate list
- Avoid overfitting with excessive covariates
- Report covariates in methods and summary statistics

---

## Trait transformations

**When to transform**
- Skewed quantitative traits
- Heavy-tailed distributions or outliers

**Common options**
- Log or Box-Cox transform
- Rank-based inverse normal transformation (INT)

See `26_normalization` for recommended workflows.

---

## Phenotype QC

**Core checks**
- Range and unit validation
- Outlier detection
- Duplicate records and inconsistent values

**Example rules**
- Remove biologically implausible values
- Flag values outside 4-6 SD for review

---

## Missingness handling

**Patterns to evaluate**
- Missing not at random (MNAR) by case/control status
- Missingness by site or batch

**Approaches**
- Exclude individuals with high missing phenotype rate
- Multiple imputation for covariates if justified
- Sensitivity analysis for MNAR risks

---

## Multi-trait and longitudinal outcomes

**Multi-trait**
- Use multivariate models when traits are correlated
- Adjust for multiple testing or use joint tests

**Longitudinal**
- Prefer mixed models with random effects
- Model time-varying covariates and visits

---

## Checklist

- Define inclusion/exclusion and outcome labels before analysis
- Predefine covariates and transformation rules
- Record all phenotype QC filters
- Confirm that missingness is not trait-dependent

## References

- Pirastu, N., et al. (2021). Genetic analyses identify widespread sex-differential participation bias. *Nature Genetics*, 53, 663-671. https://doi.org/10.1038/s41588-021-00846-7
- Hernan, M. A., & Robins, J. M. (2020). *Causal Inference: What If*. Chapman & Hall/CRC.
