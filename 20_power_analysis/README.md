# Power analysis for GWAS

## Statistical power

## CaTS

test statistic:



power for large-scale one-stage studies

distribution of z

$P_{case}$

$P_{control}$

$u = {{P_{case} - P_{control}}\over {\sqrt{(P_{case}/N_{control} + P_{case}/N_{control})*0.5 }}}$

$C = \Phi^{-1}(1 - \alpha / 2 )$

$ Power = 1 - \Phi(-C-u) + \Phi(C-u)$

!!! example "GAS power calculator"
    url : https://csg.sph.umich.edu/abecasis/cats/gas_power_calculator/index.html
    
    ![image](https://user-images.githubusercontent.com/40289485/218300614-cc36e850-e5ee-4ec8-aa41-b75d5002518a.png)


## Reference:

- Skol, A. D., Scott, L. J., Abecasis, G. R., & Boehnke, M. (2006). Joint analysis is more efficient than replication-based analysis for two-stage genome-wide association studies. Nature genetics, 38(2), 209-213.
- Johnson, J. L., & Abecasis, G. R. (2017). GAS Power Calculator: web-based power calculator for genetic association studies. BioRxiv, 164343.
