
# Winner's curse

## Winner's curse definition

Winner's curse refers to the phenomenon that genetic effects are systematically overestimated by thresholding or selection process in genetic association studies. 

!!! info "Winner's curse in auctions"
    This term was initially used to describe a phenomenon that occurs in auctions. The winning bid is very likely to overestimate the intrinsic value of an item even if all the bids are unbiased (the auctioned item is of equal value to all bidders). The thresholding process in GWAS resembles auctions, where the lead variants are the winning bids.
    ![image](https://user-images.githubusercontent.com/40289485/219857681-e500620f-da3f-49ce-82d4-eb6191e17c7b.png)
    
    Reference: 
    
    - Bazerman, M. H., & Samuelson, W. F. (1983). I won the auction but don't want the prize. Journal of conflict resolution, 27(4), 618-634.
    - Göring, H. H., Terwilliger, J. D., & Blangero, J. (2001). Large upward bias in estimation of locus-specific effects from genomewide scans. The American Journal of Human Genetics, 69(6), 1357-1369.
    
## WC correction

The asymptotic distribution of $\beta_{Observed}$ is:

$$\beta_{Observed} \sim N(\beta_{True},\sigma^2)$$

!!! info "An example of distribution of $\beta_{Observed}$"
    ![image](https://user-images.githubusercontent.com/40289485/219680828-2300b866-b64f-4141-b63c-d21f7826db87.png)


- $c$ :  Z score cutpoint corresponding to the significance threshold.

It is equivalent to:

$${{\beta_{Observed} - \beta_{True}}\over{\sigma}} \sim N(0,1)$$

!!! info "An example of distribution of ${{\beta_{Observed} - \beta_{True}}\over{\sigma}}$"
    ![image](https://user-images.githubusercontent.com/40289485/219680536-eb20ae9c-2220-450a-95b1-9b4b6a7c91ce.png)


We can obtain the asymptotic sampling distribution (which is a [truncated normal distribution](https://en.wikipedia.org/wiki/Truncated_normal_distribution)) for $\beta_{Observed}$ by:

$$f(x,\beta_{True}) ={{1}\over{\sigma}} {{\phi({{{x - \beta_{True}}\over{\sigma}}})} \over {\Phi({{{\beta_{True}}\over{\sigma}}-c}) + \Phi({{{-\beta_{True}}\over{\sigma}}-c})}}$$

when

$$|{{x}\over{\sigma}}|\geq c$$

- $\phi(x)$ : standard normal density function.
- $\Phi(x)$ : standard normal cumulative density function.

From the asymptotic sampling distribution, the expectation of effect sizes for the selected variants can then be approximated by: 

$$ E(\beta_{Observed}; \beta_{True}) = \beta_{True} + \sigma {{\phi({{{\beta_{True}}\over{\sigma}}-c}) - \phi({{{-\beta_{True}}\over{\sigma}}-c})} \over {\Phi({{{\beta_{True}}\over{\sigma}}-c}) + \Phi({{{-\beta_{True}}\over{\sigma}}-c})}}$$

- $\beta_{Observed}$ is biased. 
- The bias is dependent on $\beta_{True}$, SE $\sigma$, and the selection threshold.

!!! tip "Derivation of this equation can be found in the Appendix A of Ghosh, A., Zou, F., & Wright, F. A. (2008). Estimating odds ratios in genome scans: an approximate conditional likelihood approach. The American Journal of Human Genetics, 82(5), 1064-1074."

Reference: 

- Zhong, H., & Prentice, R. L. (2008). Bias-reduced estimators and confidence intervals for odds ratios in genome-wide association studies. Biostatistics, 9(4), 621-634.
- Ghosh, A., Zou, F., & Wright, F. A. (2008). Estimating odds ratios in genome scans: an approximate conditional likelihood approach. The American Journal of Human Genetics, 82(5), 1064-1074.

Also see reference: https://amandaforde.github.io/winnerscurse/articles/winners_curse_methods.html
