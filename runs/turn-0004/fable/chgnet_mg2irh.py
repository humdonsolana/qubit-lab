"""CHGNet check of Mg2IrH5 / Mg2IrH6 / Mg2IrH7 energetics for the review of C0001.
Reference-free disproportionation D = E5 + E7 - 2*E6 (per Mg2Ir formula unit).
If D > 0, cubic H6 has a window of hydrogen chemical potential where it is the
stable composition among 5/6/7; if D < 0, H6 is unstable to 1:1 H5 + H7.
CHGNet 0.4.2 (CPU). Hydrides are at the edge of the MP training set; absolute
energies are not trustworthy to better than ~30-50 meV/atom, so this is a
consistency check against the DFT numbers Astra extracted from Dolui et al.
"""
import json, numpy as np, warnings
warnings.filterwarnings("ignore")
from pymatgen.core import Structure, Lattice
from chgnet.model import StructOptimizer, CHGNet

model = CHGNet.load()
opt = StructOptimizer(model=model)

a = 6.60
# conventional Fm-3m K2PtCl6-type: Ir 4a, Mg 8c, H 24e (x,0,0)
x = 1.72 / a
def h6_conv():
    lat = Lattice.cubic(a)
    sp, fc = [], []
    fcc = [(0,0,0),(0,.5,.5),(.5,0,.5),(.5,.5,0)]
    for t in fcc:
        t = np.array(t)
        sp.append("Ir"); fc.append(t)
        for m in [(.25,.25,.25),(.75,.75,.75)]:
            sp.append("Mg"); fc.append((t+m)%1)
        for h in [(x,0,0),(-x,0,0),(0,x,0),(0,-x,0),(0,0,x),(0,0,-x)]:
            sp.append("H"); fc.append((t+h)%1)
    return Structure(lat, sp, fc)

s6c = h6_conv()
s6 = s6c.get_primitive_structure()          # 9 atoms
assert len(s6) == 9, len(s6)

# H5: remove one H per formula unit from the primitive cell (ordered vacancies)
s5 = s6.copy()
hidx = [i for i,s in enumerate(s5) if s.specie.symbol == "H"]
s5.remove_sites([hidx[0]])
# H7: add one H per f.u. at the octahedral interstitial 4b (1/2,1/2,1/2) of conventional cell
s7c = h6_conv()
s7c.append("H", (0.5,0.5,0.5)); s7c.append("H",(0.5,0,0)); s7c.append("H",(0,0.5,0)); s7c.append("H",(0,0,0.5))
s7 = s7c.get_primitive_structure()
assert len(s7) == 10, len(s7)

res = {}
for name, s in [("H5", s5), ("H6", s6), ("H7_cubic_4b", s7)]:
    r = opt.relax(s, fmax=0.02, steps=600, relax_cell=True, verbose=False)
    fs = r["final_structure"]
    e = float(r["trajectory"].energies[-1])  # eV total
    res[name] = dict(natoms=len(fs), E_total_eV=e, E_per_atom=e/len(fs),
                     E_per_fu=e, volume=fs.volume, lattice=fs.lattice.abc,
                     angles=fs.lattice.angles)
    fs.to(filename=f"outputs/Mg2Ir{name}_relaxed.cif")
    print(name, len(fs), f"E={e:.4f} eV  E/atom={e/len(fs):.4f}  V={fs.volume:.2f} A^3  abc={fs.lattice.abc}")

D = res["H5"]["E_per_fu"] + res["H7_cubic_4b"]["E_per_fu"] - 2*res["H6"]["E_per_fu"]
res["D_eV_per_fu"] = D
res["D_meV_per_H6_atom"] = 1000*D/9
res["mu_lower_eV"] = res["H6"]["E_per_fu"] - res["H5"]["E_per_fu"]   # E(H6)-E(H5): energy to add 1 H to H5
res["mu_upper_eV"] = res["H7_cubic_4b"]["E_per_fu"] - res["H6"]["E_per_fu"]
# isolated H2 for orientation only (CHGNet OOD)
h2 = Structure(Lattice.cubic(12.0), ["H","H"], [[0,0,0],[0.74/12,0,0]])
rh2 = opt.relax(h2, fmax=0.02, steps=200, relax_cell=False, verbose=False)
eh2 = float(rh2["trajectory"].energies[-1])
res["E_H2_isolated_eV"] = eh2
res["dE_H6_to_H5_plus_halfH2_eV"] = res["H5"]["E_per_fu"] + 0.5*eh2 - res["H6"]["E_per_fu"]
res["dE_H7_to_H6_plus_halfH2_eV"] = res["H6"]["E_per_fu"] + 0.5*eh2 - res["H7_cubic_4b"]["E_per_fu"]
print(json.dumps(res, indent=1, default=float))
json.dump(res, open("outputs/chgnet_mg2irh.json","w"), indent=1, default=float)
