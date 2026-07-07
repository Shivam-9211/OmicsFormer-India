import pandas as pd

# cancers = ["BRCA", "COAD", "KIRC", "LIHC", "LUAD"]

# labels = []

# for cancer in cancers:

#     file = f"data/raw/tcga/{cancer}/TCGA-{cancer}.protein.tsv.gz"

#     # Read only the header
#     df = pd.read_csv(file, sep="\t", nrows=0)

#     # Patient/sample IDs start from column 2
#     patients = df.columns[1:]

#     for sample in patients:
#         labels.append({
#             "Patient_ID": sample[:12],   # convert sample -> patient
#             "Cancer_Type": cancer
#         })

# labels = pd.DataFrame(labels)

# # Remove duplicate patients
# labels = labels.drop_duplicates(subset="Patient_ID")

# print(labels.head())
# print(labels.shape)

# labels.to_csv(
#     "data/processed/patient_labels.csv",
#     index=False
# )

# print("Saved successfully!")

# labels = pd.read_csv("data/processed/patient_labels.csv")

# print(labels.head())
# print(labels["Cancer_Type"].value_counts())
