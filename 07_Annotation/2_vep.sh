#!/usr/bin/env bash
# Run Ensembl VEP in Docker on the bundled sample VCF (GRCh37 / hg19).
# Quick setup: install Docker, pull the image, and populate VEP_DATA (see README).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

VEP_IMAGE="${VEP_IMAGE:-ensemblorg/ensembl-vep}"
# With sudo, $HOME is root's home; use the invoking user's cache and UID/GID unless overridden.
if [[ $(id -u) -eq 0 && -n "${SUDO_USER:-}" ]]; then
  _inv_home="$(getent passwd "$SUDO_USER" | cut -d: -f6)"
  VEP_DATA="${VEP_DATA:-${_inv_home}/vep_data}"
  DOCKER_USER="${DOCKER_USER:-$(id -u "$SUDO_USER"):$(id -g "$SUDO_USER")}"
else
  VEP_DATA="${VEP_DATA:-$HOME/vep_data}"
  DOCKER_USER="${DOCKER_USER:-$(id -u):$(id -g)}"
fi
INPUT_VCF="${INPUT_VCF:-$ROOT/vep_sample.vcf}"
OUT_VCF="${OUT_VCF:-$ROOT/vep_output.vcf}"

err() { echo "$*" >&2; exit 1; }

command -v docker >/dev/null 2>&1 || err "docker not found. Install Docker and retry."
docker info >/dev/null 2>&1 || err "Docker daemon is not running (or no permission). Start Docker and retry."
[[ -f "$INPUT_VCF" ]] || err "Input VCF not found: $INPUT_VCF"

for p in "$INPUT_VCF" "$OUT_VCF"; do
  [[ "$p" == "$ROOT"/* ]] || err "Paths must be under $ROOT (this directory is mounted as /work in the container)."
done

REL_IN="${INPUT_VCF#"$ROOT"/}"
REL_OUT="${OUT_VCF#"$ROOT"/}"

mkdir -p "$VEP_DATA"
if [[ -z "$(ls -A "$VEP_DATA" 2>/dev/null || true)" ]]; then
  err "VEP cache directory is empty: $VEP_DATA
Run once (large download):
  mkdir -p \"$VEP_DATA/tmp\"
  docker run --rm -it --user \"\$(id -u):\$(id -g)\" -v \"$VEP_DATA:/data\" $VEP_IMAGE \\
    INSTALL.pl -a cf -s homo_sapiens -y GRCh37 -c /data"
fi

mkdir -p "$(dirname "$OUT_VCF")"

docker run --rm \
  --user "$DOCKER_USER" \
  -v "$VEP_DATA:/data" \
  -v "$ROOT:/work" \
  -w /work \
  "$VEP_IMAGE" \
  vep --cache --offline --dir_cache /data --assembly GRCh37 --format vcf --vcf --force_overwrite \
  --input_file "$REL_IN" \
  --output_file "$REL_OUT"

echo "Wrote $OUT_VCF"
