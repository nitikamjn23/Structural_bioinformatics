import pandas as pd
import argparse

def main():
    parser = argparse.ArgumentParser(description="Rename IDs in a file using a mapping table.")

    parser.add_argument("-i", "--input", required=True, help="Input file path")
    parser.add_argument("-o", "--output", required=True, help="Output file path")
    parser.add_argument("-m", "--mapping", required=True, help="CSV/TSV file with mapping")
    parser.add_argument("--query_col", default="Query", help="Column name for old IDs")
    parser.add_argument("--target_col", default="New_name", help="Column name for new IDs")
    parser.add_argument("--sep", default="\t", help="Separator for mapping file (default: tab)")

    args = parser.parse_args()

    # Load mapping file
    df = pd.read_csv(args.mapping, sep=args.sep)

    # Create dictionary
    id_map = dict(zip(df[args.query_col], df[args.target_col]))

    # Process file
    with open(args.input, "r") as infile, open(args.output, "w") as outfile:
        for line in infile:
            if line.startswith(">"):
                old_id = line[1:].strip()
                new_id = id_map.get(old_id, old_id)
                outfile.write(f">{new_id}\n")
            else:
                outfile.write(line)

if __name__ == "__main__":
    main()
