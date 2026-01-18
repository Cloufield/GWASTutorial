```python
library(data.table)
library(TwoSampleMR)

```

**stderr:**

```
TwoSampleMR version 0.5.6
[>] New: Option to use non-European LD reference panels for clumping etc
[>] Some studies temporarily quarantined to verify effect allele
[>] See news(package='TwoSampleMR') and https://gwas.mrcieu.ac.uk for further details

```


```python
exp_raw <- fread("koges_bmi.txt.gz")

exp_raw <- subset(exp_raw,exp_raw$pval<5e-8)

exp_raw$phenotype <- "BMI"

exp_raw$n <- 72282

exp_dat <- format_data( exp_raw,
    type = "exposure",
    snp_col = "rsids",
    beta_col = "beta",
    se_col = "sebeta",
    effect_allele_col = "alt",
    other_allele_col = "ref",
    eaf_col = "af",
    pval_col = "pval",
    phenotype_col = "phenotype",
    samplesize_col= "n"
)
clumped_exp <- clump_data(exp_dat,clump_r2=0.01,pop="EAS")

```

**stderr:**

```
Warning message in .fun(piece, ...):
“Duplicated SNPs present in exposure data for phenotype 'BMI. Just keeping the first instance:

rs4665740

rs7201608

”
API: public: http://gwas-api.mrcieu.ac.uk/

Please look at vignettes for options on running this locally if you need to run many instances of this command.

Clumping rvi6Om, 2452 variants, using EAS population reference

Removing 2420 of 2452 variants due to LD with other variants or absence from LD reference panel

```


```python
out_raw <- fread("hum0197.v3.BBJ.T2D.v1/GWASsummary_T2D_Japanese_SakaueKanai2020.auto.txt.gz",
                    select=c("SNPID","Allele1","Allele2","BETA","SE","p.value","N","AF_Allele2"))

out_raw$phenotype <- "T2D"

out_dat <- format_data( out_raw,
    type = "outcome",
    snp_col = "SNPID",
    beta_col = "BETA",
    se_col = "SE",
    effect_allele_col = "Allele2",
    other_allele_col = "Allele1",
    pval_col = "p.value",
    phenotype_col = "phenotype",
    samplesize_col= "n",
    eaf_col="AF_Allele2"
)

```

**stderr:**

