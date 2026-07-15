from train_random_forest import run_baseline

run_baseline(
    modality="mutation",
    h5_file="data/processed/mutation_aligned.h5",
    key="mutation"
)