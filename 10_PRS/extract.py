import pandas as pd
df = pd.read_csv("t2d_plink.txt",sep=" ")
df2 = pd.read_csv("../04_Data_QC/sample_data.clean.bim",sep="\s+",header=None)
df.loc[df["SNPID"].isin(df2[1].values),:].to_csv("t2d_plink_reduced.txt",sep="\t",index=None)
