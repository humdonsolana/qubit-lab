"""Conditional forecast: pressure-quenched fluorinated Hg-1223.

Logic (all inputs are literature numbers, cited in README):
 * Deng et al. PNAS 2026 (10.1073/pnas.2536178123): five PQ protocols on pristine Hg-1223 (baseline onset 133 K).
   Retained-excess ratio r = (Tc_retained - 133)/(Tc_at_Pq - 133), from Astra's protocol table
   (runs/turn-0008/astra/source_inputs.json).
 * Monteverde et al. EPL 72, 458 (2005): fluorinated Hg-1223, ambient chi-onset 138 K (Lokshin et al. PRB 2001),
   Tc(P) rises to a maximum 166 +/- 1 K at 23 GPa then falls.
 * Forecast: apply the same PQ protocol (Tq = 4.2 K, Pq ~ 19-23 GPa) to F-Hg-1223 and assume the same
   retained-excess ratio. This is an AI extrapolation, not a measurement.
"""
import json, numpy as np
base = 133.0
protocols = [  # (Pq GPa, Tq K, Tc at Pq (dR/dT onset), first retained onset)
    (26.0, 77, 152, 139), (28.4, 4.2, 154, 147), (10.1, 4.2, 152, 147),
    (10.9, 4.2, 154, 149), (18.9, 4.2, 158, 151)]
r = [(t_ret - base) / (t_p - base) for _, _, t_p, t_ret in protocols]
r_cold = r[1:]  # Tq = 4.2 K protocols only
print("retained-excess ratios:", np.round(r, 3), " cold-quench mean %.3f  min %.3f  max %.3f" % (np.mean(r_cold), min(r_cold), max(r_cold)))

# F-Hg-1223: parabola Tc(P) through (0,138), (23,166) with maximum at 23 GPa -> Tc = 166 - k(P-23)^2, k=(166-138)/23^2
k = (166 - 138) / 23 ** 2
TcF = lambda P: 166 - k * (P - 23) ** 2
out = {}
for Pq in [10.0, 19.0, 23.0]:
    tp = TcF(Pq)
    exc = tp - 138
    out[Pq] = dict(Tc_at_Pq=tp, retained_mean=138 + np.mean(r_cold) * exc,
                   retained_min=138 + min(r_cold) * exc, retained_max=138 + max(r_cold) * exc)
    print("Pq=%4.1f GPa: Tc(P)=%.1f K -> retained onset %.1f K (range %.1f-%.1f)" % (Pq, tp, out[Pq]["retained_mean"], out[Pq]["retained_min"], out[Pq]["retained_max"]))
# sensitivity: if retention in F-sample is only half as efficient (F lattice already chemically compressed)
half = 138 + 0.5 * np.mean(r_cold) * (TcF(23) - 138)
print("half-efficiency pessimistic case at 23 GPa: %.1f K" % half)
json.dump(dict(ratios=r, cold_mean=float(np.mean(r_cold)), forecast={str(k_): v for k_, v in out.items()},
               pessimistic_half_eff_23GPa=float(half),
               note="dR/dT onsets, metastable state; fades above ~200 K per PNAS 2026; not a stable-at-300-K prediction"),
          open("outputs/fhg1223_pq_forecast.json", "w"), indent=1)
