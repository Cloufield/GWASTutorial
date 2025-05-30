#/bin/bash
mkdir -p docs
for dir in 55_measure_of_effect 21_twas 20_power_analysis 17_colocalization 18_Conditioning_analysis 19_ld 76_R_resources 75_R_basics 16_mendelian_randomization 11_meta_analysis 15_winners_curse 71_python_resources 70_python_basics 14_gcta_greml 12_fine_mapping 96_Assignment2 95_Assignment 33_linear_mixed_model 32_whole_genome_regression 99_About 69_resources 13_heritability 85_job_scheduler 84_ssh 90_Recommended_Reading 01_Dataset 02_Linux_basics 03_Data_formats 04_Data_QC 05_PCA 06_Association_tests 07_Annotation 08_LDSC 09_Gene_based_analysis 10_PRS 60_awk 61_sed 80_miniconda 81_jupyter_notebook 82_windows_linux_subsystem 83_git_and_github
do
cp ${dir}/README.md docs/${dir}.md
done

cp 31_imputation/Imputation.md docs/Imputation.md
cp 30_phasing/Phasing.md docs/Phasing.md
cp 10_PRS/prs_tutorial.ipynb docs/prs_tutorial.ipynb
cp 10_PRS/PRS_evaluation.md docs/PRS_evaluation.md
cp 12_fine_mapping/finemapping_susie.ipynb docs/finemapping_susie.ipynb
cp 16_mendelian_randomization/TwoSampleMR.ipynb docs/TwoSampleMR.ipynb
cp 05_PCA/plot_PCA.ipynb docs/plot_PCA.ipynb
cp 06_Association_tests/Visualization.ipynb docs/Visualization.ipynb
cp README.md docs/index.md
mkdocs gh-deploy
