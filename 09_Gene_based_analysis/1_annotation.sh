#!/bin/bash
snploc=./HDLC_chr3.magma.input.snp.chr.pos.txt
ncbi37=~/tools/magma/NCBI37/NCBI37.3.gene.loc
magma --annotate \
      --snp-loc ${snploc} \
      --gene-loc ${ncbi37} \
      --out HDLC_chr3
