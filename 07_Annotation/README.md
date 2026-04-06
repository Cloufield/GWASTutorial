# Variant Annotation

Variant annotation is the process of adding functional and biological information to genetic variants identified in genome-wide association studies (GWAS). After identifying variants associated with a trait, annotation helps researchers understand the potential biological consequences of these variants by providing information such as:

- **Gene location**: Which genes are affected by the variant (exonic, intronic, intergenic, etc.)
- **Functional consequences**: Whether the variant affects protein-coding sequences (missense, nonsense, synonymous), regulatory regions, or non-coding RNAs
- **Population frequency**: How common the variant is in different populations (e.g., from dbSNP, gnomAD, 1000 Genomes)
- **Pathogenicity**: Clinical significance and disease associations (e.g., from ClinVar)
- **Conservation scores**: Evolutionary conservation and predicted functional impact (e.g., CADD, SIFT, PolyPhen)

This information is crucial for prioritizing variants for follow-up studies, understanding biological mechanisms, and translating GWAS findings into actionable insights for personalized medicine and drug discovery.

---


**On this page**

[TOC]

!!! info "Annotation"
    <img width="700" alt="image" src="https://github.com/Cloufield/GWASTutorial/assets/40289485/980697e6-e2ae-40f6-821f-dca190e568d5">

---


## ANNOVAR

