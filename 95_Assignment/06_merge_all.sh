#!/bin/bash
plink \
      --merge-list mergelist.txt \
      --make-bed \
      --out ALL.ldpruned.nohla.common.strict.all
