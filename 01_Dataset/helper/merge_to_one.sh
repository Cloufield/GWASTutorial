#!/bin/bash
export PATH=~/tools/bin:$PATH
export OMP_NUM_THREADS=1

plink \
	--merge-list mergelist.txt \
	--make-bed \
	--keep-allele-order \
	--out 1KGEAS.auto.norm_nodup_split_maf005

