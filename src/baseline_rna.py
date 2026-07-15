from train_random_forest import run_baseline

run_baseline(
    modality="rna",
    h5_file="data/processed/rna_aligned.h5",
    key="rna"
)
