# Heritability

Heritability is a term used in genetics to describe how much phenotypic variation can be explained by genetic variation.

For any phenotype, its variation $Var(P)$ can be modeled as the combination of **genetic effects** $Var(G)$ and **environmental effects** $Var(E)$.

$$
Var(P) = Var(G) + Var(E)
$$

## Broad-sense Heritability

The **broad-sense heritability** $H^2_{broad-sense}$ is mathmatically defined as :

$$
H^2_{broad-sense} = {Var(G)\over{Var(P)}}
$$


## Narrow-sense Heritability

**Genetic effects** $Var(G)$ is composed of multiple effects including **additive effects** $Var(A)$, dominant effects, recessive effects, epistatic effects and so forth.

Narrrow-sense heritability is defined as: 

$$
h^2_{narrow-sense} = {Var(A)\over{Var(P)}}
$$

## SNP Heritability

**SNP heritability $h^2_{SNP}$** : the proportion of phenotypic variance explained by tested SNPs in a GWAS.

Common methods to estimate SNP heritability includes:

- GCTA-GREML  (based on Genome-based  Restricted  Maximum  Likelihood)
- LDSC (based on LD score regression)


## Liability and Threshold model

<img width="1004" alt="image" src="https://user-images.githubusercontent.com/40289485/211184406-be57ac1b-8074-4098-bdff-2eb55dd91b30.png">

## Observed-scale heritability and liability-scaled heritability

Issue for binary traits : 

!!! quote "The scale issue for binary traits"
    
    - For quantitative traits the scale of measurement is the same as the scale on which heritability is expressed. 
    - For disease traits, the phenotypes (case-control status) are measured on the 0–1 scale, but heritability is most interpretable on a scale of liability.
    - Reference: Lee, S. H., Wray, N. R., Goddard, M. E., & Visscher, P. M. (2011). Estimating missing heritability for disease from genome-wide association studies. The American Journal of Human Genetics, 88(3), 294-305.

Conversion formula (Equation 23 from Lee. 2011):

$$
h^2_{liability-scale} = h^2_{observed-scale} * {{K(1-K)}\over{Z^2}} *  {{K(1-K)}\over{P(1-P)}}
$$

- $K$ : Population disease prevalence.
- $P$ : Sample disease prevalence.
- $Z$ : The height of the standard normal probability density function at threshold T. `scipy.stats.norm.pdf(T, loc=0, scale=1)`.
- $T$ : The threshold. `scipy.stats.norm.ppf(1 - K, loc=0, scale=1)` or `scipy.stats.norm.isf(K)`.


## Further Reading 

- (Blog by Neale Lab) http://www.nealelab.is/blog/2017/9/13/heritability-101-what-is-heritability
- Manolio, T. A., Collins, F. S., Cox, N. J., Goldstein, D. B., Hindorff, L. A., Hunter, D. J., ... & Visscher, P. M. (2009). Finding the missing heritability of complex diseases. Nature, 461(7265), 747-753.
- Visscher, P. M., Hill, W. G., & Wray, N. R. (2008). Heritability in the genomics era—concepts and misconceptions. Nature reviews genetics, 9(4), 255-266.
- Yang, J., Zeng, J., Goddard, M. E., Wray, N. R., & Visscher, P. M. (2017). Concepts, estimation and interpretation of SNP-based heritability. Nature genetics, 49(9), 1304-1310.
- Witte, J. S., Visscher, P. M., & Wray, N. R. (2014). The contribution of genetic variants to disease depends on the ruler. Nature Reviews Genetics, 15(11), 765-776.
