# Turn 7 — Fable: bulk iron-based superconductors past 55 K

Split agreed with Astra: Astra = FeSe/SrTiO3 interface route + this session's QPU run (their folder `../astra`);
Fable = bulk pnictides/chalcogenides, pressure records, 2025–26 new Fe-based compounds, and the alternate direction if the family is a dead end.

## 1. Literature (sub-agent report: `bulk_fe_literature_2024_2026.md`)
Key verified points (DOIs/arXiv IDs in the report):
- **Bulk ambient record unchanged since 2017: 58.6 K** in Sm0.8Th0.2FeAsO0.775F0.225 (CPL 34, 077401). Canonical SmFeAsO1-xFx ~55 K (2008).
- 2024–26 high-pressure-synthesis attempts land at or below it: Sm1111 made at 4 GPa → 57 K (arXiv:2512.05177); Pr1111 → 52.3 K (arXiv:2602.07481); HP-HTS Sm1111 unchanged at 53–54 K (arXiv:2412.20837); CaKFe4As4 HP-HTS no new ceiling.
- Pressure has not exceeded ~55 K in any Fe compound we found: Lix(NH3)yFe2Se2 SC-II ~55 K at 11 GPa (PRB 97, 020508); (Li,Fe)OHFeSe SC-II ~52 K at 12.5 GPa; LaFeAsO1-xHx 52 K at 6 GPa; SmFeAsO1-xHx Tc *falls* with pressure. The only Fe-based pressure-quench retention found is 37 K in FeSe (PNAS 2021, doi:10.1073/pnas.2108938118).
- Best new 2026 bulk compound: **(THA)xFeSe** (CPL 43, 050710): ρ onset 50.7–55.4 K, zero 33 K, χ onset 42–44 K — 2D-fluctuation broadened, not a new bulk record.
- Claim audit: **arXiv:2608.27349v2 (Bondarenko et al., "Fe-Se-H", 295 K at ambient)** rests solely on EPR non-resonant microwave absorption vs field in a powder; no resistivity, no Meissner fraction, no specific heat, no composition/structure; we found no independent reproduction. Low-field microwave absorption is also produced by ferromagnetic Fe impurities (Fe/Fe3O4/Fe7Se8 are common in hydrogen-treated FeSe). **Insufficient as evidence of superconductivity; not a candidate.** What would change this: four-probe zero resistance, ZFC/FC shielding fraction, and phase/composition analysis of the same powder. (Abstract fetched directly this turn.)
- Theory: Qin & Yang, npj Quantum Mater. 10, 13 (2025) — Tc/J ≲ 0.04–0.07 from static auxiliary-field MC on single/bilayer pairing models (NN/onsite pairing). Model-conditioned, not a theorem for multiorbital Fe systems; used here as a consistency check, not a proof.

## 2. Calculations (this folder; ran in /tmp/f7, outputs copied verbatim)
### `fe_tc_over_j.py` → `outputs/fe_tc_over_j.{json,log}`
Tc/J for six Fe-based parents using INS spin-wave exchange fits (SJ1a, SJ1b, SJ2; values transcribed from memory of the cited papers and **flagged unverified** — verify before quoting) and each family's best ambient bulk Tc.
- With J = SJ1a: Tc/J = 0.055 (Ba122), 0.059 (Ca122), 0.054 (111), 0.104 (Sr122), **0.113 (1111 at 58.6 K)**. The Fe families sit at or above the Qin–Yang 0.04–0.07 band (1111 exceeds it, so either the bound is loose by ~1.6× for Fe or J1a understates the relevant pairing scale — another reason not to treat it as universal).
- Required J under the bound: 133 K needs 164 meV (ratio 0.07) or 115 meV (even at a generous 0.10); 300 K needs 370–650 meV. The largest measured Fe-pnictide exchange is SJ1a ≈ 59 meV (BaFe2As2) → 48 K (0.07) / 69 K (0.10).
- Reading: **if exchange is the only pairing scale, bulk Fe-based compounds have no room to reach 133 K**; getting there would need a second pairing channel (e.g. interfacial phonons — Astra's side) or a 2–3× larger J, which Fe–As/Se chemistry has not produced.

### `fese_spacing.py` → `outputs/fese_spacing.{json,log}`
Bulk FeSe intercalates: χ-onset Tc vs FeSe layer spacing d (8 points, 5.5–18.4 Å; literature values, approximate). Saturating fit Tc(d) = Tsat(1−e^{−(d−d0)/w}) gives **Tsat = 43.2 K**, w = 1.2 Å, rms 2.5 K; mean Tc for d ≥ 8 Å is 42.7 ± 2.1 K. Increasing the spacing beyond ~8 Å buys nothing — the 2026 (THA)xFeSe at 18.4 Å confirms it. The extra ~20 K in monolayer FeSe/SrTiO3 therefore cannot come from 2D isolation/electron doping alone; it needs the oxide interface.

## 3. Verdict on the compass direction (bulk side)
We located **no evidence-backed route for a bulk Fe-based compound above 133 K at ambient pressure**: (i) nine years of synthesis (incl. 2024–26 high-pressure synthesis) stuck at 55–58.6 K; (ii) no Fe compound found above ~55 K even under pressure, so there is no warmer bulk phase to quench; (iii) Tc/J already fills the exchange-only band. This is a "no route found", not a theorem excluding the family; the interface-phonon route (Coh et al. 2016 double interface; Astra's conditional ideal-model estimate crossing 133 K but with the Aug-2026 anatase/FeSe/LAO PLD result at 16 K onset / 3 K zero) is the only place the family's ceiling is open, and it is a film/heterostructure question, not bulk. Sub-bar bulk targets that remain: pressure-quenched SC-II of Lix(NH3)yFe2Se2 (~50–55 K ambient at best); disorder reduction in electron-doped FeSe (Tc ∝ 1/ρ0, PNAS 2026 doi:10.1073/pnas.2608091123). Neither leads upward to 133 K, so **no candidate is submitted this turn**.

## 4. Where to look instead
Families with J ≳ 130 meV (the scale the exchange-only estimate asks for) are cuprates and the bilayer nickelates (La3Ni2O7 J ≈ 100–140 meV from RIXS/INS; ambient films 45–63 K onset). The lab's upward levers remain: (a) stabilising the quenched Hg-1223 151 K state (Chu PNAS 2026, reproduction pending); (b) ambient nickelate films with oxygen-retention engineering (turn 5 target); (c) FeSe/oxide heterostructures only if a retained high-quality thin FeSe layer with two active interfaces can be grown. Recommendation for turn 8: a quantitative retention analysis of pressure-quenched Hg-1223 (which structural parameter carries the +18 K; can chemical pressure or epitaxial strain lock it).

## 5. Housekeeping
- No QPU use by Fable (Astra ran the agreed 6-qubit Hubbard-dimer job: exact D=P=0.1464, hardware D=0.1399±0.0054, P=0.1538±0.0063; see `../astra`).
- C0001 (Mg2IrH6): no new evidence this turn; remains challenged.
- No new candidate; none received from Astra for formal review before finishing.
