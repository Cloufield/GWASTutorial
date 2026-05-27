#!/usr/bin/env python3
"""Lint tutorial modules for unified structure and front matter."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

from _repo_paths import REPO_ROOT as ROOT

HANDS_ON_FULL = [
    "04_Data_QC",
    "05_PCA",
    "06_Association_tests",
    "07_Annotation",
    "08_LDSC",
    "09_Gene_based_analysis",
    "10_PRS",
    "11_meta_analysis",
    "12_fine_mapping",
    "14_gcta_greml",
    "16_mendelian_randomization",
]

RESOURCE = ["01_Dataset"]
CONCEPT = ["03_Data_formats", "13_heritability", "25_singlecell"]
HUB = ["29_postgwas"]
HANDS_ON_LITE = ["17_colocalization", "18_Conditioning_analysis", "21_twas"]
SECONDARY = [
    ROOT / "10_PRS" / "PRS_evaluation.md",
    ROOT / "45_functional_interpretation" / "SMR.md",
]

REQUIRED_HEADINGS = ["## Key terms", "## References"]
HANDS_ON_FULL_EXTRA = [
    "[TOC]",
    '!!! note "Required data and tools"',
    "## Preparation",
    "## Sample script",
]
HANDS_ON_LITE_EXTRA = [
    "[TOC]",
    '!!! note "Required data and tools"',
    "## Preparation",
]
FORBIDDEN_FRAGMENTS = ["## File Preparation", "## Sample codes", "## Table of Contents"]
H1_REFERENCES = re.compile(r"^# References\s*$", re.MULTILINE)
MANUAL_TOC_BULLET = re.compile(r"^- \[[^\]]+\]\(#")
FRONT_MATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def parse_meta(text: str) -> dict:
    if yaml is None:
        return {}
    m = FRONT_MATTER_RE.match(text)
    if not m:
        return {}
    try:
        return yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        return {}


def lint_readme(path: Path, *, mode: str) -> list[str]:
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    meta = parse_meta(text)

    if not text.startswith("---\n"):
        errors.append("missing YAML front matter")
    if "**On this page**" not in text:
        errors.append("missing **On this page**")
    for bad in FORBIDDEN_FRAGMENTS:
        if bad in text:
            errors.append(f"forbidden fragment: {bad!r}")
    if H1_REFERENCES.search(text):
        errors.append("use ## References (not h1 # References)")
    if MANUAL_TOC_BULLET.search(text):
        errors.append("manual bullet TOC (use [TOC] only)")

    if mode in ("hands_on_full", "resource"):
        for heading in REQUIRED_HEADINGS:
            if heading not in text:
                errors.append(f"missing {heading}")
        if "## Sample script" not in text:
            errors.append("missing ## Sample script")
        m = re.search(r"primary_script:\s*(\S+)", text)
        if not m:
            errors.append("missing YAML primary_script")
        else:
            script = path.parent / m.group(1)
            if not script.is_file():
                errors.append(f"primary_script not found: {script}")
            elif m.group(1) not in text:
                errors.append(f"README does not mention {m.group(1)!r}")

    if mode == "hands_on_full":
        for req in HANDS_ON_FULL_EXTRA:
            if req not in text:
                errors.append(f"missing {req!r}")

    if mode == "hands_on_lite":
        for heading in REQUIRED_HEADINGS:
            if heading not in text:
                errors.append(f"missing {heading}")
        for req in HANDS_ON_LITE_EXTRA:
            if req not in text:
                errors.append(f"missing {req!r}")

    if mode in ("concept", "hub", "secondary"):
        for heading in REQUIRED_HEADINGS:
            if heading not in text:
                errors.append(f"missing {heading}")

    if mode == "hub" and meta.get("type") != "hub":
        errors.append("expected type: hub in front matter")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    args = parser.parse_args()
    failed = False

    checks: list[tuple[str, Path, str]] = []
    for mod in HANDS_ON_FULL:
        checks.append((mod, ROOT / mod / "README.md", "hands_on_full"))
    for mod in HANDS_ON_LITE:
        checks.append((mod, ROOT / mod / "README.md", "hands_on_lite"))
    for mod in HUB:
        checks.append((mod, ROOT / mod / "README.md", "hub"))
    for mod in CONCEPT + RESOURCE:
        mode = "resource" if mod in RESOURCE else "concept"
        checks.append((mod, ROOT / mod / "README.md", mode))
    for path in SECONDARY:
        checks.append((path.stem, path, "secondary"))

    for label, path, mode in checks:
        if not path.is_file():
            print(f"SKIP {label}: no file")
            continue
        errs = lint_readme(path, mode=mode)
        if errs:
            failed = True
            print(f"FAIL {label}:")
            for e in errs:
                print(f"  - {e}")
        else:
            print(f"OK   {label}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
