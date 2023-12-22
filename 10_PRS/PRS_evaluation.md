# Polygenic risk scores evaluation

## Regressions for evaluation of PRS

$$Phenotype \sim PRS_{phenotype} + Covariates$$

$$logit(P) \sim PRS_{phenotype} + Covariates$$

Covariates usually include sex, age and top 10 PCs.

## Evaluation

### ROC, AIC, AUC, and C-index

!!! info "ROC"
    ROC: **receiver operating characteristic curve** shows the performance of a classification model at all thresholds.

    - y axis: True Positive rate. ${{TP}\over{TP + FN}}$
    - x axis: False Positive rate. ${{FP}\over{FP + TN}}$

!!! info "AUC"
    AUC: area under the ROC Curve, a common measure for the performance of a classification model.

!!! info "AIC"
    Akaike Information Criterion (AIC): a measure for comparison of different statistical models.

    $$AIC = 2k - 2ln(\hat{L})$$

    - $k$ : number of estimated parameters
    - $\hat{L}$ : maximum value of the model likelihood function


!!! info  "C-index"
    **C-index**: Harrell’s C-index (concordance index), which is a metric to evaluate the predictive performance of models and is commonly used in survival analysis. It is a measure of the probability that the predicted scores $M_i$ and $M_j$ by a model of two randomly selected individuals $i$ and $j$, have the reverse relative order as their true event times $T_i, T_j$.

    $$ C = Pr (M_j > M_i | T_j < T_i) $$

    Interpretation: Individuals with higher scores should have higher risks of the disease events
    
    - Reference: Harrell, F. E., Califf, R. M., Pryor, D. B., Lee, K. L., & Rosati, R. A. (1982). Evaluating the yield of medical tests. Jama, 247(18), 2543-2546.

    - Reference: Longato, E., Vettoretti, M., & Di Camillo, B. (2020). A practical perspective on the concordance index for the evaluation and selection of prognostic time-to-event models. Journal of Biomedical Informatics, 108, 103496.

### R2 and pseudo-R2

!!! info "Coefficient of determination"
    $R^2$ : coefficient of determination, which measures the amount of variance explained by the regression model.
    
    In linear regression:

    $$ R^2 = 1 - {{RSS}\over{TSS}} $$

    - $RSS$ : sum of squares of residuals
    - $TSS$ : total sum of squares

!!! info "Pseudo-R2 (Nagelkerke)" 

    In logistic regression, 

    One of the most commonly used Pseudo-R2 for PRS analysis is Nagelkerke's $R^2$

    $$R^2_{Nagelkerke} = {{1 - ({{L_0}\over{L_M}})^{2/n}}\over{1 - L_0^{2/n}}}$$

    - $L_0$ : Likelihood of the null model
    - $L_{full}$ : Likelihood of the full model

### R2 on the liability scale (Lee)

!!! info "R2 on liability scale"

    $R^2$ on the liability scale for ascertained case-control studies
    
    $$ R^2_l = {{R_o^2 C}\over{1 + R_o^2 \theta C }} $$

    - $C$ and $\theta$ are correcting factors for ascertainment
    - $C = {{K(1-K)}\over{Z^2}}{{K(1-K)}\over{P(1-P)}}$ 
    - $\theta = m {{P-K}\over{1-K}} ( m{{P-K}\over{1-K}} - t)$  

    - $K$ : population disease prevalence
    - $P$ : sample disease prevalence
    - $t$: the threshold on the normal distribution truncating the proportion of disease prevalence K
    - $m = z / K$ : mean liability for cases
    - $z = f(t)$ : the value of probability density function of standard normal distribution at t 
    
    Reference : Lee, S. H., Goddard, M. E., Wray, N. R., & Visscher, P. M. (2012). A better coefficient of determination for genetic profile analysis. Genetic epidemiology, 36(3), 214-224.

    The authors also provided R codes for calculation (removed unrelated codes for simplicity)
    
    ```R
    # R2 on the liability scale using the transformation

    nt = total number of the sample
    ncase = number of cases
    ncont = number of controls
    thd = the threshold on the normal distribution which truncates the proportion of disease prevalence
    K = population prevalence
    P = proportion of cases in the case-control samples

    #threshold
    thd = -qnorm(K,0,1)
    
    #value of standard normal density function at thd
    zv = dnorm(thd) 

    #mean liability for case
    mv = zv/K 
    
    #linear model
    lmv = lm(y∼g) 
    
    #R20 : R2 on the observed scale
    R2O = var(lmv$fitted.values)/(ncase/nt*ncont/nt)

    # calculate correction factors
    theta = mv*(P-K)/(1-K)*(mv*(P-K)/(1-K)-thd) 
    cv = K*(1-K)/zv^2*K*(1-K)/(P*(1-P)) 
    
    # convert to R2 on the liability scale
    R2 = R2O*cv/(1+R2O*theta*cv)
    ```

## Bootstrap Confidence Interval Methods for R2

Bootstrap is a commonly used resampling method to generate a sampling distribution from the known sample dataset. It repeatedly takes random samples with replacement from the known sample dataset.

Steps:

- Sample with replacement B times. (B should be large.)
- Estimate the parameter using the bootstrap sample. 
- Obtain the approximate distribution of the parameter.

The percentile bootstrap interval is then defined as the interval between $100 \times \alpha /2$ and $100 \times (1 - \alpha /2)$ percentiles of the parameters estimated by bootstrapping. We can use this method to estimate the  bootstrap interval for $R^2$.

## Reference

- **R2 on liability scale**: Lee, S. H., Goddard, M. E., Wray, N. R., & Visscher, P. M. (2012). A better coefficient of determination for genetic profile analysis. Genetic epidemiology, 36(3), 214-224.
- **C-index 1**: Harrell, F. E., Califf, R. M., Pryor, D. B., Lee, K. L., & Rosati, R. A. (1982). Evaluating the yield of medical tests. Jama, 247(18), 2543-2546.
- **C-index 2**: Longato, E., Vettoretti, M., & Di Camillo, B. (2020). A practical perspective on the concordance index for the evaluation and selection of prognostic time-to-event models. Journal of Biomedical Informatics, 108, 103496.
