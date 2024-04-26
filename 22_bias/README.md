
# Bias

In statistics, bias of an estimator refers to the **systematic** and **nonrandom** error in the parameter estimation.

The bias of statistic $T$ with respect to $\theta$
$$
bias(T, \theta) = E(T) - \theta
$$

- $T$: statistic used to estimate a parameter $\theta$
- $E(T)$: expected value of $T$

## Three major groups of bias

- confounding
- measurement/information bias
- selection bias

## Confounding

Confounding occurs when an exposure and outcome have a shared cause.

Two of the common confounding factors in genome-wide association testing are population structure and cryptic relateness.



## Measurement/information bias

Measurement/information bias refers to the errors occured during measuring exposure or outcome.

## Selection bias

Selection bias occurs when the study participants were selected in a biased approach so that they are not representative of the original target study population.

### Collider bias

In the context of evaluating the causal association of an exposure with an outcome, collider bias occurs when the exposure and outcome both affect a common third variable, and that common variable is controlled for in the study.
(in other words, controlling a variable that are affected by both exposure and outcome could lead to collider bias)



## Reference

- Holmberg, M. J., & Andersen, L. W. (2022). Collider bias. Jama, 327(13), 1282-1283.
- Schoeler, T., Speed, D., Porcu, E., Pirastu, N., Pingault, J. B., & Kutalik, Z. (2023). Participation bias in the UK Biobank distorts genetic associations and downstream analyses. Nature Human Behaviour, 7(7), 1216-1227.
- Griffith, G. J., Morris, T. T., Tudball, M. J., Herbert, A., Mancano, G., Pike, L., ... & Hemani, G. (2020). Collider bias undermines our understanding of COVID-19 disease risk and severity. Nature communications, 11(1), 5749.