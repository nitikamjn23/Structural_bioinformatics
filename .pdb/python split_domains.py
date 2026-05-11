"""
Split baltymas1.pdb into three domain PDB files based on MERIZO chopping info:
  Domain 1 : residues   2 – 158   → baltymas1_domain1.pdb
  Domain 2 : residues 159 – 387   → baltymas1_domain2.pdb
  Domain 3 : residues 401 – 525   → baltymas1_domain3.pdb
 
Usage:
    python split_domains.py                        # expects baltymas1.pdb in the same folder
    python split_domains.py path/to/baltymas1.pdb  # or supply a path
"""
 
import sys
import os
 
# ── Domain definitions (inclusive residue ranges from MERIZO output) ──────────
DOMAINS = {
    "domain1": (2,   158),
    "domain2": (159, 387),
    "domain3": (401, 525),
}
 
# ── Resolve input file ─────────────────────────────────────────────────────────
input_pdb = sys.argv[1] if len(sys.argv) > 1 else "baltymas1.pdb"
 
if not os.path.isfile(input_pdb):
    sys.exit(f"[ERROR] Cannot find '{input_pdb}'. "
             f"Place the script next to baltymas1.pdb or pass the path as an argument.")
 
base = os.path.splitext(os.path.basename(input_pdb))[0]   # "baltymas1"
out_dir = os.path.dirname(os.path.abspath(__file__))       # same folder as this script
 
# ── Parse ATOM / HETATM records ───────────────────────────────────────────────
def parse_residue_number(line: str) -> int | None:
    """Return the integer residue sequence number from columns 23-26 (0-based 22-25)."""
    try:
        return int(line[22:26].strip())
    except ValueError:
        return None
 
# ── Write domain files ────────────────────────────────────────────────────────
handles = {}
writers = {}   # domain_name → list of lines
 
for name in DOMAINS:
    writers[name] = []
 
# Read source
with open(input_pdb, "r") as fh:
    all_lines = fh.readlines()
 
atom_count = {name: 0 for name in DOMAINS}
 
for line in all_lines:
    record = line[:6].strip()
 
    if record in ("ATOM", "HETATM"):
        res_num = parse_residue_number(line)
        if res_num is None:
            continue
        for name, (start, end) in DOMAINS.items():
            if start <= res_num <= end:
                writers[name].append(line)
                atom_count[name] += 1
 
    elif record in ("TER", "END"):
        # Add a TER + END to every domain that already has atoms
        for name in DOMAINS:
            if writers[name]:
                if record == "TER":
                    writers[name].append(line)
                # END will be appended explicitly after the loop
 
# ── Renumber atoms sequentially and write output ──────────────────────────────
def renumber_atom_line(line: str, new_serial: int) -> str:
    """Replace the atom serial number (cols 7-11, 1-based) with new_serial."""
    serial_str = f"{new_serial:5d}"
    return line[:6] + serial_str + line[11:]
 
output_files = []
 
for name, (start, end) in DOMAINS.items():
    out_path = os.path.join(out_dir, f"{base}_{name}.pdb")
    output_files.append(out_path)
    lines = writers[name]
 
    if not lines:
        print(f"[WARNING] No ATOM lines found for {name} (residues {start}–{end}). "
              f"File not written.")
        continue
 
    serial = 1
    with open(out_path, "w") as fh:
        fh.write(f"REMARK  Domain {name[-1]} of {base}  "
                 f"residues {start}–{end}\n")
        for line in lines:
            rec = line[:6].strip()
            if rec in ("ATOM", "HETATM"):
                fh.write(renumber_atom_line(line, serial))
                serial += 1
            else:                     # TER lines
                fh.write(line)
        fh.write("END\n")
 
    print(f"[OK] {out_path}  ({atom_count[name]} ATOM/HETATM lines, "
          f"residues {start}–{end})")
 
print("\nDone! Load each file into PyMOL with:  File → Open  (or drag-and-drop)")
 