```
Warning message in format_data(out_raw, type = "outcome", snp_col = "SNPID", beta_col = "BETA", :
“effect_allele column has some values that are not A/C/T/G or an indel comprising only these characters or D/I. These SNPs will be excluded.”
Warning message in format_data(out_raw, type = "outcome", snp_col = "SNPID", beta_col = "BETA", :
“The following SNP(s) are missing required information for the MR tests and will be excluded
1:1142714:t:<cn0>
1:4288465:t:<ins:me:alu>
1:4882232:t:<cn0>
1:5172414:g:<cn0>
1:5173809:t:<cn0>
1:5934301:g:<ins:me:alu>
1:6814818:a:<ins:me:alu>
1:7921468:c:<cn2>
1:8502010:t:<ins:me:alu>
1:8924066:c:<cn0>
1:9171841:c:<cn0>
1:9403667:a:<cn2>
1:9595360:a:<cn0>
1:9846036:c:<cn0>
1:10067190:g:<cn0>
1:10482499:g:<cn0>
1:11682873:t:<cn0>
1:11830220:t:<ins:me:sva>
1:11988599:c:<cn0>
1:12475666:t:<ins:me:sva>
1:12737575:a:<ins:me:alu>
1:12842004:a:<cn0>
1:14437074:t:<cn0>
1:14437868:a:<cn0>
1:14713511:t:<cn2>
1:14735732:g:<cn0>
1:15343948:g:<cn0>
1:16151682:c:<cn0>
1:16329336:t:<ins:me:sva>
1:16358741:g:<cn0>
1:17676165:a:<cn0>
1:19486410:c:<ins:me:alu>
1:19855608:a:<cn2>
1:20257109:t:<ins:me:alu>
1:20310746:g:<cn0>
1:20496899:c:<cn0>
1:20497183:c:<cn0>
1:20864015:t:<cn0>
1:20944751:c:<ins:me:alu>
1:21346279:a:<cn0>
1:21492591:c:<ins:me:alu>
1:21786418:t:<cn0>
1:22302473:t:<cn0>
1:22901908:t:<ins:me:alu>
1:23908383:g:<cn0>
1:24223580:g:<cn0>
1:24520350:g:<cn0>
1:24804603:c:<cn0>
1:25055152:g:<cn0>
1:26460095:a:<cn0>
1:26961278:g:<cn0>
1:29373390:t:<ins:me:alu>
1:31090520:t:<ins:me:alu>
1:31316259:t:<cn0>
1:31720009:a:<cn0>
1:32535965:g:<cn0>
1:32544371:a:<cn0>
1:33785116:c:<cn0>
1:35101427:c:<cn0>
1:35177287:g:<cn0>
1:35627104:t:<cn0>
1:36474694:t:<ins:me:alu>
1:36733282:t:<cn0>
1:37215810:a:<ins:me:alu>
1:37816478:a:<cn0>
1:38132306:t:<cn0>
1:39084231:a:<cn0>
1:39677675:t:<ins:me:alu>
1:40524704:t:<ins:me:alu>
1:40552356:a:<cn0>
1:40976681:g:<cn0>
1:41021684:a:<cn0>
1:41785500:a:<ins:me:line1>
1:42390318:c:<ins:me:alu>
1:43694061:t:<cn0>
1:44059290:a:<inv>
1:45021223:t:<cn0>
1:45708588:a:<cn0>
1:45822649:t:<cn0>
1:46333195:a:<ins:me:alu>
1:46794814:t:<ins:me:alu>
1:47267517:t:<cn0>
1:47346571:a:<cn0>
1:47623401:a:<cn0>
1:47913001:t:<cn0>
1:48820285:t:<ins:me:alu>
1:48972537:g:<ins:me:alu>
1:49357693:t:<ins:me:alu>
1:49428756:t:<ins:me:line1>
1:49861993:g:<ins:me:alu>
1:50912662:c:<ins:me:alu>
1:51102445:t:<cn0>
1:52146313:a:<cn0>
1:53594175:t:<cn0>
1:53595112:c:<cn0>
1:55092043:g:<cn0>
1:55341923:c:<cn0>
1:55342224:g:<cn0>
1:55927718:a:<cn0>
1:56268665:t:<ins:me:line1>
1:56405404:t:<ins:me:line1>
1:56879062:t:<ins:me:alu>
1:57100960:t:<ins:me:sva>
1:57208746:a:<cn0>
1:58722032:t:<cn2>
1:58743910:a:<cn0>
1:58795378:a:<cn0>
1:59205317:t:<ins:me:alu>
1:59591483:t:<ins:me:alu>
1:59871876:t:<ins:me:alu>
1:60046725:a:<cn0>
1:60048628:c:<cn0>
1:60470604:t:<ins:me:alu>
1:60487912:t:<cn0>
1:60715714:t:<ins:me:line1>
1:61144594:c:<ins:me:alu>
1:62082822:a:<cn0>
1:62113386:c:<cn0>
1:62479250:t:<cn0>
1:62622902:g:<cn0>
1:62654739:c:<cn0>
1:63841704:c:<ins:me:alu>
1:64720497:a:<cn0>
1:64850193:a:<ins:me:sva>
1:65346960:t:<ins:me:alu>
1:65412505:a:<cn0>
1:68375746:a:<cn0>
1:70061670:g:<ins:me:alu>
1:70091056:t:<ins:me:alu>
1:70093557:c:<ins:me:alu>
1:70412360:t:<ins:me:alu>
1:70424730:t:<cn2>
1:70820401:t:<cn0>
1:70912433:g:<ins:me:alu>
1:72449620:a:<cn0>
1:72755694:t:<cn0>
1:72766343:t:<cn0>
1:72778537:g:<cn0>
1:73092779:c:<cn2>
1:74312425:a:<cn0>
1:75148055:t:<ins:me:alu>
1:75192907:c:<ins:me:line1>
1:75301685:t:<ins:me:alu>
1:75557174:c:<ins:me:alu>
1:76392967:t:<ins:me:alu>
1:76416074:a:<ins:me:alu>
1:76900598:c:<cn0>
1:77577928:t:<ins:me:alu>
1:77634327:a:<ins:me:alu>
1:77764994:t:<ins:me:alu>
1:77830614:t:<cn0>
1:78446240:c:<ins:me:sva>
1:78607067:t:<ins:me:alu>
1:78649157:a:<cn0>
1:78800902:t:<ins:me:line1>
1:79108845:t:<ins:me:alu>
1:79331208:c:<ins:me:alu>
1:79582082:t:<ins:me:alu>
1:79855600:c:<cn0>
1:80221781:t:<cn0>
1:80299106:t:<ins:me:alu>
1:80504615:t:<cn0>
1:80554065:t:<cn0>
1:80955976:t:<ins:me:line1>
1:81422415:c:<cn0>
1:82312054:g:<ins:me:alu>
1:82850409:g:<ins:me:alu>
1:83041946:t:<cn0>
1:84056670:a:<cn0>
1:84388330:g:<cn0>
1:84517858:a:<cn0>
1:84712009:g:<cn0>
1:84913274:c:<ins:me:alu>
1:85293152:g:<ins:me:alu>
1:85620127:t:<ins:me:alu>
1:85910957:g:<cn0>
1:86400829:t:<cn0>
1:86696940:a:<ins:me:alu>
1:87064962:c:<cn2>
1:87096974:c:<cn0>
1:87096990:t:<cn0>
1:88813625:t:<ins:me:alu>
1:89209563:t:<ins:me:alu>
1:89733616:t:<ins:me:line1>
1:89811425:g:<cn0>
1:90370569:t:<ins:me:alu>
1:90914512:g:<ins:me:line1>
1:91878937:g:<cn0>
1:92131841:g:<inv>
1:92232051:t:<cn0>
1:93291972:c:<cn0>
1:93498232:t:<ins:me:alu>
1:94288372:c:<cn0>
1:95192010:a:<ins:me:line1>
1:95342701:g:<ins:me:alu>
1:95522242:t:<cn0>
1:97458273:t:<inv>
1:98605297:t:<ins:me:alu>
1:99610528:a:<ins:me:alu>
1:99698454:g:<ins:me:alu>
1:100355940:a:<ins:me:alu>
1:100645536:g:<ins:me:alu>
1:100994221:g:<ins:me:alu>
1:101693230:t:<cn0>
1:101695346:a:<cn0>
1:101770067:g:<ins:me:alu>
1:101978980:t:<ins:me:line1>
1:102568923:g:<ins:me:line1>
1:102920544:t:<ins:me:alu>
1:103054499:t:<ins:me:alu>
1:104359763:g:<cn0>
1:104443176:t:<cn0>
1:104574487:t:<ins:me:alu>
1:105054083:t:<ins:me:alu>
1:105070244:c:<ins:me:alu>
1:105138650:t:<ins:me:alu>
1:105231111:t:<ins:me:alu>
1:105832823:g:<cn0>
1:106015797:t:<cn0>
1:106978443:t:<cn0>
1:107896853:g:<cn0>
1:107949843:t:<ins:me:alu>
1:108142479:t:<ins:me:alu>
1:108369370:a:<cn0>
1:108402972:a:<cn0>
1:109366972:g:<cn0>
1:109573240:a:<cn0>
1:110187159:a:<cn0>
1:110225019:c:<cn0>
1:111013750:a:<cn0>
1:111472607:g:<cn0>
1:111802597:g:<ins:me:sva>
1:111827762:a:<cn0>
1:111896187:c:<ins:me:sva>
1:112032284:t:<ins:me:alu>
1:112123691:t:<ins:me:alu>
1:112691740:a:<cn0>
1:112736007:a:<ins:me:alu>
1:112992009:t:<ins:me:alu>
1:113799625:g:<cn0>
1:114925678:t:<cn0>
1:115178042:c:<cn0>
1:116229468:c:<cn0>
1:116983571:t:<ins:me:alu>
1:117593370:a:<cn0>
1:119526940:a:<cn0>
1:119553366:c:<ins:me:line1>
1:120012853:a:<cn0>
1:152555495:g:<cn0>
1:152643788:a:<cn0>
1:152760084:c:<cn0>
1:153133703:a:<cn0>
1:154123770:t:<ins:me:alu>
1:154324167:g:<cn0>
1:154865017:g:<ins:me:alu>
1:157173860:t:<cn0>
1:157363502:t:<ins:me:alu>
1:157540655:g:<cn0>
1:157887236:t:<inv>
1:158371473:a:<ins:me:alu>
1:158488410:a:<cn0>
1:158726918:a:<cn0>
1:160979498:c:<cn0>
1:162263027:t:<ins:me:alu>
1:163088865:t:<ins:me:alu>
1:163314443:g:<ins:me:alu>
1:163639693:t:<ins:me:alu>
1:165553149:t:<ins:me:line1>
1:165861400:t:<ins:me:sva>
1:166189445:t:<ins:me:alu>
1:167506110:g:<ins:me:alu>
1:167712862:g:<ins:me:alu>
1:168926083:a:<ins:me:sva>
1:169004356:c:<cn0>
1:169042039:c:<cn0>
1:169225213:t:<cn0>
1:169524859:t:<ins:me:line1>
1:170603451:a:<ins:me:alu>
1:170991168:c:<ins:me:alu>
1:171358314:t:<ins:me:alu>
1:172177959:g:<cn0>
1:172825753:g:<cn0>
1:173811663:a:<cn0>
1:174654509:g:<cn0>
1:174796517:t:<cn0>
1:174894014:g:<cn0>
1:175152408:g:<cn0>
1:177509016:g:<cn0>
1:177544393:g:<cn0>
1:177946159:a:<cn0>
1:178397612:t:<ins:me:alu>
1:178495321:a:<cn0>
1:178692798:t:<ins:me:alu>
1:179491966:t:<ins:me:alu>
1:179607260:a:<cn0>
1:180272299:a:<cn0>
1:180857564:c:<ins:me:alu>
1:181043348:a:<cn0>
1:181588360:t:<ins:me:alu>
1:181601286:t:<ins:me:alu>
1:181853551:g:<ins:me:alu>
1:182420857:t:<ins:me:alu>
1:183308627:a:<cn0>
1:185009806:t:<cn0>
1:185504717:c:<ins:me:alu>
1:185584799:t:<ins:me:alu>
1:185857064:a:<cn0>
1:187464747:t:<cn0>
1:187522081:g:<ins:me:alu>
1:187609013:t:<cn0>
1:187716053:g:<cn0>
1:187932575:t:<cn0>
1:187955397:c:<ins:me:alu>
1:188174657:t:<ins:me:alu>
1:188186464:t:<ins:me:alu>
1:188438213:t:<ins:me:alu>
1:188615934:g:<ins:me:alu>
1:189247039:a:<ins:me:alu>
1:190052658:t:<cn0>
1:190309695:t:<cn0>
1:190773296:t:<ins:me:alu>
1:190874469:t:<ins:me:alu>
1:191466954:t:<ins:me:line1>
1:191580781:a:<ins:me:alu>
1:191817437:c:<ins:me:alu>
1:191916438:t:<cn0>
1:192008678:t:<ins:me:line1>
1:192262268:a:<ins:me:line1>
1:193549655:c:<ins:me:line1>
1:193675125:t:<ins:me:alu>
1:193999047:t:<cn0>
1:194067859:t:<ins:me:alu>
1:194575585:t:<cn0>
1:194675140:c:<ins:me:alu>
1:195146820:c:<ins:me:alu>
1:195746415:a:<ins:me:line1>
1:195885406:g:<cn0>
1:195904499:g:<cn0>
1:196464453:a:<ins:me:line1>
1:196602664:a:<cn0>
1:196728877:g:<cn0>
1:196734744:a:<cn0>
1:196761370:t:<ins:me:alu>
1:197756784:c:<inv>
1:197894025:c:<cn0>
1:198093872:c:<ins:me:alu>
1:198243300:t:<ins:me:alu>
1:198529696:t:<ins:me:line1>
1:198757296:t:<cn0>
1:198773749:t:<cn0>
1:198815313:a:<ins:me:alu>
1:202961159:t:<ins:me:alu>
1:203684252:t:<cn0>
1:204238474:c:<ins:me:alu>
1:204345055:t:<ins:me:alu>
1:204381864:c:<cn0>
1:205178526:t:<inv>”

```


