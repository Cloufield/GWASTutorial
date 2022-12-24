#!/bin/bash

ldsc.py \
  --h2-cts BBJ_HDLC.sumstats.gz \
  --ref-ld-chr-cts ~/tools/ldsc/resource/Cahoy_EAS_1000Gv3_ldscores/Cahoy.EAS.ldcts \
  --ref-ld-chr ~/tools/ldsc/resource/1000G_Phase3_EAS_baseline_v1_2_ldscores/baseline. \
  --w-ld-chr ~/tools/ldsc/resource/1000G_Phase3_EAS_weights_hm3_no_MHC/weights.EAS.hm3_noMHC. \
  --out BBJ_HDLC_baseline_cts
