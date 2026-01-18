# Variant Annotation

Variant annotation is the process of adding functional and biological information to genetic variants identified in genome-wide association studies (GWAS). After identifying variants associated with a trait, annotation helps researchers understand the potential biological consequences of these variants by providing information such as:

- **Gene location**: Which genes are affected by the variant (exonic, intronic, intergenic, etc.)
- **Functional consequences**: Whether the variant affects protein-coding sequences (missense, nonsense, synonymous), regulatory regions, or non-coding RNAs
- **Population frequency**: How common the variant is in different populations (e.g., from dbSNP, gnomAD, 1000 Genomes)
- **Pathogenicity**: Clinical significance and disease associations (e.g., from ClinVar)
- **Conservation scores**: Evolutionary conservation and predicted functional impact (e.g., CADD, SIFT, PolyPhen)

This information is crucial for prioritizing variants for follow-up studies, understanding biological mechanisms, and translating GWAS findings into actionable insights for personalized medicine and drug discovery.

## Table of Contents
- [ANNOVAR](#annovar)
- [VEP](#vep)

!!! info "Annotation"
    <img width="700" alt="image" src="https://github.com/Cloufield/GWASTutorial/assets/40289485/980697e6-e2ae-40f6-821f-dca190e568d5">

## ANNOVAR

[ANNOVAR](https://annovar.openbioinformatics.org/en/latest/) is a simple and efficient command line tool for variant annotation. 

In this tutorial, we will use ANNOVAR to annotate the variants in our summary statistics (hg19).

### Install

Download ANNOVAR from [here](https://annovar.openbioinformatics.org/en/latest/user-guide/download/) (registration required; freely available to personal, academic and non-profit use only.)

You will receive an email with the download link after registration. Download it and decompress:

```bash
tar -xvzf annovar.latest.tar.gz
```

For refGene annotation for hg19, we do not need to download additional files.

### Format input file

The default input file for ANNOVAR is a 1-based coordinate file.

We will only use the first 100000 variants as an example.

!!! example "annovar_input"
    ```bash
    awk 'NR>1 && NR<=100000 {print $1,$2,$2,$4,$5}' ../06_Association_tests/1kgeas.B1.glm.firth > annovar_input.txt
    ```
    
    ```
    head annovar_input.txt 
    1 13273 13273 G C
    1 14599 14599 T A
    1 14604 14604 A G
    1 14930 14930 A G
    1 69897 69897 T C
    1 86331 86331 A G
    1 91581 91581 G A
    1 122872 122872 T G
    1 135163 135163 C T
    1 233473 233473 C G
    ```

!!! info "With `-vcfinput` option, ANNOVAR can accept input files in VCF format."
    

### Annotation
Annotate the variants with gene information.

!!! example "A minimal example of annotation using refGene"
    
    ```bash
    input=annovar_input.txt
    humandb=/home/he/tools/annovar/annovar/humandb
    table_annovar.pl ${input} ${humandb} -buildver hg19 -out myannotation -remove -protocol refGene -operation g -nastring . -polish
    ```
    
    ```
    Chr	Start	End	Ref	Alt	Func.refGene	Gene.refGene	GeneDetail.refGene	ExonicFunc.refGene	AAChange.refGene
    1	13273	13273	G	C	ncRNA_exonic	DDX11L1;LOC102725121	.	.	.
    1	14599	14599	T	A	ncRNA_exonic	WASH7P	.	.	.
    1	14604	14604	A	G	ncRNA_exonic	WASH7P	.	.	.
    1	14930	14930	A	G	ncRNA_intronic	WASH7P	.	.	.
    1	69897	69897	T	C	exonic	OR4F5	.	synonymous SNV	OR4F5:NM_001005484:exon1:c.T807C:p.S269S
    1	86331	86331	A	G	intergenic	OR4F5;LOC729737	dist=16323;dist=48442	.	.
    1	91581	91581	G	A	intergenic	OR4F5;LOC729737	dist=21573;dist=43192	.	.
    1	122872	122872	T	G	intergenic	OR4F5;LOC729737	dist=52864;dist=11901	.	.
    1	135163	135163	C	T	ncRNA_exonic	LOC729737	.	.	.
    ```

### Additional databases

ANNOVAR supports a wide range of commonly used databases including `dbsnp` , `dbnsfp`, `clinvar`, `gnomad`, `1000g`, `cadd` and so forth. For details, please check [ANNOVAR's official documents](https://annovar.openbioinformatics.org/en/latest/user-guide/download/)

You can check the Table Name listed in [the link above](https://annovar.openbioinformatics.org/en/latest/user-guide/download/)  and download the database you need using the following command.

!!! example "Example: Downloading avsnp150 for hg19 from ANNOVAR"
    ```
    annotate_variation.pl -buildver hg19 -downdb -webfrom annovar avsnp150 humandb/
    ```

!!! example "An example of annotation using multiple databases"
    ```
    # input file is in vcf format
    table_annovar.pl \
      ${in_vcf} \
      ${humandb} \
      -buildver hg19 \
      -protocol refGene,avsnp150,clinvar_20200316,gnomad211_exome \
      -operation g,f,f,f \
      -remove \
      -out ${out_prefix} \
      -vcfinput
    ```

## VEP (under construction)

### Install

```
git clone https://github.com/Ensembl/ensembl-vep.git
cd ensembl-vep
perl INSTALL.pl
```


```
Hello! This installer is configured to install v108 of the Ensembl API for use by the VEP.
It will not affect any existing installations of the Ensembl API that you may have.

It will also download and install cache files from Ensembl's FTP server.

Checking for installed versions of the Ensembl API...done

Setting up directories
Destination directory ./Bio already exists.
Do you want to overwrite it (if updating VEP this is probably OK) (y/n)? y
 - fetching BioPerl
 - unpacking ./Bio/tmp/release-1-6-924.zip
 - moving files

Downloading required Ensembl API files
 - fetching ensembl
 - unpacking ./Bio/tmp/ensembl.zip
 - moving files
 - getting version information
 - fetching ensembl-variation
 - unpacking ./Bio/tmp/ensembl-variation.zip
 - moving files
 - getting version information
 - fetching ensembl-funcgen
 - unpacking ./Bio/tmp/ensembl-funcgen.zip
 - moving files
 - getting version information
 - fetching ensembl-io
 - unpacking ./Bio/tmp/ensembl-io.zip
 - moving files
 - getting version information

Testing VEP installation
 - OK!

The VEP can either connect to remote or local databases, or use local cache files.
Using local cache files is the fastest and most efficient way to run the VEP
Cache files will be stored in /home/he/.vep
Do you want to install any cache files (y/n)? y

The following species/files are available; which do you want (specify multiple separated by spaces or 0 for all): 
1 : acanthochromis_polyacanthus_vep_108_ASM210954v1.tar.gz (69 MB)
2 : accipiter_nisus_vep_108_Accipiter_nisus_ver1.0.tar.gz (55 MB)
...
466 : homo_sapiens_merged_vep_108_GRCh37.tar.gz (16 GB)
467 : homo_sapiens_merged_vep_108_GRCh38.tar.gz (26 GB)
468 : homo_sapiens_refseq_vep_108_GRCh37.tar.gz (13 GB)
469 : homo_sapiens_refseq_vep_108_GRCh38.tar.gz (22 GB)
470 : homo_sapiens_vep_108_GRCh37.tar.gz (14 GB)
471 : homo_sapiens_vep_108_GRCh38.tar.gz (22 GB)

  Total: 221 GB for all 471 files

? 470
 - downloading https://ftp.ensembl.org/pub/release-108/variation/indexed_vep_cache/homo_sapiens_vep_108_GRCh37.tar.gz
```

## References

### ANNOVAR

- **ANNOVAR**: Wang, K., Li, M., & Hakonarson, H. (2010). ANNOVAR: functional annotation of genetic variants from high-throughput sequencing data. *Nucleic Acids Research*, 38(16), e164. https://doi.org/10.1093/nar/gkq603

- **ANNOVAR website**: https://annovar.openbioinformatics.org/en/latest/

### VEP (Variant Effect Predictor)

- **VEP**: McLaren, W., Gil, L., Hunt, S. E., Riat, H. S., Ritchie, G. R., Thormann, A., ... & Cunningham, F. (2016). The Ensembl Variant Effect Predictor. *Genome Biology*, 17(1), 1-14. https://doi.org/10.1186/s13059-016-0974-4

- **VEP documentation**: https://www.ensembl.org/info/docs/tools/vep/index.html

### General annotation resources

- **dbSNP**: Sherry, S. T., Ward, M. H., Kholodov, M., Baker, J., Phan, L., Smigielski, E. M., & Sirotkin, K. (2001). dbSNP: the NCBI database of genetic variation. *Nucleic Acids Research*, 29(1), 308-311. https://doi.org/10.1093/nar/29.1.308

- **ClinVar**: Landrum, M. J., Lee, J. M., Benson, M., Brown, G. R., Chao, C., Chitipiralla, S., ... & Maglott, D. R. (2018). ClinVar: improving access to variant interpretations and supporting evidence. *Nucleic Acids Research*, 46(D1), D1062-D1067. https://doi.org/10.1093/nar/gkx1153

- **gnomAD**: Karczewski, K. J., Francioli, L. C., Tiao, G., Cummings, B. B., Alföldi, J., Wang, Q., ... & MacArthur, D. G. (2020). The mutational constraint spectrum quantified from variation in 141,456 humans. *Nature*, 581(7809), 434-443. https://doi.org/10.1038/s41586-020-2308-7
