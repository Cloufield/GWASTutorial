#!/usr/bin/env python3
"""
Replace manual `## Table of Contents` bullet lists with:

    **On this page**

    [TOC]

so MkDocs renders a single styled div.toc (see docs/stylesheets/extra.css).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Mirrors deploy.sh (line 3) — chapter README sources copied to docs/*.md
DEPLOY_DIRS = """
00_Introduction 89_programming 38_coordinate_system 37_liftover 36_alleles
28_relatedness 39_overview 29_postgwas 26_normalization 25_singlecell 22_bias
55_measure_of_effect 21_twas 20_power_analysis 17_colocalization
18_Conditioning_analysis 19_ld 76_R_resources 75_R_basics 16_mendelian_randomization
11_meta_analysis 15_winners_curse 71_python_resources 70_python_basics 14_gcta_greml
12_fine_mapping 96_Assignment2 95_Assignment 33_linear_mixed_model
32_whole_genome_regression 34_rare_variant 35_saddlepoint_approximation 98_updatelog
99_About 69_resources 13_heritability 85_job_scheduler 84_ssh 90_Recommended_Reading
01_Dataset 02_Linux_basics 03_Data_formats 04_Data_QC 05_PCA 06_Association_tests
07_Annotation 08_LDSC 09_Gene_based_analysis 10_PRS 40_1000_genome_project 60_awk
61_sed 80_miniconda 81_jupyter_notebook 82_windows_linux_subsystem 83_git_and_github
""".split()

EXTRA_SOURCES = [
    ROOT / "30_phasing" / "Phasing.md",
    ROOT / "31_imputation" / "Imputation.md",
    ROOT / "10_PRS" / "PRS_evaluation.md",
    ROOT / "45_functional_interpretation" / "SMR.md",
    ROOT / "57_chrX" / "README.md",
]

# Not produced from a chapter README in deploy.sh
DOCS_ONLY = [
    ROOT / "docs" / "plot_PCA.md",
    ROOT / "docs" / "finemapping_susie.md",
    ROOT / "docs" / "Visualization.md",
]

BULLET_RE = re.compile(r"^[ \t]*[-*]\s")


def replace_table_of_contents(content: str) -> tuple[str, bool]:
    lines = content.splitlines(keepends=True)
    out: list[str] = []
    i = 0
    changed = False
    while i < len(lines):
        raw = lines[i]
        if raw.rstrip("\r\n") == "## Table of Contents":
            changed = True
            i += 1
            while i < len(lines):
                L = lines[i]
                if not L.strip():
                    i += 1
                    continue
                if BULLET_RE.match(L):
                    i += 1
                    continue
                break
            out.append("**On this page**\n")
            out.append("\n")
            out.append("[TOC]\n")
            out.append("\n")
            continue
        out.append(raw)
        i += 1
    return "".join(out), changed


def collect_paths() -> list[Path]:
    paths: list[Path] = []
    for d in DEPLOY_DIRS:
        p = ROOT / d / "README.md"
        if p.is_file():
            paths.append(p)
    paths.extend(p for p in EXTRA_SOURCES if p.is_file())
    paths.extend(p for p in DOCS_ONLY if p.is_file())
    return paths


def main(argv: list[str]) -> int:
    paths = [Path(p) for p in argv[1:]] if len(argv) > 1 else collect_paths()
    n = 0
    for path in paths:
        if not path.is_file():
            print(f"skip missing {path}", file=sys.stderr)
            continue
        text = path.read_text(encoding="utf-8")
        new_text, did = replace_table_of_contents(text)
        if not did:
            continue
        if new_text != text:
            path.write_text(new_text, encoding="utf-8", newline="\n")
            print(f"updated {path.relative_to(ROOT)}")
            n += 1
    print(f"done, {n} file(s) modified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
