import csv

with open("final_sorted_data.tsv") as f, open("final_sorted_data_output.fasta","w") as out:
    reader = csv.DictReader(f, delimiter="\t")
    for row in reader:
        out.write(f">{row['theader']}\n{row['sequence']}\n")
