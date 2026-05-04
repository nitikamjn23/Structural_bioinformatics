######### parsor for clans cluster sequences extraction ##############

import re
import csv
import os

input_file = "unclassified_corrected.cla.byZ_scores"
seq_output = "sequences.tsv"
cluster_output = "clusters.tsv"
fasta_folder = "clusters_fasta"

os.makedirs(fasta_folder, exist_ok=True)


def parse_clans_file(filename):
    sequences = []
    clusters = []

    with open(filename) as f:
        lines = f.readlines()

    # ---------- Extract FASTA sequences ----------
    seq_id = None
    seq = []
    in_seq_block = False
    index = 0

    for line in lines:
        line = line.rstrip()

        if line.startswith("<seq>"):
            in_seq_block = True
            continue
        
        if line.startswith("</seq>"):
            in_seq_block = False

            if seq_id and seq:
                sequences.append((index, seq_id, "".join(seq)))
            break

        if in_seq_block:
            if line.startswith(">"):
                if seq_id and seq:
                    sequences.append((index, seq_id, "".join(seq)))
                    index += 1
                seq_id = line[1:]     # remove >
                seq = []
            else:
                seq.append(line)

    # ---------- Extract cluster information ----------
    current_name = None
    current_numbers = None

    for line in lines:
        line = line.strip()

        if line.startswith("name="):
            if current_name and current_numbers:
                clusters.append((current_name, current_numbers))

            current_name = line.split("name=")[1]
            current_numbers = None

        elif line.startswith("numbers="):
            nums = line.split("numbers=")[1].strip(";")
            current_numbers = [int(x) for x in nums.split(";") if x]

    if current_name and current_numbers:
        clusters.append((current_name, current_numbers))

    return sequences, clusters

sequences, clusters = parse_clans_file(input_file)

# Make lookup: index → (id, seq)
sequence_dict = {idx: (sid, seq) for idx, sid, seq in sequences}

with open(seq_output, "w", newline="") as f:
    writer = csv.writer(f, delimiter="\t")
    writer.writerow(["sequence_index", "sequence_id", "sequence"])
    for idx, sid, seq in sequences:
        writer.writerow([idx, sid, seq])

with open(cluster_output, "w", newline="") as f:
    writer = csv.writer(f, delimiter="\t")
    writer.writerow(["cluster_name", "sequence_numbers"])
    for name, nums in clusters:
        writer.writerow([name, ",".join(map(str, nums))])


# ============================
#  GENERATE FASTA PER CLUSTER
# ============================
for name, nums in clusters:
    safe_name = name.replace(":", "").replace(";", "_").replace(" ", "_")
    filename = os.path.join(fasta_folder, f"cluster_{safe_name}.fasta")

    with open(filename, "w") as f:
        for n in nums:
            if n in sequence_dict:
                sid, seq = sequence_dict[n]
                f.write(f">{sid}\n{seq}\n")
            else:
                print(f"Warning: index {n} not found in sequences!")

print("DONE: sequences.tsv, clusters.tsv & FASTA files created.")


########################### get pdb structure of the cluster ##############################

import os
import shutil

# --- USER INPUT ---
fasta_folder = "clusters_fasta"      # folder that contains cluster FASTA files
pdb_folder = "unclassified_struc/"             # folder that contains all pdb files
output_folder = "cluster_pdbs"       # final output folder

os.makedirs(output_folder, exist_ok=True)

def get_ids_from_fasta(fasta_path):
    ids = []
    with open(fasta_path) as f:
        for line in f:
            if line.startswith(">"):
                seq_id = line[1:].strip()
                ids.append(seq_id)
    return ids


# ============= MAIN PIPELINE =============
for fasta_file in os.listdir(fasta_folder):
    if not fasta_file.endswith(".fasta"):
        continue

    fasta_path = os.path.join(fasta_folder, fasta_file)
    cluster_name = os.path.splitext(fasta_file)[0]
    cluster_out_folder = os.path.join(output_folder, cluster_name)

    os.makedirs(cluster_out_folder, exist_ok=True)

    print(f"\nProcessing FASTA: {fasta_file}")

    ids = get_ids_from_fasta(fasta_path)

    for seq_id in ids:
        pdb_name = seq_id + ".pdb"
        pdb_path = os.path.join(pdb_folder, pdb_name)

        if os.path.isfile(pdb_path):
            shutil.copy(pdb_path, cluster_out_folder)
            print(f"  ✓ Copied {pdb_name}")
        else:
            print(f"  ✗ PDB not found: {pdb_name}")

print("\nAll clusters processed.")

########## get sequence identifiers and cluster names in one table from seperate cluster fasta file based on their name ##########

import os
import pandas as pd

fasta_folder = "/home/jyotika/Downloads/Clans_task/Unannotated_domains_cas_work_out/clusters_fasta"

rows = []

def get_ids_from_fasta(fasta_path):
    ids = []
    with open(fasta_path) as f:
        for line in f:
            if line.startswith(">"):
                seq_id = line[1:].strip()
                ids.append(seq_id)
    return ids

for fasta_file in os.listdir(fasta_folder):
    if not fasta_file.endswith(".fasta"):
        continue

    fasta_path = os.path.join(fasta_folder, fasta_file)
    ids = get_ids_from_fasta(fasta_path)

    for seq_id in ids:
        rows.append([fasta_file, seq_id])

# Convert to DataFrame
clust = pd.DataFrame(rows, columns=["FASTA_file", "query"])

# Save table (optional)
output_csv = "/home/jyotika/Downloads/Clans_task/Unannotated_domains_cas_work_out/cluster_fasta_ids_table.csv"
clust.to_csv(output_csv, index=False)

print("Table created successfully!")
