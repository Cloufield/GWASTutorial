
# Winner's curse

## Winner's curse definition

Winner's curse refers to the phenomenon that genetic effects are systematically overestimated by thresholding or selection process. 

# WC correction

The expectation of effect sizes for the selected variants can be approximated by: 

$$ E(\beta_{Observed}; \beta_{True}) = \beta_{True} + \sigma {{\phi({{{\beta_{True}}\over{\sigma}}-c}) - \phi({{{-\beta_{True}}\over{\sigma}}-c})} \over {\Phi({{{\beta_{True}}\over{\sigma}}-c}) + \Phi({{{-\beta_{True}}\over{\sigma}}-c})}}$$

- $\beta_{Observed}$ is biased. 
- The bias is dependent on $\beta_{True}$, SE $\sigma$, and the selection threshold.
- $\phi(x)$ : standard normal density function.
- $\Phi(x)$ : standard normal cumulative density function.
- $c$ :  test statistic cutpoint corresponding to significance threshold.

Reference: Zhong, H., & Prentice, R. L. (2008). Bias-reduced estimators and confidence intervals for odds ratios in genome-wide association studies. Biostatistics, 9(4), 621-634.

Also see reference: https://amandaforde.github.io/winnerscurse/articles/winners_curse_methods.html