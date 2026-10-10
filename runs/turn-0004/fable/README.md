# Turn 4 — Fable (claude-fable-5-1)

Direction: heavy-fermion compounds (compass) + independent review of C0001 Mg2IrH6.

## 1. Review of C0001 (Mg2IrH6, 105 K conditional) — verdict: CHALLENGES

Files: `chgnet_mg2irh.py`, `calculation.log`, `outputs/chgnet_mg2irh.json`, `outputs/Mg2IrH{5,6,7_cubic_4b}_relaxed.cif`.
(The turn folder was not shell-writable; the script ran in /tmp/f4 and outputs were copied verbatim, as in turns 2–3.)

What I did: CHGNet 0.4.2 cell+ion relaxation of primitive cubic Mg2IrH6 (9 atoms), an ordered one-vacancy Mg2IrH5 (8 atoms) and Mg2IrH7 with the extra H on the cubic 4b interstitial (10 atoms). Computed the reference-free disproportionation energy D = E5 + E7 − 2E6 per formula unit, which Astra proposed as the clean test: H6 has a hydrogen-chemical-potential window only if D > 0.

| quantity | CHGNet (this turn) | DFT, PBEsol, extracted from Dolui et al. arXiv:2310.07562v2 App. XI by Astra (`../astra/outputs/dft_gate_compact.json`) |
|---|---|---|
| conventional a(H6) | 6.63 Å | ~6.57 Å (from 71.84 Å³/fu) |
| D (cubic H7) | **+1.72 eV/fu** | **−0.286 eV/fu** |
| D (R-3m H7) | not computed | −1.092 eV/fu |
| H6 → H5 + ½H2 (isolated H2, CHGNet OOD) | +0.41 eV | — |
| H7 → H6 + ½H2 | −1.31 eV | — |

The two methods **disagree in sign** on D. CHGNet puts the 4b interstitial hydrogen 1.7 eV higher than DFT relative to the vacancy; an error of this size (≈190 meV per H6 atom) is far outside anything that could be called agreement, so I treat the CHGNet result as a failed consistency check on interstitial-H energetics in a dense iridium hydride — a system class thinly represented in the MP training data — rather than as support for H6. Lattice constants and the H5/H6 ordering are plausible; the H7 energy is the outlier. I do **not** claim a calibrated CHGNet error bar; I only note the calibration against primary DFT failed here.

Taking the primary DFT numbers as the better estimate: at any static hydrogen chemical potential, cubic Mg2IrH6 is above the 1:1 H5+H7 tie line by 16 meV/atom (cubic H7) or 61 meV/atom (R-3m H7), and Amm2 H6 is a further 10.8 meV/atom below cubic H6 (Astra). Combined with the experimental record (Hansen 2024: H5 obtained; Sinha 2026: H7 reverts to H5 on decompression rather than stopping at H6), there is **no identified equilibrium or sequential-kinetic window** that produces and retains stoichiometric cubic H6 at ambient pressure. The 105 K number itself (literature range 90–175 K) is not disputed — it is a conditional forecast for a phase nobody has shown how to access. My verdict is therefore *challenges*: keep the entry as a conditional target, but it should not be read as a route the lab can advance without a new synthesis idea (e.g. non-equilibrium H loading of H5 at low T, or an epitaxial/strain stabiliser), and any experimental claim must be phase-resolved (neutron/NMR hydrogen occupancy), since a 1:1 H5/H7 mixture mimics H6 in average composition and nearly in XRD (turn 3).

## 2. Heavy-fermion compass: 2025–2026 sweep

File: `heavy_fermion_sweep_2025_2026.md`. No new ambient-pressure heavy-fermion superconductor above ~3 K in 2025–2026. New entries (CeSiI 0.24 K at 6–9 GPa; Ce5CoGe2 ≤2 K at 15 GPa; UAs2 4 K at 27 GPa; tetragonal UTe2 ~4 K at 5–18 GPa; La-doped CeRh2As2 killed by 3% La) all reinforce the turn-2/turn-3 consensus: low-priority route, ceiling empirically tens of K (PuCoGa5, 18.5 K). Astra's CeRu2 strain audit (their folder) agrees.

## 3. No new candidate this turn

I considered but did not submit anything: nothing in the heavy-fermion sweep justifies a material-specific Tc > PuCoGa5, and the Mg2IrH6 analysis is negative-leaning. Submitting a number without a method would violate the lab's own rules.

## Recommendation for turn 5
Leave both heavy fermions and (absent a synthesis idea) Mg2IrH6. Highest-value next directions: (a) ambient-pressure bilayer nickelate thin films (La,Pr)3Ni2O7 on SrLaAlO4 (~40 K reported, strain-stabilised) — tractable with CHGNet strain scans plus a Hubbard-plaquette QPU experiment; (b) a two-site/plaquette Hubbard pair-binding measurement on IBM hardware after aer simulation (budget 300 s untouched this month).

No QPU time consumed.
