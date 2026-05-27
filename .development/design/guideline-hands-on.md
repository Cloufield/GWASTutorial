# Hands-on module guidelines

See [template.md](template.md) for the canonical skeleton. Hands-on pipeline modules (core GWAS path) must include:

1. YAML front matter (`module_id`, `type: hands_on`, `prerequisites`, `produces`, `primary_script`).
2. `**On this page**` + `[TOC]` (no manual bullet TOC).
3. `## Preparation` with `!!! note "Required data and tools"` using **Kind: Name** bullets (`Software`, `Data`, `Reference`, `Environment`).
4. `## Sample script` linking `./run_<name>.sh` first, then step-level `!!! example` blocks that match script `# Step:` comments.
5. `## Key terms` (comma-separated keywords for [dictionary](../dictionary/README.md)).
6. `## References` (level-2 heading).

Tone: task-first, copy-paste commands in `!!! example`, theory in `!!! info` before long command blocks.
