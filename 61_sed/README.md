# sed

`sed` is also one of the most commonly used test-editing command in Linux, which is short for **s**tream **ed**itor. `sed` command edits the text from standard input in a line-by-line approach. 

## sed syntax

```bash
sed [OPTIONS] PROCESS [FILENAME]
```

## Examples

### sample input 
```bash
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

### Example 1: Replacing strings

`s` for substitute
`g` for global

!!! example "Replacing strings"
    "Replace the separator from `:` to `_`"
    ```bash
    head 02_Linux_basics/sumstats.txt | sed 's/:/_/g'
    #CHROM	POS	ID	REF	ALT	A1	TEST	OBS_CT	OR	LOG(OR)_SE	Z_STAT	P	ERRCODE
    1	13273	1_13273_G_C	G	C	C	ADD	503	0.7461490.282904	-1.03509	0.300628	.
    1	14599	1_14599_T_A	T	A	A	ADD	503	1.676930.240899	2.14598	0.0318742	.
    1	14604	1_14604_A_G	A	G	G	ADD	503	1.676930.240899	2.14598	0.0318742	.
    1	14930	1_14930_A_G	A	G	G	ADD	503	1.643590.242872	2.04585	0.0407708	.
    1	69897	1_69897_T_C	T	C	T	ADD	503	1.691420.200238	2.62471	0.00867216	.
    1	86331	1_86331_A_G	A	G	G	ADD	503	1.418870.238055	1.46968	0.141649	.
    1	91581	1_91581_G_A	G	A	A	ADD	503	0.9313040.123644	-0.575598	0.564887	.
    1	122872	1_122872_T_G	T	G	G	ADD	503	1.048280.182036	0.259034	0.795609	.
    1	135163	1_135163_C_T	C	T	T	ADD	503	0.6766660.242611	-1.60989	0.107422	.
    
    ```

### Example 2: Delete header(the first line)

`-d` for deletion

!!! example "Delete header(the first line)"

    ```bash
    head 02_Linux_basics/sumstats.txt | sed '1d'
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
