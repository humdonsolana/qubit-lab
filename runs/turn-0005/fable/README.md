# Turn 5 — Fable (compass: wild card → bilayer nickelate films + Hubbard plaquette)

Split agreed with Astra: Astra audits primary composition/strain/transport evidence for
(La,Pr)3Ni2O7 films; I do (1) exact + variational 2×2 Hubbard pair-binding, (2) a
structure-only CHGNet epitaxial-strain scan, (3) decide whether any method-backed nickelate
Tc number is justified. **No candidate is submitted this turn** (reasons below). No QPU time used.

## 1. 2×2 Hubbard plaquette pair binding (exact; `hubbard_plaquette.py`, `scan_pbc.py`)
Δpb = E0(N=4)+E0(N=2)−2E0(N=3) with the Jordan–Wigner 8-qubit Hamiltonian, exact
diagonalisation per particle-number sector. **Negative Δpb = two added holes bind.**

| cluster | binding window | strongest binding |
|---|---|---|
| open 2×2 square (4 bonds) | U/t ≲ 4.5 | −0.037 t at U/t ≈ 2–3 |
| periodic 2×2 (doubled bonds, t_eff=2t) | U/t ≲ 9.5 | −0.079 t at U/t ≈ 5 |

Full tables: `outputs/scan_pbc.txt`, `outputs/exact.json` (U/t = 8: E2=−3.2078, E3=−2.3246,
E4=−1.3202, Δpb=+0.121 t, i.e. *no* binding on the open plaquette at U/t=8). These match the
classic small-cluster results (Hirsch 1980s; Fye–Scalapino) and are the yardstick for any
hardware run. Caveat: a 4-site cluster says nothing quantitative about Tc.

## 2. Variational circuit (`hva_prepare.py`, `outputs/hva_summary.json`) — not sent to hardware
2-layer number-conserving HVA (XX+YY hops on the ring, RZZ on-site, RZ phases; depth 19).
Statevector optimisation (2 restarts, 150 L-BFGS iterations, limited by the 2-CPU sandbox):
N=2 converges to within 6×10⁻³ t, but N=3 and N=4 stop 0.30 t and 0.29 t above exact, so the
variational Δpb (−0.186 t) has the **wrong sign** versus exact (+0.121 t). A hardware
measurement of these states would measure ansatz error, not physics, so the 300 s QPU budget
was left untouched. Next turn: deeper/longer optimisation (or ADAPT-style ansatz) offline,
then one estimator job per sector only when all three sectors are within ~0.02 t.

## 3. CHGNet structure-only strain scan (`chgnet_strain_scan.py`, `outputs/chgnet_strain.json`, `outputs/La3Ni2O7_a3.7705.cif`)
Idealised I4/mmm La3Ni2O7 (24 atoms), in-plane a clamped to the substrate values in Ko et al.
Fig. 5a source data (Astra, `/tmp/astra5/source.xlsx`: 3.7705, 3.7827, 3.792, 3.868 Å) + 3.83 Å;
c and internal coordinates relaxed.

| a (Å) | strain vs CHGNet free | c (Å) | c/a | inner apical Ni–O | outer apical Ni–O | eq. Ni–O | Ni–Ni bilayer |
|---|---|---|---|---|---|---|---|
| free | 0 | 20.42 (a=3.874) | 5.27 | 1.996 | 2.192 | 1.937 | 3.992 |
| 3.868 | −0.15 % | 20.39 | 5.27 | 1.987 | 2.190 | 1.934 | 3.974 |
| 3.830 | −1.14 % | 20.61 | 5.38 | 1.991 | 2.219 | 1.915 | 3.982 |
| 3.792 | −2.12 % | 20.82 | 5.49 | 2.007 | 2.263 | 1.897 | 4.013 |
| 3.7827 | −2.36 % | 20.88 | 5.52 | 2.006 | 2.277 | 1.892 | 4.012 |
| 3.7705 | −2.67 % | 20.95 | 5.56 | 2.008 | 2.292 | 1.886 | 4.015 |

Observations (structure only): CHGNet overestimates the free pseudocubic a (3.874 vs ≈3.83–3.84 Å
experimental), so absolute strains are ~1 % too large; Poisson response is c ≈ −0.2 Å per +0.1 Å
of a; compressive clamping *lengthens* the inner apical (Ni–O–Ni bridging) bond slightly
(1.99→2.01 Å) and the intra-bilayer Ni–Ni distance (3.97→4.02 Å), while shortening the
equatorial bond (1.93→1.89 Å). In the idealised tetragonal cell the Ni–O–Ni interlayer angle is
180° by symmetry, so this scan cannot address the octahedral-tilt straightening argument;
an orthorhombic (Amam/Cmcm) supercell is needed for that. No Tc is inferred from these numbers.

## 4. Why no nickelate candidate
Astra's reanalysis of the Ko et al. (Nature 2025, DOI 10.1038/s41586-024-08525-3; author
correction 31 Mar 2026 affects axis labels only) source data: Fig. 5a has 5 points with three
"0" entries that are non-observations, Fig. 5b positive-only c-fit has R²=0.08 and identical
c=20.561 Å appears with onsets 42.4 K and 26.2 K; same-film aging moves the ρ/ρ50=0.5 point from
22.1 → 14.4 → 6.2 K over 20 days and ozone annealing restores 18.2 K. A strain-only or c-only
"Tc predictor" is therefore not identifiable from the public data, and I will not fit one.
Negative controls Astra found (arXiv:2609.00542: tetragonal La2SrNi2O7−δ with 180° Ni–O–Ni and
no SC under pressure or oxygen variation; DOI 10.1038/s41563-025-02351-2: interstitial-oxygen
ordering competing with SC) say geometry alone is not sufficient. Pressure on La2SmNi2O7
films reaches 67–73 K at 16 GPa (Osada et al., Nat. Mater. 2026, DOI 10.1038/s41563-026-02695-3),
which is the strongest hint that ambient-pressure film Tc has headroom, but it is a pressure
result. I endorse Astra's unranked engineering target (La2PrNi2O7−δ/SLAO with oxygen-retention
capping, day-0/8/20 transport + mutual inductance) rather than inventing a Tc.

## Sandbox note
The turn folder is not shell-writable; all computation ran in `/tmp/f5` and scripts/outputs were
copied verbatim via write_file. `hva.json` (full parameter vectors + QASM, ~30 kB) was not
copied; `hva_prepare.py` regenerates it deterministically (numpy seed 1).
