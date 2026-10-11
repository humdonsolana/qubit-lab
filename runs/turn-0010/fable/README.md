# Turn 10 — Fable: bilayer nickelate crystals / pressure / chemical substitution

Split with Astra: Astra took ambient films + the QPU bilayer benchmark; I took bulk crystals, pressure and substitution.

## Files
- `lit_bulk_nickelate_crystals_2025_2026.md` — sub-agent literature review (fetch_url of primary pages; items it could not verify are marked UNVERIFIED).
- `c_axis_extrapolation.py` / `c_axis_extrapolation.json` — the only completed calculation (see below).
- `chgnet_c_axis_pressure.py` — CHGNet c-axis-vs-pressure EOS for I4/mmm RE3Ni2O7 (RE = La, Nd, Sm). **Did not finish**: CHGNet cell relaxations in this sandbox ran >25 min per job without producing a point; no result claimed.

## Findings (numbers first)
1. Record pressurized nickelate Tc: La1.57Sm1.43Ni2O7−δ crystals, **96 K resistive onset** at 21.6–29.6 GPa, **no zero resistance** (Li et al., Nature 2026, doi:10.1038/s41586-025-09954-4). Bulk SC (zero R 73 K, Meissner 60 K) shown only for La2SmNi2O7 at ~21 GPa. Independent polycrystals saturate at 89 K (arXiv:2510.13342). La0.6Nd2.4Ni2O7: 93 K transport onset, 98±2 K RF signature only (arXiv:2510.12359 → Nat. Commun. 2026). No nickelate has zero resistance or Meissner above ~73 K; nothing above 100 K is established.
2. All of these crystals are **not superconducting at ambient pressure**; no report of pressure-quench retention of nickelate SC exists; substitution with smaller rare earths *raises* the required pressure (13 GPa at x_Nd=0.9 → 26 GPa at x_Nd=2.1) and drives x≥1.5 Sm samples insulating.
3. Chemical pressure to straight bonds at ambient fails: tetragonal La2SrNi2O7−δ (180° Ni–O–Ni, I4/mmm) is metallic and not SC under pressure or oxygen variation (arXiv:2609.00542); tetragonal oxygen-rich La3Ni2O7 and tetragonal La4Ni3O10 are also not SC.
4. c-axis descriptor test (`c_axis_extrapolation.py`): using the published dTc/dc ≈ −28 K/Å (my 4-point refit: −32.5 K/Å), reaching 133 K would require c ≈ 18.6–18.9 Å, i.e. **1.2–1.5 Å (6–7 %) less than the most-compressed known composition** (c = 20.13 Å for La0.6Nd2.4 / La1.5Sm1.5), and 300 K would need c ≈ 12.7–13.8 Å, unphysical. Rare-earth substitution has already hit its solubility/stability limit at c ≈ 20.13 Å. The linear descriptor therefore gives no route above 133 K by chemical compression; it is also an onset-based, 4-point correlation, not a mechanism.
5. Dispute audit: no retraction/correction notices on Sun 2023 (80 K) or Li 2026 (96 K) Nature pages; Ko et al. 2025 has an Author Correction (units/axis label only, Nature 652, E8). PubPeer unreachable (403); Retraction Watch reported no matches (Astra).

## Verdict
No evidence-backed candidate above 133 K at ambient pressure in bulk bilayer nickelates; the family's pressurized ceiling (~96 K onset) is itself unretained at 1 bar. **No candidate submitted.** C0001 status unchanged (challenged, turns 4/9).

## What would change this
A nickelate with c < 19 Å and straight bonds at ambient (none exists); or a pressure-quench showing retained SC in La2SmNi2O7 after decompression with zero resistance + diamagnetism.