```python
harmonized_data <- harmonise_data(clumped_exp,out_dat,action=1)

```

**stderr:**

```
Harmonising BMI (rvi6Om) and T2D (ETcv15)

```


```python
harmonized_data

```

| SNP | effect_allele.exposure | other_allele.exposure | effect_allele.outcome | other_allele.outcome | beta.exposure | beta.outcome | eaf.exposure | eaf.outcome | remove | ⋯ | pval.exposure | se.exposure | samplesize.exposure | exposure | mr_keep.exposure | pval_origin.exposure | id.exposure | action | mr_keep | samplesize.outcome |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| rs10198356 | G | A | G | A | 0.044 | 0.027821816 | 0.450 | 0.46949841 | FALSE | ⋯ | 1.5e-17 | 0.0051 | 72282 | BMI | TRUE | reported | rvi6Om | 1 | TRUE | NA |
| rs10209994 | C | A | C | A | 0.030 | 0.028433424 | 0.640 | 0.65770918 | FALSE | ⋯ | 2.0e-08 | 0.0054 | 72282 | BMI | TRUE | reported | rvi6Om | 1 | TRUE | NA |
| rs10824329 | A | G | A | G | 0.029 | 0.018217119 | 0.510 | 0.56240335 | FALSE | ⋯ | 1.7e-08 | 0.0051 | 72282 | BMI | TRUE | reported | rvi6Om | 1 | TRUE | NA |
| rs10938397 | G | A | G | A | 0.036 | 0.044554736 | 0.280 | 0.29915686 | FALSE | ⋯ | 1.0e-10 | 0.0056 | 72282 | BMI | TRUE | reported | rvi6Om | 1 | TRUE | NA |
| rs11066132 | T | C | T | C | -0.053 | -0.031928806 | 0.160 | 0.24197159 | FALSE | ⋯ | 1.0e-13 | 0.0071 | 72282 | BMI | TRUE | reported | rvi6Om | 1 | TRUE | NA |
| rs12522139 | G | T | G | T | -0.037 | -0.010749243 | 0.270 | 0.24543922 | FALSE | ⋯ | 1.8e-10 | 0.0057 | 72282 | BMI | TRUE | reported | rvi6Om | 1 | TRUE | NA |
| rs12591730 | A | G | A | G | 0.037 | 0.033042812 | 0.220 | 0.25367536 | FALSE | ⋯ | 1.5e-08 | 0.0065 | 72282 | BMI | TRUE | reported | rvi6Om | 1 | TRUE | NA |
| rs13013021 | T | C | T | C | 0.070 | 0.104075223 | 0.907 | 0.90195307 | FALSE | ⋯ | 1.9e-15 | 0.0088 | 72282 | BMI | TRUE | reported | rvi6Om | 1 | TRUE | NA |
| rs1955337 | T | G | T | G | 0.036 | 0.019593503 | 0.300 | 0.24112816 | FALSE | ⋯ | 7.4e-11 | 0.0056 | 72282 | BMI | TRUE | reported | rvi6Om | 1 | TRUE | NA |
| rs2076308 | C | G | C | G | 0.037 | 0.041352038 | 0.310 | 0.31562874 | FALSE | ⋯ | 3.4e-11 | 0.0055 | 72282 | BMI | TRUE | reported | rvi6Om | 1 | TRUE | NA |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |
| rs476828 | C | T | C | T | 0.067 | 0.078651859 | 0.270 | 0.25309742 | FALSE | ⋯ | 2.8e-31 | 0.0057 | 72282 | BMI | TRUE | reported | rvi6Om | 1 | TRUE | NA |
| rs4883723 | A | G | A | G | 0.039 | 0.021370910 | 0.280 | 0.22189601 | FALSE | ⋯ | 8.3e-12 | 0.0057 | 72282 | BMI | TRUE | reported | rvi6Om | 1 | TRUE | NA |
| rs509325 | G | T | G | T | 0.065 | 0.035691759 | 0.280 | 0.26816326 | FALSE | ⋯ | 7.8e-31 | 0.0057 | 72282 | BMI | TRUE | reported | rvi6Om | 1 | TRUE | NA |
| rs55872725 | T | C | T | C | 0.090 | 0.121517023 | 0.120 | 0.20355108 | FALSE | ⋯ | 1.8e-31 | 0.0077 | 72282 | BMI | TRUE | reported | rvi6Om | 1 | TRUE | NA |
| rs6089309 | C | T | C | T | -0.033 | -0.018669833 | 0.700 | 0.65803267 | FALSE | ⋯ | 3.5e-09 | 0.0056 | 72282 | BMI | TRUE | reported | rvi6Om | 1 | TRUE | NA |
| rs6265 | T | C | T | C | -0.049 | -0.031642696 | 0.460 | 0.40541994 | FALSE | ⋯ | 6.1e-22 | 0.0051 | 72282 | BMI | TRUE | reported | rvi6Om | 1 | TRUE | NA |
| rs6736712 | G | C | G | C | -0.053 | -0.029716899 | 0.917 | 0.93023505 | FALSE | ⋯ | 2.1e-08 | 0.0095 | 72282 | BMI | TRUE | reported | rvi6Om | 1 | TRUE | NA |
| rs7560832 | C | A | C | A | -0.150 | -0.090481195 | 0.012 | 0.01129784 | FALSE | ⋯ | 2.0e-09 | 0.0250 | 72282 | BMI | TRUE | reported | rvi6Om | 1 | TRUE | NA |
| rs825486 | T | C | T | C | -0.031 | 0.019073554 | 0.690 | 0.75485104 | FALSE | ⋯ | 3.1e-08 | 0.0056 | 72282 | BMI | TRUE | reported | rvi6Om | 1 | TRUE | NA |
| rs9348441 | A | T | A | T | -0.036 | 0.179230794 | 0.470 | 0.42502848 | FALSE | ⋯ | 1.3e-12 | 0.0051 | 72282 | BMI | TRUE | reported | rvi6Om | 1 | TRUE | NA |


