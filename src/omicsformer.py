import torch
import torch.nn as nn

class OmicsFormer(nn.Module):

    def __init__(self):
        super(OmicsFormer, self).__init__()
        self.rna_encoder = nn.Sequential(nn.Linear(3000, 256), nn.ReLU())

        self.protein_encoder = nn.Sequential(nn.Linear(457, 256), nn.ReLU())

        self.mutation_encoder = nn.Sequential(nn.Linear(500, 256), nn.ReLU())

        self.methylation_encoder = nn.Sequential(nn.Linear(5000, 256), nn.ReLU())

        self.attention = nn.MultiheadAttention(
            embed_dim=256,
            num_heads=8,
            batch_first=True)
        self.norm1 = nn.LayerNorm(256)

        self.feedforward = nn.Sequential(
            nn.Linear(256, 512),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(512, 256)
        )

        self.norm2 = nn.LayerNorm(256)

        self.classifier = nn.Sequential(
            nn.Linear(256, 64),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(64, 5)
        )

    def forward(self, rna, protein, mutation, methylation):
        # Encode each modality
        rna = self.rna_encoder(rna)

        protein = self.protein_encoder(protein)

        mutation = self.mutation_encoder(mutation)

        methylation = self.methylation_encoder(methylation)

        tokens = torch.stack([rna, protein, mutation, methylation], dim=1)

        attention_output, attention_weights = self.attention(
            tokens,
            tokens,
            tokens)
        
        tokens = self.norm1(tokens + attention_output)

        ff_output = self.feedforward(tokens)

        tokens = self.norm2(tokens + ff_output)

        tokens = tokens.mean(dim=1)
        
        output = self.classifier(tokens)

        return output, attention_weights
