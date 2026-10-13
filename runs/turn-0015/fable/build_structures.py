"""Build candidate 'self-interface' FeSe/perovskite-oxide bulk structures.

Prototype: 42622-type Sr4V2O6Fe2As2 (P4/nmm, Zhu et al. PRB 79, 220512 (2009):
a=3.9296, c=15.6732; Fe 2a; As 2c z=0.0894; Sr1 2c z=0.1920; Sr2 2c z=0.4121;
V 2c z=0.3083; O1 2c z=0.4278; O2 4f z=0.2919).
Designs:
  A  Sr4Mg2O6Fe2Se2          charge-neutral parent (Mg2+ block, FeSe neutral)
  B  Sr4Mg1.5Ti0.5O6Fe2Se2   2x1x1 supercell, 1 of 4 Mg -> Ti4+ : 0.25 e/Fe
  C  Sr4Mg1.75Ti0.25O6Fe2Se2 2x2x1 supercell, 1 of 8 Mg -> Ti : 0.125 e/Fe
  D  Sr4Mg2O6Fe2As2 reference arsenide (exists? check novelty) and Sr4V2O6Fe2As2 (known, 37 K) as CHGNet hull calibration
  E  Sr2MgO2... not built: 21311 block Sr2MO3 cannot be neutral with FeSe.
"""
from pymatgen.core import Structure, Lattice
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
import os
os.makedirs("structures", exist_ok=True)

def build_42622(M, X, a=3.93, c=15.7, zX=0.0894):
    lat = Lattice.tetragonal(a, c)
    species, coords = [], []
    # 2a Fe: (3/4,1/4,0),(1/4,3/4,0)
    species += ["Fe", "Fe"]; coords += [[0.75, 0.25, 0.0], [0.25, 0.75, 0.0]]
    def add_2c(el, z, flip=False):
        # P4/nmm (origin 2) 2c: (1/4,1/4,z),(3/4,3/4,-z); flip puts the atom on the other sublattice column
        if flip:
            species.extend([el, el]); coords.extend([[0.75, 0.75, z], [0.25, 0.25, -z]])
        else:
            species.extend([el, el]); coords.extend([[0.25, 0.25, z], [0.75, 0.75, -z]])
    add_2c(X, zX)                 # anion above the Fe-square hollow
    add_2c("Sr", 0.1920, flip=True)  # apical Sr on the other column (Sr-X ~3.2 A)
    add_2c("Sr", 0.4121, flip=True)
    add_2c(M, 0.3083)             # M in the MO2 square plane
    add_2c("O", 0.4278)           # apical O above M
    z = 0.2919                    # 4f O2 in the MO2 plane
    species += ["O"] * 4
    coords += [[0.75, 0.25, z], [0.25, 0.75, z], [0.25, 0.75, -z], [0.75, 0.25, -z]]
    s = Structure(lat, species, coords, coords_are_cartesian=False)
    return s

A = build_42622("Mg", "Se")
A.to(filename="structures/A_Sr4Mg2O6Fe2Se2.cif")
print("A", A.composition, SpacegroupAnalyzer(A, symprec=1e-3).get_space_group_symbol())

V = build_42622("V", "As")
V.to(filename="structures/ref_Sr4V2O6Fe2As2.cif")
D = build_42622("Mg", "As")
D.to(filename="structures/D_Sr4Mg2O6Fe2As2.cif")

# B: 2x1x1, replace one Mg with Ti
B = A.copy(); B.make_supercell([2, 1, 1])
idx = [i for i, s in enumerate(B) if s.specie.symbol == "Mg"]
B.replace(idx[0], "Ti")
B.to(filename="structures/B_Sr4Mg1.5Ti0.5O6Fe2Se2.cif")
print("B", B.composition)

# C: 2x2x1, replace one Mg with Ti
C = A.copy(); C.make_supercell([2, 2, 1])
idx = [i for i, s in enumerate(C) if s.specie.symbol == "Mg"]
C.replace(idx[0], "Ti")
C.to(filename="structures/C_Sr4Mg1.75Ti0.25O6Fe2Se2.cif")
print("C", C.composition, len(C))

# F: Sr4Ti2O6Fe2Se2 fully Ti (1 e/Fe) - the 'what if' end member
F = build_42622("Ti", "Se")
F.to(filename="structures/F_Sr4Ti2O6Fe2Se2.cif")
# G: Al-substituted variant (Al3+ gives 1 e per Al): Sr4Mg1.5Al0.5O6Fe2Se2 -> 0.125 e/Fe, 2x1x1
G = A.copy(); G.make_supercell([2, 1, 1])
idx = [i for i, s in enumerate(G) if s.specie.symbol == "Mg"]
G.replace(idx[0], "Al")
G.to(filename="structures/G_Sr4Mg1.5Al0.5O6Fe2Se2.cif")
print("done")
