# Mendelian randomization

## Mendelian randomization introduction

!!! tip "Comparison between RCT and MR"
    <img width="636" alt="image" src="https://user-images.githubusercontent.com/40289485/219572347-1ebc2f0a-3c9a-49a0-a058-638e4973873e.png">

## Fundamental assumption: gene-environment equivalence

(cited from George Davey Smith Mendelian Randomization - 25th April 2024)

The fundamental assumption of mendelian randomization (MR) is of **gene-environment equivalence**. MR reflects the phenocopy/ genocopy dialectic (Goldschmidt, Schmalhausen). The idea here is that all environmental effects can be mimicked by one or several mutations. (Zuckerkandl and Villet, PNAS 1988)

Gene-environment equivalence

- Requires justifying in all situations
- Relates to biological processes that are influenced by genetic variations

If we consider BMI as the outcome, let's think about whether genetic variants related to the following exposures meet the gene-environment equivalence assumption:

- Higher calorie intake: Yes
- Physical activity level: Yes
- Losing a leg (which dramatically affects BMI): No
- Smoking:? Maybe. Complicated.


## Methods: Instrumental Variables (IV)

Instrumental variable (IV) can be defined as a variable  that is correlated with the exposure X and uncorrelated with the error $\epsilon$ in the following regression: 

$$ Y = X\beta + \epsilon $$

- $Y$ is the outcome
- $X$ is the exposure
- $C$ is the confounders

<img width="600" alt="image" src="https://github.com/Cloufield/GWASTutorial/assets/40289485/63c25ce6-e086-4010-86bf-212818f2ac64">

## IV Assumptions

!!! danger "Key Assumptions"
    |Assumptions|Description|
    |-|-|
    |**Relevance**|Instrumental variables are strongly associated with the exposure.(IVs are not independent of X)|
    |**Exclusion restriction**|Instrumental variables do not affect the outcome except through the exposure.(IV is independent of Y, conditional on X and C)|
    |**Independence**| There are no confounders of the instrumental variables and the outcome.(IV is independent of C)|
    |Monotonicity| Variants affect the exposure in the same direction for all individuals|
    |No assortative mating|Assortative mating might cause bias in MR|

## Two-stage least-squares (2SLS)

$$ X = \mu_1 + \beta_{IV} IV + \epsilon_1  $$

$$ Y = \mu_2 + \beta_{2SLS} \hat{X} + \epsilon_2 $$

## Two-sample MR

Two-sample MR refers to the approach that the genetic effects of the instruments on the exposure can be estimated in an independent sample other than that used to estimate effects between instruments on the outcome. As more and more GWAS summary statistics become publicly available, the scope of MR also expands with Two-sample MR methods.

$$ \hat{\beta}_{X,Y} = {{\hat{\beta}_{IV,Y}}\over{\hat{\beta}_{IV,X}}} $$

!!! warning "Caveats"
    For two-sample MR, there is an additional key assumption:
    
    **The two samples used for MR are from the same underlying populations. (The effect size of instruments on exposure should be the same in both samples.)** 

    Therefore, for two-sample MR, we usually use datasets from similar non-overlapping populations in terms of not only ancestry but also contextual factors. 

## IV selection

One of the first things to do when you plan to perform any type of MR is to check the associations of instrumental variables with the exposure to avoid bias caused by weak IVs.
 
The most commonly used method here is the **F-statistic**, which tests the association of instrumental variables with the exposure.


## Practice

