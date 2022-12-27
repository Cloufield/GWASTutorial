## Introduction

This module is intended to provide a minumum introduction of the Linux system for handling genomic data.  

(If you are alreay familiar with Linux commands, it is completely ok to skip this module.)

If you are a beginner with no background in programming, then it would be helpful if you could learn some basic commands first. 
In this module, we will learn the most basic commands which enable you to handle genomic files in the terminal using command lines in linux system. 

- [Linux introduction](#0-linux-system-introduction)
    - Linux kernel and distributions
    - GUI and CUI
    - `man`
- [Overview and checking the manual pages](#11-overview-of-the-basic-commands-in-linux)
- [Handling directories](#12-directories)
    - Absolute path and relative path
- [Manipulating files](#13-manipulating-files)
- [Archiving and Compression](#14-archive-and-compression)
- [Checking files](#15-read-and-check-files)
- [Editing files in terminal](#16-edit-files)
- [Permissions](#17-permission)
- [Other useful commands](#18-others)
- [Bash scripts](#19-bash-scripts)
- [Advanced text editing](#110-advanced-text-editing)
- [Job scheduling system](#111-job-scheduling-system)
- [Git and Github](#112-git-and-github)
- [SSH](#113-ssh)
- [Symbolic link](#114-symbolic-link)
- [Downloading](#115-download)

## 0 Linux System Introduction
### 0.1 What is Linux?
![image](https://user-images.githubusercontent.com/40289485/161374551-1ef3b509-b345-4be3-b45b-3f86c466aa5a.png)

### 0.2 How do we interact with computers?
![image](https://user-images.githubusercontent.com/40289485/161374590-fd4bfee0-e815-475b-8a73-e53d97447e74.png)

### 0.3 A general comparison between CUI and GUI
||GUI|CUI|
|-|-|-|
|Interaction|Graphics|Command line|
|Precision|LOW|HIGH|
|Speed|LOW|HIGH|
|Memory required|HIGH|LOW|
|Ease of operation|Easier|DIFFICULT|
|Flexibility|MORE flexible|LESS flexible|

-> CUI is better for large-scale data analysis 

Check list
- [ ] what is CUI and GUI?
- [ ] why do we use Linux over other systems? 

## 1.1 Overview of the basic commands in Linux
Just like clicking and dragging files in Windows or MacOS, in Linux, we usually handle files by typing commands in the terminal.
![image](https://user-images.githubusercontent.com/40289485/161308638-18a0efbf-92df-4795-87be-72080db316c6.png)

Here are some of the basic commands we are going to cover in this brief tutorial:
|Function group| Commands| Description|
|-|-|-|
| Directories| `pwd`, `ls`, `mkdir`, `rmdir`| Commands for checking, creating and removing directories|
| Files|`touch`,`cp`,`mv`,`rm` | Commands for creating, copying, moving and removing files|
| Checking files| `cat`,`zcat`,`head`,`tail`,`less`,`more`,`wc`| Commands for inspecting files|
| Archiving and compression| `tar`,`gzip`,`gunzip`,`zip`,`unzip`| Commands for (Un)archiving and (De)compressing files|
| Manipulating text| `sort`,`uniq`,`cut`,`join`,`tr`|Commands for manipulating (tabular) text files|
| Modifying permission| `chmod`,`chown`, `chgrp`| Commands for changing the permissions of files and directories|
| Links| `ln`| Commands for creating symbolic and hard links|
| Pipe, redirect and others| pipe, `>`,`>>`,`*`,`.`,`..` | A group of miscellaneous commands |
| Advance text editing| `awk`, `sed` | Commands for more complicated text manipulation and editing |


### How to check the usage of a command using `man`: 
check the manual of the command (e.g., `man chmod`) or `--help` option (e.g., `chmod --help`)
```
$ man pwd

```
Then you will see the manual of `pwd` in your terminal.
```

PWD(1)                                              User Commands                                              PWD(1)

NAME
       pwd - print name of current/working directory

SYNOPSIS
       pwd [OPTION]...

DESCRIPTION
       Print the full filename of the current working directory.
....
```


## 1.2 Directories
The first set of commands are: `pwd` , `cd` , `ls`, `mkdir` and `rmdir`, which are related to directories (like the folders in a Windows system).

### `pwd`: 
print working directory, which means print the path of the current directory (working directory)
```
$ pwd
/home/he/work/GWASTutorial/02_Linux_basics
```
This command prints the absolute path.
![image](https://user-images.githubusercontent.com/40289485/161308808-6a8c97a9-4c7d-46cf-9e67-c5876415866f.png)

absolute path: path starting form root: `/home/he/work/GWASTutorial/02_Linux_basics`

relative path: path starting form current directory: `./GWASTutorial/02_Linux_basics`


### `cd` : 
changing current working directory 
```
$ cd 02_Linux_basics
$ pwd
/home/he/work/GWASTutorial/02_Linux_basics
```

### `ls` : 
list the files in the directory

we can also add some options like: `ls -lha`

`-l`: in a list-like format

`-h`: convert file size into a human readable format (KB,MB,GB...)

`-a`: list all files (including hidden files, namly those files a period at the beginning of the filename)
```
$ ls
README.md  sumstats.txt

$ ls -lha
drwxr-xr-x   4 he  staff   128B Dec 23 14:07 .
drwxr-xr-x  17 he  staff   544B Dec 23 12:13 ..
-rw-r--r--   1 he  staff     0B Oct 17 11:24 README.md
-rw-r--r--   1 he  staff    31M Dec 23 14:07 sumstats.txt
```
### `mkdir` & `rmdir` :

create a new empty directory & delete an empty directory
```
$ mkdir new_directory
$ ls
new_directory  README.md  sumstats.txt
$ rmdir new_directory/
$ ls
README.md  sumstats.txt
```

## 1.3 Manipulating files
This set of commands includes: `touch`, `mv` , `rm` and `cp`

### `touch`:
`touch` command is used to create a new empty file.

For example, let's create a text file called `newfile.txt` in this directory.
```
$ ls -l
total 64048
-rw-r--r--  1 he  staff         0 Oct 17 11:24 README.md
-rw-r--r--  1 he  staff  32790417 Dec 23 14:07 sumstats.txt

touch newfile.txt

$ touch newfile.txt
$ ls -l
total 64048
-rw-r--r--  1 he  staff         0 Oct 17 11:24 README.md
-rw-r--r--  1 he  staff         0 Dec 23 14:14 newfile.txt
-rw-r--r--  1 he  staff  32790417 Dec 23 14:07 sumstats.txt

```

### `mv`: 
(1) move the files to another path , or (2) rename the file

The following command will create a new directoru called `new_directory`, and move `sumstats.txt` into that directory. Just like draggig a file in to a folder in window system.
```
# make a new directory
$ mkdir new_directory

#move sumstats to the new directory
$ mv sumstats.txt new_directory/

# list the item in new_directory
$ ls new_directory/
sumstats.txt
```

Now, let's move it back to the current directory and rename it to `sumstats_new.txt `.
```
$ mv ./new_directory/sumstats.txt ./
```
Note: `./` means the current directory
You can also use `mv` to rename a file:
```
#rename
$mv sumstats.txt sumstats_new.txt 
```

### `rm`:
remove files or diretories
```
# remove a file
$rm file

#remove files in a directory (recursive mode)
$rm -r directory/
```

### `cp` 
`cp` command is used to copy files or diretories.

```
#cp files
$cp file1 file2

# copy directory
$cp -r directory1/ directory2/
```

## 1.4 Archive and Compression
Results for millions of variants are usually very large, sometimes >10GB, or consists of multiple files. 

To save space and make it easier to transfer, we need to archive and compress these files.

Archive: combine multiple files in one file

Compress: make the file size smaller without losing infomation

![image](https://user-images.githubusercontent.com/40289485/160957877-9148b34a-93e8-40cc-9acc-7c5bb9435b71.png)



Commly used commands:
| Extensions  | Create  | Extract  | Functions  | 
|---|---|---|---|
| file.gz  |   gzip |        gunzip |          compress|
| files.tar                  |         tar -cvf|       tar -xvf|             archive|
|  files.tar.gz or files.tgz |      tar -czvf|   tar -xvzf|  archive$compress|
|  file.zip                  |            zip|       unzip | archive$compress|


```
$ ls -lh
-rw-r--r--  1 he  staff    31M Dec 23 14:07 sumstats.txt

$ gzip sumstats.txt
$ ls -lh
-rw-r--r--  1 he  staff   9.9M Dec 23 14:07 sumstats.txt.gz

$ gunzip sumstats.txt.gz
$ ls -lh
-rw-r--r--   1 he  staff    31M Dec 23 14:07 sumstats.txt
```

## 1.5 Read and check files
We have a group of handy commands to check part of or the entire file, including `cat`, `zcat`, `less`, `head`, `tail`, `wc`

### `cat`
print the file or concatenate the files
```
$ ls -lha > a_text_file.txt
$ cat a_text_file.txt 
total 32M
drwxr-x---  2 he staff 4.0K Apr  2 00:37 .
drwxr-x--- 29 he staff 4.0K Apr  1 22:20 ..
-rw-r-----  1 he staff    0 Apr  2 00:37 a_text_file.txt
-rw-r-----  1 he staff 5.0K Apr  1 22:20 README.md
-rw-r-----  1 he staff  32M Mar 30 18:17 sumstats.txt

```
!!! Be careful not to `cat` a text file with a huge number of lines. You can try to `cat sumstats.txt` and see what happends.

By the way, `> a_text_file.txt` here means redirect the output to file ` a_text_file.txt`.

### `zcat` 
zcat is similar to cat, but can only applied to compressed files.
```
$ gzip a_text_file.txt 
$ cat a_text_file.txt.gz                                                         TGba_text_file.txtя
@ȱ»O𻀙v؂𧢩¼򀳠bq}󑢤\¤n٢ª򠀬n»ڡǭ
                          w5J_½𳘧P߉=ÿK
(֣԰§ҤŶaކ                              ¬M­R󽒊m³þe¸¤¼׍Sd￱߲들ª­v
       婁                                                                                                               resize: unknown character, exiting.

$ zcat a_text_file.txt.gz 
total 32M
drwxr-x---  2 he staff 4.0K Apr  2 00:37 .
drwxr-x--- 29 he staff 4.0K Apr  1 22:20 ..
-rw-r-----  1 he staff    0 Apr  2 00:37 a_text_file.txt
-rw-r-----  1 he staff 5.0K Apr  1 22:20 README.md
-rw-r-----  1 he staff  32M Mar 30 18:17 sumstats.txt
```

### `head`
print the first 10 lines.
`-n` change the lines using this option
```
$ head sumstats.txt 
CHROM	POS	ID	REF	ALT	A1	TEST	OBS_CT	OR	LOG(OR)_SE	Z_STAT	P	ERRCODE
1	319	17	2	1	1	ADD	10000	1.04326	0.0495816	0.854176	0.393008	.
1	319	22	1	2	2	ADD	10000	1.03347	0.0493972	0.666451	0.505123	.
1	418	23	1	2	2	ADD	10000	1.02668	0.0498185	0.528492	0.597158	.
1	537	30	1	2	2	ADD	10000	1.01341	0.0498496	0.267238	0.789286	.
1	546	31	2	1	1	ADD	10000	1.02051	0.0336786	0.60284	0.546615	.
1	575	33	2	1	1	ADD	10000	1.09795	0.0818305	1.14199	0.25346	.
1	752	44	2	1	1	ADD	10000	1.02038	0.0494069	0.408395	0.682984	.
1	913	50	2	1	1	ADD	10000	1.07852	0.0493585	1.53144	0.12566	.
1	1356	77	2	1	1	ADD	10000	0.947521	0.0339805	-1.5864	0.112649	.

$ head -n 1 sumstats.txt 
CHROM	POS	ID	REF	ALT	A1	TEST	OBS_CT	OR	LOG(OR)_SE	Z_STAT	P	ERRCODE
```

### `tail`
Similar to `head`, you can use `tail` ro check the last 10 lines.
```
$ tail sumstats.txt 
22	99996057	9959945	2	1	1	ADD	10000	1.03234	0.0335547	0.948413	0.342919.
22	99996465	9959971	2	1	1	ADD	10000	1.04755	0.0337187	1.37769	0.1683	.
22	99997041	9960013	2	1	1	ADD	10000	1.01942	0.0937548	0.205195	0.837419.
22	99997608	9960051	2	1	1	ADD	10000	0.969928	0.0397711	-0.767722	0.442652	.
22	99997629	9960055	2	1	1	ADD	10000	0.986949	0.0395305	-0.332315	0.739652	.
22	99997742	9960061	2	1	1	ADD	10000	0.990829	0.0396614	-0.232298	0.816307	.
22	99998121	9960086	2	1	1	ADD	10000	1.04448	0.0335879	1.29555	0.19513	.
22	99998455	9960106	2	1	1	ADD	10000	0.880953	0.152754	-0.829771	0.406668	.
22	99999208	9960146	2	1	1	ADD	10000	0.944604	0.065187	-0.874248	0.381983	.
22	99999382	9960164	2	1	1	ADD	10000	0.970509	0.033978	-0.881014	0.37831	.
```

### `wc`
word count:

lines,words,characters

```
$ wc sumstats.txt 
  445933  5797129 32790417 sumstats.txt
```


## 1.6 Edit files
a handy text editor in command line: vim
```
vim a_new_file.txt
```

press `i` to enter insert mode, and then you can edit the file as you want.
When finished, just pres `Esc` to escape insert mode, and then press `shift + :` , then `wq` to quit and also save the file.

Vim is hard to learn for beginners, but when you get familiar with it, it will be a mighty and convient tool.
For more detailed tutorials on Vim, you can check: https://github.com/iggredible/Learn-Vim

## 1.7 Permission
The permissions of a file or directory are represented as a 10-character string (1+3+3+3) :

For example, this represents a directory(the initial d) which is readable, writable and executable for the owner(the first 3: rwx), users in the same group(the 3 characters in the middle: rwx) and others (last 3 characters: rwx).

`drwxrwxrwx`

-> `d (directory or file) rwx (permissions for owner) rwx (permissions for users in the same group) rwx (permissions for other users)`

|Notation|Description|
|-|-|
|`r`|readable|
|`w`|writable|
|`x`|executable|
|`d`|directory|
|`-`|file|

Command for checking the permissions of files in the current directory: `ls -l`

Command for changing permissions: `chmod`, `chown`, `chgrp`

Syntax:
```
chmod [3-digit Binary notation] [path]
```

|Number notation|Permission|3-digit Binary notation|
|-|-|-|
|7|`rwx`|111|
|6|`rw-`|110|
|5|`r-x`|101|
|4|`r--`|100|
|3|`-wx`|011|
|2|`-w-`|010|
|1|`--x`|001|
|0|`---`|000|

Example:
```
# there is a readme file in the directory, and its permissions are -rw-r----- 
$ ls -lh
total 4.0K
-rw-r----- 1 he staff 2.1K Feb 24 01:16 README.md

# let's change the permissions to 660, which is a numeric notation of -rw-rw---- based on the table above
$ chmod 660 README.md 

# chack again, and it was changed.
$ ls -lh
total 4.0K
-rw-rw---- 1 he staff 2.1K Feb 24 01:16 README.md

```
Note: These commands are very important because we use genome data, which could raise severe ethical and privacy issues if there is data leak. 

![image](https://user-images.githubusercontent.com/40289485/160775846-a121f48e-5652-456f-8ced-7a3a82a8d995.png)



## 1.8 others
`|` , `>`, `>>`,`*`,`.`,`..`,`~`,`-`

### `|`  (pipe)

Pipe basically is used to pass the output of the previous command to the next command as input instead of printing is in terminal.
Using pipe you can do very complicated manipulations of the files.
```
cat sumstats | sort | uniq | wc
```
### `>`
redirect output to a new file (if the file already exist, it will be overwritten)
```
cat sumstats | sort | uniq | wc > count.txt
```
### `>>`
redirect output to a file by appending to the end of the file (if the file already exist, it will not be overwritten)
```
cat sumstats | sort | uniq | wc >> count.txt
```

### `*`
`*` means all files.

Note: `Be extremely careful when you use rm and *. It is disastrous when you mistakenly type `rm *``
### `.`
`.` means current directory.
### `..`
`..` means the parent directory of the current directory.
### `~`
`~` means your home directory

### `-`

`-` means the last directory you are working in
 
## 1.9 Bash scripts
If you have a lot of commands to run, or if you want to automate some complex manipulations, bash scripts are a good way to address this issue.

A simple example of bash scripts:

use vim to create `hello.sh`

```
#!/bin/bash
echo "Hello, world1"
echo "Hello, world2"
```

`#!` is called shebang, which tells the system which interpreter to use to excute the shell script.
use `chmod` to give it permission to run.
```
chmod +x hello.sh 
```

```
./hello.sh
"Hello, world1" 
"Hello, world2" 
```

## 1.10 advanced text editing 

(optional)
(awk, sed, cut, sort, join, uniq)

## 1.11 Job scheduling system
(If needed) Try to use job scheduling system to run a simple script (slurm on lab server)
sbatch , scancel 
sq, sjobs, shosts

## 1.12 Git and Github
Git is a powerful version control software and github is a platform where you can share your codes.

Currently you just need to learn `git clone`, which simply downloads an existing repository.

`git clone https://github.com/Cloufield/GWASTutorial.git`

reference: https://git-scm.com/doc

Cheatsheet: https://training.github.com/downloads/github-git-cheat-sheet/
## 1.13 SSH
SSH stands for Secure Shell Protocol, which enables you to connect to remote server safely.

![image](https://user-images.githubusercontent.com/40289485/161377030-911a5bed-f58b-4d27-8ffa-0c6b553e5c62.png)


login to romote server:
```
ssh <username>@<host>
```

Before you login in, you need to generate keys for ssh connection:
```
ssh-keygen -t rsa -b 4096
```
You will get two keys, a public one and a private one.

public key  :  `~/.ssh/id_rsa.pub`

private key :  `~/.ssh/id_rsa`   ,please don't share this with others.       

What you need to do is just add you local public key to `~/.ssh/authorized_keys` on host server.

## 1.14 Symbolic link  
symbolic link is like a shortcut on window system, which is a special type of file that points to another file.
It is very useful when you want to organize your tool box or working space.
You can use `ln -s pathA pathB` to create such a link. 

Example:
```
ln -s /home/he/tools/plink/plink /home/he/tools/bin

cd /home/he/tools/bin
ls -lha
...
lrwxr-xr-x  1 he  staff    27B Aug 30 11:30 plink -> /home/he/tools/plink/plink
```

## 1.15 Download
We can use `wget [option] [url]` command to download files to local machine.

`-O` option specify the file name you want to change for the downloaded file. 

Example:
```
# Download hg19 reference genome from UCSC
wget https://hgdownload.soe.ucsc.edu/goldenPath/hg19/bigZips/hg19.fa.gz

# Download hg19 reference genome from UCSC and rename it to  my_refgenome.fa.gz
wget -O my_refgenome.fa.gz https://hgdownload.soe.ucsc.edu/goldenPath/hg19/bigZips/hg19.fa.gz
```
