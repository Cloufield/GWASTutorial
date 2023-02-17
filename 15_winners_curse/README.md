
# Winner's curse

## Winner's curse definition

Winner's curse refers to the phenomenon that genetic effects are systematically overestimated by thresholding or selection process. 

## WC correction

The asymptotic distribution of $\beta_{Observed}$ is:
$$ \beta_{Observed} \sim N(\beta_{True},\sigma)$$

$$ {{\beta_{Observed} - \beta_{True}}\over{\sigma}}  \sim N(0,1)$$

!!! tip "Distribution of $\beta_{Observed}$"

The asymptotic sampling distribution for $\beta_{Observed}$ is a truncated normal distribution:

$$f(x,\beta_{True}) ={{1}\over{\sigma}} {{\phi({{{x - \beta_{True}}\over{\sigma}}})} \over {\Phi({{{\beta_{True}}\over{\sigma}}-c}) + \Phi({{{-\beta_{True}}\over{\sigma}}-c})}}$$

when

$$|{{x}\over{\sigma}}|\geq c$$

- $\phi(x)$ : standard normal density function.
- $\Phi(x)$ : standard normal cumulative density function.
- $c$ :  test statistic cutpoint corresponding to the significance threshold.



The expectation of effect sizes for the selected variants can then be approximated by: 

$$ E(\beta_{Observed}; \beta_{True}) = \beta_{True} + \sigma {{\phi({{{\beta_{True}}\over{\sigma}}-c}) - \phi({{{-\beta_{True}}\over{\sigma}}-c})} \over {\Phi({{{\beta_{True}}\over{\sigma}}-c}) + \Phi({{{-\beta_{True}}\over{\sigma}}-c})}}$$

- $\beta_{Observed}$ is biased. 
- The bias is dependent on $\beta_{True}$, SE $\sigma$, and the selection threshold.


Reference: Zhong, H., & Prentice, R. L. (2008). Bias-reduced estimators and confidence intervals for odds ratios in genome-wide association studies. Biostatistics, 9(4), 621-634.

Also see reference: https://amandaforde.github.io/winnerscurse/articles/winners_curse_methods.html