In this tutorial, we will walk you through how to perform a minimal TwoSampleMR analysis. We will use the R package [TwoSampleMR](https://mrcieu.github.io/TwoSampleMR/index.html), which provides easy-to-use functions for formatting, clumping and harmonizing GWAS summary statistics. 

This package integrates a variety of commonly used MR methods for analysis, including:
```
> mr_method_list()
                             obj
1                  mr_wald_ratio
2               mr_two_sample_ml
3            mr_egger_regression
4  mr_egger_regression_bootstrap
5               mr_simple_median
6             mr_weighted_median
7   mr_penalised_weighted_median
8                         mr_ivw
9                  mr_ivw_radial
10                    mr_ivw_mre
11                     mr_ivw_fe
12                mr_simple_mode
13              mr_weighted_mode
14         mr_weighted_mode_nome
15           mr_simple_mode_nome
16                       mr_raps
17                       mr_sign
18                        mr_uwr

                                                        name PubmedID
1                                                 Wald ratio
2                                         Maximum likelihood
3                                                   MR Egger 26050253
4                                       MR Egger (bootstrap) 26050253
5                                              Simple median
6                                            Weighted median
7                                  Penalised weighted median
8                                  Inverse variance weighted
9                                                 IVW radial
10 Inverse variance weighted (multiplicative random effects)
11                 Inverse variance weighted (fixed effects)
12                                               Simple mode
13                                             Weighted mode
14                                      Weighted mode (NOME)
15                                        Simple mode (NOME)
16                      Robust adjusted profile score (RAPS)
17                                     Sign concordance test
18                                     Unweighted regression
```

### Inverse variance weighted (fixed effects)

Assumption: the underlying 'true' effect is fixed across variants

Weight for the effect of ith variant:

$$W_i = {1 \over Var(\beta_i)}$$

Effect size:

$$\beta = {{\sum_{i=1}^N{w_i \beta_i}}\over{\sum_{i=1}^Nw_i}}$$

SE:

$$SE = {\sqrt{{1}\over{\sum_{i=1}^Nw_i}}}$$

### OPENGWAS API
As of May 1, 2024, most OpenGWAS API queries require user authentication. To use the API:
1.  Log in at [OPENGWAS API](https://api.opengwas.io/profile/) and generate a token.
2.  Add the token to your .Renviron file as: `OPENGWAS_JWT=<your_token>`
3.  Restart your R session.
4.  To confirm authentication, run `ieugwasr::get_opengwas_jwt()` — if it returns a token, you’re authenticated.
5.  To check the token is working, run `user()` — it should return your profile info.

This token acts like a password. Keep it secure and do not share it. Please check [ieugwasr guide](https://mrcieu.github.io/ieugwasr/articles/guide.html#authentication) for more details.

### File Preparation

To perform two-sample MR analysis, we need summary statistics for exposure and outcome generated from independent populations with the same ancestry.

In this tutorial, we will use sumstats from [Biobank Japan pheweb](https://pheweb.jp/) and [KoGES pheweb](https://koges.leelabsg.org/).

- Type 2 diabetes sumstats from BBJ : `wget -O bbj_t2d.zip https://pheweb.jp/download/T2D`
- BMI sumstats from KoGES :  `wget -O koges_bmi.txt.gz https://koges.leelabsg.org/download/KoGES_BMI`

### R package TwoSampleMR

First, to use TwosampleMR, we need R>= 4.1.
To install the package, run:

```R
library(remotes)
install_github("MRCIEU/TwoSampleMR")
```

### Loading package

```R
library(TwoSampleMR)
```

### Reading exposure sumstats

```R
#format exposures dataset

exp_raw <- fread("koges_bmi.txt.gz")

```

### Extracting instrumental variables

```R
# select only significant variants
exp_raw <- subset(exp_raw,exp_raw$pval<5e-8)

exp_dat <- format_data( exp_raw,
    type = "exposure",
    snp_col = "rsids",
    beta_col = "beta",
    se_col = "sebeta",
    effect_allele_col = "alt",
    other_allele_col = "ref",
    eaf_col = "af",
    pval_col = "pval",
)
```

### Clumping exposure variables

```R
clumped_exp <- clump_data(exp_dat,clump_r2=0.01,pop="EAS") 
```

### outcome

```R
out_raw <- fread("hum0197.v3.BBJ.T2D.v1/GWASsummary_T2D_Japanese_SakaueKanai2020.auto.txt.gz",
                    select=c("SNPID","Allele1","Allele2","BETA","SE","p.value"))
out_dat <- format_data( out_raw,
    type = "outcome",
    snp_col = "SNPID",
    beta_col = "BETA",
    se_col = "SE",
    effect_allele_col = "Allele2",
    other_allele_col = "Allele1",
    pval_col = "p.value",
)
```

### Harmonizing data

```
harmonized_data <- harmonise_data(clumped_exp,out_dat,action=1)
```

### Perform MR analysis

```R
res <- mr(harmonized_data)

id.exposure	id.outcome	outcome	exposure	method	nsnp	b	se	pval
<chr>	<chr>	<chr>	<chr>	<chr>	<int>	<dbl>	<dbl>	<dbl>
9J8pv4	IyUv6b	outcome	exposure	MR Egger	28	1.3337580	0.69485260	6.596064e-02
9J8pv4	IyUv6b	outcome	exposure	Weighted median	28	0.6298980	0.09401352	2.083081e-11
9J8pv4	IyUv6b	outcome	exposure	Inverse variance weighted	28	0.5598956	0.23225806	1.592361e-02
9J8pv4	IyUv6b	outcome	exposure	Simple mode	28	0.6097842	0.15180476	4.232158e-04
9J8pv4	IyUv6b	outcome	exposure	Weighted mode	28	0.5946778	0.12820220	8.044488e-05
```


## Sensitivity analysis

### Heterogeneity 

Test if there is heterogeneity among the causal effect of x on y estimated from each variants.

```R
mr_heterogeneity(harmonized_data)

id.exposure	id.outcome	outcome	exposure	method	Q	Q_df	Q_pval
<chr>	<chr>	<chr>	<chr>	<chr>	<dbl>	<dbl>	<dbl>
9J8pv4	IyUv6b	outcome	exposure	MR Egger	670.7022	26	1.000684e-124
9J8pv4	IyUv6b	outcome	exposure	Inverse variance weighted	706.6579	27	1.534239e-131
```

### Horizontal Pleiotropy 

Intercept in MR-Egger

```R
mr_pleiotropy_test(harmonized_data)

id.exposure	id.outcome	outcome	exposure	egger_intercept	se	pval
<chr>	<chr>	<chr>	<chr>	<dbl>	<dbl>	<dbl>
9J8pv4	IyUv6b	outcome	exposure	-0.03603697	0.0305241	0.2484472
```

### Single SNP MR and leave-one-out MR

Single SNP MR

```
res_single <- mr_singlesnp(harmonized_data)
res_single

exposure	outcome	id.exposure	id.outcome	samplesize	SNP	b	se	p
<chr>	<chr>	<chr>	<chr>	<lgl>	<chr>	<dbl>	<dbl>	<dbl>
1	exposure	outcome	9J8pv4	IyUv6b	NA	rs10198356	0.6323140	0.2082837	2.398742e-03
2	exposure	outcome	9J8pv4	IyUv6b	NA	rs10209994	0.9477808	0.3225814	3.302164e-03
3	exposure	outcome	9J8pv4	IyUv6b	NA	rs10824329	0.6281765	0.3246214	5.297739e-02
4	exposure	outcome	9J8pv4	IyUv6b	NA	rs10938397	1.2376316	0.2775854	8.251150e-06
5	exposure	outcome	9J8pv4	IyUv6b	NA	rs11066132	0.6024303	0.2232401	6.963693e-03
6	exposure	outcome	9J8pv4	IyUv6b	NA	rs12522139	0.2905201	0.2890240	3.148119e-01
7	exposure	outcome	9J8pv4	IyUv6b	NA	rs12591730	0.8930490	0.3076687	3.700413e-03
8	exposure	outcome	9J8pv4	IyUv6b	NA	rs13013021	1.4867889	0.2207777	1.646925e-11
9	exposure	outcome	9J8pv4	IyUv6b	NA	rs1955337	0.5442640	0.2994146	6.910079e-02
10	exposure	outcome	9J8pv4	IyUv6b	NA	rs2076308	1.1176226	0.2657969	2.613132e-05
11	exposure	outcome	9J8pv4	IyUv6b	NA	rs2278557	0.6238587	0.2968184	3.556906e-02
12	exposure	outcome	9J8pv4	IyUv6b	NA	rs2304608	1.5054682	0.2968905	3.961740e-07
13	exposure	outcome	9J8pv4	IyUv6b	NA	rs2531995	1.3972908	0.3130157	8.045689e-06
14	exposure	outcome	9J8pv4	IyUv6b	NA	rs261967	1.5303384	0.2921192	1.616714e-07
15	exposure	outcome	9J8pv4	IyUv6b	NA	rs35332469	-0.2307314	0.3479219	5.072217e-01
16	exposure	outcome	9J8pv4	IyUv6b	NA	rs35560038	-1.5730870	0.2018968	6.619637e-15
17	exposure	outcome	9J8pv4	IyUv6b	NA	rs3755804	0.5314915	0.2325073	2.225933e-02
18	exposure	outcome	9J8pv4	IyUv6b	NA	rs4470425	0.6948046	0.3079944	2.407689e-02
19	exposure	outcome	9J8pv4	IyUv6b	NA	rs476828	1.1739083	0.1568550	7.207355e-14
20	exposure	outcome	9J8pv4	IyUv6b	NA	rs4883723	0.5479721	0.2855004	5.494141e-02
21	exposure	outcome	9J8pv4	IyUv6b	NA	rs509325	0.5491040	0.1598196	5.908641e-04
22	exposure	outcome	9J8pv4	IyUv6b	NA	rs55872725	1.3501891	0.1259791	8.419325e-27
23	exposure	outcome	9J8pv4	IyUv6b	NA	rs6089309	0.5657525	0.3347009	9.096620e-02
24	exposure	outcome	9J8pv4	IyUv6b	NA	rs6265	0.6457693	0.1901871	6.851804e-04
25	exposure	outcome	9J8pv4	IyUv6b	NA	rs6736712	0.5606962	0.3448784	1.039966e-01
26	exposure	outcome	9J8pv4	IyUv6b	NA	rs7560832	0.6032080	0.2904972	3.785077e-02
27	exposure	outcome	9J8pv4	IyUv6b	NA	rs825486	-0.6152759	0.3500334	7.878772e-02
28	exposure	outcome	9J8pv4	IyUv6b	NA	rs9348441	-4.9786332	0.2572782	1.992909e-83
29	exposure	outcome	9J8pv4	IyUv6b	NA	All - Inverse variance weighted	0.5598956	0.2322581	1.592361e-02
30	exposure	outcome	9J8pv4	IyUv6b	NA	All - MR Egger	1.3337580	0.6948526	6.596064e-02
```

leave-one-out MR

```
res_loo <- mr_leaveoneout(harmonized_data)
res_loo

exposure	outcome	id.exposure	id.outcome	samplesize	SNP	b	se	p
<chr>	<chr>	<chr>	<chr>	<lgl>	<chr>	<dbl>	<dbl>	<dbl>
1	exposure	outcome	9J8pv4	IyUv6b	NA	rs10198356	0.5562834	0.2424917	2.178871e-02
2	exposure	outcome	9J8pv4	IyUv6b	NA	rs10209994	0.5520576	0.2388122	2.079526e-02
3	exposure	outcome	9J8pv4	IyUv6b	NA	rs10824329	0.5585335	0.2390239	1.945341e-02
4	exposure	outcome	9J8pv4	IyUv6b	NA	rs10938397	0.5412688	0.2388709	2.345460e-02
5	exposure	outcome	9J8pv4	IyUv6b	NA	rs11066132	0.5580606	0.2417275	2.096381e-02
6	exposure	outcome	9J8pv4	IyUv6b	NA	rs12522139	0.5667102	0.2395064	1.797373e-02
7	exposure	outcome	9J8pv4	IyUv6b	NA	rs12591730	0.5524802	0.2390990	2.085075e-02
8	exposure	outcome	9J8pv4	IyUv6b	NA	rs13013021	0.5189715	0.2386808	2.968017e-02
9	exposure	outcome	9J8pv4	IyUv6b	NA	rs1955337	0.5602635	0.2394505	1.929468e-02
10	exposure	outcome	9J8pv4	IyUv6b	NA	rs2076308	0.5431355	0.2394403	2.330758e-02
11	exposure	outcome	9J8pv4	IyUv6b	NA	rs2278557	0.5583634	0.2394924	1.972992e-02
12	exposure	outcome	9J8pv4	IyUv6b	NA	rs2304608	0.5372557	0.2377325	2.382639e-02
13	exposure	outcome	9J8pv4	IyUv6b	NA	rs2531995	0.5419016	0.2379712	2.277590e-02
14	exposure	outcome	9J8pv4	IyUv6b	NA	rs261967	0.5358761	0.2376686	2.415093e-02
15	exposure	outcome	9J8pv4	IyUv6b	NA	rs35332469	0.5735907	0.2378345	1.587739e-02
16	exposure	outcome	9J8pv4	IyUv6b	NA	rs35560038	0.6734906	0.2217804	2.391474e-03
17	exposure	outcome	9J8pv4	IyUv6b	NA	rs3755804	0.5610215	0.2413249	2.008503e-02
18	exposure	outcome	9J8pv4	IyUv6b	NA	rs4470425	0.5568993	0.2392632	1.993549e-02
19	exposure	outcome	9J8pv4	IyUv6b	NA	rs476828	0.5037555	0.2443224	3.922224e-02
20	exposure	outcome	9J8pv4	IyUv6b	NA	rs4883723	0.5602050	0.2397325	1.945000e-02
21	exposure	outcome	9J8pv4	IyUv6b	NA	rs509325	0.5608429	0.2468506	2.308693e-02
22	exposure	outcome	9J8pv4	IyUv6b	NA	rs55872725	0.4419446	0.2454771	7.180543e-02
23	exposure	outcome	9J8pv4	IyUv6b	NA	rs6089309	0.5597859	0.2388902	1.911519e-02
24	exposure	outcome	9J8pv4	IyUv6b	NA	rs6265	0.5547068	0.2436910	2.282978e-02
25	exposure	outcome	9J8pv4	IyUv6b	NA	rs6736712	0.5598815	0.2387602	1.902944e-02
26	exposure	outcome	9J8pv4	IyUv6b	NA	rs7560832	0.5588113	0.2396229	1.969836e-02
27	exposure	outcome	9J8pv4	IyUv6b	NA	rs825486	0.5800026	0.2367545	1.429330e-02
28	exposure	outcome	9J8pv4	IyUv6b	NA	rs9348441	0.7378967	0.1366838	6.717515e-08
29	exposure	outcome	9J8pv4	IyUv6b	NA	All	0.5598956	0.2322581	1.592361e-02
```

## Visualization

### Scatter plot

```
res <- mr(harmonized_data)
p1 <- mr_scatter_plot(res, harmonized_data)
p1[[1]]
```

![image](https://user-images.githubusercontent.com/40289485/214480227-396f816f-e1e6-49a1-9f3e-2e43a9d03abf.png)


### Single SNP 
```
res_single <- mr_singlesnp(harmonized_data)
p2 <- mr_forest_plot(res_single)
p2[[1]]
```

![image](https://user-images.githubusercontent.com/40289485/214480253-6de266cf-2737-4d4f-b7fb-e889fea3ea4e.png)

### Leave-one-out

```
res_loo <- mr_leaveoneout(harmonized_data)
p3 <- mr_leaveoneout_plot(res_loo)
p3[[1]]
```

![image](https://user-images.githubusercontent.com/40289485/214480292-5bc318a3-1d74-4f09-8b07-b8a3cc62d2e0.png)


### Funnel plot

```
res_single <- mr_singlesnp(harmonized_data)
p4 <- mr_funnel_plot(res_single)
p4[[1]]
```

![image](https://user-images.githubusercontent.com/40289485/214480351-86288d44-52fb-416a-bdf4-2a4f4804e744.png)


## MR Steiger directionality test

MR Steiger directionality test is a method to test the causal direction.

Steiger test: test whether the SNP-outcome correlation is greater than the SNP-exposure correlation.

```
harmonized_data$"r.outcome" <- get_r_from_lor(
  harmonized_data$"beta.outcome",
  harmonized_data$"eaf.outcome",
  45383,
  132032,
  0.26,
  model = "logit",
  correction = FALSE
)

out <- directionality_test(harmonized_data)
out

id.exposure	id.outcome	exposure	outcome	snp_r2.exposure	snp_r2.outcome	correct_causal_direction	steiger_pval
<chr>	<chr>	<chr>	<chr>	<dbl>	<dbl>	<lgl>	<dbl>
rvi6Om	ETcv15	BMI	T2D	0.02125453	0.005496427	TRUE	NA
```

Reference: Hemani, G., Tilling, K., & Davey Smith, G. (2017). Orienting the causal relationship between imprecisely measured traits using GWAS summary data. PLoS genetics, 13(11), e1007081.

## MR-Base (web app)

[MR-Base web app](https://app.mrbase.org/)

## STROBE-MR

Before reporting any MR results, please check the STROBE-MR Checklist first, which consists of 20 things that should be addressed when reporting a mendelian randomization study.

- Skrivankova, V. W., Richmond, R. C., Woolf, B. A., Yarmolinsky, J., Davies, N. M., Swanson, S. A., ... & Richards, J. B. (2021). Strengthening the reporting of observational studies in epidemiology using Mendelian randomization: the STROBE-MR statement. Jama, 326(16), 1614-1621.

## References

- Sanderson, E., Glymour, M. M., Holmes, M. V., Kang, H., Morrison, J., Munafò, M. R., ... & Davey Smith, G. (2022). Mendelian randomization. Nature Reviews Methods Primers, 2(1), 1-21.
- Hemani, G., Zheng, J., Elsworth, B., Wade, K. H., Haberland, V., Baird, D., ... & Haycock, P. C. (2018). The MR-Base platform supports systematic causal inference across the human phenome. elife, 7, e34408.
- Zuckerkandl, E., & Villet, R. (1988). Concentration-affinity equivalence in gene regulation: convergence of genetic and environmental effects. Proceedings of the National Academy of Sciences, 85(13), 4784-4788.
- Skrivankova, V. W., Richmond, R. C., Woolf, B. A., Yarmolinsky, J., Davies, N. M., Swanson, S. A., ... & Richards, J. B. (2021). Strengthening the reporting of observational studies in epidemiology using Mendelian randomization: the STROBE-MR statement. Jama, 326(16), 1614-1621.
