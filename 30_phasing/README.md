# Phasing (hands-on)

Shell steps live in **three scripts** (run from `30_phasing/`). Narrative and citations: [Phasing.md](Phasing.md).

---


## Scripts

| Script | Purpose |
|--------|---------|
| `prepare.phasing.sh` | `plink2 --ref-from-fa` → `sample_data.clean.alignment` |
| `phasing_eagle2.sh` | JPT / chr22 / MAF subset → Eagle2 → phased VCF.gz |
| `phasing_shapeit2.sh` | Same subset → intersect with `chr22_phase1_shapeit_panel_positions.txt` → SHAPEIT2 → VCF.gz |

**Eagle2** phases the full chr22 subset (`sample_data.chr22.clean`). **SHAPEIT2** uses **`sample_data.chr22.shapeit_ref`** (same samples, SNPs restricted to the Phase I panel list in the bundled position file).

---


## Configure

Edit the **`# --- configure ---`** block at the top of each script, or set environment variables when you run it (e.g. `REF_FASTA`, `SHAPEIT2_REFERENCE_DIR`, `EAGLE_GENETIC_MAP`, `SHAPEIT_PANEL_POSITIONS`, `CHR`, `MAF_THRESH`).

`SHAPEIT2`, `eagle`, `plink2`, `bgzip`, and `tabix` must be on your `PATH`.

---


## Run

```bash
cd 30_phasing

bash prepare.phasing.sh
bash phasing_eagle2.sh
bash phasing_shapeit2.sh
```

---


## Required upstream data

- `../04_Data_QC/sample_data.clean` (after QC)
- `../01_Dataset/JPT.sample`
- Reference FASTA for `prepare.phasing.sh` (see [Phasing.md](Phasing.md))
- `chr22_phase1_shapeit_panel_positions.txt` (bundled; regenerate if your `.bim` changes)
