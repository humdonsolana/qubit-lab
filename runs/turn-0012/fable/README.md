# Turn 12 — Fable: ML / high-throughput screens of known crystals for strong electron-phonon coupling

Direction (compass): machine-learning screens of known crystals for strong e-ph coupling.
Split with Astra: Astra audited the experimentally tested ML hits (Y/LuRu3B2 calibration, Nepal–Wang 2026
B/C tables, MC3D provenance) and ran the QPU Holstein benchmark; I took the frontier prediction with the
highest Tc, tried to design past it, and ran the lab's stability gates + the one QE job.

Sandbox note: the turn folder was not shell-writable; computation ran in `/tmp/f12`; outputs copied
verbatim with write_file (see `outputs/`).

## 1. Where the ML/HT screens of known crystals stand (Oct 2026; verified at source)

| Screen | Scope | Best *new* ambient-pressure prediction | Status |
|---|---|---|---|
| Bercx, Poncé, … Pizzi, Marzari, PRX Energy 4, 033012 (2025); arXiv:2503.10943 | 4533 MC3D known metals → 250 EPW | **hole-doped BaB2: λ=1.39, Tc_aniso 61.6 K** (pristine P6/mmm BaB2 has a soft acoustic mode at H; stabilised only by ≥0.065 h/cell homogeneous doping). Undoped best: W2N3 33.7 K; TaRu3C 25 K (flagged possibly magnetic) | prediction; their only explicit dopant test (1 Cs in 3×3×1) **failed** to stabilise (local stress, E_F +0.64 eV) |
| Zhang, Gao, … Lu, Xiang, arXiv:2608.02426 (Aug 2026) | 36,377 MattKeyBond (MP+ICSD) → 8833 metals → 260 → 150 stable → 34 with Tc>10 K | BC7 57.4 K, LiBeB (mp-1103047) 46 K, B13C2 41.2 K, BC5 35 K; metallised-σ route beats DOS-piling route | predictions; BC7/BC5/LiBeB have no synthesis record |
| Tang, … Duan, Xiang, Xu, arXiv:2606.21251 (Jun 2026) | σDOS descriptor + DeepH, 2 M structures | B13Se >40 K and B13X family | prediction |
| Nepal & Wang, npj Comput. Mater. 12, 152 (2026) | 417 B/C compounds, CGCNN/ALIGNN + DFPT | B2CN 60.7 K (up to 0.35 eV/atom above hull), Ca5B3N6 35–42 K (smearing-stabilised), TaNbC2 28.4 K (0.02 eV/atom) | predictions (Astra audited) |
| Aalto-led 2026 (arXiv:2512.16945) | ML-predicted → synthesised | YRu3B2 / LuRu3B2 measured < 1 K vs 2–7 K predicted | only experimental test of this screen class; Astra's audit: internal inconsistencies, no universal correction factor |

**Ceiling of the direction.** Every screen of *known* crystals tops out at predicted 40–62 K, and the top
entries are all metastable or conditionally stabilised. Allen–Dynes bookkeeping (`ad_requirements.py`):
133 K at mu*=0.13 needs λ ≥ 1.9 at ω_log = 80 meV, λ ≥ 2.7 at 60 meV, λ ≥ 3.5 at 50 meV. No non-hydride known
crystal in any 2024–26 screen has λ > 1.7 with ω_log > 50 meV. This direction cannot reach the bar by
itself; it supplies calibration data and starting structures.

## 2. What I tried: design past hole-doped BaB2 (the highest prediction)

Idea: Bercx et al. need 0.065 h/cell but their Cs test failed because Cs+ (Shannon CN12 1.88 Å) is far
bigger than Ba2+ (1.61 Å). K+ (1.64 Å) is size-matched, so ordered Ba1−xKxB2 should supply the holes
without the local stress. Built P6/mmm supercells: Ba3KB8 (x=0.25, 2×2×1), BaKB4 (x=0.5, layered 1×1×2),
plus Na/Rb/Cs/Sr variants, KB2, CaB2, SrB2, MgBaB4, Mg2BaB6, MgCaB4 and MgB2 as control (`build_structs.py`).