```python
res <- mr(harmonized_data)

```

**stderr:**

```
Analysing 'rvi6Om' on 'hff6sO'

```


```python
res

```

| id.exposure | id.outcome | outcome | exposure | method | nsnp | b | se | pval |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| rvi6Om | hff6sO | T2D | BMI | MR Egger | 28 | 1.3337580 | 0.69485260 | 6.596064e-02 |
| rvi6Om | hff6sO | T2D | BMI | Weighted median | 28 | 0.6298980 | 0.08516315 | 1.399605e-13 |
| rvi6Om | hff6sO | T2D | BMI | Inverse variance weighted | 28 | 0.5598956 | 0.23225806 | 1.592361e-02 |
| rvi6Om | hff6sO | T2D | BMI | Simple mode | 28 | 0.6097842 | 0.13305429 | 9.340189e-05 |
| rvi6Om | hff6sO | T2D | BMI | Weighted mode | 28 | 0.5946778 | 0.12680355 | 7.011481e-05 |


```python
mr_heterogeneity(harmonized_data)

```

| id.exposure | id.outcome | outcome | exposure | method | Q | Q_df | Q_pval |
| --- | --- | --- | --- | --- | --- | --- | --- |
| rvi6Om | hff6sO | T2D | BMI | MR Egger | 670.7022 | 26 | 1.000684e-124 |
| rvi6Om | hff6sO | T2D | BMI | Inverse variance weighted | 706.6579 | 27 | 1.534239e-131 |


