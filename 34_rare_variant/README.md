

## Rare-variant association tests

- Burden tests : collapse variants into genetic socres
- Adaptive Burden tests : data-adaptive weights
- Variance component tests : test variance of genetic effects
- Combined tests (Omnibus Tests) : combine both burden tests and variance component tests


## Burden test

!!! quote

## SKAT and SKAT-O

!!! quote

## ACTA: aggregated Cauchy association test

$
T_{ACTA} = \sum^k_{i=1}w_itan\{(0.5 - p_i)\pi\} 
$

$
p \approx 1/2 - {arctan(T/w)}/\pi
$

!!! quote
    The most distinctive feature of ACAT is that it only takes the p values (and weights) as input, and the p value of ACAT can be well approximated by a Cauchy distribution. Specifically, neither the linkage disequilibrium (LD) information in a region of the genome nor the correlation structure of set-level test statistics is needed for calculating the p value of ACAT.

    Liu, Y., Chen, S., Li, Z., Morrison, A. C., Boerwinkle, E., & Lin, X. (2019). ACAT: a fast and powerful p value combination method for rare-variant analysis in sequencing studies. The American Journal of Human Genetics, 104(3), 410-421.