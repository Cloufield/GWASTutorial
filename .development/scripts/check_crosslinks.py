#!/usr/bin/env python3
"""Verify relative links in Markdown files under docs/ resolve in the repository.

Each docs/*.md file is treated as copied from a source tree (README or topic folder).
Relative links are resolved from that source directory, not from docs/.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import unquote

# docs/<stem>.md -> repo-relative directory containing the source .md (POSIX for display)
_OVERRIDES: dict[str, str] = {
    "index": ".",
    "Imputation": "31_imputation",
    "Phasing": "30_phasing",
    "LiftOver": "37_liftover",
    "basics": "90_Recommended_Reading",
    "PRS_evaluation": "10_PRS",
    "plot_PCA": "05_PCA",
    "Visualization": "06_Association_tests",
    "TwoSampleMR": "16_mendelian_randomization",
    "prs_tutorial": "10_PRS",
    "prs_evaluation": "10_PRS",
    "finemapping_susie": "12_fine_mapping",
}

# Skip images: only check [...](...) where [ is not preceded by !
_LINK_RE = re.compile(r"(?<!!)\[([^\]]*)\]\(([^)]+)\)")


def _link_target(raw: str) -> str:
    s = raw.strip()
    if s.endswith('"') and ' "' in s:
        s = s.rsplit(" ", 1)[0].strip()
    if s.startswith("<") and s.endswith(">"):
        s = s[1:-1]
    s = s.strip()
    if "#" in s:
        s = s.split("#", 1)[0]
    return unquote(s.strip())


def _source_base(repo: Path, stem: str) -> Path:
    if stem in _OVERRIDES:
        return (repo / _OVERRIDES[stem]).resolve()
    d = repo / stem
    if (d / "README.md").is_file():
        return d.resolve()
    return (repo / "docs").resolve()


def _target_exists(repo: Path, resolved: Path) -> bool:
    if resolved.is_file():
        return True
    if resolved.is_dir():
        return True
    # Directory links sometimes omit trailing slash
    if (resolved / "README.md").is_file():
        return True
    return False


def check_docs(repo: Path, docs_dir: Path) -> list[str]:
    errors: list[str] = []
    for md_path in sorted(docs_dir.glob("*.md")):
        stem = md_path.stem
        base = _source_base(repo, stem)
        text = md_path.read_text(encoding="utf-8", errors="replace")
        for m in _LINK_RE.finditer(text):
            raw_url = m.group(2)
            url = _link_target(raw_url)
            if not url or url.startswith("#"):
                continue
            lower = url.lower()
            if lower.startswith(
                ("http://", "https://", "mailto:", "ftp://", "data:", "javascript:")
            ):
                continue
            # Site-root style (rare); nothing to verify on disk
            if url.startswith("/"):
                continue

            joined = (base / url).resolve()
            try:
                joined.relative_to(repo.resolve())
            except ValueError:
                errors.append(f"{md_path.relative_to(repo)}: escapes repo: {raw_url!r}")
                continue
            if not _target_exists(repo, joined):
                errors.append(
                    f"{md_path.relative_to(repo)}: missing {url!r} "
                    f"(from {base.relative_to(repo) if base.is_relative_to(repo) else base})"
                )
    return errors


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--repo",
        type=Path,
        default=None,
        help="Repository root (default: repo root, parent of .development/)",
    )
    p.add_argument(
        "--docs",
        type=Path,
        default=None,
        help="Docs directory (default: <repo>/docs)",
    )
    args = p.parse_args()
    if args.repo is None:
        from _repo_paths import REPO_ROOT

        repo = REPO_ROOT
    else:
        repo = args.repo.resolve()
    docs_dir = (args.docs or repo / "docs").resolve()
    if not docs_dir.is_dir():
        print(f"error: docs directory not found: {docs_dir}", file=sys.stderr)
        return 2
    errors = check_docs(repo, docs_dir)
    if errors:
        for line in errors:
            print(line, file=sys.stderr)
        print(f"\n{len(errors)} broken link(s)", file=sys.stderr)
        return 1
    print("Cross-link check: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
