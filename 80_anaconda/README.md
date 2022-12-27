# Anaconda

Conda is an open-source package and environment management system. 

It is a very handy tool when you need to manage python packages.

# Download

https://www.anaconda.com/products/distribution

For example, download the latest linux version:

```
wget https://repo.anaconda.com/archive/Anaconda3-2021.11-Linux-x86_64.sh
```

![image](https://user-images.githubusercontent.com/40289485/161550000-43448964-fdd6-4f76-bd63-51e108c4c0e7.png)


# Install
```
# give it permission to execute
chmod +x Anaconda3-2021.11-Linux-x86_64.sh 

# install
bash ./Anaconda3-2021.11-Linux-x86_64.sh
```

Follow the instructions on :
https://docs.anaconda.com/anaconda/install/linux/



If everything goes well, then you can see the `(base)` before the prompt, which indicate the base environment:
```
(base) [heyunye@gc019 ~]$
```

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
