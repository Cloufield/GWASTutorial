#!/bin/bash

awk 'NR>1 && NR<100000 {print $1,$2,$2,$4,$5}' ../06_Association_tests/1kgeas.B1.glm.logistic.hybrid > annovar_input.txt

##CHROM	POS	ID	REF	ALT	A1	FIRTH?	TEST	OBS_CT	OR	LOG(OR)_SE	Z_STAT	P	ERRCODE#1	13273	1:13273:G:C	G	C	C	N	ADD	503	0.750168	0.280794	-1.02373	0.305961
