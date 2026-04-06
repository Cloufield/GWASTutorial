# GWAS Dictionary tooling

Automate **`## Key terms`** sections in tutorial Markdown using definitions and URLs from the [GWAS Dictionary](https://cloufield.github.io/GWASDictionary/) [raw terms](https://cloufield.github.io/GWASDictionary/raw-terms/) table.

## Workflow

1. In `docs/*.md` (the actual MkDocs build inputs), add a section:

   ```markdown
   ## Key terms

   GWAS, SNP, linkage disequilibrium, polygenic risk score
   ```

   Use **comma- or newline-separated** keywords (titles, abbreviations, or slugs such as `gwas`). Matching is case-insensitive.

2. From the **repository root**, refresh the dictionary cache and expand all `docs/*.md` Markdown files:

   ```bash
   python3 .gwasdictionary/expand_key_terms.py
   ```

   Or target specific files:

   ```bash
   python3 .gwasdictionary/expand_key_terms.py docs/00_Introduction.md
   ```

3. The script **rewrites in place** each `## Key terms` body (until the next `##` heading) into bullets:

   `- **[Term title](https://cloufield.github.io/GWASDictionary/terms/.../)** — definition`

### Options

| Flag | Meaning |
|------|--------|
| `--offline` | Use `.gwasdictionary/cache/gwas_dictionary_by_slug.json` only (no network). |
| `--dry-run` | Print which files would change; do not write. |
| `--refresh` | If the section is **already** a bullet list with dictionary links, re-fetch definitions from the URL slugs and rewrite bullets. |
| `--repo-root PATH` | Default: parent of `.gwasdictionary/`. |
| `--aliases-yaml` / `--aliases-json` | Optional maps from keyword → slug (see `term_aliases.example.yaml`). |

**Idempotency:** If the first non-empty line under `## Key terms` already starts with `- ` (expanded list), the file is **skipped** unless you pass `--refresh` or replace the section with keywords again.

### Unmatched keywords

If a token does not resolve to a dictionary row, the script still emits a bullet, prints a **stderr** warning, and suggests `term_aliases.yaml`. Add a file `.gwasdictionary/term_aliases.yaml` (see `term_aliases.example.yaml`):

```yaml
aliases:
  "C+T": prs-clumping-and-thresholding
```

Requires **PyYAML** only if you use YAML aliases (`pip install pyyaml`). JSON aliases are supported via `term_aliases.json` with `{"aliases": {...}}`.

## Files

| Path | Role |
|------|------|
| `gwas_dictionary_fetch.py` | Fetches raw-terms page, parses **HTML** (live site) or legacy Markdown tables, writes `cache/gwas_dictionary_by_slug.json`. |
| `dictionary_indexes.py` | Builds lookup indexes (slug, title, abbreviation, substring). |
| `expand_key_terms.py` | Scans Markdown, expands `## Key terms`. Default file list is `docs/**/*.md`. |
| `term_aliases.example.yaml` | Optional template for keyword aliasing when your text does not directly match a dictionary title/abbr/slug. |
| `cache/gwas_dictionary_by_slug.json` | Generated cache (safe to regenerate; not required in git if you always run online). |
