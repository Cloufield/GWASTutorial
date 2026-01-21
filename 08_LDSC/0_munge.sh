#!/bin/bash
LDSC_PATH=~/tools/ldsc
LDSC_RESOURCE=~/tools/ldsc/resource
snplist=${LDSC_RESOURCE}/w_hm3.snplist
${LDSC_PATH}/munge_sumstats.py \
	--sumstats BBJ_HDLC.txt.gz \
	--merge-alleles $snplist \
	--a1 ALT \
	--a2 REF \
	--chunksize 500000 \
	--out BBJ_HDLC
${LDSC_PATH}/munge_sumstats.py \
        --sumstats BBJ_LDLC.txt.gz \
	--a1 ALT \
        --a2 REF \
	--chunksize 500000 \
        --merge-alleles $snplist \
        --out BBJ_LDLC
	
