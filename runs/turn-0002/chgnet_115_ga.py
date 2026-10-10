"""
CHGNet screen: is a Ga-based Ce-115 (CeCoGa5, HoCoGa5-type P4/mmm) plausibly
stable relative to simple competing phases, with CeCoIn5 as a calibration case?

Motivation: in the Ce-115 family Tc tracks the Kondo coherence scale T*
(Tc/T* ~ 0.016 for CeCoIn5, see hf_ceiling.py).  Replacing In by the smaller Ga
would raise the f-c hybridization (chemical pressure) and thus T*.  CeCoGa5 is
not reported experimentally (the 115 Ga phases are known for Pu, Np, U, Am, and
the rare-earth RCoGa5 for small R=Ho..Lu/Y, but not Ce), which usually means it
does not form.  We check with CHGNet (CPU) whether it is far from the hull.

Competing phases built from standard prototypes (no MP API needed):
  Ce fcc (a=5.16), Co hcp (a=2.507,c=4.069), alpha-Ga (Cmce), In (tetragonal
  I4/mmm a=3.25 c=4.95), CeGa2 (AlB2-type, P6/mmm a=4.32 c=4.31), CeIn3 (Cu3Au,
  a=4.69), CoGa (CsCl, a=2.88), CoIn2 is skipped (complex); CoIn3 (FeGa3-type)
  skipped.  Hull is therefore approximate (an upper bound on the decomposition
  energy only if the omitted phases are less stable than our combinations).
Everything is relaxed with CHGNet (positions+cell).
"""
import numpy as np, json, warnings
warnings.filterwarnings("ignore")
from pymatgen.core import Structure, Lattice
from chgnet.model import StructOptimizer, CHGNet

model = CHGNet.load()
opt = StructOptimizer(model=model)

def relax(s, steps=300):
    r = opt.relax(s, fmax=0.05, steps=steps, verbose=False)
    fs = r["final_structure"]
    e = float(r["trajectory"].energies[-1]) / len(fs)  # eV/atom
    return fs, e

def s115(X, a, c):
    # HoCoGa5-type: Ce 1a (0,0,0); Co 1b (0,0,1/2); X1 1c (1/2,1/2,0); X2 4i (0,1/2,z~0.31)
    lat = Lattice.tetragonal(a, c)
    z = 0.31
    sp = ["Ce", "Co", X, X, X, X, X]
    fc = [[0,0,0],[0,0,.5],[.5,.5,0],[0,.5,z],[0,.5,-z],[.5,0,z],[.5,0,-z]]
    return Structure(lat, sp, fc)

structs = {
 "Ce":    Structure(Lattice.cubic(5.16), ["Ce"]*4, [[0,0,0],[.5,.5,0],[.5,0,.5],[0,.5,.5]]),
 "Co":    Structure(Lattice.hexagonal(2.507,4.069), ["Co","Co"], [[1/3,2/3,.25],[2/3,1/3,.75]]),
 "Ga":    Structure.from_spacegroup("Cmce", Lattice.orthorhombic(4.52,7.66,4.53), ["Ga"], [[0,0.1549,0.0810]]),
 "In":    Structure(Lattice.tetragonal(3.25,4.95), ["In","In"], [[0,0,0],[.5,.5,.5]]),
 "CeGa2": Structure(Lattice.hexagonal(4.32,4.31), ["Ce","Ga","Ga"], [[0,0,0],[1/3,2/3,.5],[2/3,1/3,.5]]),
 "CeIn3": Structure(Lattice.cubic(4.69), ["Ce","In","In","In"], [[0,0,0],[.5,.5,0],[.5,0,.5],[0,.5,.5]]),
 "CoGa":  Structure(Lattice.cubic(2.88), ["Co","Ga"], [[0,0,0],[.5,.5,.5]]),
 "CoIn":  Structure(Lattice.cubic(3.20), ["Co","In"], [[0,0,0],[.5,.5,.5]]),  # hypothetical CsCl, placeholder
 "CeCoIn5": s115("In", 4.61, 7.55),
 "CeCoGa5": s115("Ga", 4.20, 6.80),
}
E = {}; V = {}
for k, s in structs.items():
    fs, e = relax(s)
    E[k] = e; V[k] = fs.volume/len(fs)
    print(f"{k:8s} E={e:9.4f} eV/atom  V={V[k]:6.2f} A^3/atom  a,b,c={fs.lattice.abc}")

def decomp(target, parts):
    # parts: dict phase->number of formula units; energies per atom -> per cell
    natoms = {"Ce":1,"Co":1,"Ga":1,"In":1,"CeGa2":3,"CeIn3":4,"CoGa":2,"CoIn":2,"CeCoIn5":7,"CeCoGa5":7}
    Etot = sum(E[p]*natoms[p]*n for p,n in parts.items())
    return (E[target]*7 - Etot)/7  # eV/atom, negative = target more stable

res = {
 "CeCoIn5_vs_CeIn3+CoIn+In": decomp("CeCoIn5", {"CeIn3":1,"CoIn":1,"In":1}),
 "CeCoIn5_vs_CeIn3+Co+2In":  decomp("CeCoIn5", {"CeIn3":1,"Co":1,"In":2}),
 "CeCoIn5_vs_elements":      decomp("CeCoIn5", {"Ce":1,"Co":1,"In":5}),
 "CeCoGa5_vs_CeGa2+CoGa+2Ga": decomp("CeCoGa5", {"CeGa2":1,"CoGa":1,"Ga":2}),
 "CeCoGa5_vs_CeGa2+Co+3Ga":  decomp("CeCoGa5", {"CeGa2":1,"Co":1,"Ga":3}),
 "CeCoGa5_vs_elements":      decomp("CeCoGa5", {"Ce":1,"Co":1,"Ga":5}),
}
print(json.dumps({"E_per_atom_eV":E,"V_per_atom_A3":V,"decomposition_eV_per_atom":res}, indent=2))
