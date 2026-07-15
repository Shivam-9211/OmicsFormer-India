from train_random_forest import run_baseline

run_baseline(
    modality="methylation",
    h5_file="data/processed/methylation_aligned.h5",
    key="methylation"
)