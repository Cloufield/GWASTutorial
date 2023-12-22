
## Concepts

### Risk

Risk: the probability that a subject within a population will develop a given disease, or other health outcome, over a specified follow-up period.

$$
R = {{E}\over{E + N}}
$$

- E (Event): number of individuals with events
- N (Non-event): number of individuals without events

### Odds 

Odds: the likelihood of a new event occurring rather than not occurring. It is the probability that an event will occur divided by the probability that the event will not occur.

$$
Odds = {E \over N }
$$

### Hazard

Hazard function $h(t)$: the event rate at time $t$ conditional on survival until time $t$ (namely, $T≥t$)

$$
h(t) = Pr(t<=T<t_{+1} | T>=t )
$$

*T* is a discrete random variable indicating the time of occurrence of the event.


## Relative risk (RR) and Odds ratio (OR)
### 2×2 Contingency Table

|  | Intervention I | Control C |
| --- | --- | --- |
| Events E | IE | CE |
| Non-events N | IN | CN |


### Relative risk (RR)
RR: relative risk (risk ratio), usually used in cohort studies.

$$
RR = {{R_{Intervention}}\over{R_{ conrol}}}={{IE/(IE+IN)}\over{CE/(CE+CN)}}
$$

### Odds ratio (OR)
OR: usually used in case control studies.

$$
OR = {{Odds_{Intervention}}\over{Odds_{ conrol}}}={{IE/IN}\over{CE/CN}} = {{IE * CN}\over{CE * IN}}
$$

When the event occurs in less than 10% of the unexposed population, the OR provides a reasonable approximation of the RR.

## Hazard ratios (HR)
Hazard ratios (relative hazard) are usually estimated from Cox proportional hazards model:

$$
h_i(t) = h_0(t) \times e^{\beta_0 + \beta_1X_{i1} + ... + \beta_nX_{in} } = h_0(t) \times e^{X_i\beta }
$$

HR: the ratio of the hazard rates corresponding to the conditions characterised by two distinct levels of a treatment variable of interest.

$$
HR = {{h(t | X_i)}\over{h(t|X_j)}} = {{h_0(t) \times e^{X_i\beta }}\over{h_0(t) \times e^{X_j\beta }}} = e^{(X_i-X_j)\beta}
$$