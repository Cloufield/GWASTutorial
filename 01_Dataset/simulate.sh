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

#shuf 1KG.EAS.auto.snp.norm.nodup.split.rare002.common015.bim | head -n 5 | awk '{print $2, 3}' > causal.snplist

gcta  \
	--bfile 1KG.EAS.auto.snp.norm.nodup.split.rare002.common015 \
	--simu-cc 250 254  \
	--simu-causal-loci causal.snplist  \
	--simu-hsq 0.8  \
	--simu-k 0.5  \
	--simu-rep 1  \
	--out 1kgeas_binary

echo "FID IID B1" >1kgeas_binary.txt
cat 1kgeas_binary.phen >>1kgeas_binary.txt