```python
mr_pleiotropy_test(harmonized_data)

```

| id.exposure | id.outcome | outcome | exposure | egger_intercept | se | pval |
| --- | --- | --- | --- | --- | --- | --- |
| rvi6Om | hff6sO | T2D | BMI | -0.03603697 | 0.0305241 | 0.2484472 |


```python
res_single <- mr_singlesnp(harmonized_data)

```


```python
res_single

```

| exposure | outcome | id.exposure | id.outcome | samplesize | SNP | b | se | p |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BMI | T2D | rvi6Om | hff6sO | NA | rs10198356 | 0.6323140 | 0.2082837 | 2.398742e-03 |
| BMI | T2D | rvi6Om | hff6sO | NA | rs10209994 | 0.9477808 | 0.3225814 | 3.302164e-03 |
| BMI | T2D | rvi6Om | hff6sO | NA | rs10824329 | 0.6281765 | 0.3246214 | 5.297739e-02 |
| BMI | T2D | rvi6Om | hff6sO | NA | rs10938397 | 1.2376316 | 0.2775854 | 8.251150e-06 |
| BMI | T2D | rvi6Om | hff6sO | NA | rs11066132 | 0.6024303 | 0.2232401 | 6.963693e-03 |
| BMI | T2D | rvi6Om | hff6sO | NA | rs12522139 | 0.2905201 | 0.2890240 | 3.148119e-01 |
| BMI | T2D | rvi6Om | hff6sO | NA | rs12591730 | 0.8930490 | 0.3076687 | 3.700413e-03 |
| BMI | T2D | rvi6Om | hff6sO | NA | rs13013021 | 1.4867889 | 0.2207777 | 1.646925e-11 |
| BMI | T2D | rvi6Om | hff6sO | NA | rs1955337 | 0.5442640 | 0.2994146 | 6.910079e-02 |
| BMI | T2D | rvi6Om | hff6sO | NA | rs2076308 | 1.1176226 | 0.2657969 | 2.613132e-05 |
| ... | ... | ... | ... | ... | ... | ... | ... | ... |
| BMI | T2D | rvi6Om | hff6sO | NA | rs509325 | 0.5491040 | 0.1598196 | 5.908641e-04 |
| BMI | T2D | rvi6Om | hff6sO | NA | rs55872725 | 1.3501891 | 0.1259791 | 8.419325e-27 |
| BMI | T2D | rvi6Om | hff6sO | NA | rs6089309 | 0.5657525 | 0.3347009 | 9.096620e-02 |
| BMI | T2D | rvi6Om | hff6sO | NA | rs6265 | 0.6457693 | 0.1901871 | 6.851804e-04 |
| BMI | T2D | rvi6Om | hff6sO | NA | rs6736712 | 0.5606962 | 0.3448784 | 1.039966e-01 |
| BMI | T2D | rvi6Om | hff6sO | NA | rs7560832 | 0.6032080 | 0.2904972 | 3.785077e-02 |
| BMI | T2D | rvi6Om | hff6sO | NA | rs825486 | -0.6152759 | 0.3500334 | 7.878772e-02 |
| BMI | T2D | rvi6Om | hff6sO | NA | rs9348441 | -4.9786332 | 0.2572782 | 1.992909e-83 |
| BMI | T2D | rvi6Om | hff6sO | NA | All - Inverse variance weighted | 0.5598956 | 0.2322581 | 1.592361e-02 |
| BMI | T2D | rvi6Om | hff6sO | NA | All - MR Egger | 1.3337580 | 0.6948526 | 6.596064e-02 |


