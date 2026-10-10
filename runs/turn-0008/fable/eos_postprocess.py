"""Post-process the CHGNet volume scan of Hg-1223 (points copied from eos.log of
chgnet_hg1223_eos.py, whose final block crashed on a pymatgen FloatWithUnit type).
Fits 3rd-order Birch-Murnaghan, converts the 151 K 'equivalent pressure' from the
literature Tc(P) curve into a frozen-lattice contraction and a CuKa (200) Bragg shift."""
import json, numpy as np
from scipy.optimize import curve_fit, brentq
pts = [  # V(A^3), E(eV), a, c  (CHGNet 0.4.2 weights v0.3.0, fixed-V cell+ion relax, fmax 0.05)
 (209.47, -91.2214, 3.7694, 14.7425), (216.83, -91.8480, 3.8031, 14.9919),
 (224.24, -92.2636, 3.8218, 15.3523), (231.60, -92.5274, 3.8392, 15.7131),
 (238.92, -92.6603, 3.8693, 15.9586), (246.23, -92.6723, 3.9038, 16.1573),
 (253.53, -92.6093, 3.9260, 16.4488)]
V = np.array([p[0] for p in pts]); E = np.array([p[1] for p in pts])
A = np.array([p[2] for p in pts]); C = np.array([p[3] for p in pts])
def bm(V, E0, V0, B0, Bp):
    x = (V0 / V) ** (2 / 3)
    return E0 + 9 * V0 * B0 / 16 * ((x - 1) ** 3 * Bp + (x - 1) ** 2 * (6 - 4 * x))
p, _ = curve_fit(bm, V, E, p0=[-92.7, 244, 0.4, 5])
E0, V0, B0, Bp = p; B0_GPa = B0 * 160.2177
print("BM: V0=%.2f A^3 B0=%.1f GPa B0'=%.2f" % (V0, B0_GPa, Bp))
def P_BM(v):
    x = (V0 / v) ** (2 / 3)
    return 1.5 * B0_GPa * (x ** 3.5 - x ** 2.5) * (1 + 0.75 * (Bp - 4) * (x - 1))
# literature Tc(P) Hg-1223: 133 K (0), ~153 K (15 GPa), 164 K (31 GPa) [Gao et al. PRB 50, 4260 (1994), digitised approx.]
cf = np.polyfit([0, 15, 31], [133, 153, 164], 2)
P151 = brentq(lambda x: np.polyval(cf, x) - 151, 0, 31)
V151 = brentq(lambda v: P_BM(v) - P151, 0.8 * V0, V0)
o = np.argsort(V)
a151, c151 = np.interp(V151, V[o], A[o]), np.interp(V151, V[o], C[o])
a0, c0 = np.interp(V0, V[o], A[o]), np.interp(V0, V[o], C[o])
lam = 1.5406
tt = lambda d: 2 * np.degrees(np.arcsin(lam / (2 * d)))
out = dict(BM=dict(V0=V0, B0_GPa=B0_GPa, B0p=Bp, exp_B0_note="experimental Hg-1223 bulk modulus ~70-90 GPa (Hunter 1994 / Armstrong 1995 ranges); CHGNet value is in range"),
           P_eq_151K_GPa=P151, V_over_V0=V151 / V0, da_a_pct=100 * (a151 / a0 - 1), dc_c_pct=100 * (c151 / c0 - 1),
           shift_200_deg=tt(a151 / 2) - tt(a0 / 2), shift_006_deg=tt(c151 / 6) - tt(c0 / 6),
           reported=dict(pristine_200_FWHM=0.12, recovered_200_FWHM=0.20, recovered_lattice="slightly enlarged, not contracted (PNAS 2026 Fig.3, Astra audit)"))
for k, v in out.items(): print(k, v)
json.dump(out, open("outputs/hg1223_eos.json", "w"), indent=1)
