#!/bin/bash
zcat ../08_LDSC/BBJ_HDLC.txt.gz | awk 'NR>1 && $2==3 {print $1,$2,$3}' > HDLC_chr3.magma.input.snp.chr.pos.txt
zcat ../08_LDSC/BBJ_HDLC.txt.gz | awk 'NR>1 && $2==3 {print $1,10^(-$11)}' >  HDLC_chr3.magma.input.p.txt
