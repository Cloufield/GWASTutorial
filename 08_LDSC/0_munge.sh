#!/bin/bash
snplist=~/tools/ldsc/resource/w_hm3.snplist
munge_sumstats.py \
	--sumstats BBJ_HDLC.txt.gz \
	--merge-alleles $snplist \
	--a1 ALT \
	--a2 REF \
	--chunksize 500000 \
	--out BBJ_HDLC
munge_sumstats.py \
        --sumstats BBJ_LDLC.txt.gz \
	--a1 ALT \
        --a2 REF \
	--chunksize 500000 \
        --merge-alleles $snplist \
        --out BBJ_LDLC
	
