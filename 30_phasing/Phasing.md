# Phasing

The human genome is diploid, meaning each individual carries two copies of each chromosome (one inherited from each parent). A **haplotype** is the combination of alleles on a single chromosome copy that are inherited together. **Phasing** (also called haplotype phasing) is the process of determining which alleles at different variant sites are located on the same chromosome copy (i.e., on the same haplotype). 

Standard genotyping methods typically produce unphased data, where we know an individual's genotypes at each position but not which alleles are physically linked together on the same chromosome. The distribution of variants between the two homologous chromosomes can significantly affect the interpretation of genotype data. For example, phasing is essential for:

- **Allele-specific expression**: Understanding which parental allele is expressed
- **Context-informed annotation**: Determining the functional impact of variant combinations
- **Loss-of-function compound heterozygous events**: Identifying when different mutations on different chromosomes result in gene knockout 

!!! example "Simple example of phasing"
    Consider two variants in a gene:

    - Variant A: position 1000, alleles C/T
    - Variant B: position 2000, alleles G/A
    
    An individual with unphased genotypes:

    - Variant A: `0/1` (heterozygous, C/T)
    - Variant B: `0/1` (heterozygous, G/A)
    
    Without phasing, we don't know which alleles are on the same chromosome. There are two possibilities:
    
    - **Possibility 1**: Chromosome 1 has C and G; Chromosome 2 has T and A → `C|G` and `T|A`
    - **Possibility 2**: Chromosome 1 has C and A; Chromosome 2 has T and G → `C|A` and `T|G`
    
    Phasing resolves this ambiguity by determining which alleles are on the same chromosome (same haplotype). This is crucial for understanding compound heterozygotes, where two different mutations on different chromosomes can cause disease.

