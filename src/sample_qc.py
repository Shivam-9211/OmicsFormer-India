import os
import pandas as pd 
import matplotlib.pyplot as plt


# data = pd.read_csv(r"data\raw\tcga\BRCA\TCGA-BRCA.methylation450.tsv.gz", sep="\t")
# print(data.columns)

# data = pd.read_csv(r"data\raw\tcga\BRCA\TCGA-BRCA.protein.tsv.gz", sep="\t")
# print(data.columns)

# data = pd.read_csv(r"data\raw\tcga\BRCA\TCGA-BRCA.somaticmutation_wxs.tsv.gz", sep="\t")
# print(data.columns)

# data = pd.read_csv(r"data\raw\tcga\BRCA\TCGA-BRCA.star_fpkm(genes).tsv.gz", sep="\t")
# print(data.columns)


''' In datasets- [methylation450.tsv.gz, protein.tsv.gz, star_fpkm(genes)], columns represents sample_id(Patients_data) and
in somaticmutation dataset, rows are sample_id(Patients_data) '''

## =================================================================================================================================================================

# cancers = ["BRCA", "LUAD", "COAD", "KIRC", "LIHC"]
# counts = []

# for cancer in cancers:

#     meth = pd.read_csv(rf"data\raw\tcga\{cancer}\TCGA-{cancer}.methylation450.tsv.gz", sep="\t")
#     protein = pd.read_csv(rf"data\raw\tcga\{cancer}\TCGA-{cancer}.protein.tsv.gz", sep="\t")
#     mut = pd.read_csv(rf"data\raw\tcga\{cancer}\TCGA-{cancer}.somaticmutation_wxs.tsv.gz", sep="\t")
#     rna = pd.read_csv(rf"data\raw\tcga\{cancer}\TCGA-{cancer}.star_fpkm(genes).tsv.gz", sep="\t")

#     meth_samples = {x[:12] for x in meth.columns[1:]}
#     rna_samples = {x[:12] for x in rna.columns[1:]}
#     protein_samples = {x[:12] for x in protein.columns[1:]}
#     mutation_samples = {x[:12] for x in mut["sample"]}

#     common_patients = (meth_samples & rna_samples & protein_samples & mutation_samples)
#     print("=" * 50)
#     print(f"Cancer: {cancer}")
#     print(f"Methylation patients : {len(meth_samples)}")
#     print(f"RNA patients          : {len(rna_samples)}")
#     print(f"Protein patients      : {len(protein_samples)}")
#     print(f"Mutation patients     : {len(mutation_samples)}")
#     print(f"Common patients       : {len(common_patients)}")
#     print()

   
##  ============================================================================================================================================

## Plotting Bar graph

# cancers = ["BRCA", "LUAD", "COAD", "KIRC", "LIHC"]
# counts = []

# for cancer in cancers:

#     meth = pd.read_csv(rf"data\raw\tcga\{cancer}\TCGA-{cancer}.methylation450.tsv.gz", sep="\t", nrows=0)
#     protein = pd.read_csv(rf"data\raw\tcga\{cancer}\TCGA-{cancer}.protein.tsv.gz", sep="\t", nrows=0)
#     mut = pd.read_csv(rf"data\raw\tcga\{cancer}\TCGA-{cancer}.somaticmutation_wxs.tsv.gz", sep="\t", usecols=["sample"])
#     rna = pd.read_csv(rf"data\raw\tcga\{cancer}\TCGA-{cancer}.star_fpkm(genes).tsv.gz", sep="\t", nrows=0)

#     meth_samples = {x[:12] for x in meth.columns[1:]}
#     rna_samples = {x[:12] for x in rna.columns[1:]}
#     protein_samples = {x[:12] for x in protein.columns[1:]}
#     mutation_samples = {x[:12] for x in mut["sample"]}

#     common_patients = (meth_samples & rna_samples & protein_samples & mutation_samples)

#     counts.append(len(common_patients))


# plt.figure(figsize=(7,4))
# plt.bar(cancers, counts)

# plt.title("Patient Counts per Cancer Type")
# plt.xlabel("Cancer Type")
# plt.ylabel("Common Patients")

# plt.tight_layout()
# plt.savefig("figures/fig_sample_counts.png")
# plt.show()

