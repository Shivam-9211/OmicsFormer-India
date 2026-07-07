import os 

path = 'data/raw/tcga'
cancers = ["BRCA", "COAD", "KIRC", "LIHC", "LUAD"]

print("TCGA Data Inventory")
error_found = False

for cancer in cancers:
    print()
    print("=" * 70)
    print("Cancer Type:", cancer,"\n")

    files = os.listdir(f"{path}/{cancer}")

    for dataset in files:
        filepath = f"{path}/{cancer}/{dataset}"

        if os.path.exists(filepath):
            size_mb = os.path.getsize(filepath) / (1024 * 1024)
            print(f"{dataset:<45} {size_mb:8.2f} MB")
        else:
            error_found = True
            print(f"{dataset:<45} ERROR: File not found")
print("="*70)
if not error_found:
    print("No download errors found.")



