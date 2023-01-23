#!/bin/bash
wget -O t2d_bbj_v2.tar.gz http://jenger.riken.jp/95/
tar -xvzf t2d_bbj_v2.tar.gz
zcat T2D.auto.rsq07.mac10.txt.gz | awk '{gsub("_",":",$3); print $3, $5, $9, $12}'> t2d_plink.txt
python extract.py 
