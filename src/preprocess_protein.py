import pandas as pd 

# data=pd.read_csv("data\merged\protein.tsv", sep='\t')

# ========***================****====================*****===================*****======================***=====
# First checking-

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

# removed = data.loc[missing_percent > 30, "peptide_target"]
# print("Proteins removed:")
# print(removed.tolist())

# # =================****=====================****=================****=============****=========

# missing_percent = data.isna().mean(axis=1) * 100
# data = data.loc[missing_percent <= 30].reset_index(drop=True)
# print(data.shape)

# print(data.isna().sum().sum())

# numeric = data.iloc[:, 1:]

# for i in numeric.index:
#     median = numeric.loc[i].median()
#     numeric.loc[i] = numeric.loc[i].fillna(median)

# data.iloc[:, 1:] = numeric

# print(data.isna().sum().sum())

# # ====****===================****==================*****====================***==============****==========

# numeric = data.iloc[:, 1:]

# mean = numeric.mean(axis=1)
# std = numeric.std(axis=1)

# numeric = numeric.sub(mean, axis=0)
# numeric = numeric.div(std, axis=0)

# data.iloc[:, 1:] = numeric
# print(numeric.mean(axis=1).round(6).head())
# print(numeric.std(axis=1).round(6).head())

# # ===========*****===================================*****=========================****======================****======

# data.to_hdf(
#     "data/processed/protein.h5",
#     key="protein",
#     mode="w")

protein = pd.read_hdf(
    "data/processed/protein.h5",
    key="protein")

print(protein.head())
print(protein.shape)