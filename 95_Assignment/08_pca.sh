#!/bin/bash
plink \
      --bfile  ALL.ldpruned.nohla.common.strict.all \
      --pca \
      --out ALL.ldpruned.nohla.common.strict.all
