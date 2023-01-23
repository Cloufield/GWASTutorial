# Mendelian randomization

## Mendelian randomization introduction

## Instrumental Variables (IV)

## Assumptions
!!! danger "Key Assumptions"
	
	- **The relevance assumption**: instrumental variables are associated with the exposure.
	- **The independence assumption**: there are no confounders of the instrumental variables and the outcome.
	- **The exclusion restriction assumption**: instrumental variables do not affect the outcome except through the exposure.


## Two-stage least-squares (2SLS)

## Two-sample MR

### Loading package
```
library(TwoSampleMR)
```

### Reading exposure sumstats
```
#format exposures dataset

exposures_raw <-fread("./exposure_sumstats.txt")
#exposures$"p.value"= type.convert(exposures_raw$"p.value") 


```

### Extracting instrumental variables

```
# select only significant variants
exposures <- subset(exposures_raw,exposures_raw$`p.value`<5e-8)

# add a phenotype column
exposures$phenotype <- "exposure_trait"

exposures <- format_data(exposures,  type = "exposure",  snps = NULL,  header = TRUE,
                  snp_col = "SNP",beta_col = "beta",se_col = "se",effect_allele_col = "effect_allele",
                  other_allele_col = "non_effect_allele", pval_col = "p.value",phenotype_col="phenotype",
                  samplesize_col = "N",chr_col = "chr",pos_col = "pos")
```

### Clumping exposure variables

```
clumped_exposures <- clump_data(exposures,  clump_r2 = 0.01,  pop = "EAS")
```

### outcome

```
outcome <-fread("./outcome_sumstats.txt")

outcome <- format_data(outcome,  type = "exposure",  snps = NULL,  header = TRUE,
                  snp_col = "SNP",beta_col = "beta",se_col = "se",effect_allele_col = "effect_allele",
                  other_allele_col = "non_effect_allele", pval_col = "p.value",phenotype_col="phenotype",
                  samplesize_col = "N",chr_col = "chr",pos_col = "pos")
```

### Harmonizing data

```
harmonized_data <- harmonise_data(clumped_exposures, outcome, action=1)
```

### Perform MR analysis

```
res <-mr(harmonized_data, method_list=c("mr_ivw_fe", "mr_ivw_mre", "mr_egger_regression","mr_weighted_median", "mr_weighted_mode"))
```


## Sensitivity analysis

### Heterogeneity 

```
mr_heterogeneity(harmonized_data)
```

### Horizontal Pleiotropy 

Intercept in MR-Egger

```
mr_pleiotropy_test(harmonized_data)
```

### Single SNP MR and leave-one-out MR


## Visualization

### Scatter plot

### Forest plot

### Funnel plot

## Bi-directional MR

## Reference

- Sanderson, E., Glymour, M. M., Holmes, M. V., Kang, H., Morrison, J., Munafò, M. R., ... & Davey Smith, G. (2022). Mendelian randomization. Nature Reviews Methods Primers, 2(1), 1-21.