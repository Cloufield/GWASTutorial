#/bin/bash
mkdir -p docs
for dir in 01_Dataset 02_Linux_basics 03_Data_formats 04_Data_QC 05_PCA 06_Association_tests 07_Annotation 08_LDSC 09_Gene_based_analysis 10_PRS 80_anaconda 81_jupyter_notebook 82_windows_linux_subsystem 83_git_and_github
do
cp ${dir}/README.md docs/${dir}.md
done
cp 06_Association_tests/Visualization.ipynb docs/Visualization.ipynb
cp README.md docs/index.md
mkdocs gh-deploy
