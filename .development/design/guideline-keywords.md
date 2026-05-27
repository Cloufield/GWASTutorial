# Key terms and GWAS Dictionary

Under `## Key terms`, use a **comma-separated** list of phrases (not hand-written definitions in source READMEs). Run:

```bash
python3 .development/dictionary/expand_key_terms.py docs/NN_topic.md
```

after `deploy.sh` copies READMEs to `docs/`. Expanded bullets link to [GWAS Dictionary](https://cloufield.github.io/GWASDictionary/).

For knowledge-graph extraction, terms also appear in module YAML `concepts:` and `.development/kg/modules/*.json`.
