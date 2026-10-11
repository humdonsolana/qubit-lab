# Turn 13 — Fable: MgB2-mold phonon superconductors (layered borocarbides, hole-doped σ bands)

Split with Astra: Astra took borocarbide/borohydride (H-decorated) frontier, audits and the QPU benchmark;
I took 2024–26 layered borides / LiBC-type hole doping, new designs, CHGNet gates and the one QE job.

## Results
1. **Turn-12 BaB2 QE finished** (`outputs/BaB2_quick_eph_result.json`): DFPT 3×3×2 q confirms the Bercx et al. soft mode
   (ω_min = −374 cm⁻¹); λ=2.89 is an unstable-phonon artefact, AD Tc 18–20 K not physical. CHGNet had reported BaB2 stable:
   tool caveat confirmed — CHGNet phonons are not sufficient for AlB2-type borides.
2. **Designs** (`build_structs.py`): stoichiometric ordered A⁺M²⁺B4C4 (0.25 h/BC, no vacancies) in the flat LiBC stacking.
   CHGNet hull (`outputs/hull_*.json`): NaMgB4C4 30, LiMgB4C4 39, LiBeB4C4 66, LiZnB4C4 82, LiCaB4C4 113, ordered Li0.5BC 81–92,
   MgB2C2-hex 33 meV/atom; LiBC −0.2 (control). Novelty: NaMgB4C4 no match in MP/Alexandria/AFLOW/GNoME/JARVIS (OQMD, COD, arXiv down).
   CHGNet phonons (`phonon_where.py`, `outputs/phonon_where.json`): NaMgB4C4 Na-rattler instability (−1.7 THz, 94% Na weight);
   LiMgB4C4 only near-Γ −0.9 THz (likely acoustic/ASR artefact).
3. **Prior-art check kills the candidate**: Li_xMg_(1-x)B2C2 was computed by Spanò et al. PRB 72, 014530 (2005) (67 K McMillan) and
   **made** by Mori & Takayama-Muromachi (2004): Mg0.5Li0.8B2C2 metallic, no SC to 1.8 K. Tomassetti et al. PRMater 2024 cover
   Mg_xB2C2/Na_xBC (43–84 K aME). My ordering is untested but inside a published, experimentally negative composition space → not submitted.
4. **Family ceiling** (`family_ceiling.py`): 133 K needs λ ≥ 1.9 at ω_log 80 meV (2.7 at 60 meV); published λ 0.9–1.5; more holes buckle
   or soften the layer. Predicted ceiling 60–90 K, measured 39 K. No evidence-backed route above 133 K in this family.
5. **C0001 rejected** as a lab listing (prior art Dolui PRL 2024 / Sanna npj CM 2024; calibrated expectation 36–80 K); kept as benchmark.
6. QE `runs/LiMgB4C4_quick` (quick preset, 10 atoms) still in `relax` at cap — next session: `labphys eph status runs/LiMgB4C4_quick`;
   target question: does flat ordered x=0.5 give λ≈1, ω_log≈90 meV like Spanò's x=0.125.

Files: build_structs.py, phonon_where.py, family_ceiling.py, lit_layered_borides_2024_2026.md, structs/*.cif, outputs/*. No Fable QPU use.
