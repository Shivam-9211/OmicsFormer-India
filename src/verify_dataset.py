import json
import pandas as pd

# Load datasets

protein = pd.read_hdf(
    "data/processed/protein_aligned.h5",
    key="protein")

rna = pd.read_hdf(
    "data/processed/rna_aligned.h5",
    key="rna")

mutation = pd.read_hdf(
    "data/processed/mutation_aligned.h5",
    key="mutation")

methylation = pd.read_hdf(
    "data/processed/methylation_aligned.h5",
    key="methylation")

labels = pd.read_csv(
    "data/processed/patient_labels.csv")

with open("data/splits.json", "r") as d:
    splits = json.load(d)



print("Dataset Shapes")
print("-" * 40)
print("Protein     :", protein.shape)
print("RNA         :", rna.shape)
print("Mutation    :", mutation.shape)
print("Methylation :", methylation.shape)


# Verify patient IDs

assert protein.index.equals(rna.index), "Protein and RNA IDs do not match!"
assert protein.index.equals(mutation.index), "Protein and Mutation IDs do not match!"
assert protein.index.equals(methylation.index), "Protein and Methylation IDs do not match!"

print()
print("Patient IDs match across all four datasets.")


# Prepare labels

labels = labels.set_index("Patient_ID")
labels = labels.loc[protein.index]


# Split sizes

print("\nSplit Sizes")
print("-" * 40)

print("Train      :", len(splits["train"]))
print("Validation :", len(splits["validation"]))
print("Test       :", len(splits["test"]))


# Cancer distribution

print("\nCancer Distribution")
print("-" * 40)

x = ["train", "validation", "test"]
for split_name in x:

    ids = splits[split_name]

    split_labels = labels.loc[ids]

    print(f"\n{split_name.upper()}")

    print(split_labels["Cancer_Type"].value_counts().sort_index())


# Overlap check

train = set(splits["train"])
val = set(splits["validation"])
test = set(splits["test"])

assert len(train & val) == 0
assert len(train & test) == 0
assert len(val & test) == 0

print()
print("No overlap between train, validation and test.")