```python
res_loo <- mr_leaveoneout(harmonized_data)
res_loo

```

| exposure | outcome | id.exposure | id.outcome | samplesize | SNP | b | se | p |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BMI | T2D | rvi6Om | hff6sO | NA | rs10198356 | 0.5562834 | 0.2424917 | 2.178871e-02 |
| BMI | T2D | rvi6Om | hff6sO | NA | rs10209994 | 0.5520576 | 0.2388122 | 2.079526e-02 |
| BMI | T2D | rvi6Om | hff6sO | NA | rs10824329 | 0.5585335 | 0.2390239 | 1.945341e-02 |
| BMI | T2D | rvi6Om | hff6sO | NA | rs10938397 | 0.5412688 | 0.2388709 | 2.345460e-02 |
| BMI | T2D | rvi6Om | hff6sO | NA | rs11066132 | 0.5580606 | 0.2417275 | 2.096381e-02 |
| BMI | T2D | rvi6Om | hff6sO | NA | rs12522139 | 0.5667102 | 0.2395064 | 1.797373e-02 |
| BMI | T2D | rvi6Om | hff6sO | NA | rs12591730 | 0.5524802 | 0.2390990 | 2.085075e-02 |
| BMI | T2D | rvi6Om | hff6sO | NA | rs13013021 | 0.5189715 | 0.2386808 | 2.968017e-02 |
| BMI | T2D | rvi6Om | hff6sO | NA | rs1955337 | 0.5602635 | 0.2394505 | 1.929468e-02 |
| BMI | T2D | rvi6Om | hff6sO | NA | rs2076308 | 0.5431355 | 0.2394403 | 2.330758e-02 |
| ... | ... | ... | ... | ... | ... | ... | ... | ... |
| BMI | T2D | rvi6Om | hff6sO | NA | rs4883723 | 0.5602050 | 0.2397325 | 1.945000e-02 |
| BMI | T2D | rvi6Om | hff6sO | NA | rs509325 | 0.5608429 | 0.2468506 | 2.308693e-02 |
| BMI | T2D | rvi6Om | hff6sO | NA | rs55872725 | 0.4419446 | 0.2454771 | 7.180543e-02 |
| BMI | T2D | rvi6Om | hff6sO | NA | rs6089309 | 0.5597859 | 0.2388902 | 1.911519e-02 |
| BMI | T2D | rvi6Om | hff6sO | NA | rs6265 | 0.5547068 | 0.2436910 | 2.282978e-02 |
| BMI | T2D | rvi6Om | hff6sO | NA | rs6736712 | 0.5598815 | 0.2387602 | 1.902944e-02 |
| BMI | T2D | rvi6Om | hff6sO | NA | rs7560832 | 0.5588113 | 0.2396229 | 1.969836e-02 |
| BMI | T2D | rvi6Om | hff6sO | NA | rs825486 | 0.5800026 | 0.2367545 | 1.429330e-02 |
| BMI | T2D | rvi6Om | hff6sO | NA | rs9348441 | 0.7378967 | 0.1366838 | 6.717515e-08 |
| BMI | T2D | rvi6Om | hff6sO | NA | All | 0.5598956 | 0.2322581 | 1.592361e-02 |


