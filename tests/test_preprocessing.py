import pandas as pd

def test_protein():
    protein = pd.read_hdf(
        "data/processed/protein.h5",
        key="protein")

    assert protein.shape[0] > 0
    assert protein.shape[1] > 0
    assert protein.isna().sum().sum() == 0

def test_rna():
    rna = pd.read_hdf(
        "data/processed/rna.h5",
        key="rna")

    assert rna.shape == (3363, 3000)
    assert rna.isna().sum().sum() == 0

def test_mutation():
    mutation = pd.read_hdf(
        "data/processed/mutation.h5",
        key="mutation")

    assert mutation.shape == (2695, 500)
    assert mutation.isna().sum().sum() == 0

    values = set(mutation.to_numpy().flatten())
    assert values.issubset({0, 1})

def test_methylation():
    methylation = pd.read_hdf(
        "data/processed/methylation.h5",
        key="methylation")

    assert methylation.shape == (2655, 5000)
    assert methylation.isna().sum().sum() == 0

