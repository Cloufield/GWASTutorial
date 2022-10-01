#!/bin/bash
#$ -S /bin/bash
#$ -cwd
#$ -o temp
#$ -e temp
#$ -q '!mjobs_rerun.q' 
#$ -l mem_req=3G,s_vmem=3G 
#$ -pe def_slot 1

export PATH=~/tools/bin:$PATH
export OMP_NUM_THREADS=1
echo "job id:$JOB_ID"
echo "job name:$JOB_NAME"
genotypeFile="../1_Dataset/1KGEAS.auto.norm_nodup_split_maf005"  #!!!please set this to your own path
phenotypeFile="../1_Dataset/1kgeas_binary.txt" #!!!please set this to your own path
#covariateFile="./plink_results_projected.s"
#covariateCols=6-10
colName="B1"
threadnum=12

plink2 \
	--bfile ${genotypeFile} \
	--pheno ${phenotypeFile} \
	--pheno-name ${colName} \
	--maf 0.01 \
	--glm hide-covar allow-no-covars \
	--threads ${threadnum} \
	--out 1kgeas
