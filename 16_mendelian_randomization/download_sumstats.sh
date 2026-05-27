#!/bin/bash
# Module: 16_mendelian_randomization | Script: download_sumstats.sh
# Step: download_sumstats

set -euo pipefail
cd "$(dirname "$0")"

wget -O bbj_t2d.zip https://pheweb.jp/download/T2D
unzip bbj_t2d.zip
wget -O koges_bmi.txt.gz https://koges.leelabsg.org/download/KoGES_BMI
