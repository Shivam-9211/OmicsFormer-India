import pandas as pd 

# data=pd.read_csv("data\merged\somaticmutation_wxs.tsv", sep='\t')

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
# print(data.isna().sum())

## ===================***=========================*****=====================*****===============================***=======

# data = data.drop_duplicates()

# data = data.dropna(
#     subset=["gene", "Tumor_Sample_Barcode"])
# # print(data.isna().sum())

# mutation = data[["Tumor_Sample_Barcode", "gene"]].copy()
# mutation["Tumor_Sample_Barcode"] = (
#     mutation["Tumor_Sample_Barcode"].str[:12])

# # print(mutation["Tumor_Sample_Barcode"])

# mutation["mutated"] = 1

# mutation_matrix = mutation.pivot_table(
#     index="Tumor_Sample_Barcode",
#     columns="gene",
#     values="mutated",
#     aggfunc="max",
#     fill_value=0)

# gene_frequency = mutation_matrix.sum(axis=0)
# top500 = gene_frequency.nlargest(500).index
# mutation_matrix = mutation_matrix[top500]

# mutation_matrix.to_hdf(
#     "data/processed/mutation.h5",
#     key="mutation",
#     mode="w")

# print(mutation_matrix.shape)
# print(mutation_matrix.head())

mutation = pd.read_hdf(
    "data/processed/mutation.h5",
    key="mutation")

# print(mutation.shape)
# print(mutation.head())

print(mutation.nunique().unique())
print(mutation.stack().unique())