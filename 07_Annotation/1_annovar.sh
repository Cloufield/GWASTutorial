#!/bin/bash
input=annovar_input.txt
humandb=~/tools/annovar/annovar/humandb
table_annovar.pl ${input} ${humandb} -buildver hg19 -out myannotation -remove -protocol refGene -operation g -nastring . -polish
