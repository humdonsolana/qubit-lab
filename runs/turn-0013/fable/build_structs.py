"""Build ordered, stoichiometric hole-doped honeycomb borocarbides (LiBC/MgB2C2 mold).

Idea: Li_xBC deintercalation (Rosner 2002 route) fails experimentally because Li vacancies
disorder/buckle the BC layers (Kolmogorov group, PRMater 8, 114801 (2024)). Here the hole count is
fixed by stoichiometry instead: A(+1) M(+2) B4 C4 gives 0.5 hole per B2C2 with every cation site
in a MgB2C2-like half-filled arrangement, no vacancies to disorder.

Hexagonal approximant: 2x1 in-plane supercell of the LiBC (P6_3/mmc) cell: 4 BC per layer-pair,
4 cation sites, 2 filled (one A, one M) -> 10 atoms.
"""
from pymatgen.core import Structure, Lattice
import numpy as np, os

os.makedirs("structs", exist_ok=True)

def libc(a=2.752, c=7.058):
    lat = Lattice.hexagonal(a, c)
    species = ["Li", "Li", "B", "C", "B", "C"]
    coords = [[0, 0, 0], [0, 0, 0.5],
              [1/3, 2/3, 0.25], [2/3, 1/3, 0.25],
              [2/3, 1/3, 0.75], [1/3, 2/3, 0.75]]
    return Structure(lat, species, coords)

def amb4c4(A, M, a=2.752, c=7.058, same_gap=False):
    s = libc(a, c) * (2, 1, 1)   # 4 Li, 4 B, 4 C
    li = [i for i, sp in enumerate(s) if sp.specie.symbol == "Li"]
    # sites: index -> (x, z)
    info = [(i, round(s[i].frac_coords[0], 3), round(s[i].frac_coords[2], 3)) for i in li]
    gap0 = [i for i, x, z in info if z < 0.3]
    gap1 = [i for i, x, z in info if z > 0.3]
    keep = {gap0[0]: M, gap1[0]: A} if not same_gap else {gap0[0]: M, gap0[1]: A}
    remove = [i for i in li if i not in keep]
    for i, sp in keep.items():
        s.replace(i, sp)
    s.remove_sites(remove)
    return s

designs = {
    "LiMgB4C4": ("Li", "Mg"),
    "NaMgB4C4": ("Na", "Mg"),
    "LiCaB4C4": ("Li", "Ca"),
    "LiZnB4C4": ("Li", "Zn"),
    "LiBeB4C4": ("Li", "Be"),
}
for name, (A, M) in designs.items():
    s = amb4c4(A, M)
    s.to(filename=f"structs/{name}.cif")
    print(name, s.composition.reduced_formula, len(s))

# references
libc().to(filename="structs/LiBC.cif")
# MgB2C2 hexagonal approximant: same supercell with Mg in both gaps
s = amb4c4("Mg", "Mg"); s.to(filename="structs/MgB2C2_hex.cif")
# Li0.5BC ordered (Rosner-type) for comparison: 2x1 cell with one Li per gap
s = amb4c4("Li", "Li"); s.to(filename="structs/Li0.5BC.cif")
print("done")
