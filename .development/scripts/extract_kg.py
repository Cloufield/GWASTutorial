#!/usr/bin/env python3
"""Extract module knowledge-graph JSON from README front matter and structure."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore

from _repo_paths import KG_MODULES, REPO_ROOT as ROOT

FRONT_MATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
HEADING_RE = re.compile(r"^(#{2,3})\s+(.+)$", re.MULTILINE)
STEP_COMMENT_RE = re.compile(r"^#\s*Step:\s*(.+)$", re.MULTILINE)

CORE_DIRS = [
    "01_Dataset",
    "03_Data_formats",
    "04_Data_QC",
    "05_PCA",
    "06_Association_tests",
    "07_Annotation",
    "08_LDSC",
    "09_Gene_based_analysis",
    "10_PRS",
    "11_meta_analysis",
    "12_fine_mapping",
    "13_heritability",
    "14_gcta_greml",
    "16_mendelian_randomization",
    "17_colocalization",
    "18_Conditioning_analysis",
    "21_twas",
    "25_singlecell",
    "29_postgwas",
]

EXTRA_SOURCES: list[tuple[str, str]] = [
    ("10_PRS", "PRS_evaluation.md"),
    ("45_functional_interpretation", "SMR.md"),
]


def parse_front_matter(text: str) -> tuple[dict, str]:
    m = FRONT_MATTER_RE.match(text)
    if not m or yaml is None:
        return {}, text
    try:
        meta = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        meta = {}
    body = text[m.end() :]
    return meta, body


def extract_steps(body: str, script_path: Path | None) -> list[dict]:
    steps: list[dict] = []
    for line in body.splitlines():
        hm = HEADING_RE.match(line)
        if hm and hm.group(1) == "###":
            label = hm.group(2).strip()
            sid = re.sub(r"[^a-z0-9]+", "_", label.lower()).strip("_")
            steps.append({"id": f"step_{sid}", "kind": "Step", "label": label, "anchor": sid})
    if script_path and script_path.is_file():
        script = script_path.read_text(encoding="utf-8")
        for m in STEP_COMMENT_RE.finditer(script):
            label = m.group(1).strip()
            if not any(s["label"] == label for s in steps):
                sid = re.sub(r"[^a-z0-9]+", "_", label.lower()).strip("_")
                steps.append(
                    {"id": f"step_{sid}", "kind": "Step", "label": label, "script_step": True}
                )
    return steps


def build_module_graph(
    module_id: str,
    meta: dict,
    body: str,
    source_readme: str,
    base_dir: Path | None = None,
) -> dict:
    primary = meta.get("primary_script")
    script_path = (base_dir / primary) if (base_dir and primary) else None
    title = meta.get("title")
    if not title:
        first_line = body.split("\n", 1)[0]
        title = first_line.lstrip("# ").strip() if first_line.startswith("#") else module_id

    nodes: list[dict] = [{"id": module_id, "kind": "Module", "label": title}]
    edges: list[dict] = []

    for prereq in meta.get("prerequisites") or []:
        edges.append({"from": module_id, "to": prereq, "type": "requires"})

    parent = meta.get("parent")
    if parent:
        edges.append({"from": module_id, "to": parent, "type": "requires"})

    for rel in meta.get("related_modules") or []:
        edges.append({"from": module_id, "to": rel, "type": "related_module"})

    for tool in meta.get("tools") or []:
        nodes.append({"id": f"tool_{tool}", "kind": "Tool", "label": tool})
        edges.append({"from": module_id, "to": f"tool_{tool}", "type": "uses_tool"})

    for artifact in meta.get("produces") or []:
        oid = f"out_{re.sub(r'[^a-z0-9]+', '_', artifact.lower())}"
        nodes.append({"id": oid, "kind": "Output", "label": artifact})
        edges.append({"from": module_id, "to": oid, "type": "produces"})

    for concept in meta.get("concepts") or []:
        cid = f"concept_{re.sub(r'[^a-z0-9]+', '_', concept.lower())}"
        nodes.append({"id": cid, "kind": "Concept", "label": concept})
        edges.append({"from": module_id, "to": cid, "type": "defines_concept"})

    steps = extract_steps(body, script_path)
    prev = module_id
    for step in steps:
        sid = f"{module_id}.{step['id']}"
        nodes.append({"id": sid, "kind": "Step", "label": step["label"]})
        edges.append({"from": prev, "to": sid, "type": "documents_step"})
        prev = sid

    return {
        "module_id": module_id,
        "title": title,
        "type": meta.get("type", "hands_on"),
        "source_readme": source_readme,
        "primary_script": primary,
        "prerequisites": meta.get("prerequisites") or [],
        "produces": meta.get("produces") or [],
        "tools": meta.get("tools") or [],
        "concepts": meta.get("concepts") or [],
        "related_modules": meta.get("related_modules") or [],
        "nodes": nodes,
        "edges": edges,
    }


def process_readme(path: Path, module_id: str | None = None) -> dict:
    text = path.read_text(encoding="utf-8")
    meta, body = parse_front_matter(text)
    mid = meta.get("module_id") or module_id or path.parent.name
    if not meta.get("module_id"):
        meta["module_id"] = mid
    rel = path.relative_to(ROOT).as_posix()
    return build_module_graph(mid, meta, body, rel, path.parent)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--modules", nargs="*", default=CORE_DIRS)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if yaml is None:
        print("PyYAML required: pip install pyyaml", file=sys.stderr)
        return 1

    KG_MODULES.mkdir(parents=True, exist_ok=True)
    for mod in args.modules:
        readme = ROOT / mod / "README.md"
        if not readme.is_file():
            print(f"skip missing {readme}", file=sys.stderr)
            continue
        graph = process_readme(readme, mod)
        out = KG_MODULES / f"{graph['module_id']}.json"
        payload = json.dumps(graph, indent=2, ensure_ascii=False) + "\n"
        if args.dry_run:
            print(f"would write {out}")
        else:
            out.write_text(payload, encoding="utf-8")
            print(f"wrote {out}")

    for subdir, filename in EXTRA_SOURCES:
        path = ROOT / subdir / filename
        if not path.is_file():
            print(f"skip missing {path}", file=sys.stderr)
            continue
        graph = process_readme(path)
        out = KG_MODULES / f"{graph['module_id']}.json"
        payload = json.dumps(graph, indent=2, ensure_ascii=False) + "\n"
        if args.dry_run:
            print(f"would write {out}")
        else:
            out.write_text(payload, encoding="utf-8")
            print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
