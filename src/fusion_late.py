import json
import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (accuracy_score, classification_report, confusion_matrix, roc_auc_score)


rna = pd.read_hdf("data/processed/rna_aligned.h5")
protein = pd.read_hdf("data/processed/protein_aligned.h5")
mutation = pd.read_hdf("data/processed/mutation_aligned.h5")
methylation = pd.read_hdf("data/processed/methylation_aligned.h5")

rna_model = joblib.load("models/random_forest_rna.pkl")
protein_model = joblib.load("models/random_forest_protein.pkl")
mutation_model = joblib.load("models/random_forest_mutation.pkl")
methylation_model = joblib.load("models/random_forest_methylation.pkl")

with open("data/splits.json", "r") as f:
    splits = json.load(f)

labels = pd.read_csv("data/processed/patient_labels.csv")
labels = labels.set_index("Patient_ID")

rna_test = rna.loc[splits["test"]]
protein_test = protein.loc[splits["test"]]
mutation_test = mutation.loc[splits["test"]]
methylation_test = methylation.loc[splits["test"]]

y_test = labels.loc[splits["test"], "Cancer_Type"]

encoder = LabelEncoder()

encoder.fit(labels["Cancer_Type"])

y_test_encoded = encoder.transform(y_test)

# print(rna_test.shape)
# print(protein_test.shape)
# print(mutation_test.shape)
# print(methylation_test.shape)
# print(y_test_encoded.shape)

rna_prob = rna_model.predict_proba(rna_test)

protein_prob = protein_model.predict_proba(protein_test)

mutation_prob = mutation_model.predict_proba(mutation_test)

methylation_prob = methylation_model.predict_proba(methylation_test)

# print(rna_prob.shape)
# print(protein_prob.shape)
# print(mutation_prob.shape)
# print(methylation_prob.shape)

avg_prob = np.mean([
        rna_prob,
        protein_prob,
        mutation_prob,
        methylation_prob], axis=0)

y_pred = np.argmax(avg_prob, axis=1)

# print(avg_prob.shape)
# print(y_pred.shape)
# print(y_pred[:10])

accuracy = accuracy_score(y_test_encoded, y_pred)

macro_auc = roc_auc_score(
    y_test_encoded,
    avg_prob,
    multi_class="ovr",
    average="macro")

print(f"Macro AUC: {macro_auc:.4f}")

print(f"Late Fusion Test Accuracy: {accuracy:.4f}")

print(classification_report(
        y_test_encoded,
        y_pred,
        target_names=encoder.classes_))

cm = confusion_matrix(y_test_encoded, y_pred)

print(cm)

results = pd.DataFrame({
    "Patient_ID": y_test.index,
    "True_Label": y_test.values,
    "Predicted_Label": encoder.inverse_transform(y_pred),
    "Confidence": np.max(avg_prob, axis=1)
})

results.to_csv("results/late_fusion_predictions.csv",
    index=False)

print("Predictions saved!")

metrics = pd.DataFrame({
    "Model": ["Late Fusion"],
    "Accuracy": [accuracy],
    "Macro_AUC": [macro_auc]})

metrics.to_csv(
    "results/late_fusion_metrics.csv",
    index=False)