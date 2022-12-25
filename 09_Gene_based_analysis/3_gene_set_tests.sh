#!/bin/bash
geneset=/home/he/tools/magma/MSigDB/msigdb_v2022.1.Hs_files_to_download_locally/msigdb_v2022.1.Hs_GMTs/msigdb.v2022.1.Hs.entrez.gmt
magma \
	--gene-results HDLC_chr3.genes.raw \
	--set-annot ${geneset} \
	--out HDLC_chr3
