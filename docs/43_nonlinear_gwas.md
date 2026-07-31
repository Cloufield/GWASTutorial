---
module_id: 43_nonlinear_gwas
type: concept
title: Nonlinear models in GWAS
prerequisites: [06_Association_tests, 33_linear_mixed_model]
concepts:
  - nonlinear genetic effects
  - set-based association test
  - kernel association test
  - genetic interaction
  - gene-environment interaction
  - variance component
---

# Nonlinear models in GWAS

Nonlinear genetic effects include **gene-gene interaction (GxG)** and **gene-environment interaction (GxE)**. Their joint extension, GxGxE, asks whether a gene-gene interaction itself changes across an environment. This page begins with the GxG problem because it makes the statistical challenge visible, then introduces a set-based alternative. 

---

**On this page**

[TOC]

---

Building on the [linear mixed model (LMM)](https://cloufield.github.io/GWASTutorial/33_linear_mixed_model/) framework, we write a single tested variant $j$ as

$$
\mathbf{y} = \mathbf{C}\boldsymbol{\alpha} + \mathbf{g}_j\beta_j + u + \boldsymbol{\epsilon},
$$

where $y$ is the phenotype vector, $C$ contains measured covariates, $g_j$ is the dosage vector for variant $j$, $u$ models background relatedness, and $\epsilon$ is residual noise.

## Epistasis

In a statistical GWAS model, **epistasis** means that the joint effect of two variants is not fully described by adding their separate effects. For two dosage vectors $g_i$ and $g_j$, a pairwise interaction model is

$$
\mathbf{y} = \mathbf{C}\boldsymbol{\alpha} + \mathbf{g}_i\beta_i + \mathbf{g}_j\beta_j + (\mathbf{g}_i \odot \mathbf{g}_j)\beta_{ij} + \boldsymbol{\epsilon}.
$$

Here $\beta_{ij}$ measures the interaction on the chosen phenotype scale after covariate adjustment. Check the [LMM section](https://cloufield.github.io/GWASTutorial/33_linear_mixed_model/) if you are not familiar with the expression.

### Beyond one pair

A flexible model can include higher-order and nonlinear terms, for example

$$
\mathbf{y} = \mathbf{C}\boldsymbol{\alpha} + \mathbf{g}_i\beta_i + \mathbf{g}_j\beta_j + \sum_{a=1}^{P}\sum_{b=1}^{P}\theta_{ab}\left(\mathbf{g}_i^{\circ a} \odot \mathbf{g}_j^{\circ b}\right) + \boldsymbol{\epsilon}.
$$

In practice, this flexibility must be balanced against the amount of data available to estimate it.

### Why a genome-wide interaction scan is difficult

Suppose genotype matrix $G$ contains $M$ variants measured in $n$ individuals. Testing every pair requires an interaction design matrix $Z_{\mathrm{GxG}}$ with one column for each product $g_i g_j$ ($i<j$):

$$
\mathbf{y} = \mathbf{C}\boldsymbol{\alpha} + \mathbf{G}\boldsymbol{\beta} + \mathbf{Z}_{\mathrm{GxG}}\boldsymbol{\gamma} + \boldsymbol{\epsilon},
\qquad
Z_{\mathrm{GxG}} \in \mathbb{R}^{n \times \binom{M}{2}}.
$$

For $M=1{,}000{,}000$ variants, this produces roughly $5\times10^{11}$ pairwise columns before considering higher-order terms. The resulting computation, multiple-testing burden, and correlation among interaction features make exhaustive estimation poorly powered and often poorly identified. In 254,679 unrelated UK Biobank participants, [Hivert *et al.* (2021)](https://doi.org/10.1016/j.ajhg.2021.02.014) found no statistically significant estimate of epistatic variance across 70 traits.

Researchers therefore need to choose their angle when studying epistasis, much like blindfolded people touching different parts of one elephant. 

![Illustration of complementary views of epistasis: blindfolded people touch different parts of an elephant.](/GWASTutorial/images/epistasis_concept.png)

*Figure. Different statistical tests can each capture a useful part of an epistatic signal. Interpreting a result requires keeping the method's question and resolution in view.*



### Set-based epistasis testing

One strategy is to ask whether epistatic signal is present within a predefined, confined set of variants—for example, a gene or a genomic window. The [rare-variant association tests](https://cloufield.github.io/GWASTutorial/34_rare_variant/) section introduces the linear set model used by SKAT:

!!! info "SKAT model"
    For a region with $k$ variants, SKAT assumes:
    
    $$y_i = \alpha + \sum_{j=1}^{k} G_{ij} \beta_j + \epsilon_i$$
    
    where $\beta_j \sim N(0, w_j^2 \tau)$ are random effects with variance $\tau$. The null hypothesis is $H_0: \tau = 0$ (no association).
    
    The SKAT test statistic is:
    
    $$Q = (y - \hat{\mu})' K (y - \hat{\mu})$$
    
    where $K = GWG'$ is a kernel matrix, $G$ is the genotype matrix, and $W = diag(w_1^2, ..., w_k^2)$ contains variant weights.

This linear kernel aggregates additive effects across the set. The following kernels extend the same set-based idea to different kinds of non-additivity.

#### Quadratic kernel: pairwise epistasis within a set

[QuadKAST](https://genome.cshlp.org/content/34/9/1294) focuses on pairwise interaction effects—also called quadratic effects—within small to medium-sized variant sets. Conceptually, it replaces a separate test for every pair with a kernel built from their products:

$$
\mathbf{K}_{\mathrm{quad}} = \mathbf{Z}_{\mathrm{quad}}\mathbf{Z}_{\mathrm{quad}}^{\mathsf T},
\qquad
\mathbf{Z}_{\mathrm{quad}} = \left[\mathbf{g}_a \odot \mathbf{g}_b\right]_{a \leq b,\; a,b\in S}.
$$

The set-level test targets aggregate quadratic signal after additive effects are handled; follow-up is still required to localize the contributing pairs.

!!! quote "Quadratic-kernel reference"
    - Fu, B., Anand, P., Anand, A., Mefford, J., & Sankararaman, S. (2024). [A scalable adaptive quadratic kernel method for interpretable epistasis analysis in complex traits](https://doi.org/10.1101/gr.279140.124). *Genome Research*, 34(9), 1294–1303. QuadKAST.

#### Shift-invariant RKHS kernels: broader nonlinearity

[FastKAST](https://github.com/sriramlab/FastKAST) extends set testing beyond quadratic effects by using shift-invariant reproducing-kernel Hilbert space (RKHS) kernels. For example, the radial basis function (RBF) kernel compares two individuals' genotype vectors $\mathbf{z}_i$ and $\mathbf{z}_j$ in the set as

$$
k(\mathbf{z}_i, \mathbf{z}_j) = \exp\left(-\gamma\frac{\lVert\mathbf{z}_i - \mathbf{z}_j\rVert^2}{2}\right).
$$

This admits a broader class of smooth nonlinear relationships than the quadratic kernel. FastKAST uses a randomized feature approximation so these set tests can scale to biobank-sized quantitative-trait analyses.

!!! quote "Shift-invariant-kernel reference"
    - Fu, B., Pazokitoroudi, A., Sudarshan, M., Liu, Z., Subramanian, L., & Sankararaman, S. (2023). [Fast kernel-based association testing of non-linear genetic effects for biobank-scale data](https://doi.org/10.1038/s41467-023-40346-2). *Nature Communications*, 14, 4936. FastKAST.

!!! warning "Nonlinear does not mean automatically epistatic"
    A significant nonlinear set test establishes a departure from the fitted additive model under its chosen kernel and adjustment strategy. It does not, on its own, identify a particular interacting SNP pair or prove a biological mechanism. A future GxG submodule can distinguish pairwise, marginal, and set-level claims explicitly.

### Marginal epistasis

One complementary perspective anchors a target variant $t$ and asks whether its effect is modified, in aggregate, by the genetic background. It does not require knowing which other variants interact with the target. A pairwise marginal epistasis model is

$$
\mathbf{y}
= \mathbf{C}\boldsymbol{\alpha} + \mathbf{g}_t\beta_t + \mathbf{G}_{-t}\boldsymbol{\beta}_{-t}
+ \left(\mathbf{g}_t \odot \mathbf{G}_{-t}\right)\boldsymbol{\gamma}_t
+ \boldsymbol{\epsilon}.
$$

Here $\mathbf{G}_{-t}$ contains all variants other than $t$, $\mathbf{g}_t \odot \mathbf{G}_{-t}$ denotes row-wise multiplication of the target dosage vector by that matrix, and $\boldsymbol{\gamma}_t$ contains the target's interaction effects. MAPIT and FAME test whether these interaction effects have nonzero aggregate variance rather than estimating every element separately.

!!! quote "Marginal-epistasis references"
    - Crawford, L., Zeng, P., Mukherjee, S., & Zhou, X. (2017). [Detecting epistasis with the marginal epistasis test in genetic mapping studies of quantitative traits](https://doi.org/10.1371/journal.pgen.1006869). *PLOS Genetics*, 13, e1006869. MAPIT.
    - Fu, B. *et al.* (2025). [A biobank-scale test of marginal epistasis reveals genome-wide signals of polygenic interaction effects](https://doi.org/10.1038/s41588-025-02411-y). *Nature Genetics*, 57, 3175–3184. FAME.



## Module map and scope

| Child module | Primary unit tested | Main question | Status |
|---|---|---|---|
| GxG: Gene-Gene Interaction | SNP pair, focal SNP, or variant set | Do genetic effects depend on genetic background? | Planned; no page or implementation yet |
| GxE: Gene-Environment Interaction | Variant, set, and measured exposure | Does a genetic effect vary across an environment or exposure? | Planned; no page or implementation yet |

The planned GxG submodule can use three complementary levels of inference:

1. **Pairwise interaction:** tests a specified product $g_j g_k$ and can identify a pair, but genome-wide scans have a large multiple-testing and computation burden.
2. **Marginal epistasis:** asks whether a focal variant interacts with the remaining genetic background in aggregate. MAPIT established this perspective; FAME makes a biobank-scale version practical.
3. **Set-based nonlinearity:** tests whether a defined locus, window, or gene has a nonlinear aggregate contribution. FastKAST is the first method planned for this branch.

!!! tip "What belongs in a child module"
    Each child should state its unit of analysis, model and null hypothesis, covariate and additive-effect adjustment, genomic-set definition, multiple-testing family, output fields, and the strongest justified interpretation. This shared structure will make GxG and future GxE pages comparable without forcing them into the same method.

## Design and interpretation checks

- **Match the model to the trait.** The first FastKAST paper targets quantitative traits; do not imply that its calibration or implementation transfers unchanged to binary, survival, family-based, or multi-ancestry analyses.
- **Preserve the study design.** Population structure, relatedness, batch effects, phenotype transformations, and genotype QC remain issues after moving beyond a linear test.
- **Separate discovery from explanation.** A kernel signal prioritizes a set for follow-up. Pairwise localization, functional evidence, and replication answer different questions.
- **Define the testing family in advance.** Correct over the number of tested sets and traits, and state whether the analysis is a discovery scan or a targeted test.

## Extension template for future submodules

Use this short specification before adding a GxG or GxE method:

1. **Question and unit:** What is tested: a pair, focal variant, region, gene, pathway, exposure, or genotype-exposure pair?
2. **Model:** Which terms are fixed effects, random effects, and kernel/interaction effects? State the dimensions and meaning of each new symbol.
3. **Null and alternative:** Which coefficient or variance component is zero under $H_0$?
4. **Adjustment:** Which covariates, additive genetic effects, relatedness terms, and local LD controls are included?
5. **Inference:** What statistic, calibration procedure, and multiple-testing family are used?
6. **Output and interpretation:** What does a significant result identify, and what does it not identify?
7. **Practical tutorial:** Only after the preceding items are fixed, add installation, data preparation, a reproducible script, and expected outputs.

## Key terms

Nonlinear genetic effect, set-based association test, kernel, kernel matrix, variance component, random feature approximation, genetic interaction, epistasis, marginal epistasis, gene-environment interaction (GxE), genetic relationship matrix (GRM), FastKAST

## References

- Crawford, L. *et al.* [Detecting epistasis with the marginal epistasis test in genetic mapping studies of quantitative traits](https://doi.org/10.1371/journal.pgen.1006869). *PLOS Genetics* 13, e1006869 (2017). MAPIT.
- Hivert, V. *et al.* [Estimation of non-additive genetic variance in human complex traits from a large sample of unrelated individuals](https://doi.org/10.1016/j.ajhg.2021.02.014). *The American Journal of Human Genetics* 108, 786–798 (2021).
- Fu, B., Anand, P., Anand, A., Mefford, J., & Sankararaman, S. [A scalable adaptive quadratic kernel method for interpretable epistasis analysis in complex traits](https://doi.org/10.1101/gr.279140.124). *Genome Research* 34, 1294–1303 (2024). QuadKAST.
- Fu, B. *et al.* [Fast kernel-based association testing of non-linear genetic effects for biobank-scale data](https://doi.org/10.1038/s41467-023-40346-2). *Nature Communications* 14, 4936 (2023). FastKAST.
- Fu, B. *et al.* [A biobank-scale test of marginal epistasis reveals genome-wide signals of polygenic interaction effects](https://doi.org/10.1038/s41588-025-02411-y). *Nature Genetics* 57, 3175–3184 (2025). FAME.
