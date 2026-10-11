# Layered borides / borocarbides in the MgB2 mold — what the record says (checked 11 Oct 2026)

Scope: hole-doped honeycomb (AlB2-type) layers of B or B/C, i.e. the "metallised σ-band" route. Sources are the
ones I actually opened (arXiv abs/HTML pages) plus turn-12 notes (`runs/turn-0012/fable/lit_ml_eph_screens_2024_2026.md`),
plus items Astra passed on with DOIs that I could not open (APS 403) — marked *unopened*.

## Theory frontier (ambient pressure)

| Phase | Tc (pred.) | λ, ω_log | Stability | Source |
|---|---|---|---|---|
| Li_xBC ordered (x≈0.5), honeycomb | 65–100 K (2002–03); >30 K aME (2024) | λ ~1–1.5 | metastable, kinetically protected | Rosner, Kitaigorodsky, Pickett PRL 88, 127001 (2002); Dewhurst et al. PRB 68, 020504 (2003); Tomassetti, Kafle, Marcial, Margine, Kolmogorov, J. Mater. Chem. C 12, 4870 (2024) = arXiv:2403.00738 (opened) |
| Li_xM_yBC reintercalated (M = Na, Mg, K, Ca) | up to 73 K aME | — | Li1/2Na_yBC "tantalisingly close to hull"; NaBC predicted a ground state | same (arXiv:2403.00738) |
| Mg_xB2C2, Na_xBC (deintercalated) | 43–84 K aME | — | metastable; buckling in heavily doped Na_xBC kills σ coupling | Tomassetti, Gochitashvili, Renskers, Margine, Kolmogorov, PRMater 8, 114801 (2024) = arXiv:2407.09347 (opened) |
| Li_xMg_(1-x)B2C2, x=0.125–0.25 | 67 K McMillan (μ*=0.1) | λσσ=0.91, ω_ln=777 cm⁻¹ (96 meV) | "might be synthesized under Mg deficiency" | Spanò, Bernasconi, Kopnin PRB 72, 014530 (2005) (abstract via search) |
| AgBC, CuBC (topochemical from Li_xBC) | >50 K two-gap aME | — | metastable | Gochitashvili, Tomassetti, Margine, Kolmogorov arXiv:2507.14281 / J. Mater. Chem. C 2025 (opened abs) |
| hole-doped BaB2 (P6/mmm) | 61.6 K aniso | λ=1.39 | 0.6–0.74 eV/atom above hull (turn 12); H-point soft mode | Bercx et al. PRX Energy 4, 033012 (2025) |
| XM2B6C6 (K/Rb Li2 B6C6, AgNa2B6C6) stabilising LiB2C2-type layers | (not read) | — | — | PRB 113, 214105 (2026), DOI 10.1103/j33d-y9sq — *unopened* (APS 403); relayed by Astra |
| strained Li_nB_(n+1)C_(n-1) | ≤37 K | — | — | Commun. Phys. 9, 81 (2026), DOI 10.1038/s42005-026-02495-w — *unopened*; relayed by Astra |
| H-decorated BC3 (H7-B2C6, H8-B2C6) | 91 K / 87 K | λ=3.33, ω_log=13.9 meV / λ=2.44, ω_log=25.3 meV | — | Chen et al. CPL 43, 060709 (2026) — relayed by Astra (his audit) |
| MgB4H / CaB4H | ≤64 K | — | — | Adv. Theory Simul. 2026, DOI 10.1002/adts.70356 — relayed by Astra |

## Experiment (the part that matters)

- Li_xBC delithiation, 2002–2019 (Bharathi 2002; Zhao 2003; Fogg/Rosseinsky 2003, 2006; Nakamori 2003; Kalkan & Ozdas 2019): metallic
  samples, **no superconductivity** at any x; B expulsion / layer breakdown below x≈0.45 (Fogg JACS 2006); Daumas–Hérold staging (Kalkan 2019).
- Mg_0.5Li_0.8B2C2 (Mori & Takayama-Muromachi, Curr. Appl. Phys. 4, 276 (2004), DOI 10.1016/j.cap.2003.11.027): Pauli-paramagnetic metal,
  **no superconductivity down to 1.8 K**; high-pressure (Mg,Li)B2C2 and B-for-C doping gave LiBC + MgB2 side phases.
- MgB2 itself: 39 K; the entire family's only confirmed superconductor at ambient pressure with σ-band pairing.
- Nothing in 2024–26 reports a superconducting hole-doped borocarbide; no retractions found for the theory papers above (they are
  predictions, not claims of observation).

## What limits Tc here (quantitative, `family_ceiling.py`, outputs/family_ceiling.json)

With ω_log pinned by B–C/B–B bond stretching at 60–100 meV, Allen–Dynes at μ*=0.13 needs λ = 2.7 (60 meV), 2.2 (70), 1.9 (80),
1.7 (90), 1.5 (100) to reach 133 K. Published λ for hole-doped honeycomb layers sits at 0.9–1.5 and increasing hole count
beyond ~0.3–0.5 h per B2C2 either buckles the layer (Tomassetti 2024) or softens the E2g-like mode into an instability
(BaB2: our QE run gives ω_min = −374 cm⁻¹). So the family's realistic predicted ceiling is 60–90 K, and its measured ceiling is 39 K.
Pushing λ to ≥2 at ω_log ≥ 80 meV in a flat, defect-free layer is what a candidate would have to show; nothing published does.
