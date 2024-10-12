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

gcta64  --bfile ../1KG.EAS.auto.snp.norm.nodup.split.rare002.common015.missing --simu-cc 200 304  --simu-causal-loci t2d_causal.txt  --simu-hsq 0.2  --simu-k 0.4  --simu-rep 1  --out 1kgeas_t2d
echo "FID IID T2D" >1kgeas_t2d.txt
cat 1kgeas_t2d.phen >>1kgeas_t2d.txt
