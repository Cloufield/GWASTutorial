
# R

## Installing R

### Download R from CRAN

R can be downloaded from its official website CRAN (The Comprehensive R Archive Network).

[https://cran.r-project.org/](https://cran.r-project.org/)

### Install R using conda

It is convenient to use conda to manage your R environment. 

```
conda install -c conda-forge r-base=4.x.x
```

### IDE for R: Posit(Rstudio)

Posit(Rstudio) is one of the most commonly used Integrated development environment(IDE) for R.

[https://posit.co/](https://posit.co/)


## Use R in interactive mode
```
R
```

## Run R script
```
Rscript mycode.R
```


## Installing and Using R packages 

```
install.packages("package_name")

library(package_name)
```

## Basic syntax

### Assignment and Evaluation

```
> x <- 1

> x
[1] 1

> print(x)
[1] 1
```

## Data types

### Atomic data types

logical, integer, real, complex, string (or character) 

|Atomic data types|Description|Examples|
|-|-|-|
|**logical**|boolean|`TRUE`, `FALSE`|
|**integer**|integer|`1`,`2`|
|**numeric**|float number|`0.01`|
|**complex**|complex number|`1+0i`|
|**string** |string or chracter|`abc`|

### Vectors 

```
myvector <- c(1,2,3)
myvector < 1:3

myvector <- c(TRUE,FALSE)
myvector <- c(0.01, 0.02)
myvector <- c(1+0i, 2+3i)
myvector <- c("a","bc")
```

### Matrices

```
> mymatrix <- matrix(1:6, nrow = 2, ncol = 3)
> mymatrix
     [,1] [,2] [,3]
[1,]    1    3    5
[2,]    2    4    6

> ncol(mymatrix)
[1] 3
> nrow(mymatrix)
[1] 2
> dim(mymatrix)
[1] 2 3
> length(mymatrix)
[1] 6
```

### List

`list()` is a special vector-like data type that can contain different data types.

```
> mylist <- list(1, 0.02, "a", FALSE, c(1,2,3), matrix(1:6,nrow=2,ncol=3))
> mylist
[[1]]
[1] 1

[[2]]
[1] 0.02

[[3]]
[1] "a"

[[4]]
[1] FALSE

[[5]]
[1] 1 2 3

[[6]]
     [,1] [,2] [,3]
[1,]    1    3    5
[2,]    2    4    6
```

### Dataframe

```
> df <- data.frame(score = c(90,80,70,60),  rank = c("a", "b", "c", "d"))
> df
  score rank
1    90    a
2    80    b
3    70    c
4    60    d
```

## Subsetting

```
myvector
[1] 1 2 3
> myvector[0]
integer(0)
> myvector[1]
[1] 1
myvector[1:2]
[1] 1 2
> myvector[-1]
[1] 2 3
> myvector[-1:-2]
[1] 3
```

```
> mymatrix
     [,1] [,2] [,3]
[1,]    1    3    5
[2,]    2    4    6
> mymatrix[0]
integer(0)
> mymatrix[1]
[1] 1
> mymatrix[1,]
[1] 1 3 5
> mymatrix[1,2]
[1] 3
> mymatrix[1:2,2]
[1] 3 4
> mymatrix[,2]
[1] 3 4

```

```
> df
  score rank
1    90    a
2    80    b
3    70    c
4    60    d
> df[score]
Error in `[.data.frame`(df, score) : object 'score' not found
> df[[score]]
Error in (function(x, i, exact) if (is.matrix(i)) as.matrix(x)[[i]] else .subset2(x,  :
  object 'score' not found
> df[["score"]]
[1] 90 80 70 60
> df["score"]
  score
1    90
2    80
3    70
4    60
> df[1, "score"]
[1] 90
> df[1:2, "score"]
[1] 90 80
> df[1:2,2]
[1] "a" "b"
> df[1:2,1]
[1] 90 80
> df[,c("rank","score")]
  rank score
1    a    90
2    b    80
3    c    70
4    d    60
```

## Data Input and Output

```
mydata <- read.table("data.txt", header=T)

write.table(mydata, "data.txt")
```

## Control flow

### if

```
if (x > y){
  print ("x")
} else if (x < y){
  print ("y")
} else {
  print("tie")
}
```

### for 

```
> for (x in 1:5) {
    print(x)
}

[1] 1
[1] 2
[1] 3
[1] 4
[1] 5
```

### while

```
x<-0
while (x<5)
{
    x<-x+1
    print("Hello world")
}

[1] "Hello world"
[1] "Hello world"
[1] "Hello world"
[1] "Hello world"
[1] "Hello world"
```

## Functions

```
myfunction <- function(x){
  // actual code here
  return(result)
}

> my_add_function <- function(x,y){
  c = x + y
  return(c)
}
> my_add_function(1,3)
[1] 4
```