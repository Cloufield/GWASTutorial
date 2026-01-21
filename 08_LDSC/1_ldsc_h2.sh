#!/bin/bash
LDSC_PATH=~/tools/ldsc
LDSC_RESOURCE=~/tools/ldsc/resource

${LDSC_PATH}/ldsc.py \
  --h2 BBJ_HDLC.sumstats.gz \
  --ref-ld-chr ${LDSC_RESOURCE}/eas_ldscores/ \
  --w-ld-chr ${LDSC_RESOURCE}/eas_ldscores/ \
  --out BBJ_HDLC

${LDSC_PATH}/ldsc.py \
  --h2 BBJ_LDLC.sumstats.gz \
  --ref-ld-chr ${LDSC_RESOURCE}/eas_ldscores/ \
  --w-ld-chr ${LDSC_RESOURCE}/eas_ldscores/ \
  --out BBJ_LDLC
