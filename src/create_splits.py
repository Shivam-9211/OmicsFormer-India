# import pandas as pd
# from sklearn.model_selection import train_test_split
# import json

# # Load aligned patients
# protein = pd.read_hdf(
#     "data/processed/protein_aligned.h5",
#     key="protein"
# )

# # Load labels
# labels = pd.read_csv(
#     "data/processed/patient_labels.csv"
# )

# # Keep only aligned patients
# labels = labels[
#     labels["Patient_ID"].isin(protein.index)
# ].copy()

# # Make sure order matches protein dataset
# labels = labels.set_index("Patient_ID")
# labels = labels.loc[protein.index]

# # Safety check
# assert labels.index.equals(protein.index)

# # -----------------------------
# # 60% Train
# # -----------------------------
# train_ids, temp_ids = train_test_split(
#     labels.index,
#     test_size=0.4,
#     stratify=labels["Cancer_Type"],
#     random_state=42
# )

# # -----------------------------
# # Remaining 40%
# # Split into 20% Validation + 20% Test
# # -----------------------------
# temp_labels = labels.loc[temp_ids]

# val_ids, test_ids = train_test_split(
#     temp_ids,
#     test_size=0.5,
#     stratify=temp_labels["Cancer_Type"],
#     random_state=42
# )

# print("Train:", len(train_ids))
# print("Validation:", len(val_ids))
# print("Test:", len(test_ids))

# # Save
# splits = {
#     "train": train_ids.tolist(),
#     "validation": val_ids.tolist(),
#     "test": test_ids.tolist()
# }

# with open("data/splits.json", "w") as f:
#     json.dump(splits, f, indent=4)

# print("Saved data/splits.json")

# import json

# with open("data/splits.json") as f:
#     splits = json.load(f)

# print(len(splits["train"]))
# print(len(splits["validation"]))
# print(len(splits["test"]))

# assert len(set(train_ids) & set(val_ids)) == 0
# assert len(set(train_ids) & set(test_ids)) == 0
# assert len(set(val_ids) & set(test_ids)) == 0

# print("No overlap between splits.")