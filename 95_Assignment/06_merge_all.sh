#!/bin/bash
mkdir -p 1kg-merge

plink \
      --merge-list mergelist.txt \
      --make-bed \
      --out 1kg-merge/ALL.ldpruned.nohla.common.strict.all
