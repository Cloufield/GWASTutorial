#!/bin/bash

ldsc.py \
  --rg BBJ_HDLC.sumstats.gz,BBJ_LDLC.sumstats.gz \
  --ref-ld-chr ~/tools/ldsc/resource/eas_ldscores/ \
  --w-ld-chr ~/tools/ldsc/resource/eas_ldscores/ \
  --out BBJ_HDLC_LDLC
