from train_random_forest import run_baseline

run_baseline(
    modality="protein",
    h5_file="data/processed/protein_aligned.h5",
    key="protein")

