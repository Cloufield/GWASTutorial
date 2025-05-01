# Phasing

Human genome is diploid. Distribution of variants between homologous chromosomes can affect the interpretation of genotype data, such as allele specific expression, 
context-informed annotation, loss-of-function compound heterozygous events. 

!!! example
    <img width="270" alt="image" src="https://github.com/Cloufield/GWASTutorial/assets/84720165/7e18a7e1-0c17-4cce-9e74-d387294ba702">

    ( [SHAPEIT5](https://www.biorxiv.org/content/10.1101/2022.10.19.512867v2.full) )

    *In the above illustration, when LoF variants are on both copies of a gene, the gene is thought knocked out*

Trio data and long read sequencing can solve the haplotyping problem. That is not always possible. Statistical phasing is based on the [Li & Stephens]() Markov model. 
The haploid version of this model (see Imputation) is easier to understand. Because the maternal and paternal haplotypes are independent, 
unphased genotype could be constructed by the addition of two haplotypes.

Recent methods had incorporated long IBD sharing, local haplotypes, etc, to make it tractable for large datasets. 
You could read the following methods if you are interested.

- [PHASE](https://linkinghub.elsevier.com/retrieve/pii/S0002929707633412)
- [MaCH](https://onlinelibrary.wiley.com/doi/full/10.1002/gepi.20533)
- [EAGLE2](https://www.nature.com/articles/ng.3679)
- [SHAPEIT5](https://www.biorxiv.org/content/10.1101/2022.10.19.512867v2.full)
- [BEAGLE3](http://www.cell.com/article/S0002929709000123/fulltext)


## How to do phasing

In most of the cases, phasing is just a pre-step of imputation, and we do not care about how the phasing goes. But there are several considerations, like reference-based or reference-free, large and small sample size, rare variants' cutoff. There is no single method that could best fit all cases. 

We will show two examples:

- Reference-based phasing using SHAPEIT2
- Cohort-based phasing using Eagle2

## Prepare for phasing

Before phasing, we need to align input file to 1KG reference panel.

```
before_alignment_bfile="../04_Data_QC/sample_data.clean"
foralignment="./1KG_foralignment.tsv"

awk -F'\t' '{
  split($2, arr, ":");
  print $2 "\t" arr[3] "\t" arr[4]
}' ${before_alignment_bfile}.bim > ${foralignment}

after_alignment_bfile="./sample_data.clean.alignment"

plink \
	--bfile ${before_alignment_bfile} \
	--a1-allele ${foralignment} 2 \
	--make-bed \
	--out ${after_alignment_bfile}
```

## Phasing using SHAPEIT2

Here, we show an example using SHAPEIT2, which is another commonly used tool for haplotype phasing. SHAPEIT2 is usually used for small cohorts.

!!! note
	We will do a phasing for 1KG EAS samples using 1KG as reference, which does not make any sense. This is just to demonstrate how to do reference-based phasing using SHAPEIT2.

!!! quote
	Delaneau, O., Zagury, J. F., & Marchini, J. (2013). Improved whole-chromosome phasing for disease and population genetic studies. Nature methods, 10(1), 5-6.

We will conduct a reference-based phasing using SHAPEIT2 for chromosome 22.

First, download SHPAEIT2 from [SHPAEIT2 website](https://mathgen.stats.ox.ac.uk/genetics_software/shapeit/shapeit.html#download). Unzip and add it to your environment. We also need reference files (1000 Genomes Phase I integrated haplotypes (produced using SHAPEIT2) b37 June 2014) and genetic maps, which are also available on [SHPAEIT2 website](https://mathgen.stats.ox.ac.uk/impute/impute_v2.html#reference)

Next, for simplicity, we extract only JPT samples and common variants on chr22 from the clean datasets obtained in the previous section.

```
inputbed=./sample_data.clean.alignment
jptsample=../01_Dataset/JPT.sample
inputbedchr22=./sample_data.chr22.clean

plink2 \
        --bfile ${inputbed} \
        --make-bed \
		--keep ${jptsample} \
		--maf 0.05 \
        --chr 22 \
        --out ${inputbedchr22}
```

!!! tip
	Usually, we also remove G/C or A/T SNPs before phasing.

Then, it is needed to check the alignment of SNPs between your genotype file and the reference file.

```
out=./1KG.JPT.chr22.phased.shapeit2.reference_based
outputhaps=${out}.haps
outputsample=${out}.sample
outputlog=${out}
outputlogcheck=${out}.check

geneticmap=~/tools/shapeit2/shapeit.v2.904.3.10.0-693.11.6.el7.x86_64/reference/ALL.integrated_phase1_SHAPEIT_16-06-14.nomono/genetic_map_chr22_combined_b37.txt
inputrefhap=~/tools/shapeit2/shapeit.v2.904.3.10.0-693.11.6.el7.x86_64/reference/ALL.integrated_phase1_SHAPEIT_16-06-14.nomono/ALL.chr22.integrated_phase1_v3.20101123.snps_indels_svs.genotypes.nomono.haplotypes.gz
inputreflegend=~/tools/shapeit2/shapeit.v2.904.3.10.0-693.11.6.el7.x86_64/reference/ALL.integrated_phase1_SHAPEIT_16-06-14.nomono/ALL.chr22.integrated_phase1_v3.20101123.snps_indels_svs.genotypes.nomono.legend.gz
inputrefsample=~/tools/shapeit2/shapeit.v2.904.3.10.0-693.11.6.el7.x86_64/reference/ALL.integrated_phase1_SHAPEIT_16-06-14.nomono/ALL.integrated_phase1_v3.20101123.snps_indels_svs.genotypes.sample

shapeit -check \
        -B ${inputbedchr22} \
        -M ${geneticmap} \
        --input-ref ${inputrefhap} ${inputreflegend} ${inputrefsample} \
        --output-log ${outputlogcheck}
```
This command will generate a list of variants for exclusion. See [Phasing with a reference panel Step2](https://mathgen.stats.ox.ac.uk/genetics_software/shapeit/shapeit.html#reference).

Finally, excluded the mismatched variants and run phasing using 1KG PhaseI EAS samples as reference.

```
excludesnp=${outputlogcheck}.snp.strand.exclude
echo "EAS" > group.list
includegrp=group.list

shapeit --input-bed ${inputbedchr22} \
        --input-map ${geneticmap} \
        --input-ref ${inputrefhap} ${inputreflegend} ${inputrefsample} \
        --output-max ${outputhaps} ${outputsample} \
        --output-log ${outputlog} \
        --exclude-snp  ${excludesnp} \
        --thread 1 \
        --include-grp ${includegrp} \
        --seed 123 \
        --states 200 \
        --window 2
```

This command will generate a haplotype file `.hap` and a sample file `.sample`. We need to convert the files to VCF, compress and index the VCF for downstream analysis.

```
outputvcf=${out}.vcf

shapeit \
    -convert \
	--input-haps ${outputhaps} ${outputsample} \
    --output-vcf ${outputvcf}

bgzip ${outputvcf} && \
tabix -p vcf ${outputvcf}.gz
```

A look at the phased VCF:

`|` indicates that the genotypes are phased.

```
##fileformat=VCFv4.1
##fileDate=16102024_11h58m32s
##source=SHAPEIT2.v904
##log_file=shapeit_16102024_11h58m32s_53660203-b6af-49ba-a054-ae0fdd303a78.log
##FORMAT=<ID=GT,Number=1,Type=String,Description="Phased Genotype">
#CHROM  POS     ID      REF     ALT     QUAL    FILTER  INFO    FORMAT  NA18939 NA18940 NA18941 NA18942 NA18943 NA18944
NA18945 NA18946 NA18947 NA18948 NA18949 NA18950 NA18951 NA18952 NA18953 NA18954 NA18956 NA18957 NA18959 NA18960 NA18961
NA18962 NA18964 NA18965 NA18966 NA18967 NA18968 NA18969 NA18970 NA18971 NA18972 NA18973 NA18974 NA18975 NA18976 NA18977
NA18978 NA18979 NA18980 NA18981 NA18982 NA18983 NA18984 NA18985 NA18986 NA18987 NA18988 NA18989 NA18990 NA18991 NA18992
NA18993 NA18994 NA18995 NA18997 NA18998 NA18999 NA19000 NA19001 NA19002 NA19003 NA19004 NA19005 NA19006 NA19007 NA19009
NA19010 NA19011 NA19012 NA19054 NA19055 NA19056 NA19057 NA19058 NA19059 NA19060 NA19062 NA19063 NA19064 NA19065 NA19066
NA19067 NA19068 NA19070 NA19072 NA19074 NA19075 NA19076 NA19077 NA19078 NA19079 NA19080 NA19081 NA19082 NA19083 NA19084
NA19085 NA19086 NA19087 NA19088 NA19089 NA19090 NA19091
22      16051453        22:16051453:A:C C       A       .       PASS    .       GT      1|1     1|1     1|1     1|1
1|1     1|1     0|1     1|1     1|1     1|1     1|1     0|1     0|1     1|1     1|1     1|1     1|1     1|1     1|1
1|1     1|1     1|1     1|1     1|1     1|1     1|1     1|1     1|1     1|1     1|1     1|1     1|1     0|1     1|1
0|1     1|1     1|1     1|1     1|1     1|1     1|1     1|1     0|1     1|1     0|1     1|1     1|1     1|1     1|1
1|1     0|1     1|1     0|1     1|1     1|1     1|1     1|1     1|1     1|1     1|1     1|1     1|1     1|1     1|1
1|1     1|1     1|1     1|1     1|1     1|1     1|1     1|1     1|1     0|1     0|1     1|1     1|1     1|1     0|1
1|1     1|1     0|1     1|1     1|1     1|1     1|1     1|1     1|1     0|1     1|1     0|1     1|1     1|1     1|1
1|1     1|1     1|1     1|1     1|1     1|1     1|1     1|1     1|1
```

## Phasing using Eagle 

Next, we will use Eagle2  as an example for cohort-based phasing.

!!! quote
	Loh, P. R., Danecek, P., Palamara, P. F., Fuchsberger, C., A Reshef, Y., K Finucane, H., ... & L Price, A. (2016). Reference-based phasing using the Haplotype Reference Consortium panel. Nature genetics, 48(11), 1443-1448.

Download Eagle  from [Eagle2 website](https://alkesgroup.broadinstitute.org/Eagle/). Unzip and add it to your environment. We also need genetic maps, which are also available on [Eagle2 website](https://alkesgroup.broadinstitute.org/Eagle/)

Cohort-based phasing (without reference) using eagle2. Eagle2 

```
inputbedchr22=./sample_data.chr22.clean
geneticmap=~/tools/eagle/genetic_map_hg19_withX.txt.gz
out=./1KG.JPT.chr22.phased.eagle2.cohort_based

eagle \
    --bfile=${inputbedchr22} \
    --geneticMapFile=${geneticmap} \
    --outPrefix=${out} \
    --maxMissingPerSnp=1 \
    --maxMissingPerIndiv=1 \
    --numThreads=4 \
    --chrom=22
```

Use shapeit2 to convert `.hap` and `.sample` to VCF

```
outputhaps=${out}.haps.gz
outputsample=${out}.sample
outputvcf=${out}.vcf

shapeit \
    -convert \
    --input-haps ${outputhaps} ${outputsample} \
    --output-vcf ${outputvcf}

bgzip ${outputvcf} && \
tabix -p vcf ${outputvcf}.gz
```


```
##fileformat=VCFv4.1
##fileDate=16102024_17h46m51s
##source=SHAPEIT2.v904
##log_file=shapeit_16102024_17h46m51s_16aef2b1-de11-4c78-b8a6-f15bf1c2d14b.log
##FORMAT=<ID=GT,Number=1,Type=String,Description="Phased Genotype">
#CHROM  POS     ID      REF     ALT     QUAL    FILTER  INFO    FORMAT  NA18939 NA18940 NA18941 NA18942 NA18943 NA18944NA18945  NA18946 NA18947 NA18948 NA18949 NA18950 NA18951 NA18952 NA18953 NA18954 NA18956 NA18957 NA18959 NA18960 NA18961NA18962  NA18964 NA18965 NA18966 NA18967 NA18968 NA18969 NA18970 NA18971 NA18972 NA18973 NA18974 NA18975 NA18976 NA18977NA18978  NA18979 NA18980 NA18981 NA18982 NA18983 NA18984 NA18985 NA18986 NA18987 NA18988 NA18989 NA18990 NA18991 NA18992NA18993  NA18994 NA18995 NA18997 NA18998 NA18999 NA19000 NA19001 NA19002 NA19003 NA19004 NA19005 NA19006 NA19007 NA19009NA19010  NA19011 NA19012 NA19054 NA19055 NA19056 NA19057 NA19058 NA19059 NA19060 NA19062 NA19063 NA19064 NA19065 NA19066NA19067  NA19068 NA19070 NA19072 NA19074 NA19075 NA19076 NA19077 NA19078 NA19079 NA19080 NA19081 NA19082 NA19083 NA19084NA19085  NA19086 NA19087 NA19088 NA19089 NA19090 NA19091
22      16051453        22:16051453:A:C C       A       .       PASS    .       GT      1|1     1|1     1|1     1|1    1|1      1|1     0|1     1|1     1|1     1|1     1|1     1|0     1|0     1|1     1|1     1|1     1|1     1|1     1|1    1|1      1|1     1|1     1|1     1|1     1|1     1|1     1|1     1|1     1|1     1|1     1|1     1|1     0|1     1|1    0|1      1|1     1|1     1|1     1|1     1|1     1|1     1|1     0|1     1|1     0|1     1|1     1|1     1|1     1|1    1|1      0|1     1|1     1|0     1|1     1|1     1|1     1|1     1|1     1|1     1|1     1|1     1|1     1|1     1|1    1|1      1|1     1|1     1|1     1|1     1|1     1|1     1|1     1|1     0|1     0|1     1|1     1|1     1|1     0|1    1|1      1|1     1|0     1|1     1|1     1|1     1|1     1|1     1|1     1|0     1|1     1|0     1|1     1|1     1|1    1|1      1|1     1|1     1|1     1|1     1|1     1|1     1|1     1|1
```