[ANNOVAR](https://annovar.openbioinformatics.org/en/latest/) is a simple and efficient command line tool for variant annotation. 

In this tutorial, we will use ANNOVAR to annotate the variants in our summary statistics (hg19).

!!! note "Required data and tools"

    - **ANNOVAR** — download and unpack the package ([Install](#install)); for the minimal `refGene` example you need an **hg19** `humandb` (see ANNOVAR docs for extra annotation databases).
    - **GWAS summary statistics** — PLINK2-style association output to build the coordinate input, e.g. [06_Association_tests/1kgeas.B1.glm.firth](../06_Association_tests/README.md) ([Format input file](#format-input-file)).

---


### Install

Download ANNOVAR from [here](https://annovar.openbioinformatics.org/en/latest/user-guide/download/) (registration required; freely available to personal, academic and non-profit use only.)

You will receive an email with the download link after registration. Download it and decompress:

!!! example "Unpack the ANNOVAR archive"

    ```bash
    tar -xvzf annovar.latest.tar.gz
    ```

For refGene annotation for hg19, we do not need to download additional files.

---


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

---

    

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

---


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

---


## VEP

[Ensembl VEP](https://www.ensembl.org/vep) (Variant Effect Predictor) adds transcript-level consequences, regulatory overlap, and optional frequency or pathogenicity annotations. Ensembl [recommends Docker or Singularity](https://useast.ensembl.org/info/docs/tools/vep/script/vep_download.html) on modern systems so you do not install Perl, BioPerl, HTSlib, and the Ensembl API yourself.

**In this folder:** a small tracked VCF, [`vep_sample.vcf`](vep_sample.vcf) (same variant style as [`annovar_input.txt`](#format-input-file)), [`2_vep.sh`](2_vep.sh) (runs VEP in Docker and writes `vep_output.vcf`), and [`vep_output.example.vcf`](vep_output.example.vcf) (checked-in header + first variant so you can inspect output without running Docker).

!!! note "Required data and tools"

    - **Docker** — [Docker Engine](https://www.docker.com/) and image [`ensemblorg/ensembl-vep`](https://hub.docker.com/r/ensemblorg/ensembl-vep/).
    - **VEP cache + FASTA (one-time)** — human GRCh37 data are **large** (on the order of **tens of GB** on disk after download and unpack). Keep them on the host under **`$HOME/vep_data`** (mounted as **`/data`** in the container). Details: [download and install](https://useast.ensembl.org/info/docs/tools/vep/script/vep_download.html).
    - **Sample input** — [`vep_sample.vcf`](vep_sample.vcf), or build a larger VCF from association results or `annovar_input.txt` (below).

!!! tip "Downloads take time"

    **`docker pull ensemblorg/ensembl-vep`** can take several minutes depending on bandwidth. The **`INSTALL.pl -a cf …`** step downloads the indexed cache and FASTA over the network, then unpacks (and may run cache conversion); **expect roughly tens of minutes to well over an hour** for a full human GRCh37 install, depending on connection speed, disk, and CPU. The terminal may sit on “downloading” or “unpacking” for a long time—this is normal. After the first install, **`./2_vep.sh`** only reads local cache and finishes quickly for small inputs like `vep_sample.vcf`.

Open the release directory (change **`115`** to your Ensembl release if needed):

[https://ftp.ensembl.org/pub/release-115/variation/indexed_vep_cache/](https://ftp.ensembl.org/pub/release-115/variation/indexed_vep_cache/)

---


### Quick setup (Docker image + cache)

1. Pull the image ([Docker section](https://useast.ensembl.org/info/docs/tools/vep/script/vep_download.html#docker) of the Ensembl guide):

!!! example "Pull the Ensembl VEP Docker image"

    ```bash
    docker pull ensemblorg/ensembl-vep
    ```

2. Install **GRCh37** cache and FASTA (**hg19**, same assembly as the ANNOVAR example above):

!!! example "Install GRCh37 cache and FASTA (one-time, large download)"

    ```bash
    mkdir -p "$HOME/vep_data/tmp"
    docker run --rm -it \
      --user "$(id -u):$(id -g)" \
      -v "$HOME/vep_data:/data" \
      ensemblorg/ensembl-vep \
      INSTALL.pl -a cf -s homo_sapiens -y GRCh37 -c /data
    ```

- **`-a cf`:** cache + FASTA. **`-c /data`:** store everything on the mounted volume (not the image default `$HOME/.vep`).
- **`--user "$(id -u):$(id -g)"`:** the image user `vep` often cannot write bind-mounted host directories; without matching UID/GID, `INSTALL.pl` may report “downloading” then fail on **`/data/tmp/…`**. [`2_vep.sh`](2_vep.sh) uses the same `--user` so it can read the cache and write outputs here.

**Optional:** on a shared machine you may use **`-u 0`** instead of `--user "$(id -u):$(id -g)"` for install; leave the cache **world-readable** (default `umask` is usually enough) if you later run `vep` as the image’s `vep` user without `--user`.

**If install failed halfway:** clear `$HOME/vep_data` and repeat step 2.

--- 

### Run the tutorial script

From `07_Annotation`, after setup:

!!! example "Run the tutorial script (default input/output)"

    ```bash
    ./2_vep.sh
    ```

The script requires Docker, a non-empty **`$VEP_DATA`** (default **`$HOME/vep_data`**), then runs `vep` on **`vep_sample.vcf`** and writes **`vep_output.vcf`**. If you run with **`sudo`**, the default cache path is **`~<invoking-user>/vep_data`** (via **`SUDO_USER`**) so it still matches a cache you installed as yourself—prefer **`./2_vep.sh` without sudo** if your user can use Docker.

!!! example "Custom cache path, input VCF, and output VCF"

    ```bash
    VEP_DATA=/path/to/vep_cache ./2_vep.sh
    INPUT_VCF="$PWD/my.vcf" OUT_VCF="$PWD/my_vep.vcf" ./2_vep.sh
    ```

`INPUT_VCF` and `OUT_VCF` must live under this directory (mounted as `/work`; subpaths such as `subdir/file.vcf` are fine).

!!! example "`vep_output.vcf` (header + first variant)"

    Same text as [`vep_output.example.vcf`](vep_output.example.vcf). VEP meta lines and the first row for [`vep_sample.vcf`](vep_sample.vcf) (Ensembl **115** / **115_GRCh37** in this snapshot; `##VEP` and `##VEP-command-line` change with cache version, flags, and run time). Consequences are in **`INFO/CSQ`**: comma-separated transcript blocks, fields pipe-separated as in the `##INFO` line.

    ```vcf
    ##fileformat=VCFv4.2
    ##reference=GRCh37
    ##VEP="v115.2" API="v115" time="2026-04-06 06:52:15" cache="/data/homo_sapiens/115_GRCh37" ensembl=115.266b84d ensembl-compara=115.ae48a7a ensembl-funcgen=115.57f7061 ensembl-io=115.25061d3 ensembl-variation=115.b7c2637 1000genomes="phase3" COSMIC="98" ClinVar="202306" HGMD-PUBLIC="20204" assembly="GRCh37.p13" dbSNP="156" gencode="GENCODE 19" genebuild="2011-04" gnomADe="v4.1" gnomADg="v4.1" polyphen="2.2.2" regbuild="1.0" sift="sift5.2.2"
    ##INFO=<ID=CSQ,Number=.,Type=String,Description="Consequence annotations from Ensembl VEP. Format: Allele|Consequence|IMPACT|SYMBOL|Gene|Feature_type|Feature|BIOTYPE|EXON|INTRON|HGVSc|HGVSp|cDNA_position|CDS_position|Protein_position|Amino_acids|Codons|Existing_variation|DISTANCE|STRAND|FLAGS|SYMBOL_SOURCE|HGNC_ID">
    ##VEP-command-line='vep --assembly GRCh37 --cache --database 0 --dir_cache /data --dir_plugins /plugins --force_overwrite --format vcf --input_file vep_sample.vcf --offline --output_file vep_output.vcf --vcf'
    #CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO
    1	15774	1:15774:G:A	G	A	.	PASS	CSQ=A|intron_variant&non_coding_transcript_variant|MODIFIER|WASH7P|ENSG00000227232|Transcript|ENST00000423562|unprocessed_pseudogene||8/9||||||||||-1||HGNC|38034,A|intron_variant&non_coding_transcript_variant|MODIFIER|WASH7P|ENSG00000227232|Transcript|ENST00000438504|unprocessed_pseudogene||10/11||||||||||-1||HGNC|38034,A|downstream_gene_variant|MODIFIER|DDX11L1|ENSG00000223972|Transcript|ENST00000450305|transcribed_unprocessed_pseudogene|||||||||||2104|1||HGNC|37102,A|downstream_gene_variant|MODIFIER|DDX11L1|ENSG00000223972|Transcript|ENST00000456328|processed_transcript|||||||||||1365|1||HGNC|37102,A|intron_variant&non_coding_transcript_variant|MODIFIER|WASH7P|ENSG00000227232|Transcript|ENST00000488147|unprocessed_pseudogene||9/10||||||||||-1||HGNC|38034,A|downstream_gene_variant|MODIFIER|DDX11L1|ENSG00000223972|Transcript|ENST00000515242|transcribed_unprocessed_pseudogene|||||||||||1362|1||HGNC|37102,A|downstream_gene_variant|MODIFIER|DDX11L1|ENSG00000223972|Transcript|ENST00000518655|transcribed_unprocessed_pseudogene|||||||||||1365|1||HGNC|37102,A|intron_variant&non_coding_transcript_variant|MODIFIER|WASH7P|ENSG00000227232|Transcript|ENST00000538476|unprocessed_pseudogene||11/12||||||||||-1||HGNC|38034,A|intron_variant&non_coding_transcript_variant|MODIFIER|WASH7P|ENSG00000227232|Transcript|ENST00000541675|unprocessed_pseudogene||7/8||||||||||-1||HGNC|38034
    ```

---


### Larger VCFs from your data

From the same PLINK2-style file as in the ANNOVAR section ([`../06_Association_tests/1kgeas.B1.glm.firth`](../06_Association_tests/README.md)):

!!! example "VCF from association results, then `2_vep.sh`"

    ```bash
    awk 'BEGIN{OFS="\t"; print "##fileformat=VCFv4.2"; print "##reference=GRCh37"; print "#CHROM","POS","ID","REF","ALT","QUAL","FILTER","INFO"} \
      NR>1 && NR<=1001 {print $1,$2,$3,$4,$5,".","PASS","."}' \
      ../06_Association_tests/1kgeas.B1.glm.firth > vep_input.vcf
    INPUT_VCF="$PWD/vep_input.vcf" OUT_VCF="$PWD/vep_large_output.vcf" ./2_vep.sh
    ```

From **`annovar_input.txt`** (space-separated `Chr Start End Ref Alt`), first ~1000 variants:

!!! example "VCF from `annovar_input.txt`, then `2_vep.sh`"

    ```bash
    awk 'BEGIN{OFS="\t"; print "##fileformat=VCFv4.2"; print "##reference=GRCh37"; print "#CHROM","POS","ID","REF","ALT","QUAL","FILTER","INFO"} \
      NF>=5 && !/^#/ {id=$1":"$2":"$4":"$5; print $1,$2,id,$4,$5,".","PASS","."}' \
      annovar_input.txt | head -n 1003 > vep_from_annovar.vcf
    ```

(`head` limits to header + 1000 lines of variants; omit `head` for the full file.)

Annotated VCFs carry consequences in **`INFO`** (e.g. **`CSQ`**). More options: [Running VEP](https://useast.ensembl.org/info/docs/tools/vep/script/vep_options.html), [examples](https://useast.ensembl.org/info/docs/tools/vep/script/vep_example.html).

**Without Docker:** clone [ensembl-vep](https://github.com/Ensembl/ensembl-vep) and run `perl INSTALL.pl` per the [download and install](https://useast.ensembl.org/info/docs/tools/vep/script/vep_download.html) guide (again, cache downloads are large and slow the first time).

---


## References

---


### ANNOVAR

- **ANNOVAR**: Wang, K., Li, M., & Hakonarson, H. (2010). ANNOVAR: functional annotation of genetic variants from high-throughput sequencing data. *Nucleic Acids Research*, 38(16), e164. https://doi.org/10.1093/nar/gkq603

- **ANNOVAR website**: https://annovar.openbioinformatics.org/en/latest/

---


### VEP (Variant Effect Predictor)

- **VEP**: McLaren, W., Gil, L., Hunt, S. E., Riat, H. S., Ritchie, G. R., Thormann, A., ... & Cunningham, F. (2016). The Ensembl Variant Effect Predictor. *Genome Biology*, 17(1), 1-14. https://doi.org/10.1186/s13059-016-0974-4

- **VEP documentation**: https://www.ensembl.org/info/docs/tools/vep/index.html

- **VEP download and install (Docker, cache, Singularity)**: https://useast.ensembl.org/info/docs/tools/vep/script/vep_download.html

---


### General annotation resources

- **dbSNP**: Sherry, S. T., Ward, M. H., Kholodov, M., Baker, J., Phan, L., Smigielski, E. M., & Sirotkin, K. (2001). dbSNP: the NCBI database of genetic variation. *Nucleic Acids Research*, 29(1), 308-311. https://doi.org/10.1093/nar/29.1.308

- **ClinVar**: Landrum, M. J., Lee, J. M., Benson, M., Brown, G. R., Chao, C., Chitipiralla, S., ... & Maglott, D. R. (2018). ClinVar: improving access to variant interpretations and supporting evidence. *Nucleic Acids Research*, 46(D1), D1062-D1067. https://doi.org/10.1093/nar/gkx1153

- **gnomAD**: Karczewski, K. J., Francioli, L. C., Tiao, G., Cummings, B. B., Alföldi, J., Wang, Q., ... & MacArthur, D. G. (2020). The mutational constraint spectrum quantified from variation in 141,456 humans. *Nature*, 581(7809), 434-443. https://doi.org/10.1038/s41586-020-2308-7
