"""Turn 9 (Fable): how well have harmonic-DFT/Eliashberg Tc predictions for cage/clathrate
hydrides matched experiment, and what does that track record imply for the ambient-pressure
predictions now on the table (Mg2IrH6 66-160 K, MgAlFeH6 ~130 K)?

Data: (predicted Tc at or near the experimental pressure, measured Tc onset) pairs for hydrides
with a synthesised, superconducting phase of the predicted structure.  Sources listed per entry;
numbers are from the abstracts/tables cited and were transcribed by me (flagged 'tier' = how
clean the comparison is: A = same structure, same pressure within ~30 GPa; B = different pressure
or uncertain phase identity).

Also: Allen-Dynes inversion -- which (lambda, omega_log) pairs give Tc >= 133 K, compared to the
(lambda, omega_log) of the ambient-stable hydride set in Sanna et al. Commun. Phys. 2026 (max 17 K).
Outputs: outputs/calibration.json, outputs/calibration.txt
"""
import json, numpy as np, os
os.makedirs("outputs", exist_ok=True)

pairs = [
 # name, Tc_pred(K), Tc_exp(K), P_exp(GPa), tier, source note
 ("H3S Im-3m",        200, 203, 155, "A", "pred Duan et al. Sci.Rep.4,6968(2014) 191-204K@200GPa; exp Drozdov Nature 525,73(2015)"),
 ("LaH10 Fm-3m",      280, 250, 170, "A", "pred Liu et al. PNAS 114,6990(2017) 274-286K@210GPa; exp Drozdov Nature 569,528(2019)/Somayazulu PRL 122,027001"),
 ("YH6 Im-3m",        264, 224, 166, "A", "pred Peng et al. PRL 119,107001(2017) 264K@120GPa; exp Troyan Adv.Mater.33,2006832(2021) 224K@166GPa"),
 ("YH9 P63/mmc",      276, 243, 201, "A", "pred Peng 2017 276K@150GPa; exp Kong Nat.Commun.12,5075(2021) 243K@201GPa"),
 ("CaH6 Im-3m",       228, 215, 172, "A", "pred Wang et al. PNAS 109,6463(2012) 220-235K@150GPa; exp Ma PRL 128,167001(2022)"),
 ("ThH10 Fm-3m",      230, 161, 175, "A", "pred Kvashnin ACS AMI 10,43809(2018) 220-241K@100GPa; exp Semenok Mater.Today 33,36(2020) 161K@175GPa"),
 ("CeH9 P63/mmc",     110, 100, 110, "A", "pred Peng 2017 105-117K@100GPa; exp Salke Nat.Commun.10,4453(2019) ~100K; Chen PRL 127,117001(2021) up to 115K"),
 ("LaBeH8 Fm-3m",     185, 110,  80, "B", "pred Zhang PRL 128,047001(2022) 185K@20GPa (harmonic); exp Song PRL 130,266001(2023) 110K@80GPa; pred at 80GPa not reported in abstract"),
 ("BaSiH8 Fm-3m",      71,   9, 142, "B", "pred Lucrezi npj CM 8,119(2022) 71K@30GPa (SSCHA); exp Semenok arXiv:2603.14051 9K@142GPa, non-metal <50GPa"),
 ("Mg2RhH6 Fm-3m",     48,  24,  30, "B", "pred Sanna npj CM 10,44(2024) 45-52K@0GPa; exp Wu/Jin JACS 148,36854(2026) 24K@30GPa, 29K@53GPa"),
]

names = [p[0] for p in pairs]; Tp = np.array([p[1] for p in pairs], float); Te = np.array([p[2] for p in pairs], float)
tier = np.array([p[4] for p in pairs]); Pexp = np.array([p[3] for p in pairs], float)
ratio = Te / Tp

lines = []
lines.append(f"{'material':16s} {'Tpred':>6s} {'Texp':>6s} {'P':>5s} tier  Texp/Tpred")
for n, a, b, p, t, r in zip(names, Tp, Te, Pexp, tier, ratio):
    lines.append(f"{n:16s} {a:6.0f} {b:6.0f} {p:5.0f}  {t}    {r:5.2f}")
A = tier == "A"; B = tier == "B"
lines.append(f"\nTier A (same structure, P within ~50 GPa; n={A.sum()}): median ratio {np.median(ratio[A]):.2f}, "
             f"range {ratio[A].min():.2f}-{ratio[A].max():.2f}")
lines.append(f"Tier B (low-P ternaries, imperfect comparison; n={B.sum()}): median ratio {np.median(ratio[B]):.2f}, "
             f"range {ratio[B].min():.2f}-{ratio[B].max():.2f}")

