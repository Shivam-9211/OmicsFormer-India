import json
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import torch
from torch.utils.data import TensorDataset, DataLoader
import torch.nn as nn


rna = pd.read_hdf("data/processed/rna_aligned.h5")
protein = pd.read_hdf("data/processed/protein_aligned.h5")
mutation = pd.read_hdf("data/processed/mutation_aligned.h5")
methylation = pd.read_hdf("data/processed/methylation_aligned.h5")


# print(rna.shape)
# print(protein.shape)
# print(mutation.shape)
# print(methylation.shape)

# print(rna.index.equals(protein.index))
# print(rna.index.equals(mutation.index))
# print(rna.index.equals(methylation.index))

# print(rna.iloc[:5, :5])
# print(protein.iloc[:5, :5])
# print(mutation.iloc[:5, :5])
# print(methylation.iloc[:5, :5])

# Early Fusion

X = pd.concat([rna, protein, mutation, methylation], axis=1)

# print("\nEarly Fusion Shape:")
# print(X.shape)


with open("data/splits.json", "r") as f:
    splits = json.load(f)


labels = pd.read_csv("data/processed/patient_labels.csv")

labels = labels.set_index("Patient_ID")


X_train = X.loc[splits["train"]]
X_val = X.loc[splits["validation"]]
X_test = X.loc[splits["test"]]



y_train = labels.loc[splits["train"], "Cancer_Type"]

y_val = labels.loc[splits["validation"], "Cancer_Type"]

y_test = labels.loc[splits["test"], "Cancer_Type"]



encoder = LabelEncoder()

y_train_encoded = encoder.fit_transform(y_train)

y_val_encoded = encoder.transform(y_val)

y_test_encoded = encoder.transform(y_test)



# print("\nTrain/Test Shapes")

# print("X_train :", X_train.shape)
# print("X_val   :", X_val.shape)
# print("X_test  :", X_test.shape)

# print()


# model = RandomForestClassifier(
#     n_estimators=100,
#     class_weight="balanced",
#     random_state=42)

# print("Training Early Fusion Random Forest...")

# model.fit(X_train, y_train_encoded)

# print("Training Completed!")

# y_pred = model.predict(X_test)

# y_score = model.predict_proba(X_test)

# print("First 10 Predictions")
# print(y_pred[:10])

# print("First 10 Actual Labels")
# print(y_test_encoded[:10])


# accuracy = accuracy_score(y_test_encoded, y_pred)

# print(f"Accuracy : {accuracy:.4f}")

# print(classification_report(
#         y_test_encoded, y_pred, target_names=encoder.classes_))

# cm = confusion_matrix(
#     y_test_encoded,
#     y_pred)

# print(cm)



# Feature tensors
X_train_tensor = torch.FloatTensor(X_train.values)
X_val_tensor   = torch.FloatTensor(X_val.values)
X_test_tensor  = torch.FloatTensor(X_test.values)

# Label tensors
y_train_tensor = torch.LongTensor(y_train_encoded)
y_val_tensor   = torch.LongTensor(y_val_encoded)
y_test_tensor  = torch.LongTensor(y_test_encoded)

# print(X_train_tensor.shape)
# print(y_train_tensor.shape)

# print(X_train_tensor.dtype)
# print(y_train_tensor.dtype)

train_dataset = TensorDataset(
    X_train_tensor,
    y_train_tensor
)

val_dataset = TensorDataset(
    X_val_tensor,
    y_val_tensor
)

test_dataset = TensorDataset(
    X_test_tensor,
    y_test_tensor
)

train_loader = DataLoader(
    train_dataset,
    batch_size=32,
    shuffle=True
)

val_loader = DataLoader(
    val_dataset,
    batch_size=32,
    shuffle=False
)

test_loader = DataLoader(
    test_dataset,
    batch_size=32,
    shuffle=False
)

# print(len(train_loader))
# print(len(val_loader))
# print(len(test_loader))

# for X_batch, y_batch in train_loader:
#     print(X_batch.shape)
#     print(y_batch.shape)
#     break

class EarlyFusionNet(nn.Module):

    def __init__(self):

        super(EarlyFusionNet, self).__init__()

        self.network = nn.Sequential(

            nn.Linear(8957, 1024),
            nn.ReLU(),
            nn.Dropout(0.3),

            nn.Linear(1024, 256),
            nn.ReLU(),
            nn.Dropout(0.3),

            nn.Linear(256, 64),
            nn.ReLU(),

            nn.Linear(64, 5)
        )

    def forward(self, x):

        return self.network(x)
    
# model = EarlyFusionNet()
# # print(model)

# X_batch, y_batch = next(iter(train_loader))

# output = model(X_batch)

# # print(output.shape)

device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

model = EarlyFusionNet().to(device)

criterion = nn.CrossEntropyLoss()

optimizer = torch.optim.Adam(
    model.parameters(),
    lr=0.001
)

# print(device)
# print(optimizer)

model.train()

epochs = 20

for epoch in range(epochs):

    # TRAINING

    model.train()

    running_loss = 0

    for X_batch, y_batch in train_loader:

        X_batch = X_batch.to(device)
        y_batch = y_batch.to(device)

        optimizer.zero_grad()

        outputs = model(X_batch)

        loss = criterion(outputs, y_batch)

        loss.backward()

        optimizer.step()

        running_loss += loss.item()

    
    # VALIDATION

    model.eval()

    correct = 0
    total = 0

    with torch.no_grad():

        for X_batch, y_batch in val_loader:

            X_batch = X_batch.to(device)
            y_batch = y_batch.to(device)

            outputs = model(X_batch)

            _, predicted = torch.max(outputs, 1)

            total += y_batch.size(0)

            correct += (predicted == y_batch).sum().item()

    val_accuracy = correct / total

    # print(
    #     f"Epoch {epoch+1}/{epochs} | "
    #     f"Train Loss: {running_loss/len(train_loader):.4f} | "
    #     f"Validation Accuracy: {val_accuracy:.4f}"
    # )
# ----------------------------------------------------

model.eval()

correct = 0
total = 0

all_preds = []
all_labels = []

with torch.no_grad():

    for X_batch, y_batch in test_loader:

        X_batch = X_batch.to(device)
        y_batch = y_batch.to(device)

        outputs = model(X_batch)

        _, predicted = torch.max(outputs, 1)

        correct += (predicted == y_batch).sum().item()
        total += y_batch.size(0)

        all_preds.extend(predicted.cpu().numpy())
        all_labels.extend(y_batch.cpu().numpy())

test_accuracy = correct / total

# print(f"\nTest Accuracy: {test_accuracy:.4f}")

from sklearn.metrics import classification_report

# print(
#     classification_report(
#         all_labels,
#         all_preds,
#         target_names=encoder.classes_
#     )
# )

from sklearn.metrics import confusion_matrix

cm = confusion_matrix(all_labels, all_preds)

# print(cm)

torch.save(
    model.state_dict(),
    "models/early_fusion_model.pth"
)

print("Model saved successfully!")