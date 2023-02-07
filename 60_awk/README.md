# AWK

## AWK Introduction
'awk' is one of the most powerful text processing tools for tabular text files.

## AWK syntax

```
awk OPTION 'CONDITION {PROCESS}' FILENAME
```

Some special variable in awk:

- `$0` : all columns
- `$n` : column n. For example, $1 means the first column. $4 means column 4.
- `NR` : Row number.

## Examples

Using the sample sumstats, we will demonstate some simple but useful one-liners.

```bash
# sample sumstats
head ../02_Linux_basics/sumstats.txt 
#CHROM	POS	ID	REF	ALT	A1	TEST	OBS_CT	OR	LOG(OR)_SE	Z_STAT	P	ERRCODE
1	13273	1:13273:G:C	G	C	C	ADD	503	0.7461490.282904	-1.03509	0.300628	.
1	14599	1:14599:T:A	T	A	A	ADD	503	1.676930.240899	2.14598	0.0318742	.
1	14604	1:14604:A:G	A	G	G	ADD	503	1.676930.240899	2.14598	0.0318742	.
1	14930	1:14930:A:G	A	G	G	ADD	503	1.643590.242872	2.04585	0.0407708	.
1	69897	1:69897:T:C	T	C	T	ADD	503	1.691420.200238	2.62471	0.00867216	.
1	86331	1:86331:A:G	A	G	G	ADD	503	1.418870.238055	1.46968	0.141649	.
1	91581	1:91581:G:A	G	A	A	ADD	503	0.9313040.123644	-0.575598	0.564887	.
1	122872	1:122872:T:G	T	G	G	ADD	503	1.048280.182036	0.259034	0.795609	.
1	135163	1:135163:C:T	C	T	T	ADD	503	0.6766660.242611	-1.60989	0.107422	.
```

### Example 1

!!! example "Select variants on chromosome 3 (keeping the headers)"

    ```bash
    awk 'NR==1 ||  $1==2 {print $0}' ../02_Linux_basics/sumstats.txt | head
    #CHROM	POS	ID	REF	ALT	A1	TEST	OBS_CT	OR	LOG(OR)_SE	Z_STAT	P	ERRCODE
    2	22398	2:22398:C:T	C	T	T	ADD	503	1.287540.161017	1.56962	0.116503	.
    2	24839	2:24839:C:T	C	T	T	ADD	503	1.318170.179754	1.53679	0.124344	.
    2	26844	2:26844:C:T	C	T	T	ADD	503	1.3173	0.161302	1.70851	0.0875413	.
    2	28786	2:28786:T:C	T	C	C	ADD	503	1.3043	0.161184	1.64822	0.0993082	.
    2	30091	2:30091:C:G	C	G	G	ADD	503	1.3043	0.161184	1.64822	0.0993082	.
    2	30762	2:30762:A:G	A	G	A	ADD	503	1.099560.158614	0.598369	0.549594	.
    2	34503	2:34503:G:T	G	T	T	ADD	503	1.323720.179789	1.55988	0.118789	.
    2	39340	2:39340:A:G	A	G	G	ADD	503	1.3043	0.161184	1.64822	0.0993082	.
    2	55237	2:55237:T:C	T	C	C	ADD	503	1.314860.161988	1.68983	0.0910614	.
    ```

The `NR` here means row number. The condition here `NR==1 || $1==3` means if it is the first row or the first column is equal to 3, conduct the process `print $0`, which mean print all columns. 

### Example 2

!!! example "Select all genome-wide significant variants (p<5e-8)"
    
    ```bash
    awk 'NR==1 ||  $13 <5e-8 {print $0}' ../02_Linux_basics/sumstats.txt | head
    #CHROM	POS	ID	REF	ALT	A1	TEST	OBS_CT	OR	LOG(OR)_SE	Z_STAT	P	ERRCODE
    1	13273	1:13273:G:C	G	C	C	ADD	503	0.7461490.282904	-1.03509	0.300628	.
    1	14599	1:14599:T:A	T	A	A	ADD	503	1.676930.240899	2.14598	0.0318742	.
    1	14604	1:14604:A:G	A	G	G	ADD	503	1.676930.240899	2.14598	0.0318742	.
    1	14930	1:14930:A:G	A	G	G	ADD	503	1.643590.242872	2.04585	0.0407708	.
    1	69897	1:69897:T:C	T	C	T	ADD	503	1.691420.200238	2.62471	0.00867216	.
    1	86331	1:86331:A:G	A	G	G	ADD	503	1.418870.238055	1.46968	0.141649	.
    1	91581	1:91581:G:A	G	A	A	ADD	503	0.9313040.123644	-0.575598	0.564887	.
    1	122872	1:122872:T:G	T	G	G	ADD	503	1.048280.182036	0.259034	0.795609	.
    1	135163	1:135163:C:T	C	T	T	ADD	503	0.6766660.242611	-1.60989	0.107422	.
    
    ```

### Example 3

!!! example "Create a bed-like format for annotation"
    
    ```
    awk 'NR>1 {print $1,$2,$2,$4,$5}' ../02_Linux_basics/sumstats.txt | head
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

### awk workflow




### awk variables

|Variable|Desciption|
|-|-|
|NR|The number of input records|
|FS|The input field separator. The default value is " " |
|OFS|The output field separator.  The default value is " "|
|RS|The input record separator. The default value is "\n"|
|ORS|The output record separator.The default value is "\n" |
|FILENAME|The name of the current input file.|
|FNR|The current record number in the current file|

### awk functions

Numeric functions

- exp(x)
- int(x)
- log(x)
- sqrt(x)

String manipulating function

- length([string])
- split(string, array [, fieldsep [, seps ] ])
- sub(regexp, replacement [, target]) 
- gsub(regexp, replacement [, target])
- substr(string, start [, length ])
- tolower(string)
- toupper(string)

### awk options

```
$ awk --help
Usage: awk [POSIX or GNU style options] -f progfile [--] file ...
Usage: awk [POSIX or GNU style options] [--] 'program' file ...
POSIX options:          GNU long options: (standard)
        -f progfile             --file=progfile
        -F fs                   --field-separator=fs
        -v var=val              --assign=var=val
Short options:          GNU long options: (extensions)
        -b                      --characters-as-bytes
        -c                      --traditional
        -C                      --copyright
        -d[file]                --dump-variables[=file]
        -D[file]                --debug[=file]
        -e 'program-text'       --source='program-text'
        -E file                 --exec=file
        -g                      --gen-pot
        -h                      --help
        -i includefile          --include=includefile
        -l library              --load=library
        -L[fatal|invalid]       --lint[=fatal|invalid]
        -M                      --bignum
        -N                      --use-lc-numeric
        -n                      --non-decimal-data
        -o[file]                --pretty-print[=file]
        -O                      --optimize
        -p[file]                --profile[=file]
        -P                      --posix
        -r                      --re-interval
        -S                      --sandbox
        -t                      --lint-old
        -V                      --version

To report bugs, see node `Bugs' in `gawk.info', which is
section `Reporting Problems and Bugs' in the printed version.

gawk is a pattern scanning and processing language.
By default it reads standard input and writes standard output.

Examples:
        gawk '{ sum += $1 }; END { print sum }' file
        gawk -F: '{ print $1 }' /etc/passwd
```