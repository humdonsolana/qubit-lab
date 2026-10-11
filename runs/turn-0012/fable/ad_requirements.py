"""Allen-Dynes lambda required for Tc = 133 K as a function of omega_log and mu*."""
import numpy as np
def ad(lam, wlog, mu):
    f1 = (1 + (lam / (2.46 * (1 + 3.8 * mu))) ** 1.5) ** (1 / 3)
    return f1 * wlog / 1.2 * np.exp(-1.04 * (1 + lam) / (lam - mu * (1 + 0.62 * lam)))
for wl_meV in [50, 60, 70, 80, 100]:
    wl = wl_meV * 11.604
    for mu in [0.10, 0.13, 0.16]:
        lam = np.linspace(0.5, 4, 3501); tc = ad(lam, wl, mu)
        need = lam[np.argmax(tc >= 133)] if tc.max() >= 133 else None
        print(f"omega_log={wl_meV} meV mu*={mu}: lambda needed for 133 K = {need:.2f}")
# Output (outputs/ad_requirements.txt):
# 50 meV: 3.19/3.53/3.91 ; 60 meV: 2.45/2.70/2.98 ; 70 meV: 2.01/2.21/2.43 ; 80 meV: 1.73/1.90/2.08 ; 100 meV: 1.40/1.53/1.67
