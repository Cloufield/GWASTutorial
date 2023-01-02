#!/bin/bash

zcat BBJ_RA.txt.gz | awk 'NR==1 || !($2==6 && $3>25000000 && $3<34000000) '| gzip > BBJ_RA_noHLA.txt.gz

snplist=~/tools/ldsc/resource/w_hm3.snplist
munge_sumstats.py \
	--sumstats ./BBJ_RA_noHLA.txt.gz \
	--N 19190 \
	--merge-alleles $snplist \
	--chunksize 500000 \
	--out BBJ_RA
	