CHGNet results (`outputs/chgnet_results.md`):

| structure | a, c (Å) | E_hull CHGNet (meV/atom) | Alexandria DFT E_hull | CHGNet phonons |
|---|---|---|---|---|
| MgB2 (control) | 3.080, 3.516 | −0.1 | 0.0 | — |
| BaB2 P6/mmm | 3.344, 4.805 | **595** | **738** (agm010185718) | no imaginary modes (3×3×2 supercell) |
| KB2 | 3.137, 4.941 | 496 | 557 | stable |
| BaKB4 | 3.238, 9.710 | 704 | — | stable |
| Ba3KB8 | 6.583, 4.788 | 643 | — (not in any DB; novelty: no match) | stable |
| CaB2 | | 179 | 188 | |
| SrB2 | | 481 | 536 | |
| MgCaB4 / MgBaB4 / Mg2BaB6 | | 227 / 433 / 360 | 212 / 490 / — | |
| LiBeB mp-1103047 (Zhang 46 K) | | 57 | 108 | |

Verdict: **hole-doped BaB2 is not a synthesizable target.** AlB2-type BaB2 sits 0.6–0.74 eV/atom above
Ba + BaB6 (both CHGNet and Alexandria PBE agree) — an order of magnitude beyond anything retained
metastably (Aykol et al. 2018: ~0.1 eV/atom amorphous limit). K substitution does not help (K-B2 is itself
+0.5 eV/atom), and the whole AeB2 series climbs monotonically with cation size (Ca 0.18 → Sr 0.48 → Ba
0.60 eV/atom). The 61.6 K number is a property of a phase that will not exist; Bercx et al.'s own remark
"we suspect that pure BaB2 cannot be made easily" is quantitatively confirmed. Note also CHGNet shows *no*
H-point instability for pristine BaB2 whereas DFPT does: CHGNet misses the soft mode, so the lab's CHGNet
phonon gate is not a sufficient check for AlB2-type borides (recorded as a tool caveat).

Of the other screen leads, LiBeB (108 meV/atom DFT above hull) is the only one near a plausible
metastability window and is published prior work (Zhang et al. 2026), not a lab candidate.

## 3. Quantum ESPRESSO run (sole QE job this turn, agreed with Astra)

`labphys eph start structs/BaB2-relaxed.cif runs/BaB2_quick --preset quick` — undoped P6/mmm BaB2, to see
whether the lab's quick pipeline reproduces the H-point soft mode and the λ≈1.4 scale reported by
Bercx et al. Status at end of turn: see `outputs/eph_status.json` and the notebook entry; if unfinished
the next session should read `labphys eph status runs/BaB2_quick` (in /tmp/f12 — ephemeral; result
copied if finished).

## 4. No candidate submitted

No design in this direction has an evidence-backed route above 133 K at ambient pressure; the best
frontier prediction (61.6 K) is on a phase 0.7 eV/atom above the hull. Submitting Ba3KB8 (novel, CHGNet
dynamically stable, predicted by analogy ≈ 40–60 K) would be a below-bar candidate with no credible route
upward and a fatal thermodynamic gate, so it is reported here as ruled out.

## 5. Files
- `build_structs.py` — structure generator (AlB2-type supercells).
- `ad_requirements.py` — Allen–Dynes λ needed for 133 K vs ω_log, mu*.
- `outputs/chgnet_results.md` — relax/hull/phonon/novelty outputs (verbatim numbers).
- `outputs/eph_status.json` — QE job status at end of turn.
- `structs/*.cif` — Ba3KB8, BaKB4, BaB2, KB2 relaxed CIFs.
- `lit_ml_eph_screens_2024_2026.md` — source notes (sub-agent review returned empty; notes written by me from fetched pages).
