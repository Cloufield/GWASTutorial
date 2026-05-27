#!/bin/bash
# Module: 07_Annotation | Script: 1_annovar.sh
# Step: annovar

set -euo pipefail
cd "$(dirname "$0")"

input=annovar_input.txt
humandb=~/tools/annovar/annovar/humandb
table_annovar.pl ${input} ${humandb} -buildver hg19 -out myannotation -remove -protocol refGene -operation g -nastring . -polish
