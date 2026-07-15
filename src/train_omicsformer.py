import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from sklearn.metrics import classification_report, confusion_matrix
import joblib
from sklearn.metrics import roc_auc_score
import matplotlib.pyplot as plt
import seaborn as sns

from dataset import MultiOmicsDataset
from omicsformer import OmicsFormer


# ---------------------------------------------------


device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

print("Device:", device)


train_dataset = MultiOmicsDataset("train")
val_dataset = MultiOmicsDataset("validation")
test_dataset = MultiOmicsDataset("test")


# Dataloader

train_loader = DataLoader(
    train_dataset,
    batch_size=32,
    shuffle=True)

val_loader = DataLoader(
    val_dataset,
    batch_size=32,
    shuffle=False)

test_loader = DataLoader(
    test_dataset,
    batch_size=32,
    shuffle=False)


# Model

model = OmicsFormer().to(device)

criterion = nn.CrossEntropyLoss()

optimizer = torch.optim.Adam(
    model.parameters(),
    lr=0.001)


# ---------------------------------------------------
# Training

epochs = 20

best_val_accuracy = 0

train_losses = []
val_accuracies = []


for epoch in range(epochs):

    model.train()

    running_loss = 0

    for batch in train_loader:

        rna = batch["rna"].to(device)

        protein = batch["protein"].to(device)

        mutation = batch["mutation"].to(device)

        methylation = batch["methylation"].to(device)

        labels = batch["label"].to(device)

        optimizer.zero_grad()

        outputs, _ = model(rna, protein, mutation, methylation)

        loss = criterion(outputs, labels)

        loss.backward()

        optimizer.step()

        running_loss += loss.item()

    train_loss = running_loss / len(train_loader)

    model.eval()

    correct = 0
    total = 0

    with torch.no_grad():

        for batch in val_loader:

            rna = batch["rna"].to(device)

            protein = batch["protein"].to(device)

            mutation = batch["mutation"].to(device)

            methylation = batch["methylation"].to(device)

            labels = batch["label"].to(device)

            outputs, _ = model(rna, protein, mutation, methylation)

            _, predicted = torch.max(outputs, 1)

            total += labels.size(0)

            correct += (predicted == labels).sum().item()

    val_accuracy = correct / total

    train_losses.append(train_loss)
    val_accuracies.append(val_accuracy)

    print(
        f"Epoch {epoch+1}/{epochs}"
        f" | Train Loss: {train_loss:.4f}"
        f" | Validation Accuracy: {val_accuracy:.4f}")


    # Save Best Model

    if val_accuracy > best_val_accuracy:

        best_val_accuracy = val_accuracy

        torch.save(
            model.state_dict(),
            "models/omicsformer_best.pt")


print("\nTraining Finished!")

print("Best Validation Accuracy:", best_val_accuracy)

import matplotlib.pyplot as plt

# Loss
plt.figure(figsize=(6,4))
plt.plot(train_losses)
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.title("Training Loss")
plt.grid(True)
plt.savefig("figures/train_loss.png", dpi=300)
plt.close()

# Validation Accuracy
plt.figure(figsize=(6,4))
plt.plot(val_accuracies)
plt.xlabel("Epoch")
plt.ylabel("Accuracy")
plt.title("Validation Accuracy")
plt.grid(True)
plt.savefig("figures/val_accuracy.png", dpi=300)
plt.close()
# ---------------------------------------------------
# Load Best Model

model.load_state_dict(
    torch.load("models/omicsformer_best.pt")
)

model.eval()


# Test

all_predictions = []
all_attention = []
all_labels = []
all_probabilities = []

with torch.no_grad():

    for batch in test_loader:

        rna = batch["rna"].to(device)

        protein = batch["protein"].to(device)

        mutation = batch["mutation"].to(device)

        methylation = batch["methylation"].to(device)

        labels = batch["label"].to(device)

        outputs, attention = model(rna, protein, mutation, methylation)

        probabilities = torch.softmax(outputs, dim=1)

        all_probabilities.extend(probabilities.cpu().numpy())

        _, predicted = torch.max(outputs, 1)

        all_attention.append(attention.cpu())

        all_predictions.extend(predicted.cpu().numpy())

        all_labels.extend(labels.cpu().numpy())


encoder = train_dataset.encoder

attention_tensor = torch.cat(all_attention, dim=0)

mean_attention = attention_tensor.mean(dim=0)

print(mean_attention)

print(attention_tensor.shape)

print()

print(classification_report(
    all_labels,
    all_predictions,
    target_names=encoder.classes_))

print()

print(confusion_matrix(all_labels, all_predictions))

macro_auc = roc_auc_score(
    all_labels,
    all_probabilities,
    multi_class="ovr",
    average="macro"
)

print(f"\nMacro AUC: {macro_auc:.4f}")

# -----------------------------------------------------------------------------

plt.figure(figsize=(7,6))

sns.heatmap(
    mean_attention.numpy(),
    annot=True,
    fmt=".2f",
    cmap="viridis",
    xticklabels=["RNA","Protein","Mutation","Methylation"],
    yticklabels=["RNA","Protein","Mutation","Methylation"])

plt.title("Average Cross-Attention Between Omics Modalities")
plt.xlabel("Key")
plt.ylabel("Query")

plt.tight_layout()

plt.savefig("figures/attention_heatmap.png", dpi=300)

# plt.show()
