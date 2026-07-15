import pandas as pd

from train_random_forest import run_baseline


protein = run_baseline(
    "protein",
    "data/processed/protein_aligned.h5",
    "protein"
)

rna = run_baseline(
    "rna",
    "data/processed/rna_aligned.h5",
    "rna"
)

mutation = run_baseline(
    "mutation",
    "data/processed/mutation_aligned.h5",
    "mutation"
)

methylation = run_baseline(
    "methylation",
    "data/processed/methylation_aligned.h5",
    "methylation"
)

df = pd.DataFrame([
    protein,
    rna,
    mutation,
    methylation
])

df.to_csv(
    "results/table1_baselines.csv",
    index=False
)

print(df)

print("\nBaseline table saved!")