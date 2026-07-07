import pandas as pd

# Load processed datasets
protein = pd.read_hdf(
    "data/processed/protein.h5",
    key="protein")

rna = pd.read_hdf(
    "data/processed/rna.h5",
    key="rna")

mutation = pd.read_hdf(
    "data/processed/mutation.h5",
    key="mutation")

methylation = pd.read_hdf(
    "data/processed/methylation.h5",
    key="methylation")

# Convert sample IDs to patient IDs
protein.index = protein.index.str[:12]
rna.index = rna.index.str[:12]
methylation.index = methylation.index.str[:12]

# Remove duplicate patients
protein = protein[~protein.index.duplicated()]
rna = rna[~rna.index.duplicated()]
mutation = mutation[~mutation.index.duplicated()]
methylation = methylation[~methylation.index.duplicated()]

# Find common patients
common = (
    protein.index
    .intersection(rna.index)
    .intersection(mutation.index)
    .intersection(methylation.index)
)

print("Common patients:", len(common))

# Keep only common patients

protein = protein.loc[common]
rna = rna.loc[common]
mutation = mutation.loc[common]
methylation = methylation.loc[common]

print(protein.shape)
print(rna.shape)
print(mutation.shape)
print(methylation.shape)

# verify that all datasets have the same patient order.
assert protein.index.equals(rna.index)
assert protein.index.equals(mutation.index)
assert protein.index.equals(methylation.index)

print("All patient orders match!")

# # Save aligned datasets
# protein.to_hdf(
#     "data/processed/protein_aligned.h5",
#     key="protein",
#     mode="w"
# )

# rna.to_hdf(
#     "data/processed/rna_aligned.h5",
#     key="rna",
#     mode="w"
# )

# mutation.to_hdf(
#     "data/processed/mutation_aligned.h5",
#     key="mutation",
#     mode="w"
# )

# methylation.to_hdf(
#     "data/processed/methylation_aligned.h5",
#     key="methylation",
#     mode="w"
# )

print("Alignment complete.")