# Does the ratio trend with pressure?  Spearman-type check on all points
from scipy.stats import spearmanr, linregress
rho, pval = spearmanr(Pexp, ratio)
lines.append(f"Spearman(ratio vs P_exp) over all 10: rho={rho:.2f}, p={pval:.3f}")
lr = linregress(np.log(Tp), np.log(Te))
lines.append(f"log-log fit all 10: Texp = {np.exp(lr.intercept):.3f} * Tpred^{lr.slope:.2f}  (R^2={lr.rvalue**2:.2f})")
lrA = linregress(Tp[A], Te[A])
lines.append(f"Tier-A linear fit: Texp = {lrA.slope:.2f}*Tpred + {lrA.intercept:.1f}  (R^2={lrA.rvalue**2:.2f})")

# Apply the three scalings to the live ambient predictions
amb = {"Mg2IrH6 (Dolui 2024, mu*=0.16)": 160, "Mg2IrH6 (Sanna 2024, ab initio Coulomb)": 71,
       "MgAlFeH6 (npj CM 2026, aniso Eliashberg)": 130, "LaBeH8 harmonic at 20 GPa": 185}
lines.append("\nImplied experimental Tc if the past record holds (three scalings):")
lines.append(f"{'prediction':44s} {'xTierA_med':>10s} {'xTierB_med':>10s} {'loglog':>8s}")
proj = {}
for k, v in amb.items():
    a = v * np.median(ratio[A]); b = v * np.median(ratio[B]); c = np.exp(lr.intercept) * v ** lr.slope
    proj[k] = dict(pred=v, tierA=a, tierB=b, loglog=c)
    lines.append(f"{k:44s} {a:10.0f} {b:10.0f} {c:8.0f}")

# ---------- Allen-Dynes: what (lambda, omega_log) is needed for 133 K ----------
def allen_dynes(lam, wlog_meV, mu=0.10, w2_over_wlog=1.2):
    # Allen & Dynes PRB 12, 905 (1975) with strong-coupling f1 and shape f2 corrections
    kB = 8.617e-5  # eV/K
    wlog = wlog_meV * 1e-3 / kB  # K
    L1 = 2.46 * (1 + 3.8 * mu); L2 = 1.82 * (1 + 6.3 * mu) * w2_over_wlog
    f1 = (1 + (lam / L1) ** 1.5) ** (1 / 3)
    f2 = 1 + ((w2_over_wlog - 1) * lam ** 2) / (lam ** 2 + L2 ** 2)
    return f1 * f2 * wlog / 1.2 * np.exp(-1.04 * (1 + lam) / (lam - mu * (1 + 0.62 * lam)))

# reproduce the published numbers as a sanity check
chk = {"Mg2IrH6 Sanna lam2.1 w50 mu0.10": allen_dynes(2.1, 50, 0.10),
       "Mg2IrH6 Sanna lam2.1 w50 mu0.16": allen_dynes(2.1, 50, 0.16),
       "Mg2IrH6 Sanna lam2.1 w50 mu0.25": allen_dynes(2.1, 50, 0.25),
       "Mg2RhH6 Sanna lam1.3 w66 mu0.10": allen_dynes(1.3, 66, 0.10),
       "Mg2RhH6 Sanna lam1.3 w66 mu0.16": allen_dynes(1.3, 66, 0.16)}
lines.append("\nAllen-Dynes checks (w2/wlog=1.2 assumed):")
for k, v in chk.items(): lines.append(f"  {k}: {v:.0f} K")

lines.append("\nlambda required for Tc=133 K (Allen-Dynes, w2/wlog=1.2):")
need = {}
for mu in (0.10, 0.13, 0.16, 0.20):
    row = []
    for w in (30, 40, 50, 60, 80, 100):
        lams = np.linspace(0.3, 6, 2000); tcs = allen_dynes(lams, w, mu)
        ok = lams[tcs >= 133]
        lam_req = float(ok[0]) if ok.size else None
        row.append((w, lam_req))
    need[mu] = row
    lines.append(f"  mu*={mu:.2f}: " + ", ".join(f"wlog={w}meV->lam>={l:.2f}" if l else f"wlog={w}meV->none<6" for w, l in row))
lines.append("Context: Sanna/Errea Commun.Phys. 9,94 (2026) screened thermodynamically-stable GNoME hydrides -> max Tc 17 K; "
             "the 133 K line needs lam ~1.5-2.5 at wlog 50-80 meV, i.e. Mg2IrH6-class coupling, which so far appears only in off-hull H6 cages.")

txt = "\n".join(lines); print(txt)
open("outputs/calibration.txt", "w").write(txt + "\n")
json.dump(dict(pairs=[dict(name=n, Tpred=a, Texp=b, P=p, tier=t, ratio=r, note=s) for (n,a,b,p,t,s), r in zip(pairs, ratio)],
               tierA_median=float(np.median(ratio[A])), tierB_median=float(np.median(ratio[B])),
               loglog=dict(prefactor=float(np.exp(lr.intercept)), exponent=float(lr.slope), r2=float(lr.rvalue**2)),
               spearman_P=dict(rho=float(rho), p=float(pval)), projections=proj, allen_dynes_checks=chk,
               lambda_required_for_133K={str(k): v for k, v in need.items()}),
          open("outputs/calibration.json", "w"), indent=1)
