# Turn 9 — Fable — heavy-element-cage hydrides at moderate pressure

Split with Astra: Astra took LaSc2H24 / thermodynamic pressure-to-ambient gates, the C0001 Coulomb-sensitivity numbers and the QPU benchmark (3-qubit Holstein); I took the <~100 GPa heavy-cage leads, the retraction/dispute audit and a prediction-vs-experiment calibration. No Fable QPU use this turn (agreed, to avoid duplicating hardware).

## Files
- `lit_low_pressure_cage_hydrides.md` — sub-agent literature review 2024–Oct 2026 with per-number verification tiers (V-src / V-id / 2nd). Tables: confirmed Tc>100 K ranked by lowest pressure; predictions with low stability pressure.
- `dispute_audit.md` — retraction / expression-of-concern / failed-replication check for every source used (PubPeer and Retraction Watch unreachable from sandbox: HTTP 403 — stated, not glossed).
- `hydride_prediction_calibration.py` → `outputs/calibration.{txt,json}` — (i) Texp/Tpred for 10 synthesised hydrides; (ii) Allen–Dynes reproduction of Sanna's Mg2IrH6/Mg2RhH6 numbers and the (λ, ωlog) needed for 133 K.
- Sandbox note: the turn folder is not shell-writable (uid mismatch); script ran in /tmp/f9 and outputs were copied verbatim with write_file.

## What the newest evidence says (verified at source unless flagged)
1. **No hydride has a confirmed Tc > 100 K below ~78–80 GPa.** Lowest-pressure confirmed: LaBeH8 110 K @ 80 GPa (PRL 130, 266001; single group), LaB2H8 106 K @ 90 GPa (JACS 146, 13797; single group), (La,Ce)H9–10 150–178 K @ ~100 GPa (two independent groups — the only reproduced one). The Semenok review (Ann. Phys. 2025 e00467) concludes alloying lowers the stability pressure but never raises Tc above the parent binary.
2. **The first XYH8 cage recovered to ambient is a dud:** BaSiH8 (arXiv:2603.14051, Mar 2026) made at 18–31 GPa, survives to 1 bar, but Tc only 9 K at 142 GPa and a weakly-localised poor metal/degenerate semiconductor below 50 GPa, vs a 71 K SSCHA prediction. Kinetic (not dynamical) pressure controls survival, and the retained phase lost its metallicity.
3. **First experimental Mg2XH6:** Mg2RhH6 (Jin group, JACS 148, 36854 (2026)): 24 K @ 30 GPa, 29 K @ 53 GPa via Mg2RhH5 precursor + H supplementation, vs Sanna's 45–52 K at 0 GPa. The route exists; the number is ~half of the prediction (pressures differ, so treat as indicative).
4. **Mg2IrH6 theory is split:** Sanna et al. npj CM 10, 44 (2024) Table 1: λ=2.1, ωlog=50 meV, Tc 65.9/71/77 K (iso-SCDFT / aniso-SCDFT / iso-Eliashberg) vs Dolui's 160 K. My Allen–Dynes with the same λ, ωlog: 103/87/65 K at μ*=0.10/0.16/0.25 (Astra's independent envelope 84–90 K at μ*=0.16 agrees). Honest bracket 66–160 K; leaderboard 105 K is upper-half.
5. **Systemic negative:** Sanna/Errea Commun. Phys. 9, 94 (2026): thermodynamically stable GNoME hydrides max out at 17 K. Every ≥100 K ambient prediction (Mg2IrH6, MgAlFeH6 ~130 K at +0.11 eV/atom, RbPH3, LaBeH8 at 20 GPa) is off-hull.
6. **Calibration:** 7 like-for-like binary clathrates: Texp/Tpred median 0.89 (0.70–1.01). The 3 low-pressure ternaries actually made: 0.59 (LaBeH8), 0.13 (BaSiH8), 0.50 (Mg2RhH6). Applying the ternary median to the live ambient predictions: Mg2IrH6 (Dolui) → ~80 K, (Sanna) → ~36 K, MgAlFeH6 → ~65 K. None clears 133 K under any scaling except LaBeH8-at-20-GPa under the binary scaling (165 K), which is a harmonic number for a phase that has never been seen below 80 GPa. For 133 K Allen–Dynes needs λ ≥ 2.0 at ωlog = 80 meV or λ ≥ 3.5 at 50 meV (μ*=0.16) — coupling that so far exists only in off-hull H6/H8 cages.

## Candidate decision
**None submitted.** The direction (heavy cages, moderate pressure, ambient retention) has no evidence-backed route above 133 K at ambient pressure today: the best moderate-pressure Tc is 176 K at 100 GPa, nothing >30 K is confirmed below 30 GPa, and the one ambient-recovered cage compound is not a good metal. The only live sub-bar leads with an upward path are the Mg2XH6 family (synthesis route now demonstrated for Rh; Ir would need the H6 phase that Sinha's experiments bypass toward H7→H5) and electron-doped Mg2PtH6 (Sanna: ">100 K with appropriate electron doping", on-hull parent) — both are literature predictions I did not re-compute, so I do not put them on the board.

## C0001 review
Filed **challenges** (reason in the review and in `dispute_audit.md`): theory bracket 66–160 K, ternary calibration ~36–80 K, phase access unchanged (H7→H5, no H6 observed). Defensible number ~70–80 K, low confidence, conditional on a non-equilibrium H6 route.

## Recommendation for turn 10
Leave moderate-pressure hydrides unless someone shows a recovered cage hydride that stays metallic at 1 bar. Strongest remaining ambient leads are still the cuprate pressure-quench retention problem (turn 8: Arrhenius gate for the 151 K state) and nickelate-film oxygen retention (turn 5). If hydrides come back, the useful computation is kinetic (decomposition barrier at 1 bar), not more Eliashberg.
