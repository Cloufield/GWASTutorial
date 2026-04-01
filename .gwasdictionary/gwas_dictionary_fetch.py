"""
Fetch and parse the GWAS Dictionary "Raw Terms" page.

Source: https://cloufield.github.io/GWASDictionary/raw-terms/

The live site (Zensical) serves **HTML** with a 4-column table:
  Term | Abbreviation | Definition | /terms/<letter>/<slug>/

Some rows leave Abbreviation empty; older snapshots used Markdown pipe tables with 3 or 4 columns.
The last column is always the term page path; the slug is the final path segment.
"""

from __future__ import annotations

import html as html_module
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

RAW_TERMS_URL = "https://cloufield.github.io/GWASDictionary/raw-terms/"
SITE_BASE = "https://cloufield.github.io/GWASDictionary"

DEFAULT_CACHE = Path(__file__).resolve().parent / "cache" / "gwas_dictionary_by_slug.json"


def _row_cells(line: str) -> list[str]:
    parts = line.split("|")
    cells = [p.strip() for p in parts[1:-1]] if len(parts) >= 2 else []
    return [c for c in cells if c != ""]


def parse_raw_terms_markdown(text: str) -> dict[str, dict]:
    """Return mapping slug -> {term_title, abbreviation, definition, path}."""
    by_slug: dict[str, dict] = {}
    for raw in text.splitlines():
        line = raw.strip()
        if not line.startswith("|"):
            continue
        cells = _row_cells(line)
        if len(cells) < 3:
            continue
        if cells[0] in ("Term", "---") or cells[0].startswith("---"):
            continue
        last = cells[-1]
        if not last.startswith("/terms/"):
            continue

        path = last.split()[0] if last else ""
        slug = path.rstrip("/").split("/")[-1]
        if not slug:
            continue

        if len(cells) == 3:
            term_title, definition, _path = cells
            abbreviation = None
        elif len(cells) == 4:
            term_title, abbreviation, definition, _path = cells
        else:
            # Unexpected column count: treat all middle cells as definition
            term_title = cells[0]
            abbreviation = None
            definition = " ".join(cells[1:-1])
            _path = cells[-1]

        by_slug[slug] = {
            "term_title": term_title,
            "abbreviation": abbreviation,
            "definition": definition,
            "path": path,
        }
    return by_slug


def _strip_html_tags(s: str) -> str:
    return re.sub(r"<[^>]+>", "", s)


def parse_raw_terms_html(text: str) -> dict[str, dict]:
    """Parse the Zensical HTML table on raw-terms (four <td> cells per row)."""
    by_slug: dict[str, dict] = {}
    for block in text.split("<tr"):
        if "<td" not in block.lower():
            continue
        cells = re.findall(r"<td[^>]*>(.*?)</td>", block, flags=re.DOTALL | re.IGNORECASE)
        if len(cells) < 4:
            continue
        term_title = html_module.unescape(_strip_html_tags(cells[0])).strip()
        abbreviation = html_module.unescape(_strip_html_tags(cells[1])).strip() or None
        definition = html_module.unescape(_strip_html_tags(cells[2])).strip()
        last = html_module.unescape(_strip_html_tags(cells[3])).strip()
        if term_title in ("Term", "---", "") or last.startswith("---"):
            continue
        if not last.startswith("/terms/"):
            continue
        path = last.split()[0]
        slug = path.rstrip("/").split("/")[-1]
        if not slug:
            continue
        by_slug[slug] = {
            "term_title": term_title,
            "abbreviation": abbreviation,
            "definition": definition,
            "path": path,
        }
    return by_slug


def parse_raw_terms(text: str) -> dict[str, dict]:
    """Auto-detect HTML (live site) vs Markdown pipe table."""
    head = text.lstrip()[:8000]
    if re.search(r"<!doctype\s+html", head, re.I) or re.search(r"<html[\s>]", head, re.I):
        return parse_raw_terms_html(text)
    return parse_raw_terms_markdown(text)


def fetch_raw_terms_text(url: str = RAW_TERMS_URL, timeout: int = 60) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "GWASTutorial-dictionary-sync/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")


def load_dictionary(
    *,
    offline: bool = False,
    cache_path: Path | None = None,
    url: str = RAW_TERMS_URL,
) -> dict[str, dict]:
    """
    Load term index by slug. If offline, read cache only.
    Otherwise fetch URL and refresh cache file.
    """
    cache_path = cache_path or DEFAULT_CACHE
    if offline:
        if not cache_path.is_file():
            raise FileNotFoundError(
                f"Offline mode but no cache at {cache_path}. Run build without --offline once."
            )
        data = json.loads(cache_path.read_text(encoding="utf-8"))
        return data.get("by_slug", data)

    try:
        text = fetch_raw_terms_text(url)
    except (urllib.error.URLError, OSError) as e:
        if cache_path.is_file():
            print(f"Warning: could not fetch {url} ({e}); using cache {cache_path}", file=sys.stderr)
            data = json.loads(cache_path.read_text(encoding="utf-8"))
            return data.get("by_slug", data)
        raise

    by_slug = parse_raw_terms(text)
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "source_url": url,
        "site_base": SITE_BASE,
        "term_count": len(by_slug),
        "by_slug": by_slug,
    }
    cache_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return by_slug


def term_url(path: str, site_base: str = SITE_BASE) -> str:
    p = path if path.startswith("/") else "/" + path
    return site_base.rstrip("/") + p
