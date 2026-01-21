#!/bin/bash
LDSC_PATH=~/tools/ldsc
LDSC_RESOURCE=~/tools/ldsc/resource

${LDSC_PATH}/ldsc.py \
  --h2-cts BBJ_HDLC.sumstats.gz \
  --ref-ld-chr-cts ${LDSC_RESOURCE}/Cahoy_EAS_1000Gv3_ldscores/Cahoy.EAS.ldcts \
  --ref-ld-chr ${LDSC_RESOURCE}/1000G_Phase3_EAS_baseline_v1_2_ldscores/baseline. \
  --w-ld-chr ${LDSC_RESOURCE}/1000G_Phase3_EAS_weights_hm3_no_MHC/weights.EAS.hm3_noMHC. \
  --out BBJ_HDLC_baseline_cts
