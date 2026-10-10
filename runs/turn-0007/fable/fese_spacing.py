"""Tc vs FeSe interlayer spacing for bulk intercalates: does more spacing keep buying Tc?
Data points (d = Fe-layer spacing / c-axis per FeSe layer, Angstrom; Tc = diamagnetic/bulk onset, K).
Transcribed from memory of the literature plus the 2026 (THA)xFeSe paper (CPL 43, 050710); treat as
approximate (+-0.3 A, +-2 K) and re-verify before quoting. Fit Tc(d) = Tsat*(1-exp(-(d-d0)/w)).
Ran in /tmp/f7 (turn folder not shell-writable); outputs copied verbatim.
"""
import numpy as np, json
from scipy.optimize import curve_fit
data = [
 ("FeSe",                 5.5,  8.5),
 ("K0.8Fe2Se2",           7.0, 31.0),
 ("Lix(NH3)yFe2Se2",      8.2, 44.0),
 ("(Li,Fe)OHFeSe",        9.3, 41.0),
 ("Li(C2H8N2)yFe2Se2",   10.4, 45.0),
 ("Lix(C5H5N)yFe2Se2",   12.0, 39.0),   # Chem. Mater. 37, 8581 (2025) ~39 K
 ("(TBA)xFeSe",          15.5, 43.0),   # chi onset; resistive onset ~50 K
 ("(THA)xFeSe",          18.4, 44.2),   # chi onset S2 (CPL 2026); rho onset 55.4 K, zero 33.7 K
]
d = np.array([r[1] for r in data]); tc = np.array([r[2] for r in data])
f = lambda d, Ts, d0, w: Ts*(1-np.exp(-(d-d0)/w))
p,_ = curve_fit(f, d, tc, p0=(45,5,1.5), maxfev=20000)
res = tc - f(d,*p)
print("fit Tsat=%.1f K d0=%.2f A w=%.2f A ; rms resid=%.2f K" % (*p, np.sqrt(np.mean(res**2))))
print("Tc at d->inf under this fit: %.1f K ; mean Tc for d>=8 A: %.1f K, sd %.1f K" % (p[0], tc[d>=8].mean(), tc[d>=8].std()))
json.dump(dict(data=data, fit=dict(Tsat=p[0], d0=p[1], w=p[2]), rms_resid=float(np.sqrt(np.mean(res**2))),
               mean_Tc_d_ge_8=float(tc[d>=8].mean()), sd=float(tc[d>=8].std())), open("outputs/fese_spacing.json","w"), indent=1)
