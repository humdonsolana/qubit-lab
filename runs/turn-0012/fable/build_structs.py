"""Build AlB2-type diboride designs around hole-doped BaB2.
Frontier: Bercx et al., PRX Energy 4, 033012 (2025) / arXiv:2503.10943: pristine P6/mmm BaB2 has a soft
acoustic mode at H; homogeneous hole doping >=0.065 h/cell stabilises it; lambda=1.39, Tc_aniso=61.6 K.
Their only explicit dopant test (1 Cs in 3x3x1) FAILED to stabilise (local stress, E_F shift +0.64 eV).
Design idea here: K+ is nearly size-matched to Ba2+ (Shannon CN12: K 1.64, Ba 1.61, Cs 1.88 A), so
ordered Ba(1-x)K(x)B2 should dope holes without the Cs lattice stress.
Run (in a writable dir): python build_structs.py; then labphys relax/hull/phonons/novelty on structs/*.cif"""
from pymatgen.core import Structure, Lattice
a, c = 3.26, 4.6
def alb2(M, a=a, c=c):
    return Structure(Lattice.hexagonal(a, c), [M, "B", "B"], [[0,0,0],[1/3,2/3,0.5],[2/3,1/3,0.5]])
S = {}
S["BaB2"] = alb2("Ba")
S["KB2"]  = alb2("K", a=3.2, c=4.9)
S["MgB2"] = alb2("Mg", a=3.085, c=3.52)
S["CaB2"] = alb2("Ca", 3.15, 4.1); S["SrB2"] = alb2("Sr", 3.25, 4.4)
s = alb2("Ba"); s.make_supercell([1,1,2]); s.replace(1, "K"); S["BaKB4"] = s      # x=0.5, layered
for dop in ["K","Na","Rb","Cs"]:
    s = alb2("Ba"); s.make_supercell([2,2,1]); s.replace(1, dop); S[f"Ba3{dop}B8"] = s   # x=0.25
s = alb2("Ba"); s.make_supercell([2,2,1]); s.replace(1, "Sr"); S["Ba3SrB8"] = s   # isovalent control
s = alb2("Mg",3.15,4.1); s.make_supercell([1,1,2]); s.replace(1,"Ba"); S["MgBaB4"] = s
s = alb2("Mg",3.1,3.8); s.make_supercell([1,1,3]); s.replace(1,"Ba"); S["Mg2BaB6"] = s
s = alb2("Mg",3.1,3.8); s.make_supercell([1,1,2]); s.replace(1,"Ca"); S["MgCaB4"] = s
import os; os.makedirs("structs", exist_ok=True)
for k,v in S.items():
    v.to(filename=f"structs/{k}.cif"); print(k, v.composition.reduced_formula, len(v), v.get_space_group_info())
