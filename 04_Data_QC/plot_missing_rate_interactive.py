#!/usr/bin/env python3
"""Build interactive Plotly HTML for the Data QC tutorial (docs site).

Writes under docs/assets/plots/04_data_qc/:
  - missing_rate_distributions.html — from plink_results.imiss / .lmiss
  - f_het_distribution.html — from plink_results.het
  - ld_r2_first10_heatmap.html — pairwise r² for first 10 SNPs by position from plink_results.ld

SNP missingness uses pre-binned counts so the HTML stays small.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

HERE = Path(__file__).resolve().parent
OUT_DIR = HERE.parent / "docs" / "assets" / "plots" / "04_data_qc"
OUT_MISSING = OUT_DIR / "missing_rate_distributions.html"
OUT_HET = OUT_DIR / "f_het_distribution.html"
OUT_LD = OUT_DIR / "ld_r2_first10_heatmap.html"
IMISS = HERE / "plink_results.imiss"
LMISS = HERE / "plink_results.lmiss"
HET = HERE / "plink_results.het"
LD = HERE / "plink_results.ld"

# Fewer bins => wider bins on the x-axis (sample + SNP missing rate both use this)
NBINS_MISSING = 12
NBINS_HET = 24

# Tutorial uses ±0.1 as a convenient F threshold (see README)
F_HET_THRESHOLD = 0.1

# LD heatmap: SNPs ordered by genomic position (chr, bp)
N_LD_SNPS_HEATMAP = 10


def build_missing_rate_html() -> bool:
    if not IMISS.is_file() or not LMISS.is_file():
        print(f"Skip missing-rate plot: need {IMISS.name} and {LMISS.name} in {HERE}")
        return False

    imiss = pd.read_csv(IMISS, sep=r"\s+")
    lmiss = pd.read_csv(LMISS, sep=r"\s+")
    s = imiss["F_MISS"].astype(float).to_numpy()
    l = lmiss["F_MISS"].astype(float).to_numpy()

    counts_l, edges_l = np.histogram(l, bins=NBINS_MISSING)
    centers_l = (edges_l[:-1] + edges_l[1:]) / 2
    width_l = float(edges_l[1] - edges_l[0])

    fig = make_subplots(
        rows=2,
        cols=1,
        subplot_titles=(
            "Sample missing rate (F_MISS from .imiss)",
            "SNP missing rate (F_MISS from .lmiss)",
        ),
        vertical_spacing=0.11,
    )
    fig.add_trace(
        go.Histogram(
            x=s,
            nbinsx=min(NBINS_MISSING, max(8, len(np.unique(s)))),
        ),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Bar(
            x=centers_l,
            y=counts_l,
            width=width_l * 0.92,
            marker_line_width=0,
        ),
        row=2,
        col=1,
    )
    fig.update_layout(
        height=720,
        showlegend=False,
        title_text="Distribution of sample and SNP missing rates",
        margin=dict(t=88, b=48),
    )
    fig.update_xaxes(title_text="Missing rate", row=1, col=1)
    fig.update_xaxes(title_text="Missing rate", row=2, col=1)
    fig.update_yaxes(title_text="Number of samples", row=1, col=1)
    fig.update_yaxes(title_text="Number of SNPs", row=2, col=1)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    fig.write_html(
        OUT_MISSING,
        include_plotlyjs="cdn",
        config={"displayModeBar": True, "responsive": True},
        full_html=True,
    )
    print(f"Wrote {OUT_MISSING}")
    return True


def build_het_html() -> bool:
    if not HET.is_file():
        print(f"Skip F_het plot: need {HET.name} in {HERE}")
        return False

    het = pd.read_csv(HET, sep=r"\s+")
    f_vals = het["F"].astype(float).to_numpy()

    fig = go.Figure()
    fig.add_trace(
        go.Histogram(
            x=f_vals,
            nbinsx=min(NBINS_HET, max(8, len(np.unique(f_vals)))),
        )
    )
    fig.add_vline(
        x=F_HET_THRESHOLD,
        line_dash="dash",
        line_color="firebrick",
        annotation_text=f"+{F_HET_THRESHOLD}",
        annotation_position="top",
    )
    fig.add_vline(
        x=-F_HET_THRESHOLD,
        line_dash="dash",
        line_color="firebrick",
        annotation_text=f"-{F_HET_THRESHOLD}",
        annotation_position="top",
    )
    fig.update_layout(
        title_text="Distribution of F (heterozygosity, from plink --het)",
        xaxis_title="F",
        yaxis_title="Number of samples",
        bargap=0.05,
        margin=dict(t=72, b=48),
        height=520,
        showlegend=False,
    )

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    fig.write_html(
        OUT_HET,
        include_plotlyjs="cdn",
        config={"displayModeBar": True, "responsive": True},
        full_html=True,
    )
    print(f"Wrote {OUT_HET}")
    return True


def build_ld_r2_heatmap_html() -> bool:
    if not LD.is_file():
        print(f"Skip LD r² heatmap: need {LD.name} in {HERE}")
        return False

    ld_df = pd.read_csv(LD, sep=r"\s+")
    if ld_df.empty:
        print("Skip LD r² heatmap: empty .ld file")
        return False

    snp_pos: dict[str, tuple[int, int]] = {}
    for _, r in ld_df.iterrows():
        a, b = str(r["SNP_A"]), str(r["SNP_B"])
        if a not in snp_pos:
            snp_pos[a] = (int(r["CHR_A"]), int(r["BP_A"]))
        if b not in snp_pos:
            snp_pos[b] = (int(r["CHR_B"]), int(r["BP_B"]))

    ordered = sorted(snp_pos.keys(), key=lambda s: snp_pos[s])
    labels = ordered[:N_LD_SNPS_HEATMAP]
    if len(labels) < 2:
        print("Skip LD r² heatmap: fewer than 2 SNPs in .ld")
        return False

    n = len(labels)
    idx = {s: i for i, s in enumerate(labels)}
    z = np.full((n, n), np.nan, dtype=float)
    np.fill_diagonal(z, 1.0)

    for _, r in ld_df.iterrows():
        a, b = str(r["SNP_A"]), str(r["SNP_B"])
        if a in idx and b in idx:
            i, j = idx[a], idx[b]
            v = float(r["R2"])
            z[i, j] = v
            z[j, i] = v

    # Axis labels: chr:bp (compact)
    tick = [f"{snp_pos[s][0]}:{snp_pos[s][1]}" for s in labels]

    text = []
    for i in range(n):
        row = []
        for j in range(n):
            v = z[i, j]
            if np.isnan(v):
                row.append("")
            else:
                row.append(f"{v:.3f}")
        text.append(row)

    hover = []
    for i in range(n):
        row = []
        for j in range(n):
            v = z[i, j]
            if np.isnan(v) and i != j:
                h = f"{labels[i]}<br>vs<br>{labels[j]}<br>r²: (not in .ld)"
            elif np.isnan(v):
                h = f"{labels[i]}"
            else:
                h = f"{labels[i]}<br>vs<br>{labels[j]}<br>r²: {v:.4f}"
            row.append(h)
        hover.append(row)

    fig = go.Figure(
        data=go.Heatmap(
            z=z,
            x=tick,
            y=tick,
            text=text,
            texttemplate="%{text}",
            textfont={"size": 10},
            hoverinfo="text",
            hovertext=hover,
            colorscale="Reds",
            zmin=0.0,
            zmax=1.0,
            colorbar={"title": "r²"},
        )
    )
    fig.update_layout(
        title_text=(
            f"Pairwise LD (r²), {n} SNPs with smallest positions in plink_results.ld"
        ),
        xaxis_title="SNP (chr:bp)",
        yaxis_title="SNP (chr:bp)",
        yaxis={"autorange": "reversed"},
        width=640,
        height=640,
        margin=dict(l=100, r=40, t=72, b=100),
    )

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    fig.write_html(
        OUT_LD,
        include_plotlyjs="cdn",
        config={"displayModeBar": True, "responsive": True},
        full_html=True,
    )
    print(f"Wrote {OUT_LD}")
    return True


def main() -> None:
    wrote_missing = build_missing_rate_html()
    wrote_het = build_het_html()
    wrote_ld = build_ld_r2_heatmap_html()
    if not wrote_missing and not wrote_het and not wrote_ld:
        raise SystemExit(
            f"No PLINK outputs found in {HERE}. "
            "Run plink --missing, plink --het, and/or plink --r2, then re-run this script."
        )


if __name__ == "__main__":
    main()
