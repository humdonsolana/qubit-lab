"""Allen-Dynes ceiling for the MgB2-mold (hole-doped sigma-band) family.

Published inputs (all from the sources' own tables; see lit notes in README):
  MgB2            lambda 0.87, omega_log ~ 62 meV  (measured Tc 39 K)        Choi et al. Nature 418, 758 (2002); isotropic lambda
  Li0.125Mg0.875B2C2  lambda_tot ~0.9-1.0, omega_ln 777 cm-1 (96 meV)      Spano et al. PRB 72, 014530 (2005): McMillan 67 K
  hole-doped LiBC (Li0.5BC) lambda ~ 1.0-1.5, Tc 65-100 K (predictions)     Rosner PRL 88,127001 (2002); Dewhurst PRB 68,020504 (2003)
  BaB2 (h-doped) lambda 1.39, Tc_aniso 61.6 K                              Bercx et al. PRX Energy 4, 033012 (2025)
  AgBC            two-gap > 50 K                                            Gochitashvili et al. arXiv:2507.14281 (2025)
Question: with omega_log pinned at 60-100 meV by B-C/B-B bond-stretching modes, what lambda does 133 K need,
and what does lambda do to omega_log (softening)?
"""
from labphys import tc
import json
rows = []
for wl_meV in (60, 70, 80, 90, 100):
    for lam in (1.0, 1.3, 1.6, 2.0, 2.5, 3.0):
        wl_K = wl_meV * 11.604
        r = {}
        for mu in (0.10, 0.13):
            r[mu] = round(tc.allen_dynes(lam, wl_K, mustar=mu), 1)
        rows.append({"omega_log_meV": wl_meV, "lambda": lam, "Tc_AD_mu0.10": r[0.10], "Tc_AD_mu0.13": r[0.13]})
need = {}
for wl_meV in (60, 70, 80, 90, 100):
    wl_K = wl_meV * 11.604
    lam = 0.5
    while tc.allen_dynes(lam, wl_K, mustar=0.13) < 133 and lam < 10:
        lam += 0.01
    need[wl_meV] = round(lam, 2)
out = {"table": rows, "lambda_needed_for_133K_mu0.13": need}
print(json.dumps(out["lambda_needed_for_133K_mu0.13"], indent=1))
for r in rows:
    print(r)
json.dump(out, open("outputs/family_ceiling.json", "w"), indent=1)
