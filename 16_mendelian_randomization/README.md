# Mendelian randomization

## Mendelian randomization introduction

## Instrumental Variables (IV)

## Assumptions
!!! danger "Key Assumptions"
    |Assumptions|Description|
    |-|-|
    |**Relevance**|Instrumental variables are strongly associated with the exposure.|
    |**Exclusion restriction**|Instrumental variables do not affect the outcome except through the exposure.|
    |**Independence**| There are no confounders of the instrumental variables and the outcome.|
    |Monotonicity| Variants affect the exposure in the same direction for all individuals|
    |No assortative mating|Assortative mating might cause bias in MR|

## Two-stage least-squares (2SLS)

$$ X = \mu_1 + \beta_{IV} IV + \epsilon_1  $$

$$ Y = \mu_2 + \beta_{2SLS} \hat{X} + \epsilon_2 $$

## Two-sample MR

$$ \hat{\beta_{X,Y}} = {{hat{\beta_{IV,Y}}\over{{hat{\beta_{IV,X}}} $$

## Practice

### R package TwoSampleMR


```
library(remotes)
install_github("MRCIEU/TwoSampleMR")
```

Reuqires R>= 4.1

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