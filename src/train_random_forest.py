import json
import joblib
import pandas as pd
import matplotlib.pyplot as plt
import wandb
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, label_binarize
from sklearn.metrics import (accuracy_score, classification_report,
    confusion_matrix, roc_curve, auc, f1_score)


# ==========================================================
# Load Data

def load_data(modality, h5_file, key):

    print(f"\nLoading {modality} dataset...")

    X = pd.read_hdf(h5_file, key=key)

    labels = pd.read_csv("data/processed/patient_labels.csv")
    labels = labels.set_index("Patient_ID")

    with open("data/splits.json", "r") as f:
        splits = json.load(f)

    return X, labels, splits


# ==========================================================
# Train Baseline Model

def run_baseline(modality, h5_file, key):

    # ----------------------------
    # Load data
    X, labels, splits = load_data(
        modality,
        h5_file,
        key)
 
    # -------------------------------------------------------------------------

    wandb.init(
        project="OmicsFormer-India",
        name=f"RandomForest-{modality}",
        config={
            "model": "RandomForest",
            "modality": modality,
            "n_estimators": 100,
            "class_weight": "balanced",
            "random_state": 42})


    X_train = X.loc[splits["train"]]
    X_test = X.loc[splits["test"]]

    y_train = labels.loc[splits["train"], "Cancer_Type"]
    y_test = labels.loc[splits["test"], "Cancer_Type"]


    encoder = LabelEncoder()

    y_train_encoded = encoder.fit_transform(y_train)
    y_test_encoded = encoder.transform(y_test)

    print("\nCancer Classes")
    print(encoder.classes_)


    model = RandomForestClassifier(
        n_estimators=100,
        class_weight="balanced",
        random_state=42)

    print("\nTraining Random Forest...")

    model.fit(X_train, y_train_encoded)

    print("Training completed!")


    # Prediction

    print("\nPredicting on test set...")

    y_pred = model.predict(X_test)

    y_score = model.predict_proba(X_test)

    print("Prediction completed!")

    print("\nFirst 10 Predictions")
    print(y_pred[:10])

    print("\nFirst 10 Actual Labels")
    print(y_test_encoded[:10])

    # ======================================================
    # Evaluation

    accuracy = accuracy_score(y_test_encoded, y_pred)

    print(f"\nAccuracy : {accuracy:.4f}")

    print("\nClassification Report")

    print(
        classification_report(
            y_test_encoded,
            y_pred,
            target_names=encoder.classes_))

    cm = confusion_matrix(y_test_encoded, y_pred)

    print("\nConfusion Matrix")
    print(cm)

    # ======================================================
    # ROC Curve

    y_test_bin = label_binarize(
        y_test_encoded,
        classes=range(len(encoder.classes_)))

    plt.figure(figsize=(8, 6))

    auc_scores = []

    for i in range(len(encoder.classes_)):

        fpr, tpr, _ = roc_curve(
            y_test_bin[:, i],
            y_score[:, i])

        roc_auc = auc(fpr, tpr)

        auc_scores.append(roc_auc)

        print(f"{encoder.classes_[i]} AUC : {roc_auc:.4f}")

        plt.plot(fpr, tpr,
            label=f"{encoder.classes_[i]} (AUC={roc_auc:.3f})")
    

    # Calculate Macro AUC

    macro_auc = sum(auc_scores) / len(auc_scores)
    
    plt.plot([0, 1], [0, 1], linestyle="--")

    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")

    plt.title(f"ROC Curve ({modality})")

    plt.legend()

    plt.savefig(f"results/{modality}_roc.png")

    wandb.log({
    "ROC Curve": wandb.Image(f"results/{modality}_roc.png")})

    wandb.log({
    "confusion_matrix": wandb.plot.confusion_matrix(
        probs=None,
        y_true=y_test_encoded,
        preds=y_pred,
        class_names=list(encoder.classes_))})

    plt.close()

    print(f"\nROC curve saved to results/{modality}_roc.png")

    # ======================================================
    # Save Model

    model_path = f"models/random_forest_{modality}.pkl"

    joblib.dump(
        model,
        model_path
    )

    print(f"\nModel saved to {model_path}")

    # ======================================================
    # Metrics Dictionary

    macro_f1 = f1_score(y_test_encoded, y_pred, average="macro")

    report = classification_report(
        y_test_encoded,
        y_pred,
        target_names=encoder.classes_,
        output_dict=True)

    metrics = {
        "data_type": modality,
        "accuracy": accuracy,
        "macro_auc": macro_auc,
        "macro_f1": macro_f1,
        "sensitivity_BRCA": report["BRCA"]["recall"],
        "sensitivity_COAD": report["COAD"]["recall"],
        "sensitivity_KIRC": report["KIRC"]["recall"],
        "sensitivity_LIHC": report["LIHC"]["recall"],
        "sensitivity_LUAD": report["LUAD"]["recall"],
    }

    wandb.log({
    "accuracy": accuracy,
    "macro_f1": macro_f1,
    "macro_auc": macro_auc
    })

    wandb.finish()
    return metrics

