#!/usr/bin/env python3
"""
Fetch and parse GWAS Dictionary raw terms page.

Outputs a JSON file mapping terms to short definitions and term URLs.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin
from urllib.request import urlopen


RAW_TERMS_URL = "https://cloufield.github.io/GWASDictionary/raw-terms/"


@dataclass
class RawTerm:
    term: str
    definition: str
    url: str


class RawTermsTableParser(HTMLParser):
    """Extract rows from the first HTML table on the page."""

    def __init__(self) -> None:
        super().__init__()
        self.in_table = False
        self.in_row = False
        self.in_cell = False
        self.current_cell: list[str] = []
        self.current_row: list[str] = []
        self.rows: list[list[str]] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag == "table" and not self.in_table:
            self.in_table = True
            return
        if not self.in_table:
            return
        if tag == "tr":
            self.in_row = True
            self.current_row = []
            return
        if tag in {"td", "th"} and self.in_row:
            self.in_cell = True
            self.current_cell = []

    def handle_endtag(self, tag: str) -> None:
        if tag == "table" and self.in_table:
            self.in_table = False
            return
        if not self.in_table:
            return
        if tag in {"td", "th"} and self.in_cell:
            cell = " ".join("".join(self.current_cell).split())
            self.current_row.append(cell)
            self.current_cell = []
            self.in_cell = False
            return
        if tag == "tr" and self.in_row:
            if self.current_row:
                self.rows.append(self.current_row)
            self.current_row = []
            self.in_row = False

    def handle_data(self, data: str) -> None:
        if self.in_cell:
            self.current_cell.append(data)


def fetch_html(url: str) -> str:
    with urlopen(url) as resp:
        return resp.read().decode("utf-8")


def _clean_definition(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    # Keep hover text short and readable.
    if len(text) > 280:
        text = text[:277].rstrip() + "..."
    return text


def parse_terms_from_html(html: str, page_url: str) -> list[RawTerm]:
    parser = RawTermsTableParser()
    parser.feed(html)

    out: list[RawTerm] = []
    for row in parser.rows:
        # Expected columns in raw-terms page:
        # [Term, Abbreviation, Definition, Term page URL, ...]
        if len(row) < 4:
            continue

        term = row[0].strip()
        definition = row[2].strip() or row[1].strip()
        rel_url = row[3].strip()
        if not term or term.lower() == "term":
            continue
        if not definition:
            continue

        full_url = urljoin(page_url, rel_url) if rel_url else page_url
        out.append(RawTerm(term=term, definition=_clean_definition(definition), url=full_url))

    # Deduplicate while preserving first occurrence.
    seen: set[str] = set()
    uniq: list[RawTerm] = []
    for item in out:
        key = item.term.lower()
        if key in seen:
            continue
        seen.add(key)
        uniq.append(item)
    return uniq


def to_json_payload(items: list[RawTerm]) -> dict:
    return {
        "source": RAW_TERMS_URL,
        "count": len(items),
        "terms": [
            {
                "term": item.term,
                "definition": item.definition,
                "url": item.url,
            }
            for item in items
        ],
    }


def main() -> None:
    argp = argparse.ArgumentParser(description="Fetch GWAS Dictionary raw terms.")
    argp.add_argument(
        "--url",
        default=RAW_TERMS_URL,
        help=f"Raw terms URL (default: {RAW_TERMS_URL})",
    )
    argp.add_argument(
        "--output",
        default=str(Path(__file__).with_name("gwas_terms.json")),
        help="Output JSON path",
    )
    args = argp.parse_args()

    html = fetch_html(args.url)
    terms = parse_terms_from_html(html, args.url)
    payload = to_json_payload(terms)

    out_path = Path(args.output).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Saved {payload['count']} terms to {out_path}")


if __name__ == "__main__":
    main()
