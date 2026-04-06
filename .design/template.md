# Tutorial page template (GWASTutorial)

This summarizes **recurring structure** across `README.md` modules, standalone `.md` files (e.g. `30_phasing/Phasing.md`), and `docs/*.md` copies. It is a **starting point**, not a strict requirement. For tone and depth, see [guideline-hands-on.md](guideline-hands-on.md) and [guideline-concept-pages.md](guideline-concept-pages.md).

---

## 0. Canonical heading labels

Use these **exact spellings and casing** for shared sections so pages and TOCs stay consistent (MkDocs anchors are usually lowercase with hyphens; duplicate titles get `_1`, `_2`, …).

| Use this | Do not use |
|----------|------------|
| `**On this page**` then `[TOC]` on the next line (MkDocs auto-TOC) | `## Table of Contents` with hand-maintained bullet lists, `Table of contents` alone |
| `## Key terms` | `Key Terms`, `Keywords` (as a section title; see [guideline-keywords.md](guideline-keywords.md) for dictionary “Keywords” prose) |
| `## References` | `Reference`, `Bibliography` (unless you intentionally mean something else) |
| `## Further reading` | — (optional; use for non-citation links if you split from **References**) |
| `## Additional resources` | `Additional Resources` (same meaning as extra links / docs) |
| `## Data preparation` | `Data Preparation`, trailing spaces on the heading line |
| `## Preparation` | — (hands-on setup: install, paths, downloads—broader than data-only prep) |
| `## Prerequisites` | — (reserve for short “before you start” pages, e.g. environment assumptions) |
| `## Overview` | — (high-level summary section when the word fits; keep page-specific titles like “Overview of …” when needed) |
| `## Exercise` | `Exercises` unless there are multiple called out |
| `## Summary` | — (optional closing recap; do not use as a synonym for **Key terms**) |

**Admonition titles** (not headings, but normalize casing): prefer `!!! note "Required data and tools"` for the standard checklist callout on hands-on pages.

---

## 1. Common skeleton (most pages)

Use this order when it fits; reorder or omit sections as needed.

```markdown
# Short, task- or topic-focused title

One or two paragraphs: what this page covers, who it is for, and (for tools) credit / link to upstream software.

Optional: short bullet list of key facts (populations, build, file types).

---

**On this page**

[TOC]

---

## First major section

Body text, figures, or callouts.

### Subsection

More detail, commands, or examples.

## Key terms

Comma-separated or bulleted list of vocabulary.

## References

Numbered or bulleted citations with DOI / URL.
```

**Notes**

- **`---` rules**: Many pages use horizontal rules before the TOC or between major blocks (e.g. overview vs. linked chapters). Optional.
- **TOC**: Long pages use **`On this page`** + **`[TOC]`** (Python-Markdown / MkDocs `toc` extension) so the outline matches headings automatically and shares one site style (`docs/stylesheets/extra.css`). Short concept pages may omit it.
- **First heading level**: Use a single `#` for the page title; use `##` / `###` for everything else.

---

## 2. Hands-on / pipeline pages (typical)

Pattern: **motivation → requirements → ordered steps → wrap-up**. Examples: `04_Data_QC`, `06_Association_tests`, `30_phasing/Phasing.md`.

| Block | Role |
|--------|------|
| Opening | Task and outcome; tool credits; link to prerequisite modules or data (e.g. `01_Dataset`). |
| `!!! note "Required data and tools"` | Bulleted checklist: software, versions, input files, paths—often with internal links to install/download subsections. |
| Concept chunks | Short theory in `!!! info` / `!!! tip` before long command sequences. |
| `## Preparation` (general) / `## Data preparation` (inputs & files) | Environment layout, downloads, reference files. |
| `###` substeps | One coherent step per subsection (install, QC, one PLINK command family, etc.). |
| `!!! example "…"` | Runnable `bash` / copy-paste blocks; optional fenced title for file snippets (`title="pheno.txt"`). |
| `!!! warning` / `!!! tip` | Common mistakes, OS differences (Linux / Mac / WSL), version quirks. |
| Optional **Exercise** | Short “try it yourself” prompt. |
| **Key terms** | Glossary-style list. |
| **References** | Papers and software manuals. |

**Scripts**: Link to `*.sh` in the module folder or show representative fragments; keep paths consistent with the rest of the tutorial.

---

## 3. Concept / Topics pages (typical)

Pattern: **definition → notation → relationships → pitfalls → links to hands-on**. Examples: `19_ld`, `13_heritability`, `55_measure_of_effect`.

| Block | Role |
|--------|------|
| `#` title + lead | Define the idea in words before symbols. |
| `##` sections | Logical flow: definition → estimators/measures → assumptions/limits → “in practice” pointers. |
| Math / tables | `$$…$$`, inline `$…$`; tables for notation or method comparison. |
| `!!! info` / `!!! warning` | Intuition lists; common misinterpretations. |
| Code | Minimal: one-line command or tiny format sample, or link to a hands-on module instead of full pipelines. |
| **References** | Primary literature; optional “see also” links to other modules. |

TOC optional; useful when the page is long (e.g. liftover-related material).

---

## 4. Hub / overview pages (typical)

Pattern: **big picture → TOC as map → one section per linked area**. Examples: `39_overview/README.md`, `29_postgwas/README.md`.

- Lead paragraph states scope (whole workflow, or post-GWAS landscape).
- Optional workflow figure or sequence of `!!! note` callouts as stages.
- `## Table of Contents` entries often link to **other modules** (`../NN_topic/` or site paths) with short descriptions.
- Each linked area may be a `##` section with “Biological questions answered”, required inputs, and a link to the detailed tutorial.

---

## 5. Data / resource-only pages (typical)

Example: `01_Dataset/README.md`.

- `#` title + immediate context (cohort, build, URL).
- TOC then sections such as **processing summary**, **download**, **phenotype simulation** (with `###` for models), **key terms**, **references**.
- Heavy use of `!!! note` / `!!! warning` for hosting, licensing, or regional access.

---

## 6. Callouts (Material / MkDocs)

Use consistently with [guideline-hands-on.md](guideline-hands-on.md):

| Admonition | Typical use |
|------------|-------------|
| `!!! example` | Runnable commands, file dumps, copy-paste blocks. |
| `!!! note` | Repository facts, prerequisites, structural reminders. |
| `!!! info` | Definitions, factor lists, intuition. |
| `!!! tip` | Optional improvements, workflow hints. |
| `!!! warning` | Costly or common errors, access limitations. |
| `!!! quote` | Sparingly: cited methodological caveats. |

---

## 7. Repo integration checklist

When adding or substantially rewriting a page:

1. Source of truth: `NN_topic/README.md` (or special paths like `30_phasing/Phasing.md`, `31_imputation/Imputation.md`).
2. `deploy.sh`: folder in the `cp` loop or explicit `cp` for special files.
3. `mkdocs.yml`: `nav` entry and correct `docs/*.md` filename.
4. Cross-links: relative paths to sibling modules and shared data (e.g. under `01_Dataset`, `04_Data_QC`).
5. Optional **keywords**: [guideline-keywords.md](guideline-keywords.md).

---

## 8. Minimal empty scaffold (copy me)

```markdown
# Title

Brief introduction.

**On this page**

[TOC]

## Section A

## Section B

## Key terms

## References
```

Replace section names, add `###` substeps, callouts, and code blocks as the page needs.
