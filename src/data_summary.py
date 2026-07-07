import os
import pandas as pd

# print(os.getcwd())

# print(os.path.exists(path))

cancers = ["BRCA", "LUAD", "COAD", "KIRC", "LIHC"]

for cancer in cancers:
    path = f"data/raw/tcga/{cancer}"

    files = os.listdir(path)
    for file in files:
        print("=" * 60)
        print(f"\nDataset: {file.replace('.tsv.gz', '')}")
        df = pd.read_csv(f"{path}/{file}",sep="\t")
        if "somaticmutation" in file.lower():
            patients = df["sample"].nunique()
            print("Patients:", patients)
            features = df["gene"].nunique()
            print("Genes:", features)

        else:
            print(f"Patients: {df.shape[1]-1}")
            print(f"Features: {df.shape[0]}")

        missing = df.isna().sum().sum()
        total = df.size
        percent = missing / total * 100
        print(f"Missing: {percent:.2f}%")
        print()
