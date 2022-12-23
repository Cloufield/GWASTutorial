#!/bin/bash

ldsc.py \
  --h2 BBJ_HDLC.sumstats.gz \
  --ref-ld-chr ~/tools/ldsc/resource/eas_ldscores/ \
  --w-ld-chr ~/tools/ldsc/resource/eas_ldscores/ \
  --out BBJ_HDLC

ldsc.py \
  --h2 BBJ_LDLC.sumstats.gz \
  --ref-ld-chr ~/tools/ldsc/resource/eas_ldscores/ \
  --w-ld-chr ~/tools/ldsc/resource/eas_ldscores/ \
  --out BBJ_LDLC
