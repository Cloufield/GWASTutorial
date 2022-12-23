#!/bin/bash
snplist=~/tools/ldsc/resource/w_hm3.snplist
munge_sumstats.py \
	--sumstats BBJ_HDLC.txt.gz \
	--merge-alleles $snplist \
	--a1 ALT \
	--a2 REF \
	--out BBJ_HDLC
munge_sumstats.py \
        --sumstats BBJ_LDLC.txt.gz \
	--a1 ALT \
        --a2 REF \
        --merge-alleles $snplist \
        --out BBJ_LDLC
	
