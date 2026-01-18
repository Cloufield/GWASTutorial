# Winner's curse

## Introduction

Winner's curse refers to the phenomenon that genetic effects are systematically overestimated by thresholding or selection process in genetic association studies. 

When we select variants based on significance thresholds (e.g., $p < 5 \times 10^{-8}$), the observed effect sizes for these selected variants tend to be inflated compared to their true effect sizes. This bias occurs because we're conditioning on the variants that passed the significance threshold, which are more likely to have observed effects that are larger than their true effects due to random sampling variation.

!!! info "Winner's curse in auctions"
    This term was initially used to describe a phenomenon that occurs in auctions. The winning bid is very likely to overestimate the intrinsic value of an item even if all the bids are unbiased (the auctioned item is of equal value to all bidders). The thresholding process in GWAS resembles auctions, where the lead variants are the winning bids.
    ![image](https://user-images.githubusercontent.com/40289485/219857681-e500620f-da3f-49ce-82d4-eb6191e17c7b.png)
    
    Reference: 
    
    - Bazerman, M. H., & Samuelson, W. F. (1983). I won the auction but don't want the prize. Journal of conflict resolution, 27(4), 618-634.
    - Göring, H. H., Terwilliger, J. D., & Blangero, J. (2001). Large upward bias in estimation of locus-specific effects from genomewide scans. The American Journal of Human Genetics, 69(6), 1357-1369.

!!! note "Why does winner's curse matter?"
    - **Effect size estimation**: Inflated effect sizes can mislead downstream analyses such as polygenic risk scores (PRS) or Mendelian randomization
    - **Replication studies**: Overestimated effects can lead to failed replications in independent cohorts
    - **Biological interpretation**: Accurate effect sizes are crucial for understanding the true magnitude of genetic associations
    - **Power calculations**: Biased effect estimates can affect power calculations for future studies

## Mathematical framework

### Asymptotic distribution

The asymptotic distribution of $\beta_{Observed}$ is:

$$\beta_{Observed} \sim N(\beta_{True},\sigma^2)$$

!!! info "An example of distribution of $\beta_{Observed}$"
    ![image](https://user-images.githubusercontent.com/40289485/219680828-2300b866-b64f-4141-b63c-d21f7826db87.png)

where:
- $\beta_{True}$: The true (unbiased) effect size
- $\sigma$: The standard error of the effect estimate
- $c$: Z score cutpoint corresponding to the significance threshold (e.g., $c = 5.45$ for $p = 5 \times 10^{-8}$)

It is equivalent to:

$${{\beta_{Observed} - \beta_{True}}\over{\sigma}} \sim N(0,1)$$

!!! info "An example of distribution of ${{\beta_{Observed} - \beta_{True}}\over{\sigma}}$"
    ![image](https://user-images.githubusercontent.com/40289485/219680536-eb20ae9c-2220-450a-95b1-9b4b6a7c91ce.png)

### Truncated normal distribution

We can obtain the asymptotic sampling distribution (which is a [truncated normal distribution](https://en.wikipedia.org/wiki/Truncated_normal_distribution)) for $\beta_{Observed}$ by:

$$f(x,\beta_{True}) ={{1}\over{\sigma}} {{\phi({{{x - \beta_{True}}\over{\sigma}}})} \over {\Phi({{{\beta_{True}}\over{\sigma}}-c}) + \Phi({{{-\beta_{True}}\over{\sigma}}-c})}}$$

when

$$|{{x}\over{\sigma}}|\geq c$$

where:
- $\phi(x)$: standard normal density function
- $\Phi(x)$: standard normal cumulative density function

### Expected bias

From the asymptotic sampling distribution, the expectation of effect sizes for the selected variants can then be approximated by: 

$$ E(\beta_{Observed}; \beta_{True}) = \beta_{True} + \sigma {{\phi({{{\beta_{True}}\over{\sigma}}-c}) - \phi({{{-\beta_{True}}\over{\sigma}}-c})} \over {\Phi({{{\beta_{True}}\over{\sigma}}-c}) + \Phi({{{-\beta_{True}}\over{\sigma}}-c})}}$$

Key observations:
- $\beta_{Observed}$ is biased upward (for positive effects) or downward (for negative effects)
- The bias is dependent on $\beta_{True}$, SE $\sigma$, and the selection threshold $c$
- The bias is larger when the standard error is larger relative to the true effect size

!!! tip "Derivation of this equation"
    The derivation of this equation can be found in the Appendix A of Ghosh, A., Zou, F., & Wright, F. A. (2008). Estimating odds ratios in genome scans: an approximate conditional likelihood approach. The American Journal of Human Genetics, 82(5), 1064-1074.

## Winner's curse correction

To correct for winner's curse, we need to solve for $\beta_{True}$ given the observed $\beta_{Observed}$ and standard error $\sigma$. This is done by finding the value of $\beta_{True}$ that satisfies:

$$E(\beta_{Observed}; \beta_{True}) = \beta_{Observed}$$

This requires solving a nonlinear equation, typically using numerical methods.

### Implementation in Python

!!! example "Winner's curse correction function in Python"
    ```python
    import scipy.stats as sp
    import scipy.optimize
    import numpy as np
    
    def wc_correct(beta, se, sig_level=5e-8):
        """
        Correct for winner's curse bias in effect size estimates.
        
        Parameters:
        -----------
        beta : float or array-like
            Observed effect size(s)
        se : float or array-like
            Standard error(s) of the effect size(s)
        sig_level : float
            Significance threshold (default: 5e-8 for genome-wide significance)
        
        Returns:
        --------
        float or array
            Corrected effect size(s)
        """
        # Calculate z-score cutpoint
        c2 = sp.chi2.ppf(1 - sig_level, df=1)
        c = np.sqrt(c2)
        
        def bias(beta_T, beta_O, se):
            """Calculate the bias for a given true effect size."""
            z = beta_T / se
            numerator = sp.norm.pdf(z - c) - sp.norm.pdf(-z - c)
            denominator = sp.norm.cdf(z - c) + sp.norm.cdf(-z - c)
            return beta_T + se * numerator / denominator - beta_O
        
        # Handle both scalar and array inputs
        if np.isscalar(beta):
            beta_corrected = scipy.optimize.brentq(
                lambda x: bias(x, beta, se),
                a=-100, b=100,
                maxiter=1000
            )
        else:
            beta_corrected = np.array([
                scipy.optimize.brentq(
                    lambda x: bias(x, b, s),
                    a=-100, b=100,
                    maxiter=1000
                )
                for b, s in zip(beta, se)
            ])
        
        return beta_corrected
    
    # Example usage
    beta_obs = 0.15
    se = 0.02
    beta_corrected = wc_correct(beta_obs, se)
    
    print(f"Observed effect: {beta_obs:.4f}")
    print(f"Corrected effect: {beta_corrected:.4f}")
    print(f"Bias: {beta_obs - beta_corrected:.4f}")
    ```

### Implementation in R

!!! example "Winner's curse correction function in R"
    ```r
    WC_correction <- function(BETA,        # Effect size (vector)
                              SE,          # Standard Error (vector)
                              alpha=5e-8){ # Significance threshold
    
      # Calculate z-score cutpoint
      Q <- qchisq(alpha, df=1, lower.tail=FALSE)
      c <- sqrt(Q)
      
      # Bias function
      bias <- function(betaTrue, betaObs, se){
        z <- betaTrue / se
        num <- dnorm(z - c) - dnorm(-z - c)
        den <- pnorm(z - c) + pnorm(-z - c)
        return(betaObs - betaTrue + se * num / den)
      }
      
      # Solve for true beta
      solveBetaTrue <- function(betaObs, se){
        result <- uniroot(
          f = function(b) bias(b, betaObs, se),
          lower = -100,
          upper = 100
        )
        return(result$root)
      }
      
      # Apply correction to all variants
      BETA_corrected <- sapply(
        1:length(BETA),
        function(i) solveBetaTrue(BETA[i], SE[i])
      )
      
      return(BETA_corrected)
    }
    
    # Example usage
    beta_obs <- 0.15
    se <- 0.02
    beta_corrected <- WC_correction(beta_obs, se)
    
    cat("Observed effect:", beta_obs, "\n")
    cat("Corrected effect:", beta_corrected, "\n")
    cat("Bias:", beta_obs - beta_corrected, "\n")
    ```

### Applying correction to GWAS summary statistics

!!! example "Correcting multiple variants from GWAS summary statistics"
    ```python
    import pandas as pd
    
    # Load GWAS summary statistics
    sumstats = pd.read_csv("gwas_results.tsv", sep="\t")
    
    # Filter for significant variants
    significant = sumstats[sumstats["P"] < 5e-8].copy()
    
    # Apply winner's curse correction
    significant["BETA_corrected"] = wc_correct(
        significant["BETA"].values,
        significant["SE"].values,
        sig_level=5e-8
    )
    
    # Calculate the bias
    significant["Bias"] = significant["BETA"] - significant["BETA_corrected"]
    
    # Display results
    print(significant[["SNP", "BETA", "BETA_corrected", "Bias", "SE", "P"]].head())
    ```

!!! tip "When to apply winner's curse correction"
    - **Before replication studies**: Correct effect sizes to get more accurate estimates for power calculations
    - **Before PRS construction**: Use corrected effect sizes for more accurate polygenic risk scores
    - **Before Mendelian randomization**: Corrected effect sizes improve MR estimates
    - **For meta-analysis**: Correct effect sizes from discovery studies before meta-analysis

## Available tools and packages

Several tools and packages are available for winner's curse correction:

!!! note "R packages"
    - **winnerscurse**: R package providing multiple methods for winner's curse correction
      - Installation: `install.packages("winnerscurse")`
      - Documentation: https://amandaforde.github.io/winnerscurse/
      - Methods include: conditional likelihood, FDR inverse quantile transformation, and bootstrap-based methods

!!! note "Python packages"
    - Custom implementation (as shown above) using `scipy`
    - The `winnerscurse` R package can also be used via `rpy2` in Python

!!! tip "Comparison of methods"
    Different methods for winner's curse correction have been developed:
    - **Conditional likelihood approach**: Used in the examples above (Zhong & Prentice, 2008; Ghosh et al., 2008)
    - **FDR inverse quantile transformation**: Alternative approach that may be more robust
    - **Bootstrap methods**: Can be computationally intensive but may handle complex scenarios better
    
    For a comprehensive comparison, see: https://amandaforde.github.io/winnerscurse/articles/winners_curse_methods.html

## Limitations and considerations

!!! warning "Important considerations"
    - **Assumptions**: The correction assumes that the asymptotic normal distribution holds and that variants are independent
    - **LD structure**: The correction may not fully account for linkage disequilibrium (LD) between variants
    - **Multiple testing**: The correction is typically applied per-variant; accounting for multiple testing may require additional considerations
    - **Effect direction**: The correction works for both positive and negative effects, but the bias direction differs
    - **Small effects**: For very small true effects, the correction may be less reliable

!!! tip "Best practices"
    - Apply correction only to variants that passed the significance threshold
    - Use the same significance threshold for correction as was used for selection
    - Consider the standard error when interpreting corrected effects
    - Validate corrected effects in independent replication cohorts when possible

## References

### Methodological papers

- **Zhong, H., & Prentice, R. L.** (2008). Bias-reduced estimators and confidence intervals for odds ratios in genome-wide association studies. *Biostatistics*, 9(4), 621-634. https://doi.org/10.1093/biostatistics/kxn001

- **Ghosh, A., Zou, F., & Wright, F. A.** (2008). Estimating odds ratios in genome scans: an approximate conditional likelihood approach. *The American Journal of Human Genetics*, 82(5), 1064-1074. https://doi.org/10.1016/j.ajhg.2008.03.002

### Review and comparison papers

- **Forde, A., & Wade, K. H.** (2022). Winner's Curse Correction and Variable Thresholding Improve Performance of Polygenic Risk Modeling Based on Genome-Wide Association Study Summary-Level Data. *PLoS Genetics*, 18(6), e1010173. https://doi.org/10.1371/journal.pgen.1010173

### Software and resources

- **winnerscurse R package**: https://amandaforde.github.io/winnerscurse/
- **Comparison of winner's curse methods**: https://amandaforde.github.io/winnerscurse/articles/winners_curse_methods.html
