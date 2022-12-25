#!/bin/bash
ref=~/tools/magma/g1000_eas/g1000_eas
magma \
	--bfile $ref \
	--pval ./HDLC_chr3.magma.input.p.txt N=70657 \
	--gene-annot HDLC_chr3.genes.annot \
	--out HDLC_chr3
