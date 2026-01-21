#!/bin/bash
LDSC_PATH=~/tools/ldsc
LDSC_RESOURCE=~/tools/ldsc/resource

${LDSC_PATH}/ldsc.py \
  --rg BBJ_HDLC.sumstats.gz,BBJ_LDLC.sumstats.gz \
  --ref-ld-chr ${LDSC_RESOURCE}/eas_ldscores/ \
  --w-ld-chr ${LDSC_RESOURCE}/eas_ldscores/ \
  --out BBJ_HDLC_LDLC
