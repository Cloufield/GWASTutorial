#!/bin/bash

plinkFile="../04_Data_QC/sample_data.clean"

gcta \
  --bfile ${plinkFile} \
  --autosome \
  --maf 0.01 \
  --make-grm \
  --out 1kg_eas
