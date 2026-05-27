"""Repository and .development paths for maintainer tooling."""

from __future__ import annotations

from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
DEV_ROOT = SCRIPTS_DIR.parent
REPO_ROOT = DEV_ROOT.parent
KG_DIR = DEV_ROOT / "kg"
KG_MODULES = KG_DIR / "modules"
