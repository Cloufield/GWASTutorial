#!/bin/bash
LDSC_PATH=~/tools/ldsc
LDSC_RESOURCE=~/tools/ldsc/resource

${LDSC_PATH}/ldsc.py \
  --h2 BBJ_HDLC.sumstats.gz \
  --overlap-annot \
  --ref-ld-chr ${LDSC_RESOURCE}/1000G_Phase3_EAS_baseline_v1_2_ldscores/baseline. \
  --frqfile-chr ${LDSC_RESOURCE}/1000G_Phase3_EAS_plinkfiles/1000G.EAS.QC. \
  --w-ld-chr ${LDSC_RESOURCE}/1000G_Phase3_EAS_weights_hm3_no_MHC/weights.EAS.hm3_noMHC. \
  --out BBJ_HDLC_baseline
