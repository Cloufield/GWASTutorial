#!/usr/bin/env python3
"""
Expand ## Key terms sections: comma/newline-separated keywords -> linked term list.

1) Load term definitions and URLs from GWAS Dictionary (fetch or cache).
2) Scan Markdown files (default: docs/*.md used to build site).
3) Rewrite in place: each keyword becomes a bullet with link (definition kept in link title).

Section detection: heading ## Key terms (case-insensitive). Body runs until the next ## heading or EOF.

Idempotency: if the first non-empty line in the body already looks like a markdown list item ('- '),
the file is skipped unless --refresh (refresh definitions from existing link URLs) or you replace
the section with keywords again.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# Same directory imports (run as python3 .gwasdictionary/expand_key_terms.py from repo root)
_ROOT = Path(__file__).resolve().parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from dictionary_indexes import build_indexes, normalize_definition, resolve_term  # noqa: E402
from gwas_dictionary_fetch import load_dictionary  # noqa: E402

SECTION_RE = re.compile(
    r"^(##\s+Key\s+terms\s*)\n(.*?)(?=^##\s+|\Z)",
    re.MULTILINE | re.DOTALL | re.IGNORECASE,
)

BULLET_LINK_RE = re.compile(
    r'^-\s+(?:\*\*)?\[([^\]]+)\]\(([^)\s]+)(?:\s+"([^"]*)")?\)(?:\*\*)?.*$'
)

DEFAULT_ALIASES_YAML = _ROOT / "term_aliases.yaml"
DEFAULT_ALIASES_JSON = _ROOT / "term_aliases.json"


def load_aliases(path_yaml: Path | None, path_json: Path | None) -> dict[str, str]:
    """Lowercase token -> dictionary slug."""
    out: dict[str, str] = {}
    for p in (path_yaml, path_json):
        if p is None or not p.is_file():
            continue
        try:
            if p.suffix.lower() in (".yaml", ".yml"):
                import yaml  # type: ignore

                data = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
            else:
                data = json.loads(p.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"Warning: could not load aliases {p}: {e}", file=sys.stderr)
            continue
        aliases = data.get("aliases") if isinstance(data, dict) else None
        if not isinstance(aliases, dict):
            continue
        for k, v in aliases.items():
            if k is not None and v is not None:
                out[str(k).strip().lower()] = str(v).strip().lower()
    return out


def docs_markdown_targets(repo_root: Path) -> list[Path]:
    """Return markdown files under docs/ (actual MkDocs build inputs)."""
    docs_dir = repo_root / "docs"
    if not docs_dir.is_dir():
        return []
    return sorted(p for p in docs_dir.rglob("*.md") if p.is_file())


def looks_expanded(body: str) -> bool:
    for line in body.splitlines():
        s = line.strip()
        if s:
            return s.startswith("- ")
    return False


def parse_keyword_tokens(body: str) -> list[str]:
    raw = body.strip()
    if not raw:
        return []
    parts = re.split(r"[\n,]+", raw)
    return [p.strip() for p in parts if p.strip()]


def slug_from_dictionary_url(url: str) -> str | None:
    # .../GWASDictionary/terms/x/slug/ or .../terms/x/slug
    m = re.search(r"/terms/[^/]+/([^/#?]+)/?", url)
    if m:
        return m.group(1).rstrip("/")
    return None


def format_bullet(entry: dict) -> str:
    title = (entry.get("term_title") or entry.get("slug") or "term").strip()
    url = entry.get("url") or ""
    defin = normalize_definition(entry.get("definition") or "")
    defin = defin.replace('"', '\\"')
    return f'- **[{title}]({url} "{defin}")**'


def expand_body_from_keywords(
    body: str,
    ix: dict,
    aliases: dict[str, str],
    by_slug: dict,
) -> tuple[str, list[str]]:
    warnings: list[str] = []
    tokens = parse_keyword_tokens(body)
    lines: list[str] = []
    for tok in tokens:
        tl = tok.lower()
        slug = aliases.get(tl)
        entry = None
        if slug:
            row = by_slug.get(slug)
            if row:
                from gwas_dictionary_fetch import SITE_BASE, term_url

                entry = {**row, "slug": slug, "url": term_url(row["path"], SITE_BASE)}
            else:
                warnings.append(f"alias {tok!r} -> slug {slug!r} not in dictionary")
        if entry is None:
            entry = resolve_term(tok, ix)
        if entry is None:
            warnings.append(f"no dictionary match for {tok!r}")
            lines.append(f"- **{tok}**")
        else:
            lines.append(format_bullet(entry))
    # Trailing blank line keeps the next ## heading separated in Markdown
    return "\n".join(lines) + ("\n\n" if lines else ""), warnings


def refresh_expanded_body(body: str, by_slug: dict) -> tuple[str, list[str]]:
    from gwas_dictionary_fetch import SITE_BASE, term_url

    warnings: list[str] = []
    out_lines: list[str] = []
    for line in body.splitlines():
        s = line.strip()
        if not s:
            out_lines.append(line)
            continue
        m = BULLET_LINK_RE.match(s)
        if not m:
            out_lines.append(line)
            continue
        _label, url, _old_def = m.group(1), m.group(2), m.group(3)
        slug = slug_from_dictionary_url(url)
        if not slug:
            warnings.append(f"could not parse slug from URL {url!r}")
            out_lines.append(line)
            continue
        row = by_slug.get(slug)
        if not row:
            warnings.append(f"slug {slug!r} not in dictionary cache")
            out_lines.append(line)
            continue
        entry = {**row, "slug": slug, "url": term_url(row["path"], SITE_BASE)}
        out_lines.append(format_bullet(entry))
    new_body = "\n".join(out_lines)
    if body.endswith("\n") and not new_body.endswith("\n"):
        new_body += "\n"
    return new_body, warnings


def process_file(
    path: Path,
    *,
    by_slug: dict,
    ix: dict,
    aliases: dict[str, str],
    dry_run: bool,
    refresh: bool,
) -> int:
    text = path.read_text(encoding="utf-8")
    m = SECTION_RE.search(text)
    if not m:
        return 0
    heading = m.group(1)
    body = m.group(2)
    if refresh and looks_expanded(body):
        new_body, warns = refresh_expanded_body(body, by_slug)
    elif looks_expanded(body):
        print(f"skip (already list): {path}", file=sys.stderr)
        return 0
    else:
        new_body, warns = expand_body_from_keywords(body, ix, aliases, by_slug)
    for w in warns:
        print(f"{path}: {w}", file=sys.stderr)
    new_section = heading + "\n" + new_body
    new_text = text[: m.start()] + new_section + text[m.end() :]
    if new_text != text:
        if not dry_run:
            path.write_text(new_text, encoding="utf-8")
        print(f"{'[dry-run] ' if dry_run else ''}updated: {path}")
        return 1
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Expand ## Key terms from GWAS Dictionary.")
    ap.add_argument(
        "paths",
        nargs="*",
        type=Path,
        help="Markdown files (default: docs/*.md when omitted)",
    )
    ap.add_argument(
        "--repo-root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="Repository root (default: parent of .gwasdictionary/)",
    )
    ap.add_argument("--offline", action="store_true", help="Use cache only (no network).")
    ap.add_argument("--dry-run", action="store_true", help="Print actions without writing files.")
    ap.add_argument(
        "--refresh",
        action="store_true",
        help="Refresh definitions in existing bullet lines (parses URLs for slugs).",
    )
    ap.add_argument(
        "--aliases-yaml",
        type=Path,
        default=None,
        help=f"YAML aliases file (default: {DEFAULT_ALIASES_YAML})",
    )
    ap.add_argument(
        "--aliases-json",
        type=Path,
        default=None,
        help=f"JSON aliases file (default: {DEFAULT_ALIASES_JSON} if present)",
    )
    args = ap.parse_args()
    repo_root = args.repo_root.resolve()

    aliases_yaml = args.aliases_yaml if args.aliases_yaml is not None else DEFAULT_ALIASES_YAML
    aliases_json = args.aliases_json if args.aliases_json is not None else DEFAULT_ALIASES_JSON
    aliases = load_aliases(aliases_yaml, aliases_json)

    by_slug = load_dictionary(offline=args.offline)
    ix = build_indexes(by_slug)

    if args.paths:
        files = [p.resolve() for p in args.paths]
    else:
        files = docs_markdown_targets(repo_root)

    n = 0
    for f in files:
        if not f.is_file():
            print(f"skip (missing): {f}", file=sys.stderr)
            continue
        n += process_file(
            f,
            by_slug=by_slug,
            ix=ix,
            aliases=aliases,
            dry_run=args.dry_run,
            refresh=args.refresh,
        )
    print(f"Done. Updated {n} file(s).", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
