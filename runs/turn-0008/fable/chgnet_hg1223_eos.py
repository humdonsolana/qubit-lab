"""CHGNet equation of state for HgBa2Ca2Cu3O8 (Hg-1223, P4/mmm) and the
'frozen-compression' test for the pressure-quenched 151 K state.

Question: if the retained 151 K state were a uniformly frozen high-pressure
lattice, how much volume compression would it have to carry, and would XRD see it?

Steps
 1. build Hg-1223 from literature P4/mmm coordinates, relax with CHGNet (0.4.2)
 2. scan volume, fit 3rd-order Birch-Murnaghan -> B0, B0'
 3. with the literature Tc(P) curve (Gao et al. PRB 50, 4260 1994: 133 K -> 164 K at 31 GPa)
    find the 'equivalent pressure' P_eq for Tc = 151 K and the corresponding V/V0 and a, c
 4. compare with the recovered-sample XRD statement (lattice NOT contracted, (200) only
    broadened) from Deng et al. PNAS 2026 -> uniform frozen compression is excluded.
Outputs: outputs/hg1223_eos.json, outputs/hg1223_relaxed.cif
"""
import json, numpy as np, warnings
warnings.filterwarnings("ignore")
from pymatgen.core import Structure, Lattice
from pymatgen.io.ase import AseAtomsAdaptor
from pymatgen.analysis.eos import EOS
from chgnet.model import CHGNet, StructOptimizer
from chgnet.model.dynamics import CHGNetCalculator
from ase.filters import UnitCellFilter, ExpCellFilter
from ase.optimize import FIRE

# Hg-1223 P4/mmm, a=3.8532, c=15.818 (Hunter et al. 1994-type coordinates, approx.)
a, c = 3.8532, 15.818
species = ["Hg", "Ba", "Ba", "Ca", "Ca", "Cu", "Cu", "Cu",
           "O", "O", "O", "O", "O", "O", "O", "O"]
coords = [
    [0, 0, 0],                       # Hg
    [0.5, 0.5, 0.1750], [0.5, 0.5, 0.8250],   # Ba
    [0.5, 0.5, 0.3975], [0.5, 0.5, 0.6025],   # Ca
    [0, 0, 0.5],                              # Cu1 (inner plane)
    [0, 0, 0.2995], [0, 0, 0.7005],           # Cu2 (outer planes)
    [0, 0, 0.1230], [0, 0, 0.8770],           # O apical
    [0, 0.5, 0.3015], [0.5, 0, 0.3015],       # O eq outer
    [0, 0.5, 0.6985], [0.5, 0, 0.6985],
    [0, 0.5, 0.5], [0.5, 0, 0.5],             # O eq inner
]
s = Structure(Lattice.tetragonal(a, c), species, coords)
assert s.composition.reduced_formula == "HgBa2Ca2Cu3O8", s.composition
model = CHGNet.load()
opt = StructOptimizer(model=model)
res = opt.relax(s, fmax=0.02, steps=600, verbose=False)
s0 = res["final_structure"]
e0 = res["trajectory"].energies[-1]
print("relaxed a=%.4f c=%.4f V=%.3f E=%.4f eV/cell" % (s0.lattice.a, s0.lattice.c, s0.volume, e0))

# volume scan with fixed-volume cell-shape+ion relaxation
calc = CHGNetCalculator(model=model)
vols, ens, acs = [], [], []
for f in np.linspace(0.80, 1.06, 14):
    st = s0.copy(); st.scale_lattice(s0.volume * f)
    atoms = AseAtomsAdaptor.get_atoms(st); atoms.calc = calc
    ucf = UnitCellFilter(atoms, constant_volume=True)
    FIRE(ucf, logfile=None).run(fmax=0.03, steps=300)
    vols.append(atoms.get_volume()); ens.append(atoms.get_potential_energy())
    cell = atoms.cell.cellpar(); acs.append((cell[0], cell[2]))
    print("V/V0=%.3f V=%.2f E=%.4f a=%.4f c=%.4f" % (f, vols[-1], ens[-1], cell[0], cell[2]))

eos = EOS("birch_murnaghan").fit(vols, ens)
B0_GPa = eos.b0_GPa; V0 = eos.v0; Bp = eos.b1
print("BM fit: V0=%.3f A^3  B0=%.1f GPa  B0'=%.2f" % (V0, B0_GPa, Bp))

def P_BM(V):
    x = (V0 / V) ** (2 / 3)
    return 1.5 * B0_GPa * (x ** 3.5 - x ** 2.5) * (1 + 0.75 * (Bp - 4) * (x - 1))

# literature Tc(P) of Hg-1223 (Gao et al. 1994): 133 K ambient, ~153 K at 15 GPa, 164 K at 31 GPa
# parabola through those three points
P = np.array([0, 15, 31.]); T = np.array([133, 153, 164.])
cf = np.polyfit(P, T, 2)
Tc = lambda p: np.polyval(cf, p)
P151 = min(np.roots(np.array([cf[0], cf[1], cf[2] - 151])).real)
# volume at P151
Vgrid = np.linspace(0.8 * V0, V0, 2000); Pgrid = P_BM(Vgrid)
V151 = np.interp(P151, Pgrid[::-1], Vgrid[::-1])
# anisotropic a,c at that V from scan (interpolate)
vs = np.array(vols); aa = np.array([x[0] for x in acs]); cc = np.array([x[1] for x in acs])
o = np.argsort(vs)
a151 = np.interp(V151, vs[o], aa[o]); c151 = np.interp(V151, vs[o], cc[o])
aV0 = np.interp(V0, vs[o], aa[o]); cV0 = np.interp(V0, vs[o], cc[o])
# Bragg shift of (200) CuKa for that a-contraction
lam = 1.5406
tt = lambda d: 2 * np.degrees(np.arcsin(lam / (2 * d)))
shift200 = tt(a151 / 2) - tt(aV0 / 2)
out = dict(relaxed=dict(a=s0.lattice.a, c=s0.lattice.c, V=s0.volume),
           exp_ref=dict(a=3.8532, c=15.818, note="Hunter et al. 1994 approx."),
           eos=dict(V0=V0, B0_GPa=B0_GPa, B0p=Bp, points=[dict(V=v, E=e, a=x[0], c=x[1]) for v, e, x in zip(vols, ens, acs)]),
           Tc_curve=dict(coef=cf.tolist(), anchors="0/133, 15/153, 31/164 (Gao PRB 1994 digitised, approx)"),
           frozen_compression_test=dict(P_eq_151K_GPa=float(P151), V_over_V0=float(V151 / V0),
                                        a_at_Peq=float(a151), c_at_Peq=float(c151), a_V0=float(aV0), c_V0=float(cV0),
                                        da_over_a_pct=float(100 * (a151 / aV0 - 1)), dc_over_c_pct=float(100 * (c151 / cV0 - 1)),
                                        CuKa_200_shift_deg=float(shift200),
                                        reported_200_FWHM_deg=dict(pristine=0.12, recovered=0.20, source="Deng et al. PNAS 2026 Fig.3 per Astra audit")))
print(json.dumps(out["frozen_compression_test"], indent=1))
json.dump(out, open("outputs/hg1223_eos.json", "w"), indent=1)
s0.to(filename="outputs/hg1223_relaxed.cif")
