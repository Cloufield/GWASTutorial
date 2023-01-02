#!/bin/bash

ldsc.py \
  --h2 BBJ_RA.sumstats.gz \
  --ref-ld-chr ~/tools/ldsc/resource/eas_ldscores/ \
  --w-ld-chr ~/tools/ldsc/resource/eas_ldscores/ \
  --out BBJ_RA
