import os
import GEOparse

SAVE_DIR = "data/raw/geo"
os.makedirs(SAVE_DIR, exist_ok=True)

print("Downloading GSE149438...")

gse = GEOparse.get_GEO(
    geo="GSE149438",
    destdir=SAVE_DIR
)

print("Download completed!")
print("Files saved in:", SAVE_DIR)