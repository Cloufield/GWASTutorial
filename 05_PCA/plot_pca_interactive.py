#!/usr/bin/env python3
"""Build interactive Plotly HTML for the PCA tutorial (docs site).

- pca_illustration.html — synthetic bivariate cloud + PC1/PC2 arrows (matches
  matplotlib reference in README).
- pc1_pc2_eas.html — projected PCs for 1KG EAS (plink_results_projected.sscore
  + 1KG panel); same logic as plot_PCA.ipynb.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
OUT_DIR = REPO / "docs" / "assets" / "plots" / "05_pca"
OUT_ILLUSTRATION = OUT_DIR / "pca_illustration.html"
OUT_EAS = OUT_DIR / "pc1_pc2_eas.html"
SSCORE = HERE / "plink_results_projected.sscore"
PANEL = REPO / "01_Dataset" / "integrated_call_samples_v3.20130502.ALL.panel"


def build_pca_illustration_html() -> None:
    """Synthetic scatter + PC arrows (numpy seed/cov as in tutorial)."""
    np.random.seed(7)
    mean = [0.0, 0.0]
    cov = [[6.5, -3.8], [-3.8, 3.5]]
    pts = np.random.multivariate_normal(mean, cov, size=550)
    x = pts[:, 0]
    y = pts[:, 1]

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode="markers",
            marker=dict(size=5, color="gray", opacity=0.5),
            name="samples",
        )
    )
    # PC1 (red) and PC2 (blue) from origin — same dx, dy as matplotlib reference
    fig.add_annotation(
        x=-7.6,
        y=5.1,
        ax=0,
        ay=0,
        xref="x",
        yref="y",
        axref="x",
        ayref="y",
        showarrow=True,
        arrowhead=2,
        arrowsize=1.2,
        arrowwidth=2.5,
        arrowcolor="red",
        opacity=1,
    )
    fig.add_annotation(
        x=-1.3,
        y=-2.1,
        ax=0,
        ay=0,
        xref="x",
        yref="y",
        axref="x",
        ayref="y",
        showarrow=True,
        arrowhead=2,
        arrowsize=1,
        arrowwidth=2.5,
        arrowcolor="blue",
        opacity=1,
    )
    # PC1 label: offset from arrow tip (-7.6, 5.1) so it does not cover the arrow head
    fig.add_annotation(
        x=-8.35,
        y=5.75,
        text="PC1",
        showarrow=False,
        font=dict(color="red", size=20),
        xanchor="left",
        yanchor="bottom",
    )
    fig.add_annotation(
        x=-0.45,
        y=-2.45,
        text="PC2",
        showarrow=False,
        font=dict(color="blue", size=20),
    )

    fig.update_xaxes(range=[-9.5, 8.5], tickfont=dict(size=11))
    fig.update_yaxes(range=[-7.2, 6.0], tickfont=dict(size=11))
    fig.update_layout(
        title="Illustration: PC1 (red) and PC2 (blue) for synthetic correlated data",
        showlegend=False,
        width=640,
        height=480,
        margin=dict(l=48, r=32, t=72, b=48),
    )

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    fig.write_html(
        OUT_ILLUSTRATION,
        include_plotlyjs="cdn",
        config={"displayModeBar": True, "responsive": True},
        full_html=True,
    )
    print(f"Wrote {OUT_ILLUSTRATION}")


def build_pc1_pc2_eas_html() -> bool:
    if not SSCORE.is_file():
        print(f"Skip EAS scatter: missing {SSCORE.name} in {HERE}")
        return False
    if not PANEL.is_file():
        print(f"Skip EAS scatter: missing panel {PANEL}")
        return False

    pca = pd.read_csv(SSCORE, sep=r"\s+")
    pca = pca.rename(columns={c: c.lstrip("#") for c in pca.columns})

    ped = pd.read_csv(PANEL, sep="\t")
    ped = ped.rename(columns=lambda x: x.strip())

    merged = pca.merge(ped, left_on="IID", right_on="sample", how="inner")
    eas = merged[merged["super_pop"].astype(str) == "EAS"].copy()
    if eas.empty:
        print("Skip EAS scatter: no EAS samples after merge.")
        return False

    fig = px.scatter(
        eas,
        x="PC1_AVG",
        y="PC2_AVG",
        color="pop",
        hover_data=["IID", "FID", "pop", "gender"],
        labels={
            "PC1_AVG": "PC1 (projected)",
            "PC2_AVG": "PC2 (projected)",
            "pop": "Population",
        },
        title="PC1 vs PC2 — 1000 Genomes East Asian samples (EAS)",
    )
    fig.update_traces(marker=dict(size=8, opacity=0.85))
    fig.update_layout(
        height=560,
        width=720,
        margin=dict(t=64, b=48, l=56, r=24),
        legend_title_text="1KG population",
    )

    fig.write_html(
        OUT_EAS,
        include_plotlyjs="cdn",
        config={"displayModeBar": True, "responsive": True},
        full_html=True,
    )
    print(f"Wrote {OUT_EAS}")
    return True


def main() -> None:
    build_pca_illustration_html()
    build_pc1_pc2_eas_html()


if __name__ == "__main__":
    main()
