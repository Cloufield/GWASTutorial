# PLINK basics

In this module, we will learn the basics of genotype data QC using PLINK, which is one of the most commonly used software in complex trait genomics. (Huge thanks to the developers: [PLINK1.9](https://www.cog-genomics.org/plink/1.9/credits) and [PLINK2](https://www.cog-genomics.org/plink/2.0/credits))

## Table of Contents
- [Preparation](#preparation)
	- [PLINK 1.9 & 2 installation](#plink-192-installation)
	- [Download genotype data](#download-genotype-data)
- [PLINK tutorial](#plink-tutorial)
	- [Calculate the missing rate and call rate](#missing-rate-call-rate)
	- [Calculate allele frequency](#allele-frequency)
	- [Hardy-Weinberg equilibrium exact test](#hardy-weinberg-equilibrium-exact-test)
	- [Applying filters](#applying-filters)
	- [LD-Pruning](#LD-pruning)
    - [Calculate the inbreeding F coefficient ](#inbreeding-f-coefficient)
	- [Sample & SNP filtering (extract/exclude/keep/remove)](#sample--snp-filtering-extractexcludekeepremove)
	- [LD calculation](#ld-calculation)
	- [Estimate IBD / PI_HAT](#ibd--pi_hat--kinship-coefficient)
	- [Data management (make-bed/recode)](#data-management-make-bedrecode)
    - [Apply all the filters to obtain a clean dataset](#apply-all-the-filters-to-obtain-a-clean-dataset)
    - [Other common QC steps not included in this tutorial](#other-common-qc-steps-not-included-in-this-tutorial)
- [Exercise](#exercise)
- [Additional resources](#additional-resources)
- [Reference](#reference)

## Preparation

### PLINK 1.9&2 installation

To get prepared for genotype QC, we will need to make directories, download software and add the software to your environment path.

First, we will simply create some directories to keep the tools we need to use.


!!! example "Create directories"
    ```bash
    cd ~
    mkdir tools
    cd tools
    mkdir bin
    mkdir plink
    mkdir plink2
    ```
    <img width="937" alt="image" src="https://user-images.githubusercontent.com/40289485/160745597-c6f4204a-d786-4af1-9041-f1531cbbe584.png">
    
You can download each tool into its corresponding directories. 

The `bin` directory here is for keeping all the symbolic links to the executable files of each tool. 

In this way, it is much easier to manage and organize the paths and tools. We will only add the `bin` directory here to the environment path.

### Download PLINK1.9 and PLINK2 and then unzip
Next, go to the Plink webpage to download the software. We will need both PLINK1.9 and PLINK2.

Download PLINK1.9 and PLINK2 from the following webpage to the corresponding directories:

- PLINK1.9 : [https://www.cog-genomics.org/plink/](https://www.cog-genomics.org/plink/)
- PLINK2 : [https://www.cog-genomics.org/plink/2.0/](https://www.cog-genomics.org/plink/2.0/)

!!! info
    If you are using Mac or Windows, then please download the Mac or Windows version. In this tutorial, we will use a Linux system and the Linux version of PLINK. 

Find the suitable version on the PLINK website, right-click and copy the link address.

!!! example "Download PLINK2 (Linux AVX2 AMD)"
    ```bash
    cd ~/tools/plink2
    wget https://s3.amazonaws.com/plink2-assets/alpha5/plink2_linux_amd_avx2_20231212.zip
    unzip plink2_linux_amd_avx2_20231212.zip
    ```
Then do the same for PLINK1.9

!!! example "Download PLINK1.9 (Linux 64-bit)"
    ```bash
    cd ~/tools/plink
    wget https://s3.amazonaws.com/plink1-assets/plink_linux_x86_64_20231211.zip
    unzip plink_linux_x86_64_20231211.zip
    ```



### Create symbolic links

After downloading and unzipping, we will create symbolic links for the plink binary files, and then move the link to `~/tools/bin/`.

!!! example "Create symbolic links"
    ```bash
    cd ~
    ln -s ~/tools/plink2/plink2 ~/tools/bin/plink2
    ln -s ~/tools/plink/plink ~/tools/bin/plink
    ```

### Add paths to the environment path

Then add `~/tools/bin/` to the environment path.

!!! example
    
    ```bash
    export PATH=$PATH:~/tools/bin/
    ```
    This command will add the path to your current shell. 
    
    If you restart the terminal, it will be lost. So you may need to add it to the Bash  configuration file. Then run 
    
    ```
    echo "export PATH=$PATH:~/tools/bin/" >> ~/.bashrc
    ```
    
    This will add a new line at the end of `.bashrc`, which will be run every time you open a new bash shell.

All done. Let's test if we installed PLINK successfully or not.

!!! example "Check if PLINK is installed successfully."

    ```bash
    ./plink
    PLINK v1.90b7.2 64-bit (11 Dec 2023)           www.cog-genomics.org/plink/1.9/
    (C) 2005-2023 Shaun Purcell, Christopher Chang   GNU General Public License v3

    plink <input flag(s)...> [command flag(s)...] [other flag(s)...]
    plink --help [flag name(s)...]

    Commands include --make-bed, --recode, --flip-scan, --merge-list,
    --write-snplist, --list-duplicate-vars, --freqx, --missing, --test-mishap,
    --hardy, --mendel, --ibc, --impute-sex, --indep-pairphase, --r2, --show-tags,
    --blocks, --distance, --genome, --homozyg, --make-rel, --make-grm-gz,
    --rel-cutoff, --cluster, --pca, --neighbour, --ibs-test, --regress-distance,
    --model, --bd, --gxe, --logistic, --dosage, --lasso, --test-missing,
    --make-perm-pheno, --tdt, --qfam, --annotate, --clump, --gene-report,
    --meta-analysis, --epistasis, --fast-epistasis, and --score.

    "plink --help | more" describes all functions (warning: long).
    ```
    
    ```bash
    ./plink2
    PLINK v2.00a5.9LM AVX2 AMD (12 Dec 2023)       www.cog-genomics.org/plink/2.0/
    (C) 2005-2023 Shaun Purcell, Christopher Chang   GNU General Public License v3

    plink2 <input flag(s)...> [command flag(s)...] [other flag(s)...]
    plink2 --help [flag name(s)...]

    Commands include --rm-dup list, --make-bpgen, --export, --freq, --geno-counts,
    --sample-counts, --missing, --hardy, --het, --fst, --indep-pairwise, --ld,
    --sample-diff, --make-king, --king-cutoff, --pmerge, --pgen-diff,
    --write-samples, --write-snplist, --make-grm-list, --pca, --glm, --adjust-file,
    --gwas-ssf, --clump, --score, --variant-score, --genotyping-rate, --pgen-info,
    --validate, and --zst-decompress.

    "plink2 --help | more" describes all functions.
    ```
    
Well done. We have successfully installed plink1.9 and plink2.


### Download genotype data

Next, we need to download the sample genotype data. The way to create the sample data is described [here].(https://cloufield.github.io/GWASTutorial/01_Dataset/)
This dataset contains 504 EAS individuals from 1000 Genome Project Phase 3v5 with around 1 million variants.

Simply run `download_sampledata.sh` in 01_Dataset to download this dataset (from Dropbox). See [here](https://cloufield.github.io/GWASTutorial/01_Dataset/#genotype-data-processing)

!!! warning "Sample dataset is currently hosted on Dropbox which may not be accessible for users in certain regions."

!!! example "Download sample data"

    ```bash
    cd ../01_Dataset
    ./download_sampledata.sh
    ```
    
    And you will get the following three PLINK files:
    
    ```
    -rw-r--r-- 1 yunye yunye 149M Dec 26 13:25 1KG.EAS.auto.snp.norm.nodup.split.rare002.common015.missing.bed
    -rw-r--r-- 1 yunye yunye  40M Dec 26 13:25 1KG.EAS.auto.snp.norm.nodup.split.rare002.common015.missing.bim
    -rw-r--r-- 1 yunye yunye  13K Dec 26 13:25 1KG.EAS.auto.snp.norm.nodup.split.rare002.common015.missing.fam
    ```
    
    Check the bim file:
    
    ```bash
    head 1KG.EAS.auto.snp.norm.nodup.split.rare002.common015.missing.bim
    1       1:14930:A:G     0       14930   G       A
    1       1:15774:G:A     0       15774   A       G
    1       1:15777:A:G     0       15777   G       A
    1       1:57292:C:T     0       57292   T       C
    1       1:77874:G:A     0       77874   A       G
    1       1:87360:C:T     0       87360   T       C
    1       1:92917:T:A     0       92917   A       T
    1       1:104186:T:C    0       104186  T       C
    1       1:125271:C:T    0       125271  C       T
    1       1:232449:G:A    0       232449  A       G
    ```
    
    Check the fam file:
    ```bash
    head 1KG.EAS.auto.snp.norm.nodup.split.rare002.common015.missing.fam
    HG00403 HG00403 0 0 0 -9
    HG00404 HG00404 0 0 0 -9
    HG00406 HG00406 0 0 0 -9
    HG00407 HG00407 0 0 0 -9
    HG00409 HG00409 0 0 0 -9
    HG00410 HG00410 0 0 0 -9
    HG00419 HG00419 0 0 0 -9
    HG00421 HG00421 0 0 0 -9
    HG00422 HG00422 0 0 0 -9
    HG00428 HG00428 0 0 0 -9
    ```

## PLINK tutorial

Detailed descriptions can be found on plink's website: [PLINK1.9](https://www.cog-genomics.org/plink/1.9/) and [PLINK2](https://www.cog-genomics.org/plink/2.0/).

The functions we will learn in this tutorial:

1. Calculating missing rate (call rate)
2. Calculating allele Frequency
3. Conducting Hardy-Weinberg equilibrium exact test
4. Applying filters
5. Conducting LD-Pruning
6. Calculating inbreeding F coefficient
7. Conducting sample & SNP filtering (extract/exclude/keep/remove)
8. Estimating IBD / PI_HAT
9. Calculating LD
10. Data management (make-bed/recode)

All sample codes and results for this module are available in `./04_data_QC`

### QC Step Summary

!!! info "QC Step Summary"
    |QC step|Option in PLINK|Commonly used threshold to exclude|
    |-|-|-|
    |SNP missing rate| `--geno`,  `--missing` | missing rate > 0.01 (0.02, or 0.05) |
    |Sample missing rate| `--mind`, `--missing` | missing rate > 0.01 (0.02, or 0.05) |
    |Minor allele frequency| `--freq`, `--maf` |maf < 0.01|
    |Sample Relatedness| `--genome` |pi_hat > 0.2 to exclude second-degree relatives|
    |Hardy-Weinberg equilibrium| `--hwe`,`--hardy`|hwe < 1e-6|
    |Inbreeding F coefficient|`--het`|outside of 3 SD from the mean|

First, we can calculate some basic statistics of our simulated data:

### Missing rate (call rate)

The first thing we want to know is the missing rate of our data. Usually, we need to check the missing rate of samples and SNPs to decide a threshold to exclude low-quality samples and SNPs. (https://www.cog-genomics.org/plink/1.9/basic_stats#missing)

- **Sample missing rate**: the proportion of missing values for an individual across all SNPs.
- **SNP missing rate**: the proportion of missing values for a SNP across all samples.

!!! info "Missing rate and Call rate"

    Suppose we have N samples and M SNPs for each sample.
    
    For sample $j$ :
    
    $$Sample\ Missing\ Rate_{j} = {{N_{missing\ SNPs\ for\ j}}\over{M}} = 1 - Call\ Rate_{sample, j}$$
    
    For SNP $i$ :
    
    $$SNP\ Missing\ Rate_{i} = {{N_{missing\ samples\ at\ i}}\over{N}} = 1 - Call\ Rate_{SNP, i}$$

The input is PLINK bed/bim/fam file. Usually, they have the same prefix, and we just need to pass the prefix to `--bfile` option.

### PLINK syntax

!!! info "PLINK syntax"
    ![image](https://user-images.githubusercontent.com/40289485/161413684-a128b87f-fb79-4b13-a7b5-acfa997c4421.png)

To calculate the missing rate, we need the flag `--missing`, which tells PLINK to calculate the missing rate in the dataset specified by `--bfile`. 

!!! example "Calculate missing rate"
    
    ```bash
    cd ../04_Data_QC
    genotypeFile="../01_Dataset/1KG.EAS.auto.snp.norm.nodup.split.rare002.common015.missing" #!!! Please add your own path here.  "1KG.EAS.auto.snp.norm.nodup.split.rare002.common015.missing" is the prefix of PLINK bed file. 
    
    plink \
    	--bfile ${genotypeFile} \
    	--missing \
    	--out plink_results
    ```
    Remeber to set the value for `${genotypeFile}`.

This code will generate two files `plink_results.imiss` and `plink_results.lmiss`, which contain the missing rate information for samples and SNPs respectively.

Take a look at the `.imiss` file. The last column shows the missing rate for samples. Since we used part of the 1000 Genome Project data this time, there are no missing SNPs in the original datasets. But for educational purposes, we randomly make some of the genotypes missing.

```bash
# missing rate for each sample
head plink_results.imiss
    FID       IID MISS_PHENO   N_MISS   N_GENO   F_MISS
HG00403   HG00403          Y    10020  1235116 0.008113
HG00404   HG00404          Y     9192  1235116 0.007442
HG00406   HG00406          Y    15751  1235116  0.01275
HG00407   HG00407          Y    14653  1235116  0.01186
HG00409   HG00409          Y     5667  1235116 0.004588
HG00410   HG00410          Y     6066  1235116 0.004911
HG00419   HG00419          Y    20000  1235116  0.01619
HG00421   HG00421          Y    17542  1235116   0.0142
HG00422   HG00422          Y    18608  1235116  0.01507
```

```bash
# missing rate for each SNP
head plink_results.lmiss
 CHR              SNP   N_MISS   N_GENO   F_MISS
   1      1:14930:A:G        2      504 0.003968
   1      1:15774:G:A        3      504 0.005952
   1      1:15777:A:G        3      504 0.005952
   1      1:57292:C:T        6      504   0.0119
   1      1:77874:G:A        3      504 0.005952
   1      1:87360:C:T        1      504 0.001984
   1      1:92917:T:A        7      504  0.01389
   1     1:104186:T:C        3      504 0.005952
   1     1:125271:C:T        2      504 0.003968

```

!!! example "Distribution of sample missing rate and SNP missing rate"
    
    Note: The missing values were simulated based on normal distributions for each individual.  
    
    Sample missing rate
    
    ![image](https://github.com/Cloufield/GWASTutorial/assets/40289485/ec776c99-d73f-4cc7-b1e4-d4566acc83df)

    SNP missing rate
    
    ![image](https://github.com/Cloufield/GWASTutorial/assets/40289485/30a11f16-d43e-4e1f-a281-90cf02947916)


For the meaning of headers, please refer to [PLINK documents](https://www.cog-genomics.org/plink/1.9/formats).

### Allele Frequency

One of the most important statistics of SNPs is their frequency in a certain population. Many downstream analyses are based on investigating differences in allele frequencies.

Usually, variants can be categorized into 3 groups based on their Minor Allele Frequency (MAF):

1. **Common variants** : MAF>=0.05
2. **Low-frequency variants** : 0.01<=MAF<0.05
3. **Rare variants** : MAF<0.01

!!! info "How to calculate Minor Allele Frequency (MAF)"
    
    Suppose the reference allele(REF) is A and the alternative allele(ALT) is B for a certain SNP. The posible genotypes are AA, AB and BB.  In a population of N samples (2N alleles), $N = N_{AA} + 2 \times N_{AB} + N_{BB}$ :
    
    - the number of A alleles:  $N_A = 2 \times N_{AA} + N_{AB}$
    - the number of B alleles:  $N_B = 2 \times N_{BB} + N_{AB}$
    
    So we can calculate the allele frequency:
    
    - Reference Allele Frequency : $AF_{REF}= {{N_A}\over{N_A + N_B}}$
    - Alternative Allele Frequency : $AF_{ALT}= {{N_B}\over{N_A + N_B}}$
    
    The MAF for this SNP in this specific population is defined as:
    
    $MAF = min( AF_{REF}, AF_{ALT} )$

For different downstream analyses, we might use different sets of variants. For example, for PCA, we might use only common variants. For gene-based tests, we might use only rare variants.

Using PLINK1.9 we can easily calculate the MAF of variants in the input data.

!!! example "Calculate the MAF of variants using PLINK1.9"
    ```bash
    plink \
    	--bfile ${genotypeFile} \
    	--freq \
    	--out plink_results
    ```
    
    ```bash
    # results from plink1.9
    head plink_results.frq
    CHR              SNP   A1   A2          MAF  NCHROBS
    1      1:14930:A:G    G    A       0.4133     1004
    1      1:15774:G:A    A    G      0.02794     1002
    1      1:15777:A:G    G    A      0.07385     1002
    1      1:57292:C:T    T    C       0.1054      996
    1      1:77874:G:A    A    G      0.01996     1002
    1      1:87360:C:T    T    C      0.02286     1006
    1      1:92917:T:A    A    T     0.003018      994
    1     1:104186:T:C    T    C        0.499     1002
    1     1:125271:C:T    C    T      0.03088     1004
    ```

Next, we use plink2 to run the same options to check the difference between the results.

!!! example "Calculate the alternative allele frequencies of variants using PLINK2"
    ```bash
    plink2 \
            --bfile ${genotypeFile} \
            --freq \
            --out plink_results
    ```
    
    ```bash
    # results from plink2
    head plink_results.afreq
    #CHROM  ID      REF     ALT     PROVISIONAL_REF?        ALT_FREQS       OBS_CT
    1       1:14930:A:G     A       G       Y       0.413347        1004
    1       1:15774:G:A     G       A       Y       0.0279441       1002
    1       1:15777:A:G     A       G       Y       0.0738523       1002
    1       1:57292:C:T     C       T       Y       0.105422        996
    1       1:77874:G:A     G       A       Y       0.0199601       1002
    1       1:87360:C:T     C       T       Y       0.0228628       1006
    1       1:92917:T:A     T       A       Y       0.00301811      994
    1       1:104186:T:C    T       C       Y       0.500998        1002
    1       1:125271:C:T    C       T       Y       0.969124        1004
    ```

We need to pay attention to the concepts here.

In PLINK1.9, the concept here is minor (A1) and major(A2) allele, while in PLINK2 it is the reference (REF) allele and the alternative (ALT) allele.

- **Major / Minor**: Major allele and minor allele are defined as the allele with the highest and lower(or the second highest for multiallelic variants) allele in a given population, respectively. So major and minor alleles for a certain SNP might be different in two independent populations. The range for MAF(minor allele frequencies) is [0,0.5].
- **Ref / Alt**: The reference (REF) and alternative (ALT) alleles are simply determined by the allele on a reference genome. If we use the same reference genome, the reference(REF) and alternative(ALT) alleles will be the same across populations. The reference allele could be major or minor in different populations. The range for alternative allele frequency is [0,1], since it could be the major allele or the minor allele in a given population.




### Hardy-Weinberg equilibrium exact test

For SNP QC, besides checking the missing rate, we also need to check if the SNP is in Hardy-Weinberg equilibrium:

`--hardy` will perform Hardy-Weinberg equilibrium exact test for each variant. Variants with low P value usually suggest genotyping errors, or indicate evolutionary selection for these variants.

The following command can calculate the Hardy-Weinberg equilibrium exact test statistics for all SNPs. (https://www.cog-genomics.org/plink/1.9/basic_stats#hardy)

!!! info
    Suppose we have N unrelated samples (2N alleles).
    Under HWE, the **exact probability** of observing $n_{AB}$ sample with genotype AB in N samples is:

    $$P(N_{AB} = n_{AB} | N, n_A) = {{2^{n_{AB}}}N!\over{n_{AA}!n_{AB}!n_{BB}!}} \times {{n_A!n_B!}\over{(2N)!}} $$
    
    To compute the Hardy-Weinberg equilibrium exact test statistics, we will sum up the probabilities of all configurations with probability equal to or less than the observed configuration :

    $$P_{HWE} = \sum_{n^{*}_AB} I[P(N_{AB} = n_{AB} | N, n_A) \geqq P(N_{AB} = n^{*}_{AB} | N, n_A)] \times P(N_{AB} = n^{*}_{AB} | N, n_A)$$

    $I(x)$ is the indicator function. If x is true, $I(x) = 1$; otherwise, $I(x) = 0$.

    Reference : Wigginton, J. E., Cutler, D. J., & Abecasis, G. R. (2005). A note on exact tests of Hardy-Weinberg equilibrium. The American Journal of Human Genetics, 76(5), 887-893. [Link](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC1199378/)

!!! example "Calculate the Hardy-Weinberg equilibrium exact test statistics for a single SNP using Python"

    This code is converted from [here](https://github.com/jeremymcrae/snphwe/blob/master/src/snp_hwe.cpp) (Jeremy McRae) to python. Orginal citation: Wigginton, JE, Cutler, DJ, and Abecasis, GR (2005) A Note on Exact Tests of Hardy-Weinberg Equilibrium. AJHG 76: 887-893
    ```
    def snphwe(obs_hets: int, obs_hom1: int, obs_hom2: int) -> float:
    """Calculate Hardy-Weinberg equilibrium exact test for a variant

    Args:
        obs_hets (int): observed heterozygous number
        obs_hom1 (int): first observed homozygous number
        obs_hom2 (int): second observed homozygous number

    Returns:
        float: Hardy-Weinberg equilibrium exact test p-value.
        
        - P > 0.05: No significant deviation from Hardy-Weinberg equilibrium (HWE).
        - P ≤ 0.05: Significant deviation from HWE, which could be due to factors such as population stratification, inbreeding, genotyping errors, or natural selection.
    """
    obs_minor_homs = min(obs_hom1, obs_hom2)
    obs_mijor_homs = max(obs_hom1, obs_hom2)

    rare = 2 * obs_minor_homs + obs_hets
    genotypes = obs_hets + obs_mijor_homs + obs_minor_homs

    probs = [0.0 for i in range(rare +1)]

    mid = rare * (2 * genotypes - rare) // (2 * genotypes)
    if mid % 2 != rare%2:
        mid += 1

    probs[mid] = 1.0
    sum_p = 1 #probs[mid]

    curr_homr = (rare - mid) // 2
    curr_homc = genotypes - mid - curr_homr

    for curr_hets in range(mid, 1, -2):
        probs[curr_hets - 2] = probs[curr_hets] * curr_hets * (curr_hets - 1.0)/ (4.0 * (curr_homr + 1.0) * (curr_homc + 1.0))
        sum_p+= probs[curr_hets - 2]
        curr_homr += 1
        curr_homc += 1

    curr_homr = (rare - mid) // 2
    curr_homc = genotypes - mid - curr_homr

    for curr_hets in range(mid, rare-1, 2):
        probs[curr_hets + 2] = probs[curr_hets] * 4.0 * curr_homr * curr_homc/ ((curr_hets + 2.0) * (curr_hets + 1.0))
        sum_p += probs[curr_hets + 2]
        curr_homr -= 1
        curr_homc -= 1

    target = probs[obs_hets]
    p_hwe = 0.0
    for p in probs:
        if p <= target :
            p_hwe += p / sum_p  

    return min(p_hwe,1)

    if __name__ == '__main__':
    # For an example, we had 502 samples. 
    # At position 1:14930:A:G, we count:
    #     + 407 heterozygous genotypes (signed 0|1 or 1|0).
    #     + 4 homozygous genotypes AA (signed 0|0)
    #     + 91 homozygous genotypes GG (signed 1|1)
    print(snphwe(407,4,91))
    ```


!!! example "Calculate the Hardy-Weinberg equilibrium exact test statistics using PLINK"
    ```bash
    plink \
    	--bfile ${genotypeFile} \
    	--hardy \
    	--out plink_results
    ```
    ```bash
    head plink_results.hwe
        CHR              SNP     TEST   A1   A2                 GENO   O(HET)   E(HET)            P
    1      1:14930:A:G  ALL(NP)    G    A             4/407/91   0.8108    0.485    4.864e-61
    1      1:15774:G:A  ALL(NP)    A    G             0/28/473  0.05589  0.05433            1
    1      1:15777:A:G  ALL(NP)    G    A             1/72/428   0.1437   0.1368       0.5053
    1      1:57292:C:T  ALL(NP)    T    C             3/99/396   0.1988   0.1886       0.3393
    1      1:77874:G:A  ALL(NP)    A    G             0/20/481  0.03992  0.03912            1
    1      1:87360:C:T  ALL(NP)    T    C             0/23/480  0.04573  0.04468            1
    1      1:92917:T:A  ALL(NP)    A    T              0/3/494 0.006036 0.006018            1
    1     1:104186:T:C  ALL(NP)    T    C            74/352/75   0.7026      0.5    6.418e-20
    1     1:125271:C:T  ALL(NP)    C    T             1/29/472  0.05777  0.05985       0.3798
    ```

### Applying filters

Previously we calculated the basic statistics using PLINK. But when performing certain analyses, we just want to exclude the bad-quality samples or SNPs instead of calculating the statistics for all samples and SNPs.

In this case we can apply the following filters for example:

- `--maf 0.01` : exlcude snps with maf<0.01
- `--geno 0.02` :filters out all variants with missing rates exceeding 0.02
- `--mind 0.02` :filters out all samples with missing rates exceeding 0.02
- `--hwe 1e-6` : filters out all variants which have Hardy-Weinberg equilibrium exact test p-value below the provided threshold. NOTE: With case/control data, cases and missing phenotypes are normally ignored. (see https://www.cog-genomics.org/plink/1.9/filter#hwe)

We will apply these filters in the following example if LD-pruning.

### LD Pruning

There is often strong Linkage disequilibrium(LD) among SNPs, for some analysis we don't need all SNPs and we need to remove the redundant SNPs to avoid bias in genetic estimations. For example, for relatedness estimation, we will use only LD-Pruned SNP set. 

We can use `--indep-pairwise 50 5 0.2` to filter out those in strong LD and keep only the independent SNPs.

!!! info "Meaning of `--indep-pairwise x y z`"

    - consider a window of `x` SNPs
    - calculate LD between each pair of SNPs in the window and remove one of a pair of SNPs if the LD is greater than `z`
    - shift the window `y` SNPs forward and repeat the procedure.
    
    Please check https://www.cog-genomics.org/plink/1.9/ld#indep for details.

Combined with the filters we just introduced, we can run:

!!! example 
    ```bash
    plink \
    	--bfile ${genotypeFile} \
    	--maf 0.01 \
    	--geno 0.02 \
    	--mind 0.02 \
    	--hwe 1e-6 \
    	--indep-pairwise 50 5 0.2 \
    	--out plink_results
    ```
    This command generates two outputs:  `plink_results.prune.in` and `plink_results.prune.out`
    `plink_results.prune.in` is the independent set of SNPs we will use in the following analysis.
    
    You can check the PLINK log for how many variants were removed based on the filters you applied:
    ```
    Total genotyping rate in remaining samples is 0.993916.
    108837 variants removed due to missing genotype data (--geno).
    --hwe: 9754 variants removed due to Hardy-Weinberg exact test.
    87149 variants removed due to minor allele threshold(s)
    (--maf/--max-maf/--mac/--max-mac).
    1029376 variants and 501 people pass filters and QC.
    ```
    
    Let's take a look at the LD-pruned SNP file. Basically, it just contains one SNP id per line.
    
    ```bash
    head plink_results.prune.in
    1:15774:G:A
    1:15777:A:G
    1:77874:G:A
    1:87360:C:T
    1:125271:C:T
    1:232449:G:A
    1:533113:A:G
    1:565697:A:G
    1:566933:A:G
    1:567092:T:C
    ```

### Inbreeding F coefficient 

Next, we can check the heterozygosity F of samples (https://www.cog-genomics.org/plink/1.9/basic_stats#ibc) : 

`-het` option will compute observed and expected autosomal homozygous genotype counts for each sample. Usually, we need to exclude individuals with high or low heterozygosity coefficients, which suggests that the sample might be contaminated. 

!!! info "Inbreeding F coefficient calculation by PLINK"

    $$F = {{O(HOM) - E(HOM)}\over{ M - E(HOM)}}$$
    
    - $E(HOM)$ :Expected Homozygous Genotype Count 
    - $O(HOM)$ :Observed Homozygous Genotype Count 
    - M : Number of SNPs

    High F may indicate a relatively high level of inbreeding. 
    
    Low F may suggest the sample DNA was contaminated.

!!! warning "Performing LD-pruning beforehand since these calculations do not take LD into account."

!!! example "Calculate inbreeding F coefficient"

    ```bash
    plink \
    	--bfile ${genotypeFile} \
        --extract plink_results.prune.in \
    	--het \
    	--out plink_results
    ```
    
    Check the output:
    
    ```bash
    head plink_results.het
        FID       IID       O(HOM)       E(HOM)        N(NM)            F
    HG00403   HG00403       180222    1.796e+05       217363      0.01698
    HG00404   HG00404       180127    1.797e+05       217553      0.01023
    HG00406   HG00406       178891    1.789e+05       216533   -0.0001138
    HG00407   HG00407       178992     1.79e+05       216677   -0.0008034
    HG00409   HG00409       179918    1.801e+05       218045    -0.006049
    HG00410   HG00410       179782    1.801e+05       218028    -0.009268
    HG00419   HG00419       178362    1.783e+05       215849     0.001315
    HG00421   HG00421       178222    1.785e+05       216110    -0.008288
    HG00422   HG00422       178316    1.784e+05       215938      -0.0022
    ```

A commonly used method is to exclude samples with heterozygosity F deviating more than 3 standard deviations (SD) from the mean. Some studies used a fixed value such as +-0.15 or +-0.2.

!!! warning "Usually we will use only [LD-pruned SNPs](#ld-pruning)  for the calculation of F."

We can plot the distribution of F:

!!! example "Distribution of $F_{het}$ in sample data"
    
    ![image](https://github.com/Cloufield/GWASTutorial/assets/40289485/6dec3e49-fe35-45ee-9337-d788ef3d51cd)
    

Here we use +-0.1 as the $F_{het}$ threshold for convenience. 

!!! example "Create sample list of individuals with extreme F using awk"
    ```
    # only one sample
    awk 'NR>1 && $6>0.1 || $6<-0.1 {print $1,$2}' plink_results.het > high_het.sample
    ```


### Sample & SNP filtering (extract/exclude/keep/remove)
Sometimes we will use only a subset of samples or SNPs included the original dataset. 
In this case, we can use `--extract` or `--exclude` to select or exclude SNPs from analysis, `--keep` or `--remove` to select or exclude samples.

For  `--keep` or `--remove`, the input is the filename of a sample FID and IID file.
For `--extract` or `--exclude`, the input is the filename of an SNP list file.

```bash
head plink_results.prune.in
1:15774:G:A
1:15777:A:G
1:77874:G:A
1:87360:C:T
1:125271:C:T
1:232449:G:A
1:533113:A:G
1:565697:A:G
1:566933:A:G
1:567092:T:C
```

### IBD / PI_HAT / kinship coefficient
`--genome` will estimate IBS/IBD. Usually, for this analysis, we need to prune our data first since the strong LD will cause bias in the results.
(This step is computationally intensive)

Combined with the `--extract`, we can run:

!!! info "How PLINK estimates IBD"
    
    The prior probability of IBS sharing can be modeled as: 
    
    $$P(I=i) = \sum^{z=i}_{z=0}P(I=i|Z=z)P(Z=z)$$
    
    - I: IBS state (I = 0, 1, or 2)
    - Z: IBD state (Z = 0, 1, or 2)
    - $P(I|Z)$ is a function of allele frequency. PLINK will average over all SNPs to obtain the expected value for $P(I|Z)$.
    
    So the proportion of alleles shared IBD ($\hat{\pi}$) can be estimated by:
    
    $$\hat{\pi} = {{P(Z=1)}\over{2}} + P(Z=2)$$


!!! example "Estimate IBD" 
    ```bash
    plink \
        --bfile ${genotypeFile} \
    	--extract plink_results.prune.in \
        --genome \
        --out plink_results
    ```
    
    PI_HAT is the IBD estimation. Please check https://www.cog-genomics.org/plink/1.9/ibd for more details.
    ```bash
    head plink_results.genome
        FID1     IID1     FID2     IID2 RT    EZ      Z0      Z1      Z2  PI_HAT PHE       DST     PPC   RATIO
    HG00403  HG00403  HG00404  HG00404 UN    NA  1.0000  0.0000  0.0000  0.0000  -1  0.858562  0.3679  1.9774
    HG00403  HG00403  HG00406  HG00406 UN    NA  0.9805  0.0044  0.0151  0.0173  -1  0.858324  0.8183  2.0625
    HG00403  HG00403  HG00407  HG00407 UN    NA  0.9790  0.0000  0.0210  0.0210  -1  0.857794  0.8034  2.0587
    HG00403  HG00403  HG00409  HG00409 UN    NA  0.9912  0.0000  0.0088  0.0088  -1  0.857024  0.2637  1.9578
    HG00403  HG00403  HG00410  HG00410 UN    NA  0.9699  0.0235  0.0066  0.0184  -1  0.858194  0.6889  2.0335
    HG00403  HG00403  HG00419  HG00419 UN    NA  1.0000  0.0000  0.0000  0.0000  -1  0.857643  0.8597  2.0745
    HG00403  HG00403  HG00421  HG00421 UN    NA  0.9773  0.0218  0.0010  0.0118  -1  0.857276  0.2186  1.9484
    HG00403  HG00403  HG00422  HG00422 UN    NA  0.9880  0.0000  0.0120  0.0120  -1  0.857224  0.8277  2.0652
    HG00403  HG00403  HG00428  HG00428 UN    NA  0.9801  0.0069  0.0130  0.0164  -1  0.858162  0.9812  2.1471
    ```

!!! info "KING-robust kinship estimator"
    
    PLINK2 uses KING-robust kinship estimator, which is more robust in the presence of population substructure. See [here](https://www.cog-genomics.org/plink/2.0/distance#make_king).

    Manichaikul, A., Mychaleckyj, J. C., Rich, S. S., Daly, K., Sale, M., & Chen, W. M. (2010). Robust relationship inference in genome-wide association studies. Bioinformatics, 26(22), 2867-2873.

Since the samples are unrelated, we do not need to remove any samples at this step. But remember to check this for your dataset.

### LD calculation

We can also use our data to estimate the LD between a pair of SNPs.

!!! info "Details on LD can be found [here](https://cloufield.github.io/GWASTutorial/19_ld/)"

`--chr` option in PLINK allows us to include SNPs on a specific chromosome.
To calculate LD r2 for SNPs on chr22 , we can run:

!!! example Calculate LD r2 for SNPs on chr22
    
    ```bash
    plink \
    	    --bfile ${genotypeFile} \
            --chr 22 \
            --r2 \
            --out plink_results
    ```
    
    ```bash
    head plink_results.ld
     CHR_A         BP_A             SNP_A  CHR_B         BP_B             SNP_B           R2
    22     16069141   22:16069141:C:G     22     16071624   22:16071624:A:G     0.771226
    22     16069784   22:16069784:A:T     22     16149743   22:16149743:T:A     0.217197
    22     16069784   22:16069784:A:T     22     16150589   22:16150589:C:A     0.224992
    22     16069784   22:16069784:A:T     22     16159060   22:16159060:G:A       0.2289
    22     16149743   22:16149743:T:A     22     16150589   22:16150589:C:A     0.965109
    22     16149743   22:16149743:T:A     22     16152606   22:16152606:T:C     0.692157
    22     16149743   22:16149743:T:A     22     16159060   22:16159060:G:A     0.721796
    22     16149743   22:16149743:T:A     22     16193549   22:16193549:C:T     0.336477
    22     16149743   22:16149743:T:A     22     16212542   22:16212542:C:T     0.442424
    ```

### Data management (make-bed/recode)

By far the input data we use is in binary form, but sometimes we may want the text version.

!!! info Format conversion
    ![image](https://user-images.githubusercontent.com/40289485/161413659-a489b508-63c7-4166-9f5c-25a1a125109a.png)

To convert the formats, we can run:

!!! example "Convert PLINK formats"
    
    ```bash
    #extract the 1000 samples with the pruned SNPs, and make a bed file.
    plink \
    	--bfile ${genotypeFile} \
    	--extract plink_results.prune.in \
    	--make-bed \
    	--out plink_1000_pruned
    
    #convert the bed/bim/fam to ped/map
    plink \
            --bfile plink_1000_pruned \
            --recode \
            --out plink_1000_pruned
    ```

## Apply all the filters to obtain a clean dataset

We can then apply the filters and remove samples with high $F_{het}$ to get a clean dataset for later use.

```bash
plink \
        --bfile ${genotypeFile} \
        --maf 0.01 \
        --geno 0.02 \
        --mind 0.02 \
        --hwe 1e-6 \
        --remove high_het.sample \
        --keep-allele-order \
        --make-bed \
        --out sample_data.clean
```

```
1224104 variants and 500 people pass filters and QC.
```

```
-rw-r--r--  1 yunye yunye 146M Dec 26 15:40 sample_data.clean.bed
-rw-r--r--  1 yunye yunye  39M Dec 26 15:40 sample_data.clean.bim
-rw-r--r--  1 yunye yunye  13K Dec 26 15:40 sample_data.clean.fam
```

## Other common QC steps not included in this tutorial

- check-sex: compares sex assignments in the input dataset with those imputed from X chromosome inbreeding coefficients [https://www.cog-genomics.org/plink/1.9/basic_stats#check_sex](https://www.cog-genomics.org/plink/1.9/basic_stats#check_sex)
- case/control nonrandom missingness test:  detect platform/batch differences between case and control genotype data by performing Fisher's exact test on case/control missing call counts at each variant. [https://www.cog-genomics.org/plink/1.9/assoc#test_missing](https://www.cog-genomics.org/plink/1.9/assoc#test_missing)

## Exercise
- [x] Follow this tutorial and type in the commands:
  - [x] Calculate basic statistics for the simulated data.
  - [x] Learn the meaning of each QC step.

- [x] Visualize the results of QC (using Python or R)
  - [x] Draw the distribution of MAF.(histogram)
  - [x] Draw the distribution of het.(histogram)
  - [x] Try to briefly explain what you observe

## Additional resources
- Marees, A. T., de Kluiver, H., Stringer, S., Vorspan, F., Curis, E., Marie‐Claire, C., & Derks, E. M. (2018). A tutorial on conducting genome‐wide association studies: Quality control and statistical analysis. International journal of methods in psychiatric research, 27(2), e1608.

## Reference
- Purcell, S., Neale, B., Todd-Brown, K., Thomas, L., Ferreira, M. A., Bender, D., ... & Sham, P. C. (2007). PLINK: a tool set for whole-genome association and population-based linkage analyses. The American journal of human genetics, 81(3), 559-575.
- Chang, C. C., Chow, C. C., Tellier, L. C., Vattikuti, S., Purcell, S. M., & Lee, J. J. (2015). Second-generation PLINK: rising to the challenge of larger and richer datasets. Gigascience, 4(1), s13742-015.
- Manichaikul, A., Mychaleckyj, J. C., Rich, S. S., Daly, K., Sale, M., & Chen, W. M. (2010). Robust relationship inference in genome-wide association studies. Bioinformatics, 26(22), 2867-2873.
