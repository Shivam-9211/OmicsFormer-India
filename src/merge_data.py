import pandas as pd

cancers = ["BRCA", "LUAD", "COAD", "KIRC", "LIHC"]

dfs = []

for cancer in cancers:

    file = f"data/raw/tcga/{cancer}/TCGA-{cancer}.methylation450.tsv.gz"

    df = pd.read_csv(file, sep="\t")

    df = df.set_index(df.columns[0])

    dfs.append(df)

merged = pd.concat(dfs, axis=1)
# merged = pd.concat(dfs, axis=0, ignore_index=True)   # for mutation dataset

merged.reset_index(inplace=True)

merged.to_csv(
    "data/merged/methylation.tsv",
    sep="\t",
    index=False)

