# Anaconda

Conda is an open-source package and environment management system. 

It is a very handy tool when you need to manage python packages.

# Download

!!! warning
    The comprehensive revision of Anaconda's terms of service at the end of March 2024 limits free usage in educational institutions with more than 200 users to curriculum-based courses. Please check the [terms of service](https://legal.anaconda.com/policies/en?name=terms-of-service#anaconda-terms-of-service) and [FAQ](https://www.anaconda.com/pricing/terms-of-service-faqs). However, using Miniconda and packages from conda-forge channel is still free, which will be used in this tutorial.

Follow the instructions on:
https://docs.anaconda.com/miniconda/install/#quick-command-line-install

For example, download the latest linux version:

```
# make a directory and download the miniconda installer
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
```

# Install
```
# give it permission to execute
chmod ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3

# install
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3

# remove the installer if miniconda is installed successfully
rm ~/miniconda3/miniconda.sh

# initialize conda
conda init --all
```



If everything goes well, then you can see the `(base)` before the prompt, which indicate the base environment:
```
(base) [heyunye@gc019 ~]$
```

# Set channels

create/revise the file `~/.condarc`

```
channels:
  - conda-forge
```

and then run `conda update --all`

# Conda User guide

For how to use conda, please check :
https://docs.conda.io/projects/conda/en/latest/user-guide/getting-started.html

Examples:
```
# install a specific version of python package
conda install pandas==1.5.2

#create a new python 3.9 virtual environment with the name "mypython39"
conda create -n mypython39 python=3.9

#use environment.yml to create a virtual environment
conda env create --file environment.yml

# activate a virtual environment called ldsc
conda activate ldsc

# change back to base environment
conda deactivate

# list all packages in your current environment 
conda list

# list all your current environments 
conda env list
```
