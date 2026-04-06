#!/usr/bin/env python3
"""Insert a horizontal rule (---) before each ATX ## / ### heading outside fenced code blocks.

Idempotent: does not add another --- if one already sits above the heading (ignoring blank lines).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

SKIP_DIR_PARTS = frozenset({"site", ".gwasdictionary", "__pycache__", ".git"})


def _is_h2_or_h3(line: str) -> bool:
    # ATX H2/H3 at line start only (not "> ##" etc.)
    if line.startswith("### ") and not line.startswith("####"):
        return True
    if line.startswith("## ") and not line.startswith("###"):
        return True
    return False


def _fence_toggle(line: str) -> bool:
    return line.lstrip().startswith("```")


def transform(content: str) -> str:
    ends_nl = content.endswith("\n")
    lines = content.split("\n")
    out: list[str] = []
    in_fence = False
    for line in lines:
        if _fence_toggle(line):
            in_fence = not in_fence
            out.append(line)
            continue
        if not in_fence and _is_h2_or_h3(line):
            pending: list[str] = []
            while out and out[-1].strip() == "":
                pending.insert(0, out.pop())
            if out and out[-1].strip() == "---":
                out.extend(pending)
                out.append(line)
                continue
            if out:
                out.append("")
            out.append("---")
            out.append("")
            out.extend(pending)
            out.append(line)
        else:
            out.append(line)
    result = "\n".join(out)
    if ends_nl and not result.endswith("\n"):
        result += "\n"
    elif not ends_nl and content and result.endswith("\n"):
        result = result.rstrip("\n")
    return result


def iter_markdown_files(root: Path) -> list[Path]:
    paths: list[Path] = []
    for p in root.rglob("*.md"):
        if any(part in SKIP_DIR_PARTS for part in p.parts):
            continue
        paths.append(p)
    return sorted(paths)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="Repository root",
    )
    ap.add_argument(
        "--check",
        action="store_true",
        help="Exit 1 if any file would change (no writes)",
    )
    args = ap.parse_args()
    root = args.root.resolve()
    changed = 0
    for path in iter_markdown_files(root):
        raw = path.read_text(encoding="utf-8")
        new = transform(raw)
        if new != raw:
            changed += 1
            if args.check:
                print(f"would change: {path.relative_to(root)}", file=sys.stderr)
            else:
                path.write_text(new, encoding="utf-8", newline="\n")
                print(path.relative_to(root))
    if args.check and changed:
        print(f"{changed} file(s) need updates", file=sys.stderr)
        return 1
    if not args.check:
        print(f"Updated {changed} file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
