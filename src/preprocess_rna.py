import pandas as pd 

data=pd.read_csv("data\merged\star_fpkm(genes).tsv", sep='\t')

## ========***================****====================*****===================*****======================***=====
##First checking-

# print(data.shape)
# print(data.head())
# print(data.isna().sum().sum())
# print(data.duplicated().sum())
# print(data.isna().all().sum())     # Count how many completely null columns exist

# missing = data.isna().sum().sum()
# total = data.size
# print(f"Overall missing = {missing/total*100:.2f}%")

# missing_percent = data.isna().mean(axis=1) * 100
# print(missing_percent.head())
# print(missing_percent.describe())

# high_missing = (missing_percent > 30).sum()
# print(high_missing)

# removed = data.loc[missing_percent > 30, "Ensembl_ID"]
# print("Genes removed:")
# print(removed.tolist())

# print(data.iloc[:, 1:].max().max())    # for checking the need of apply log2(numeric+1)
# print(data.iloc[:, 1:].min().min())

## =================****=====================****=================****=============****=========

# numeric = data.iloc[:, 1:]

# gene_variance = numeric.var(axis=1)
# # print(gene_variance)

# gene_variance = gene_variance.sort_values(ascending=False)
# top3000 = gene_variance.head(3000).index

# numeric = numeric.loc[top3000]

# gene_names = data.loc[top3000, "Ensembl_ID"]

# mean = numeric.mean(axis=1)
# std = numeric.std(axis=1)

# numeric = numeric.sub(mean, axis=0)
# numeric = numeric.div(std, axis=0)

# numeric.index = gene_names
# numeric = numeric.T

# numeric.to_hdf(
#     "data/processed/rna.h5",
#     key="rna",
#     mode="w")


data = pd.read_hdf(r"data\processed\rna.h5")
print(data.shape)
