'''import pandas as pd

# Input and output
input_file = "cluster_sequence_table.tsv"
output_file = "cluster_sequence_table_updated.xlsx"

# Read TSV file (IMPORTANT: sep="\t")
df = pd.read_csv(input_file, sep="\t")

# Split FASTA_ID column
split_cols = df["FASTA_ID"].str.split("__", expand=True)

# Create new columns
df["Protein_ID"] = split_cols[1]
df["Family"] = split_cols[2]

# Save as Excel
df.to_excel(output_file, index=False)

print("Done! File saved as", output_file)


import pandas as pd

# Load Excel file
file_path = "cluster_sequence_table_updated.xlsx"
df = pd.read_excel(file_path)

# ---- CHANGE THIS if your sequence column has a different name ----
sequence_column = "Sequence"

# Calculate sequence length
df["Sequence_length"] = df[sequence_column].astype(str).str.len()

# Save updated file
output_file = "cluster_sequence_table_updated_with_lengths.xlsx"
df.to_excel(output_file, index=False)

print("Done! Saved as:", output_file)


import pandas as pd

# Load Excel file
file_path = "cluster_sequence_table_updated.xlsx"
df = pd.read_excel(file_path)

# ---- CHANGE THIS if your sequence column has a different name ----
sequence_column = "Sequence"

# Calculate sequence length
df["Sequence_length"] = df[sequence_column].astype(str).str.len()

# Save updated file
output_file = "cluster_sequence_table_updated_with_lengths.xlsx"
df.to_excel(output_file, index=False)

print("Done! Saved as:", output_file)

import pandas as pd

# Load both Excel files
cluster_df = pd.read_excel("cluster_sequence_table_updated_with_lengths.xlsx")
dtodo_df = pd.read_excel("dTODO.xlsx")

# Keep only the columns we need from dTODO
dtodo_df = dtodo_df[["protein accession", "virus family"]]

# Merge on 'protein accession'
updated_df = cluster_df.merge(
    dtodo_df,
    on="protein accession",
    how="left"   # keeps all rows from cluster file
)

# Save the updated file
updated_df.to_excel("cluster_sequence_table_updated_with_lengths_updated.xlsx", index=False)

print("File updated successfully!")'''




import pandas as pd

# Load files
cluster_df = pd.read_excel("cluster_sequence_table_updated_with_lengths.xlsx")
dtodo_df = pd.read_excel("dTODO.xlsx")

# Clean column names (remove spaces + lowercase)
cluster_df.columns = cluster_df.columns.str.strip().str.lower()
dtodo_df = dtodo_df[["Protein Accession", "Virus Family Name"]]

# Now select columns
dtodo_df = dtodo_df[["protein accession", "virus family"]]

# Merge
updated_df = cluster_df.merge(
    dtodo_df,
    on="protein accession",
    how="left"
)

# Save
updated_df.to_excel("cluster_sequence_table_updated_output.xlsx", index=False)

