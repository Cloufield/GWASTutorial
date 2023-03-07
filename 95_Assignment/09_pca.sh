#!/bin/bash
mkdir -p 1kg-pca

plink \
      --bfile  1kg-merge/ALL.ldpruned.nohla.common.strict.all \
      --pca \
      --out 1kg-pca/ALL.ldpruned.nohla.common.strict.all
