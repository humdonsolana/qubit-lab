# CHGNet 0.4.2 relax / hull / phonon / novelty results (labphys, turn 12, Fable)

All at 0 GPa. Hull: CHGNet energies vs OPTIMADE/Alexandria competitors (relaxed with CHGNet); DFT column =
Alexandria PBE e_above_hull when the structure is already in Alexandria.

| structure | relaxed a, c (Å) | CHGNet E_hull (meV/atom) | decomposes to | Alexandria DFT E_hull (meV/atom) | CHGNet phonons |
|---|---|---|---|---|---|
| MgB2 (control) | 3.0802, 3.5164 | −0.1 | — | 0.0 (agm002077195) | — |
| BaB2 P6/mmm | 3.3443, 4.8054 | 594.9 | Ba + BaB6 | 737.6 (agm010185718) | 0 imaginary (default supercell, 12^3 mesh) and 0 imaginary (3×3×2 supercell, 12×12×8 mesh) |
| KB2 P6/mmm | 3.1373, 4.9406 | 496.3 | K + KB6 | 557.0 (agm011721278) | 0 imaginary |
| BaKB4 (1×1×2 layered) | 3.2378, 9.7097 | 704.1 | Ba + BaB6 + K | not in DB | 0 imaginary |
| Ba3KB8 (2×2×1) | 6.5826, 4.7875 | 642.6 | Ba + BaB6 + K | not in DB | 0 imaginary |
| CaB2 P6/mmm | — | 178.7 | | 188.2 (agm004173556) | |
| SrB2 P6/mmm | — | 480.8 | | 535.8 (agm004177304) | |
| MgBaB4 (1×1×2) | — | 433.1 | | 490.1 (agm020842838) | |
| Mg2BaB6 (1×1×3) | — | 360.2 | | not in DB | |
| MgCaB4 (1×1×2) | — | 226.6 | | 212.2 (agm020842898) | |
| LiBeB mp-1103047 (P3m1; Zhang et al. arXiv:2608.02426 Tc 46 K) | — | 57.4 | | 108.3 (agm005225095) | |

Novelty (labphys novelty, Ba3KB8-relaxed.cif): providers aflow, alexandria, cod, gnome, jarvis, mp, oqmd
searched, none failed; same_formula: []; same_structure: []; arXiv plain-text search for
Ba3KB8/KBa3B8 permutations: no papers. Verdict: "no match in the databases searched".
(Novel — but ruled out by the hull, see README.)

Tool caveat recorded: CHGNet phonons show no imaginary mode for pristine P6/mmm BaB2, whereas DFPT
(Bercx et al. 2025, Fig. 10a / Supplementary Sec. 6) finds a soft acoustic mode at H=(1/3,1/3,1/2). The
CHGNet phonon gate therefore under-detects soft modes in this family and must not be used alone.

Timings: relax 3–22 FIRE steps each; phonons ~1–4 min each on 1–2 CPUs.
