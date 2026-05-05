import csv

input_file = "test.txt"
output_file = "output.tsv"

with open(input_file, "r") as infile, open(output_file, "w", newline="") as outfile:
    writer = csv.writer(outfile, delimiter="\t")

    for line in infile:
        line = line.strip()
        if not line:
            continue

        # Split first column from rest (by first space)
        first_part, rest = line.split(" ", 1)

        # Split remaining part by "__"
        split_parts = rest.split("__")

        # Combine everything
        row = [first_part] + split_parts

        writer.writerow(row)

print("TSV file created successfully.")
