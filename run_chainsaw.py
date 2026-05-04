'''for f in *.pdb; do
    chainsaw "$f" > "${f%.pdb}_domains.txt"
done
'''
import os
import subprocess

for f in os.listdir("."):
    if f.endswith(".pdb"):
        output = f.replace(".pdb", "_domains.txt")
        with open(output, "w") as out:
            subprocess.run(["chainsaw", f], stdout=out)
