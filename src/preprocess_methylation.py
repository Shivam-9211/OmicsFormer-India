# import pandas as pd

# INPUT_FILE = "data/merged/methylation.tsv"
# OUTPUT_FILE = "data/processed/methylation.h5"

# CHUNK_SIZE = 10000


# # =====================================================
# # PASS 1 : Compute variance of every valid CpG
# # =====================================================

# variance_list = []

# print("Pass 1 : Computing variances...")

# for chunk in pd.read_csv(
#     INPUT_FILE,
#     sep="\t",
#     chunksize=CHUNK_SIZE
# ):

#     numeric = chunk.iloc[:, 1:]

#     # Remove CpGs having >20% missing values
#     missing_percent = numeric.isna().mean(axis=1) * 100

#     keep = missing_percent <= 20

#     chunk = chunk.loc[keep]
#     numeric = numeric.loc[keep]

#     # Fill NaN with patient(column) mean
#     numeric = numeric.fillna(numeric.mean(axis=0))

#     # Variance across patients
#     variance = numeric.var(axis=1)

#     temp = pd.DataFrame({
#         "CpG": chunk["Composite Element REF"].values,
#         "variance": variance.values
#     })

#     variance_list.append(temp)

# print("Combining variances...")

# variance_df = pd.concat(variance_list, ignore_index=True)

# top5000 = set(
#     variance_df
#     .nlargest(5000, "variance")["CpG"]
# )

# print("Top CpGs selected:", len(top5000))


# # =====================================================
# # PASS 2 : Read again and extract only top5000
# # =====================================================

# print("Pass 2 : Extracting top CpGs...")

# selected_chunks = []

# for chunk in pd.read_csv(
#     INPUT_FILE,
#     sep="\t",
#     chunksize=CHUNK_SIZE
# ):

#     chunk = chunk[
#         chunk["Composite Element REF"].isin(top5000)
#     ]

#     if len(chunk) == 0:
#         continue

#     numeric = chunk.iloc[:, 1:]

#     # Fill missing values
#     numeric = numeric.fillna(
#         numeric.mean(axis=0)
#     )

#     chunk.iloc[:, 1:] = numeric

#     selected_chunks.append(chunk)

# print("Combining selected CpGs...")

# final = pd.concat(
#     selected_chunks,
#     ignore_index=True
# )

# numeric = final.iloc[:, 1:]

# numeric.index = final["Composite Element REF"]

# # Patients × CpGs
# numeric = numeric.T

# print(numeric.shape)

# numeric.to_hdf(
#     OUTPUT_FILE,
#     key="methylation",
#     mode="w"
# )

# print("Saved successfully!")

import pandas as pd

meth = pd.read_hdf(
    "data/processed/methylation.h5",
    key="methylation"
)

print(meth.shape)
print(meth.head())
print(meth.isna().sum().sum())
print(meth.index[:5])
print(meth.columns[:5])