#!/bin/bash
#$ -S /bin/bash
#$ -cwd
#$ -o temp
#$ -e temp
#$ -q '!mjobs_rerun.q' 
#$ -l mem_req=18G,s_vmem=18G 
#$ -pe def_slot 1
export PATH=~/tools/bin:$PATH
export OMP_NUM_THREADS=1

#plink \
#  --bfile 1KG.EAS.auto.snp.norm.nodup.split.rare002.common015 \
#  --recode \
#  --keep-allele-order \
#  --out 1KG.EAS.auto.snp.norm.nodup.split.rare002.common015 

plink \
	--file 1KG.EAS.auto.snp.norm.nodup.split.rare002.common015.missing \
	--missing \
	--keep-allele-order \
	--make-bed \
	--out 1KG.EAS.auto.snp.norm.nodup.split.rare002.common015.missing
