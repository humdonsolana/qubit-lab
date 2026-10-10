"""Kinetic gate for the pressure-quenched Hg-1223 151 K state (Deng et al. PNAS 2026).

Reported stability facts (per Astra's primary audit of the PNAS paper/SI, turn 8):
  * sample kept at 77 K for 3 days with repeated warm-ups to 160-170 K: slight decrease of Tc (149 K sample)
  * the enhanced state degrades when warmed above ~200 K; near 300 K it is lost
We model the relaxing degree of freedom (unknown: lattice strain, oxygen/apical sublattice,
defect ordering) as a single Arrhenius process k = nu0 exp(-Ea/kT), nu0 = 1e13 s^-1
(standard attempt-frequency assumption; a 1e12-1e14 range changes Ea by only +-0.06 eV).

Questions
 1. What Ea range is consistent with: survival (<~10% loss) over 3 d at 77 K (trivially satisfied
    for any Ea > 0.25 eV), survival through warm-up to 170 K for ~1 h, and loss (>63%) within
    ~1 h at 200-300 K?
 2. What Ea would be needed for 1-year survival at 300 K (the engineering goal)?
 3. Compare to known barriers: oxygen diffusion/ordering in YBCO chains ~0.9-1.3 eV (mobile above ~300 K),
    interstitial O in Hg-1201 HgO delta layer ~0.6-1.0 eV (literature range, see lit_pq_cuprates.md),
    elastic strain relaxation via dislocation glide (athermal, 0 eV), Hg-O_delta local reordering (<0.5 eV?).
Outputs outputs/retention_kinetics.json
"""
import json, numpy as np
kB = 8.617e-5
nu0 = 1e13
def tau(Ea, T): return np.exp(Ea / (kB * T)) / nu0
def Ea_for(tau_s, T): return kB * T * np.log(tau_s * nu0)

res = {}
# constraints
# A: at least ~90% survival after 3 d at 77 K  -> tau(77) > 3d/0.105
res["Ea_min_77K_3d_90pct"] = Ea_for(3 * 86400 / 0.105, 77)
# B: survive 1 h at 170 K with <10% loss
res["Ea_min_170K_1h_90pct"] = Ea_for(3600 / 0.105, 170)
# C: lost (>63%) within 1 h at 200 K   (upper bound if loss is seen at 200 K within an hour)
res["Ea_max_200K_1h_lost"] = Ea_for(3600, 200)
# C': lost within 1 h at 300 K
res["Ea_max_300K_1h_lost"] = Ea_for(3600, 300)
# D: engineering goal 1 y at 300 K, 90% survival
res["Ea_goal_300K_1yr_90pct"] = Ea_for(365 * 86400 / 0.105, 300)
# E: 1 y at 77 K (LN2 storage)
res["Ea_goal_77K_1yr_90pct"] = Ea_for(365 * 86400 / 0.105, 77)
for k, v in res.items(): print("%-28s %.3f eV" % (k, v))

# tau table
T = [77, 150, 170, 200, 250, 300]
tab = {}
for Ea in [0.4, 0.5, 0.6, 0.8, 1.0, 1.2]:
    tab[Ea] = {t: tau(Ea, t) for t in T}
    print("Ea=%.1f eV: " % Ea + "  ".join("%dK:%.1e s" % (t, tau(Ea, t)) for t in T))

summary = dict(
    assumptions="single Arrhenius process, nu0=1e13/s, first-order decay; +-1 decade in nu0 = -+0.06 eV at 300 K, -+0.015 eV at 77 K",
    constraints_eV={k: float(v) for k, v in res.items()},
    tau_table_s={str(k): {str(t): float(x) for t, x in v.items()} for k, v in tab.items()},
    reading=(
        "The source's own facts (survives 170 K excursions, lost at ~200-300 K within the experiment's hours) bracket "
        "the effective barrier at about 0.55-0.9 eV. This is far above an athermal elastic-strain release (which "
        "would relax on decompression, consistent with the lattice NOT staying compressed in XRD) and sits in the "
        "range of interstitial/apical oxygen hopping in Hg- and Y-based cuprates (~0.6-1.0 eV; chain ordering in YBCO "
        "~1 eV is mobile only above ~300 K). A 300 K, 1-year retained state needs Ea >= ~1.2 eV, i.e. the metastable "
        "degree of freedom must be pinned by something ~0.3-0.6 eV stiffer than a mobile oxygen interstitial - "
        "e.g. fluoride on the O_delta site (stronger Hg-F/Ba-F binding), or quenching below the oxygen-mobility "
        "onset in a matrix where O_delta is replaced by an immobile anion."),
)
json.dump(summary, open("outputs/retention_kinetics.json", "w"), indent=1)
