"""
Build fast lookup indexes from GWAS Dictionary slug -> entry rows.

Matching order for a user token (see resolve_term):
1. Slug (lowercase hyphenated token)
2. Abbreviation (exact, case-insensitive)
3. Full term title (exact, case-insensitive)
4. Title with trailing parenthetical stripped
5. Substring: dictionary term title contains the token (prefer longest title)
"""

from __future__ import annotations

import re
from typing import Any

from gwas_dictionary_fetch import SITE_BASE, term_url


def build_indexes(by_slug: dict[str, dict[str, Any]]) -> dict[str, Any]:
    by_title_lower: dict[str, dict] = {}
    by_abbrev_lower: dict[str, dict] = {}
    entries: list[dict] = []

    for slug, row in by_slug.items():
        e = {**row, "slug": slug, "url": term_url(row["path"], SITE_BASE)}
        entries.append(e)
        tt = (row.get("term_title") or "").strip()
        if tt:
            by_title_lower[tt.lower()] = e
        ab = (row.get("abbreviation") or "").strip()
        if ab and len(ab) <= 64:
            key = ab.lower()
            if key not in by_abbrev_lower:
                by_abbrev_lower[key] = e

    return {
        "by_slug": by_slug,
        "by_title_lower": by_title_lower,
        "by_abbrev_lower": by_abbrev_lower,
        "entries": entries,
    }


def resolve_term(raw: str, ix: dict[str, Any]) -> dict | None:
    """Return enriched entry dict with slug, url, or None."""
    t = raw.strip().strip("`\"'")
    if not t:
        return None

    by_slug: dict = ix["by_slug"]
    by_title_lower: dict = ix["by_title_lower"]
    by_abbrev_lower: dict = ix["by_abbrev_lower"]
    entries: list = ix["entries"]

    tl = t.lower()

    # 1) Slug-like token
    if re.fullmatch(r"[a-z0-9][a-z0-9-]*", tl):
        row = by_slug.get(tl)
        if row:
            slug = tl
            return {**row, "slug": slug, "url": term_url(row["path"], SITE_BASE)}

    # 2) Abbreviation
    e = by_abbrev_lower.get(tl)
    if e:
        return e

    # 3) Full title
    e = by_title_lower.get(tl)
    if e:
        return e

    # 4) Strip parenthetical e.g. "Linkage disequilibrium (LD)"
    tl_noparen = re.sub(r"\s*\([^)]*\)\s*$", "", tl).strip()
    if tl_noparen and tl_noparen != tl:
        e = by_title_lower.get(tl_noparen)
        if e:
            return e
        inner = re.search(r"\(([^)]+)\)\s*$", t)
        if inner:
            ab = inner.group(1).strip().lower()
            e = by_abbrev_lower.get(ab)
            if e:
                return e

    # 5) Longest dictionary title that contains the token (min length avoids noisy hits)
    best = None
    best_len = -1
    for e in entries:
        title = (e.get("term_title") or "").lower()
        if not title:
            continue
        if tl == title or (len(tl) >= 4 and tl in title):
            if len(title) > best_len:
                best_len = len(title)
                best = e
    return best


def normalize_definition(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").replace("\n", " ")).strip()
