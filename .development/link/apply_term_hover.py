#!/usr/bin/env python3
"""
Annotate markdown files with term hover tooltips.

This script reads GWAS terms from .development/link/gwas_terms.json and wraps matched terms
in markdown with an HTML span containing tooltip metadata:
  <span class="gwas-term" data-tooltip="..." data-url="...">Term</span>
"""

from __future__ import annotations

import argparse
import html
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


DEFAULT_TERMS_FILE = Path(__file__).with_name("gwas_terms.json")
FETCH_SCRIPT = Path(__file__).with_name("fetch_raw_terms.py")


@dataclass
class TermEntry:
    term: str
    definition: str
    url: str


def load_terms(path: Path, min_len: int = 3) -> list[TermEntry]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    raw_terms = payload.get("terms", [])
    out: list[TermEntry] = []
    for item in raw_terms:
        term = str(item.get("term", "")).strip()
        definition = str(item.get("definition", "")).strip()
        url = str(item.get("url", "")).strip()
        if len(term) < min_len or not definition:
            continue
        out.append(TermEntry(term=term, definition=definition, url=url))
    # Replace longer terms first to avoid partial overlaps.
    out.sort(key=lambda x: len(x.term), reverse=True)
    return out


def build_term_patterns(terms: list[TermEntry]) -> list[tuple[re.Pattern[str], TermEntry]]:
    patterns: list[tuple[re.Pattern[str], TermEntry]] = []
    for item in terms:
        escaped = re.escape(item.term)
        # Token-ish boundaries around term.
        pattern = re.compile(rf"(?<![\w/])({escaped})(?![\w-])")
        patterns.append((pattern, item))
    return patterns


def _wrap_match(text: str, patterns: list[tuple[re.Pattern[str], TermEntry]]) -> str:
    for pattern, item in patterns:
        tooltip = html.escape(item.definition, quote=True)
        source_url = html.escape(item.url, quote=True)

        def repl(match: re.Match[str]) -> str:
            term_text = match.group(1)
            return (
                f'<span class="gwas-term" data-tooltip="{tooltip}" '
                f'data-url="{source_url}">{term_text}</span>'
            )

        text = pattern.sub(repl, text)
    return text


def annotate_markdown(md: str, patterns: list[tuple[re.Pattern[str], TermEntry]]) -> str:
    # Remove old native-title attributes to avoid double tooltip popups.
    md = re.sub(
        r'(<span class="gwas-term"[^>]*?)\s+title="[^"]*"([^>]*>)',
        r"\1\2",
        md,
    )

    # Protect fenced code blocks.
    fence_re = re.compile(r"```.*?```", re.DOTALL)
    fences: list[str] = []

    def stash_fence(match: re.Match[str]) -> str:
        fences.append(match.group(0))
        return f"__GWAS_FENCE_{len(fences)-1}__"

    work = fence_re.sub(stash_fence, md)

    # Protect inline code.
    inline_code_re = re.compile(r"`[^`]*`")
    inlines: list[str] = []

    def stash_inline(match: re.Match[str]) -> str:
        inlines.append(match.group(0))
        return f"__GWAS_INLINE_{len(inlines)-1}__"

    work = inline_code_re.sub(stash_inline, work)

    # Protect markdown links.
    link_re = re.compile(r"\[[^\]]+\]\([^)]+\)")
    links: list[str] = []

    def stash_link(match: re.Match[str]) -> str:
        links.append(match.group(0))
        return f"__GWAS_LINK_{len(links)-1}__"

    work = link_re.sub(stash_link, work)

    # Skip previously wrapped terms.
    span_re = re.compile(r"<span class=\"gwas-term\"[^>]*>.*?</span>")
    spans: list[str] = []

    def stash_span(match: re.Match[str]) -> str:
        spans.append(match.group(0))
        return f"__GWAS_SPAN_{len(spans)-1}__"

    work = span_re.sub(stash_span, work)

    # Apply replacements on remaining text.
    work = _wrap_match(work, patterns)

    # Restore placeholders.
    for i, value in enumerate(spans):
        work = work.replace(f"__GWAS_SPAN_{i}__", value)
    for i, value in enumerate(links):
        work = work.replace(f"__GWAS_LINK_{i}__", value)
    for i, value in enumerate(inlines):
        work = work.replace(f"__GWAS_INLINE_{i}__", value)
    for i, value in enumerate(fences):
        work = work.replace(f"__GWAS_FENCE_{i}__", value)

    return work


def iter_markdown_files(docs_dir: Path) -> list[Path]:
    return sorted(p for p in docs_dir.glob("*.md") if p.is_file())


def ensure_terms_file(terms_file: Path, fetch: bool) -> None:
    if terms_file.exists() and terms_file.stat().st_size > 0 and not fetch:
        return
    cmd = [sys.executable, str(FETCH_SCRIPT), "--output", str(terms_file)]
    subprocess.run(cmd, check=True)


def main() -> None:
    argp = argparse.ArgumentParser(description="Apply GWAS term hover tooltips to markdown docs.")
    argp.add_argument("--docs-dir", default="docs", help="Docs directory containing .md files")
    argp.add_argument("--terms-file", default=str(DEFAULT_TERMS_FILE), help="Terms JSON file")
    argp.add_argument("--fetch", action="store_true", help="Refresh terms from remote page first")
    argp.add_argument("--dry-run", action="store_true", help="Print planned changes only")
    args = argp.parse_args()

    docs_dir = Path(args.docs_dir).resolve()
    terms_file = Path(args.terms_file).resolve()
    ensure_terms_file(terms_file, fetch=args.fetch)

    terms = load_terms(terms_file)
    patterns = build_term_patterns(terms)
    files = iter_markdown_files(docs_dir)

    changed = 0
    for path in files:
        original = path.read_text(encoding="utf-8")
        updated = annotate_markdown(original, patterns)
        if updated != original:
            changed += 1
            if args.dry_run:
                print(f"Would update: {path}")
            else:
                path.write_text(updated, encoding="utf-8")
                print(f"Updated: {path}")

    if args.dry_run:
        print(f"Files that would change: {changed}")
    else:
        print(f"Files updated: {changed}")


if __name__ == "__main__":
    main()
