import torch
from torch.utils.data import Dataset

import pandas as pd
import json

from sklearn.preprocessing import LabelEncoder

# --------------------------------------------------------------------------------------

class MultiOmicsDataset(Dataset):

    def __init__(
        self,
        split="train"):

        self.rna = pd.read_hdf("data/processed/rna_aligned.h5")

        self.protein = pd.read_hdf("data/processed/protein_aligned.h5")

        self.mutation = pd.read_hdf("data/processed/mutation_aligned.h5")

        self.methylation = pd.read_hdf("data/processed/methylation_aligned.h5")

        self.labels = pd.read_csv(
            "data/processed/patient_labels.csv"
        )

        self.labels = self.labels.set_index("Patient_ID")

        with open("data/splits.json", "r") as f:
            self.splits = json.load(f)

        self.patient_ids = self.splits[split]

        self.encoder = LabelEncoder()

        self.encoder.fit(self.labels["Cancer_Type"])


    def __len__(self):
        return len(self.patient_ids)
        
    def __getitem__(self, idx):

        patient_id = self.patient_ids[idx]

        rna = self.rna.loc[patient_id].values

        protein = self.protein.loc[patient_id].values

        mutation = self.mutation.loc[patient_id].values

        methylation = self.methylation.loc[patient_id].values

        rna = torch.FloatTensor(rna)

        protein = torch.FloatTensor(protein)

        mutation = torch.FloatTensor(mutation)

        methylation = torch.FloatTensor(methylation)

        label = self.labels.loc[patient_id, "Cancer_Type"]

        label = self.encoder.transform([label])[0]

        label = torch.LongTensor([label]).squeeze()

        return {
            "rna": rna,
            "protein": protein,
            "mutation": mutation,
            "methylation": methylation,
            "label": label,}
    

if __name__ == "__main__":

    dataset = MultiOmicsDataset(split="train")

    print(len(dataset))

    sample = dataset[0]

    print(sample["rna"].shape)
    print(sample["protein"].shape)
    print(sample["mutation"].shape)
    print(sample["methylation"].shape)
    print(sample["label"])