!!! example "Example: Loss-of-function (LoF) variants and gene knockout"
    Consider a gene with two loss-of-function (LoF) variants:

    - Variant X: position 5000, LoF mutation (e.g., frameshift)
    - Variant Y: position 8000, LoF mutation (e.g., stop gain)
    
    An individual with unphased genotypes:

    - Variant X: `0/1` (heterozygous, one LoF allele)
    - Variant Y: `0/1` (heterozygous, one LoF allele)
    
    Without phasing, we cannot determine if both LoF variants are on the same chromosome or different chromosomes:

    - **Scenario 1**: Both LoF variants on the same chromosome → `LoF_X|LoF_Y` and `WT|WT`
      - One functional copy remains → Gene is **NOT knocked out**
    - **Scenario 2**: LoF variants on different chromosomes → `LoF_X|WT` and `WT|LoF_Y`
      - Both copies have a LoF variant → Gene is **knocked out**
    
    Phasing resolves this by determining the haplotype structure. When LoF variants are on both copies of a gene (different chromosomes), the gene is considered knocked out.
    
    (Reference: [SHAPEIT5](https://www.biorxiv.org/content/10.1101/2022.10.19.512867v2.full))

Trio data and long read sequencing can directly solve the haplotyping problem, but these approaches are not always available. When direct phasing is not possible, **statistical phasing methods** are used. 

---


**On this page**

[TOC]

---


## The Li & Stephens 2003 Model

Statistical phasing is fundamentally based on the [Li & Stephens 2003](https://academic.oup.com/genetics/article/165/4/2213/6050566) Markov model, which provides a probabilistic framework for reconstructing haplotypes from unphased genotype data. The model operates under the key assumption that an individual's haplotype can be modeled as a mosaic of haplotypes from a reference panel (or other individuals in the cohort).

---


### Key Concepts

The Li & Stephens model treats haplotype reconstruction as a hidden Markov model (HMM) where:

1. **Reference panel**: A set of known haplotypes (typically from a reference population) serves as templates
2. **Mosaic structure**: Each target haplotype is modeled as a series of segments copied from different reference haplotypes
3. **Recombination events**: Transitions between copied segments represent historical recombination events
4. **Mutation/error model**: Allows for differences between the target haplotype and the copied reference segments

---


### Mathematical Framework

For a diploid individual, the model treats the two haplotypes (maternal and paternal) as independent. The unphased genotype at each position is constructed by combining alleles from the two haplotypes. The haploid version of this model (used in imputation) is conceptually simpler, as it only needs to reconstruct a single haplotype rather than two.

The model uses:

- **Transition probabilities**: Govern how often the model switches between copying from different reference haplotypes (related to recombination rates)
- **Emission probabilities**: Account for differences between the observed genotype and the reference haplotypes (related to mutation and genotyping error rates)

---


### Modern Extensions

Recent methods have incorporated long IBD (Identity by Descent) sharing, local haplotype clustering, and other computational advances to make phasing tractable for large-scale datasets. The following methods are commonly used for statistical phasing:

- [PHASE](https://linkinghub.elsevier.com/retrieve/pii/S0002929707633412)
- [MaCH](https://onlinelibrary.wiley.com/doi/full/10.1002/gepi.20533)
- [EAGLE2](https://www.nature.com/articles/ng.3679)
- [SHAPEIT5](https://www.biorxiv.org/content/10.1101/2022.10.19.512867v2.full)
- [BEAGLE3](http://www.cell.com/article/S0002929709000123/fulltext)

---



## How to do phasing

In most cases for GWAS, phasing is now a **pre-step of imputation** (a strategy known as "pre-phasing" [Howie et al. 2012](https://pmc.ncbi.nlm.nih.gov/articles/PMC3696580/)). This two-step approach—first statistically estimating haplotypes for each study individual, then imputing missing genotypes into these estimated haplotypes—offers significant computational advantages:

1. **Efficiency**: GWAS samples need to be phased only once, whereas traditional imputation methods implicitly re-phase with each reference panel update
2. **Speed**: It is much faster to match a phased GWAS haplotype to one reference haplotype than to match unphased GWAS genotypes to a pair of reference haplotypes
3. **Flexibility**: The same phased haplotypes can be reused with different or updated reference panels without re-phasing, which is particularly valuable as reference panels evolve and expand

The specific phasing method may not be critical for downstream imputation accuracy, but there are several important considerations when choosing a phasing method, including whether to use reference-based or reference-free phasing, sample size (large vs. small cohorts), and rare variant cutoffs. There is no single method that best fits all cases. 

We will show two examples:

- Reference-based phasing using SHAPEIT2
- Cohort-based phasing using Eagle2

!!! note "Required data and tools"

    - **Genotype data (PLINK binary)** — QC'd `.bed`/`.bim`/`.fam`; this tutorial starts from `sample_data.clean` produced in [04_Data_QC](../04_Data_QC/README.md). Alleles are then matched to the **reference genome FASTA** before phasing (see [Prepare for phasing](#prepare-for-phasing)).
    - **Reference genome FASTA (GRCh37)** — same assembly as the tutorial data and SHAPEIT2 reference (e.g. **human_g1k_v37** from the [1000 Genomes FTP](https://ftp.1000genomes.ebi.ac.uk/vol1/ftp/technical/reference/)); keep contig names consistent with your `.bim` (here `1`, `2`, …). If needed, build an index with `samtools faidx your.fasta`.
    - **Sample list (optional)** — plain-text `--keep` file to subset individuals; the examples use `JPT.sample` from [01_Dataset](../01_Dataset/README.md).
    - **PLINK 2** (`plink2`) — to align alleles with `--ref-from-fa` (see below) and to subset by chromosome, MAF, and samples before phasing.
    - **SHAPEIT2** — for reference-based phasing; install from the [SHAPEIT2 download page](https://mathgen.stats.ox.ac.uk/genetics_software/shapeit/shapeit.html#download). You also need the **1000 Genomes Phase I integrated haplotypes** (SHAPEIT2 format, **b37**), plus **per-chromosome genetic maps**, from the [IMPUTE2 reference data](https://mathgen.stats.ox.ac.uk/impute/impute_v2.html#reference) (as described in the SHAPEIT2 documentation).
    - **Eagle2** — for cohort-based phasing; install from the [Eagle website](https://alkesgroup.broadinstitute.org/Eagle/). Download a **genetic map** for your genome build (the examples use a **hg19/GRCh37** map such as `genetic_map_hg19_withX.txt.gz`).
    - **`bgzip` and `tabix`** — to compress and index phased VCFs (typically from [HTSlib](https://www.htslib.org/) or [BCFtools](https://samtools.github.io/bcftools/)). The Eagle2 example uses **SHAPEIT2’s** `-convert` to write VCF, then `bgzip`/`tabix`.

    Example commands assume **GRCh37/b37**. Your study genotypes, reference panel, and genetic maps must all use the **same genome build**.

---


## Prepare for phasing

Before phasing, alleles should match the **reference base on the genome assembly** you use for the reference panel (here **GRCh37 / b37**). With **PLINK 2**, point `--fa` at that assembly’s FASTA and use `--ref-from-fa` so each variant’s reference allele is taken from the sequence at the `.bim` position (see also [Alleles — reference from FASTA](../36_alleles/README.md)).

If you do not already have **human_g1k_v37** (1000 Genomes GRCh37 reference), download and decompress it (optional: the `.fai` index for random access):

```
mkdir -p "${HOME}/refs"
cd "${HOME}/refs"
wget https://ftp.1000genomes.ebi.ac.uk/vol1/ftp/technical/reference/human_g1k_v37.fasta.gz
wget https://ftp.1000genomes.ebi.ac.uk/vol1/ftp/technical/reference/human_g1k_v37.fasta.fai
gunzip human_g1k_v37.fasta.gz
cd -
```

!!! tip
    If you skip the `.fai` download, build an index after decompressing: `samtools faidx "${HOME}/refs/human_g1k_v37.fasta"`.

```
before_alignment_bfile="../04_Data_QC/sample_data.clean"
after_alignment_bfile="./sample_data.clean.alignment"
ref_fasta="${HOME}/refs/human_g1k_v37.fasta"   # same build as 1KG tutorial data / SHAPEIT2 refs

plink2 \
    --bfile ${before_alignment_bfile} \
    --fa ${ref_fasta} \
    --ref-from-fa \
    --make-bed \
    --out ${after_alignment_bfile}
```

!!! tip
    If PLINK 2 exits because some variants already have a “known” reference allele that disagrees with the FASTA, rerun with **`--ref-from-fa force`** (only after you are sure the FASTA and coordinates are correct). Indels and some complex alleles may not be set from FASTA alone.

---


## Subset PLINK data for phasing (shared input)

The SHAPEIT2 and Eagle2 examples below intentionally use **the same** PLINK binary prefix (`sample_data.chr22.clean`) so both tools read identical samples and SNPs (JPT only, chromosome 22, MAF ≥ 0.05). Run this **once** after [Prepare for phasing](#prepare-for-phasing); do not rebuild a separate extract for each tool.

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

**Eagle2** uses this prefix as `--bfile=${inputbedchr22}` for cohort phasing. **SHAPEIT2** needs the further restriction described in [Restrict study SNPs to the SHAPEIT2 reference panel](#restrict-study-snps-to-the-shapeit2-reference-panel): it phases a subset `sample_data.chr22.shapeit_ref` that matches the Phase I legend (same samples as above, fewer SNPs).

!!! tip
    Usually, we also remove G/C or A/T SNPs before phasing.

!!! note "Runnable scripts"
    The same workflow is scripted in `30_phasing/`: `prepare.phasing.sh`, then `phasing_shapeit2.sh` and/or `phasing_eagle2.sh`. See `README.md` in that folder.

---


## Phasing using SHAPEIT2

Here, we show an example using SHAPEIT2, which is another commonly used tool for haplotype phasing. SHAPEIT2 is usually used for small cohorts.

!!! note
    We will do a phasing for 1KG EAS samples using 1KG as reference, which does not make any sense. This is just to demonstrate how to do reference-based phasing using SHAPEIT2.

!!! quote
    Delaneau, O., Zagury, J. F., & Marchini, J. (2013). Improved whole-chromosome phasing for disease and population genetic studies. Nature methods, 10(1), 5-6.

We will conduct a reference-based phasing using SHAPEIT2 for chromosome 22.

First, download SHAPEIT2 from [SHAPEIT2 website](https://mathgen.stats.ox.ac.uk/genetics_software/shapeit/shapeit.html#download). Unzip and add it to your environment. We also need reference files (1000 Genomes Phase I integrated haplotypes (produced using SHAPEIT2) b37 June 2014) and genetic maps, which are also available on [SHAPEIT2 website](https://mathgen.stats.ox.ac.uk/impute/impute_v2.html#reference)

Use **`inputbedchr22`** from [Subset PLINK data for phasing (shared input)](#subset-plink-data-for-phasing-shared-input) (`sample_data.chr22.clean`).

---


### Restrict study SNPs to the SHAPEIT2 reference panel

The IMPUTE2 / SHAPEIT2 **Phase I integrated** reference haplotypes only cover a fixed SNP list. The tutorial chr22 extract usually contains **extra** SNPs (e.g. from a later 1KG release), which makes `shapeit -check` fail with *Reference and Main panels are not well aligned*.

To avoid reading the large `legend.gz` every time, this repository ships **`chr22_phase1_shapeit_panel_positions.txt`**: one GRCh37 **bp position per line** (with `#` comments), precomputed as the intersection of the Phase I chr22 **SNP** legend and **`sample_data.chr22.clean.bim`** (including allele match). At runtime, **only the study `.bim`** is scanned: keep variant IDs whose physical position (column 4) is in that list, then `plink2 --extract`.

```
inputbedchr22=./sample_data.chr22.clean
shapeit_positions=./chr22_phase1_shapeit_panel_positions.txt
shapeit_extract=./shapeit_chr22.refpanel_snps.txt
inputbedshapeit=./sample_data.chr22.shapeit_ref

awk -v chr=22 -v posfile=${shapeit_positions} '
BEGIN {
  while ((getline p < posfile) > 0) {
    if (p ~ /^#/ || p == "") continue
    keep[p + 0] = 1
  }
  close(posfile)
}
$1 == chr && keep[$4] {
  print $2
}' ${inputbedchr22}.bim > ${shapeit_extract}

plink2 \
    --bfile ${inputbedchr22} \
    --extract ${shapeit_extract} \
    --make-bed \
    --out ${inputbedshapeit}
```

Use **`inputbedshapeit`** (not `inputbedchr22`) in all SHAPEIT2 commands below. **Eagle2** keeps **`inputbedchr22`** (same samples, full SNP set).

!!! note "Other cohorts or builds"
    If your `.bim` changes, regenerate `chr22_phase1_shapeit_panel_positions.txt` once (e.g. with a short `awk` over `zcat …legend.gz` and your `.bim` to require `SNP` rows and matching alleles), or set `SHAPEIT_PANEL_POSITIONS` when running `phasing_shapeit2.sh`.

Then check alignment between this reduced study panel and the reference haplotypes:

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
        -B ${inputbedshapeit} \
        -M ${geneticmap} \
        --input-ref ${inputrefhap} ${inputreflegend} ${inputrefsample} \
        --output-log ${outputlogcheck}
```
This command will generate a list of variants for exclusion. See [Phasing with a reference panel Step2](https://mathgen.stats.ox.ac.uk/genetics_software/shapeit/shapeit.html#reference).

Finally, exclude the mismatched variants and run phasing using 1KG PhaseI EAS samples as reference.

```
excludesnp=${outputlogcheck}.snp.strand.exclude
echo "EAS" > group.list
includegrp=group.list

shapeit --input-bed ${inputbedshapeit} \
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

!!! note "VCF genotype notation"
    In VCF files, the separator between alleles in the GT (genotype) field has different meanings:
    - `/` (forward slash): Indicates **unphased** genotypes (e.g., `0/1` means heterozygous, but the phase is unknown)
    - `|` (pipe): Indicates **phased** genotypes (e.g., `0|1` means the first allele is on one chromosome and the second allele is on the homologous chromosome)
    
    This tutorial demonstrates the phasing workflow. After phasing, genotypes should use `|` to indicate they are phased.

After `bgzip` and `tabix`, you get a standard VCF whose `GT` field uses `|` for phased alleles. A verbatim header and first-variant line from the current tutorial file `1KG.JPT.chr22.phased.eagle2.cohort_based.vcf.gz` (cohort-based Eagle2, then the same `shapeit -convert` step) are shown at the end of the [Phasing using Eagle](#phasing-using-eagle) section. Reference-based SHAPEIT2 uses the same VCF layout after conversion; phasing calls need not match Eagle site-for-site.

---


## Phasing using Eagle 

Next, we will use Eagle2  as an example for cohort-based phasing.

!!! quote
    Loh, P. R., Danecek, P., Palamara, P. F., Fuchsberger, C., A Reshef, Y., K Finucane, H., ... & L Price, A. (2016). Reference-based phasing using the Haplotype Reference Consortium panel. Nature genetics, 48(11), 1443-1448.

Download Eagle  from [Eagle2 website](https://alkesgroup.broadinstitute.org/Eagle/). Unzip and add it to your environment. We also need genetic maps, which are also available on [Eagle2 website](https://alkesgroup.broadinstitute.org/Eagle/)

Cohort-based phasing (without reference) using Eagle2. Use the **same** **`inputbedchr22`** prefix as SHAPEIT2 ([shared subset](#subset-plink-data-for-phasing-shared-input)); do not run a second `plink2` extract with different filters.

```
inputbedchr22=./sample_data.chr22.clean   # same PLINK prefix as SHAPEIT2 (shared subset step)
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

Excerpt from `1KG.JPT.chr22.phased.eagle2.cohort_based.vcf.gz` after a tutorial run (`##fileDate` / `##log_file` will change when you rerun):

```
##fileformat=VCFv4.1
##fileDate=06042026_14h11m12s
##source=SHAPEIT2.v904
##log_file=shapeit_06042026_14h11m12s_d2d9364e-df91-419a-99c5-4fa00c90526e.log
##FORMAT=<ID=GT,Number=1,Type=String,Description="Phased Genotype">
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	NA18939	NA18940	NA18941	NA18942	NA18943	NA18944	NA18945	NA18946	NA18947	NA18948	NA18949	NA18950	NA18951	NA18952	NA18953	NA18954	NA18956	NA18957	NA18959	NA18960	NA18961	NA18962	NA18964	NA18965	NA18966	NA18967	NA18968	NA18969	NA18970	NA18971	NA18972	NA18973	NA18974	NA18975	NA18976	NA18977	NA18978	NA18979	NA18980	NA18981	NA18982	NA18983	NA18984	NA18985	NA18986	NA18987	NA18988	NA18989	NA18990	NA18991	NA18992	NA18993	NA18994	NA18995	NA18997	NA18998	NA18999	NA19000	NA19001	NA19002	NA19003	NA19004	NA19005	NA19006	NA19007	NA19009	NA19010	NA19011	NA19012	NA19054	NA19055	NA19056	NA19057	NA19058	NA19059	NA19060	NA19062	NA19063	NA19064	NA19065	NA19066	NA19067	NA19068	NA19070	NA19072	NA19074	NA19075	NA19076	NA19077	NA19078	NA19079	NA19080	NA19081	NA19082	NA19083	NA19084	NA19085	NA19086	NA19087	NA19088	NA19089	NA19090	NA19091
22	16051453	22:16051453:A:C	C	A	.	PASS	.	GT	1|1	1|1	1|1	1|1	1|1	1|1	0|1	1|1	1|1	1|1	1|1	1|0	1|0	1|1	1|1	1|1	1|1	1|1	1|1	1|1	1|1	1|1	1|1	1|1	1|1	1|1	1|1	1|1	1|1	1|1	1|1	1|1	0|1	1|1	0|1	1|1	1|1	1|1	1|1	1|1	1|1	1|1	0|1	1|1	0|1	1|1	1|1	1|1	1|1	1|1	0|1	1|1	1|0	1|1	1|1	1|1	1|1	1|1	1|1	1|1	1|1	1|1	1|1	1|1	1|1	1|1	1|1	1|1	1|1	1|1	1|1	1|1	1|1	0|1	0|1	1|1	1|1	1|1	0|1	1|1	1|1	1|0	1|1	1|1	1|1	1|1	1|1	1|1	1|0	1|1	1|0	1|1	1|1	1|1	1|1	1|1	1|1	1|1	1|1	1|1	1|1	1|1	1|1
```

---


## References

- (**Li & Stephens model**) Li, N., & Stephens, M. (2003). Modeling linkage disequilibrium and identifying recombination hotspots using single-nucleotide polymorphism data. Genetics, 165(4), 2213-2233. https://doi.org/10.1093/genetics/165.4.2213

- (**Pre-phasing strategy**) Howie, B., Fuchsberger, C., Stephens, M., Marchini, J., & Abecasis, G. R. (2012). Fast and accurate genotype imputation in genome-wide association studies through pre-phasing. Nature Genetics, 44(8), 955-959. https://doi.org/10.1038/ng.2354

- (**PHASE**) Stephens, M., Smith, N. J., & Donnelly, P. (2001). A new statistical method for haplotype reconstruction from population data. The American Journal of Human Genetics, 68(4), 978-989. https://doi.org/10.1086/319501

- (**MaCH**) Li, Y., Willer, C. J., Ding, J., Scheet, P., & Abecasis, G. R. (2010). MaCH: using sequence and genotype data to estimate haplotypes and unobserved genotypes. Genetic Epidemiology, 34(8), 816-834. https://doi.org/10.1002/gepi.20533

- (**EAGLE2**) Loh, P. R., Danecek, P., Palamara, P. F., Fuchsberger, C., A Reshef, Y., K Finucane, H., ... & L Price, A. (2016). Reference-based phasing using the Haplotype Reference Consortium panel. Nature Genetics, 48(11), 1443-1448. https://doi.org/10.1038/ng.3679

- (**SHAPEIT2**) Delaneau, O., Zagury, J. F., & Marchini, J. (2013). Improved whole-chromosome phasing for disease and population genetic studies. Nature Methods, 10(1), 5-6. https://doi.org/10.1038/nmeth.2307

- (**SHAPEIT5**) Delaneau, O., Zagury, J. F., Robinson, M. R., Marchini, J. L., & Dermitzakis, E. T. (2019). Accurate, scalable and integrative haplotype estimation. Nature Communications, 10(1), 5436. https://doi.org/10.1038/s41467-019-13225-y

- (**BEAGLE**) Browning, S. R., & Browning, B. L. (2007). Rapid and accurate haplotype phasing and missing-data inference for whole-genome association studies by use of localized haplotype clustering. The American Journal of Human Genetics, 81(5), 1084-1097. https://doi.org/10.1086/521987
