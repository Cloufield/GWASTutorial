#!/usr/bin/env python3
"""
Educational reference: inverse-variance weighted (IVW) fixed-effect meta-analysis,
Cochran's Q / I², and DerSimonian–Laird (DL) random-effects meta-analysis.

Same structure as METAL's IVW step and the tau² formulation used in GWAMA
(random effects with between-study variance added to each study variance).

Requires: numpy, scipy
  pip install numpy scipy
"""

from __future__ import annotations

import numpy as np
from scipy.stats import chi2, norm


def fixed_effect_meta(beta: np.ndarray, se: np.ndarray) -> dict:
    """IVW fixed-effect pooled estimate (one SNP, k studies)."""
    beta = np.asarray(beta, dtype=float)
    se = np.asarray(se, dtype=float)
    v = se**2
    w = 1.0 / v
    sum_w = w.sum()
    beta_fe = (w * beta).sum() / sum_w
    var_fe = 1.0 / sum_w
    se_fe = np.sqrt(var_fe)
    z = beta_fe / se_fe
    p = 2.0 * norm.sf(abs(z))
    return {
        "beta_fe": beta_fe,
        "se_fe": se_fe,
        "var_fe": var_fe,
        "z": z,
        "p": p,
        "w": w,
        "sum_w": sum_w,
    }


def cochran_q(beta: np.ndarray, se: np.ndarray, beta_fe: float, w: np.ndarray) -> dict:
    """Cochran's Q and I² using fixed-effect weights (heterogeneity)."""
    beta = np.asarray(beta, dtype=float)
    k = beta.size
    df = k - 1
    q = (w * (beta - beta_fe) ** 2).sum()
    # I² is often reported as 0 when Q <= df
    i2 = max(0.0, (q - df) / q * 100.0) if q > 0 else 0.0
    p_het = chi2.sf(q, df) if df > 0 else float("nan")
    return {"Q": q, "df": df, "I2_percent": i2, "p_het": p_het}


def dersimonian_laird_tau2(q: float, df: int, w: np.ndarray) -> float:
    """
    DL estimator of between-study variance tau² (non-negative).

    tau² = max(0, (Q - df) / C) with C = sum(w) - sum(w²)/sum(w).
    """
    if df <= 0:
        return 0.0
    sum_w = w.sum()
    c = sum_w - (w**2).sum() / sum_w
    if c <= 0:
        return 0.0
    return max(0.0, (q - df) / c)


def random_effect_meta(beta: np.ndarray, se: np.ndarray, tau2: float) -> dict:
    """IVW random-effects pooled estimate with study-specific variance v_i + tau²."""
    beta = np.asarray(beta, dtype=float)
    se = np.asarray(se, dtype=float)
    v = se**2 + tau2
    w_star = 1.0 / v
    sum_ws = w_star.sum()
    beta_re = (w_star * beta).sum() / sum_ws
    var_re = 1.0 / sum_ws
    se_re = np.sqrt(var_re)
    z = beta_re / se_re
    p = 2.0 * norm.sf(abs(z))
    return {
        "beta_re": beta_re,
        "se_re": se_re,
        "var_re": var_re,
        "tau2": tau2,
        "z": z,
        "p": p,
        "w_star": w_star,
    }


def meta_one_variant(beta: np.ndarray, se: np.ndarray) -> dict:
    """Run fixed effect, heterogeneity, DL tau², and random effect for one variant."""
    fe = fixed_effect_meta(beta, se)
    het = cochran_q(beta, se, fe["beta_fe"], fe["w"])
    tau2 = dersimonian_laird_tau2(het["Q"], het["df"], fe["w"])
    re = random_effect_meta(beta, se, tau2)
    return {"fixed": fe, "heterogeneity": het, "random": re}


def main() -> None:
    # Toy example: three studies, same effect allele, harmonized betas and SEs
    beta = np.array([0.08, 0.12, 0.05])
    se = np.array([0.04, 0.05, 0.035])

    print("Per-study betas:", beta)
    print("Per-study SEs:  ", se)
    print()

    out = meta_one_variant(beta, se)
    fe = out["fixed"]
    het = out["heterogeneity"]
    re = out["random"]

    print("--- Fixed-effect (IVW) ---")
    print(f"  w_i = 1 / SE_i^2  ->  {fe['w']}")
    print(f"  beta_FE = sum(w*beta) / sum(w) = {fe['beta_fe']:.6f}")
    print(f"  SE_FE   = 1 / sqrt(sum(w))     = {fe['se_fe']:.6f}")
    print(f"  Z = beta_FE / SE_FE             = {fe['z']:.4f}")
    print(f"  two-sided P                     = {fe['p']:.4g}")
    print()

    print("--- Heterogeneity (Cochran Q, using FE weights) ---")
    print(f"  Q = sum(w * (beta - beta_FE)^2) = {het['Q']:.6f}")
    print(f"  df = k - 1                      = {het['df']}")
    print(f"  I^2 = max(0, (Q-df)/Q)*100      = {het['I2_percent']:.2f}%")
    print(f"  P(Q) ~ chi^2(df)                = {het['p_het']:.4g}")
    print()

    print("--- Random effects (DL tau^2, then IVW with v_i + tau^2) ---")
    print(f"  tau^2_DL                        = {re['tau2']:.6f}")
    print(f"  w*_i = 1 / (tau^2 + SE_i^2)     ->  {re['w_star']}")
    print(f"  beta_RE = sum(w*beta)/sum(w*)   = {re['beta_re']:.6f}")
    print(f"  SE_RE   = 1 / sqrt(sum(w*))     = {re['se_re']:.6f}")
    print(f"  Z = beta_RE / SE_RE             = {re['z']:.4f}")
    print(f"  two-sided P                     = {re['p']:.4g}")
    print()
    print("Note: if tau^2 = 0, RE weights match FE up to rounding; RE SE is >= FE SE when tau^2 > 0.")

    print()
    print("=" * 60)
    print("Second toy example (more spread across betas -> tau^2 > 0)")
    beta2 = np.array([0.02, 0.15, 0.20])
    se2 = np.array([0.04, 0.05, 0.05])
    out2 = meta_one_variant(beta2, se2)
    fe2, het2, re2 = out2["fixed"], out2["heterogeneity"], out2["random"]
    print(f"  beta_FE={fe2['beta_fe']:.4f}, SE_FE={fe2['se_fe']:.4f}")
    print(f"  Q={het2['Q']:.4f}, I^2={het2['I2_percent']:.1f}%")
    print(f"  tau^2={re2['tau2']:.6f}")
    print(f"  beta_RE={re2['beta_re']:.4f}, SE_RE={re2['se_re']:.4f}  (typically wider SE than FE when tau^2>0)")


if __name__ == "__main__":
    main()