```python
harmonized_data$"r.outcome" <- get_r_from_lor(
  harmonized_data$"beta.outcome",
  harmonized_data$"eaf.outcome",
  45383,
  132032,
  0.26,
  model = "logit",
  correction = FALSE
)

```


```python
out <- directionality_test(harmonized_data)
out

```

**stderr:**

```
r.exposure and/or r.outcome not present.

Calculating approximate SNP-exposure and/or SNP-outcome correlations, assuming all are quantitative traits. Please pre-calculate r.exposure and/or r.outcome using get_r_from_lor() for any binary traits

```

| id.exposure | id.outcome | exposure | outcome | snp_r2.exposure | snp_r2.outcome | correct_causal_direction | steiger_pval |
| --- | --- | --- | --- | --- | --- | --- | --- |
| rvi6Om | ETcv15 | BMI | T2D | 0.02125453 | 0.005496427 | TRUE | NA |


```python
res <- mr(harmonized_data)
p1 <- mr_scatter_plot(res, harmonized_data)
p1[[1]]

```


```python
res_single <- mr_singlesnp(harmonized_data)
p2 <- mr_forest_plot(res_single)
p2[[1]]

```


```python
res_loo <- mr_leaveoneout(harmonized_data)
p3 <- mr_leaveoneout_plot(res_loo)
p3[[1]]

```


```python
res_single <- mr_singlesnp(harmonized_data)
p4 <- mr_funnel_plot(res_single)
p4[[1]]

```
