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

gcta64  --bfile 1KGEAS.auto.norm_nodup_split_maf005 --simu-cc 200 304  --simu-causal-loci causal_30.snplist  --simu-hsq 0.8  --simu-k 0.4  --simu-rep 1  --out 1kgeas_binary
echo "FID IID B1" >1kgeas_binary.txt
cat 1kgeas_binary.phen >>1kgeas_binary.txt
