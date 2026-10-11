# ML / high-throughput electron-phonon screens of known crystals, 2024–Oct 2026 — source notes (Fable, turn 12)

(The sub-agent literature review returned without writing a file; these notes were compiled by me from the
fetched arXiv HTML / publisher pages listed. Astra's `../astra/primary_literature_audit.md` covers
Nepal–Wang 2026 and the MC3D data archive in more depth.)

## Primary screens and their top new ambient-pressure predictions

1. **Bercx, Poncé, Zhang, Trezza, Ghorbani Ghezeljehmeidan, Bastonero, Qiao, von Rohr, Pizzi, Chiavazzo, Marzari —
   "Charting the landscape of BCS superconductors in experimentally known compounds", PRX Energy 4, 033012 (2025),
   DOI 10.1103/sb28-fjc9; arXiv:2503.10943v2.** 4533 MC3D known nonmagnetic metals (≤12 atoms) → QE/Wannier90/EPW;
   250 top candidates, 137 studied for SC; 82 matchable to experiment, 74 known SCs (90 % true positive). 24 never-reported
   compounds with Tc_aniso > 10 K. Top: **BaB2 (P6/mmm, AlB2-type) λ = 1.39, Tc_AD 21.4 K, Tc_iso 33.0 K, Tc_aniso 61.6 K (two gaps
   11.54 / 1.50 meV)** — but pristine BaB2 has a soft acoustic mode at H = (1/3,1/3,1/2); stabilised only by homogeneous
   hole doping ≥ 0.065 h/cell (rigid band). Their explicit test with 1 Cs in a 3×3×1 supercell did **not** stabilise it (local
   stress, E_F shifted +0.64 eV). They write "we suspect that pure BaB2 cannot be made easily". Next: W2N3 33.7 K, TaRu3C 25.0 K
   and NbRu3C 24.9 K (both flagged potentially magnetic), Be2B 22.1 K, PtO 19.0 K, ZrRuSb 13.2 K. Fixed mu* = 0.13. Checked for
   comments/errata: none found (web search 2026-10-11); dataset revised 4× on Materials Cloud (Astra audit) — revisions, not corrections.

2. **Zhang, Gao, Han, Lv, Gao, Liu, Ren, Lu, Xiang — "Screening phonon-mediated superconductors from static orbital
   Hamiltonians", arXiv:2608.02426 (3 Aug 2026).** SEPR descriptors Ξ (meV) and χ (meV·u^1/2) from static orbital Hamiltonians;
   36,377 MattKeyBond (MP+ICSD) compounds → 8,833 nonmagnetic metals → 260 pass Ξ>15, χ>125 → 150 dynamically stable → 99 with
   Tc>2 K, 34 with Tc>10 K (McMillan–Allen–Dynes). Benchmarks Table 1: MgB2 Ξ 43.3/55.9 (SEPR/DFPT), SH3 181.6/195.4, LaH10 177.6/213.1.
   Table 2 new predictions **without** synthesis record: BC7 57.4 K (mp-1080030), **LiBeB 46.0 K (mp-1103047)**, BC7 39.0 K, BC5 35.4/32.3/28.4 K,
   Nb3Cr 22.1 K, CaSi2 14.1 K; **with** synthesis record but no low-T transport: B13C2 41.2 K (mp-576), IrS2 17.3 K, Nb4C3 16.4 K,
   Be2B 16.3 K, BeMo3 16.0 K, LuB2C 13.5 K, Si 12.7 K (?), Y4C5 10.4 K. Two routes: metallised covalent σ-bond (favourable) vs
   E_F DOS accumulation (limited). 110/260 pre-selected compounds were dynamically unstable: "recurring competition between strong EPC
   and lattice stability".

3. **Tang, Dong, Wu, … Duan, Xiang, Xu — "AI-accelerated metallized σ-bonding screening", arXiv:2606.21251 (19 Jun 2026).**
   σDOS descriptor evaluated with DeepH; 2 million structures screened; **B13Se predicted Tc > 40 K at ambient pressure** plus a
   B13X family by elemental substitution. Prediction only.

4. **Nepal & Wang, npj Comput. Mater. 12, 152 (2026), DOI 10.1038/s41524-026-01962-w.** 417 B/C compounds (MP, incl. theoretical),
   CGCNN/ALIGNN + DFPT; B2CN 60.7 K (up to 0.35 eV/atom above hull), B13C2 39.3 K, Ca5B3N6 35–42 K (harmonically unstable at H,
   smearing-stabilised), TaNbC2 28.4 K (0.02 eV/atom above hull). See Astra's audit for data-consistency flags.

5. **Cerqueira, Sanna, Marques, Adv. Mater. 36, 2307085 (2024)** — ~7000 DFPT calculations over Alexandria/MP compounds; basis for
   later ML surrogates. **Gibson, Hire, Dee, Barrera, Geisler, Hirschfeld, Hennig, BETE-NET, npj Comput. Mater. 11, 7 (2025)** —
   equivariant GNN predicting α²F. **Sanna/Errea, Commun. Phys. 9, 94 (2026)** (from turn 9): thermodynamically *stable* hydrides max
   ~17 K — all ≥100 K predictions are off-hull.

## Experimental tests of screen predictions
- **YRu3B2 / LuRu3B2 (Aalto-led, arXiv:2512.16945; supporting arXiv:2512.09314, 2512.08514):** ML/HT predicted 1.9–6.8 K (version-
  dependent, see Astra audit), measured < 1 K. Only published synthesis-and-measurement test of this screen class so far.
- No synthesis report found (web/arXiv, 2026-10-11) for hole-doped BaB2, BC7, BC5, LiBeB, B13Se, W2N3, TaRu3C, ZrRuSb, B2CN.

## What this means for the lab (see README §1–2)
- Ceiling of "known-crystal" screens: 40–62 K predicted, all metastable/conditional. 133 K at mu* = 0.13 needs λ ≥ 1.9 with
  ω_log = 80 meV or λ ≥ 2.7 with 60 meV (`ad_requirements.py`); no non-hydride entry in any screen has λ > 1.7.
- The top prediction (BaB2) is 0.6–0.74 eV/atom above the Ba + BaB6 hull (CHGNet and Alexandria PBE agree), far beyond any
  retained-metastability window (~0.1 eV/atom); K-substitution does not rescue it (`outputs/chgnet_results.md`).
