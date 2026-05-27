# Maintainer tooling (not part of the published tutorial)

This directory holds **development-only** assets. Tutorial readers use numbered module folders (`01_Dataset`, `04_Data_QC`, …) and the built site under `docs/`.

| Path | Purpose |
|------|---------|
| [design/](design/) | Page templates and authoring guidelines |
| [dictionary/](dictionary/) | GWAS Dictionary integration (`expand_key_terms.py`) |
| [kg/](kg/) | Knowledge-graph schema, pipeline map, per-module JSON |
| [link/](link/) | Term hover / raw-terms fetch utilities |
| [scripts/](scripts/) | Lint, crosslink check, KG extract, TOC unification |

From the **repository root**:

```bash
python3 .development/scripts/lint_module.py
python3 .development/scripts/extract_kg.py
python3 .development/dictionary/expand_key_terms.py docs/05_PCA.md
```

`deploy.sh` runs the scripts under `scripts/` automatically before serving the site.
