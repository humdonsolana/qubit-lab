# Turn 15 — Fable: bulk iron-based superconductors past 55 K

Direction this turn: iron-based superconductors past their 55 K bulk record. Split with Astra:
Astra = FeSe/interface (>55 K) audit, phase-stiffness gate, QPU benchmark; Fable = bulk frontier
review, retraction/dispute audit, and a CHGNet structural screen of a novel "self-interface"
FeSe/perovskite-oxide bulk design. No Quantum ESPRESSO run by either of us this turn (Fe-based
pairing is not phonon-mediated; Allen–Dynes does not apply). No Fable QPU use (Astra owns it).

## Files
- `lit_bulk_fe_based_2024_2026.md` — sub-agent literature review (bulk records, descriptors, oxide-blocked FeSe prior art, retraction audit). If missing, the sub-agent did not return in time; see notebook.
- `build_structures.py` — builds the 42622-type (P4/nmm, Sr4V2O6Fe2As2 prototype, Zhu et al. PRB 79, 220512 (2009)) cells: Sr4Mg2O6Fe2Se2 (A, neutral parent), Ti-doped variants (B, 0.25 e/Fe; F = Sr4Ti2O6Fe2Se2, 1 e/Fe), arsenide reference D, and known references (Sr4V2O6Fe2As2, Sr4MgTiO6Fe2As2, FeSe, LaFeAsO).
- `analyze.py` — descriptors: anion height h above the Fe plane, Fe–X bond, Fe–X–Fe angle, apical contacts.
- `structures/` — input and CHGNet-relaxed CIFs. `outputs/` — relax/hull/phonon/novelty JSON.

## Idea tested
Monolayer FeSe on SrTiO3 shows gaps closing at 65 K and more (ARPES, STM; the 100 K transport claim of
Ge et al. 2015 is single-group). The bulk record is 55–56 K (1111). The enhancement at the interface
is attributed to (i) ~0.12 e/Fe electron doping and (ii) coupling to the ~100 meV oxide polar phonon
(Lee et al. Nature 515, 245 (2014)). Known bulk "self-interface" Fe-pnictides exist — Sr2VO3FeAs (21311,
37 K) and Sr4(Mg,Ti)2O6Fe2As2 (42622, 39 K) — but only with FeAs layers. Design question: does a bulk
FeSe analogue, Sr4(Mg1-xTix)2O6Fe2Se2, hold together, and would it put a dopable perovskite oxide
block ~3 Å from every FeSe layer?

## CHGNet results (machine-learned screen, not DFT)
| structure | a (Å) | c (Å) | h_Se/As (Å) | E_hull (meV/atom) | decomposes to | CHGNet phonons |
|---|---|---|---|---|---|---|
| Sr4V2O6Fe2As2 (known, 37 K) | 4.006 | 16.34 | 1.50 | 103 (Alexandria DFT: 111) | FeAs, Sr3V2O7, SrO, ... | unstable (−3.1 THz, 312 imaginary modes on mesh) |
| Sr4MgTiO6Fe2As2 (known, 39 K) | 3.969 | 16.65 | 1.52 | 110 | MgO, SrFe2As2, Sr2TiO4, SrO | — |
| **A Sr4Mg2O6Fe2Se2** (new) | 3.958 | 17.14 | 1.57 | **218** | Fe, MgO, Sr3Fe2O6, SrSe | unstable (−1.5 THz, 49 modes) |
| B Sr4Mg1.5Ti0.5O6Fe2Se2 (new, 0.25 e/Fe) | 3.971 | 16.99 | 1.66 | 153 | Fe, MgO, Sr2Fe2O5, Sr2TiO4, SrSe | — |
| F Sr4Ti2O6Fe2Se2 (new, 1 e/Fe) | 3.980 | 16.31 | 1.73 | 291 | Fe, SrSe, SrTiO3 | — |
| D Sr4Mg2O6Fe2As2 (hypothetical arsenide) | 3.959 | 18.06 | 1.17 | 220 | FeAs, MgO, SrO | — |
| FeSe (known) | 3.700 | 5.48 | 1.40 | 2.5 (Alexandria DFT 0) | — | — |

Calibration: CHGNet puts the *real, synthesised* 42622 arsenides at 103–110 meV/atom above the hull
(Alexandria DFT agrees: 111 meV/atom for Sr2VFeAsO3), and calls Sr4V2O6Fe2As2 dynamically unstable, so
the CHGNet phonon verdict is unreliable for this structure type (the known compound is stable at 300 K)
and the hull threshold for "makeable" in this family is ~110 meV/atom, not 0. Against that calibration:

- The FeSe analogues sit **1.5–2.5× further off the hull** than the real arsenides (153–291 vs
  103–110 meV/atom), and the decomposition products are the obvious ones (Fe metal + SrSe + the
  Ruddlesden–Popper oxide). The Fe–Se bond expands (2.53–2.64 vs 2.39 Å in FeSe) because the oxide
  block imposes a = 3.96–3.98 Å on FeSe (bulk a = 3.77 Å): a 5% tensile strain, larger than FeSe on
  SrTiO3 (3.905 Å, 3.5%). Anion height rises to 1.57–1.73 Å (optimum from Mizuguchi et al. 2010 is
  1.38 Å); in the arsenides the same block gives h = 1.50–1.52 Å, close to the optimum, which is why
  the "self-interface" idea worked (to 37–39 K) for FeAs but not for FeSe.
- Charge balance: Mg2+ gives a neutral FeSe layer; Ti4+ (or Al3+) on the Mg site dopes electrons
  into FeSe (0.25 e/Fe for B). Nothing in the screen distinguishes whether those electrons reach the
  FeSe layer or stay in a Ti-d / Fe-oxide band — a DFT question not answered here.

## Verdict
Sr4(Mg,Ti)2O6Fe2Se2 is novel (no database or arXiv match; OQMD was down) but the CHGNet screen gives
no reason to propose it: it is 150–290 meV/atom off the hull (vs ~110 for the arsenides that do form),
the FeSe layer is stretched 5% with the anion height pushed away from the empirical optimum, and
there is no descriptor route from here to 133 K: the empirical descriptors (h_anion, bond angle,
FeSe-layer spacing) all saturate the Fe-based family at 46–56 K in bulk; everything above that is the
single-layer interface regime Astra is auditing. **No candidate submitted.** Family verdict for bulk
Fe-based: no evidence-backed route above 133 K at ambient pressure; the best bulk result remains
~55–56 K (1111), unchanged since 2008–2009.

## Dispute audit (what I checked)
See `lit_bulk_fe_based_2024_2026.md` §5 and the notebook. Summary: Ren et al. 2008 (SmFeAsO1-xFx, 55 K)
and Wang et al. 2008 (Gd1-xThxFeAsO, 56 K) are reproduced and uncontested; the FeSe/SrTiO3 100 K
in-situ transport (Ge et al., Nature Mater. 14, 285 (2015)) remains single-group and ex-situ
transport caps at ~40–65 K (Astra's audit covers this in detail); no retractions found for any
Fe-based record. Retraction Watch / PubPeer access from the sandbox is often blocked; where blocked
we say so.

## Prior art found after the screen (web search, this turn)
- Coh, Lee, Louie & Cohen, PRB 93, 245138 (2016), "Proposal for a bulk material based on a monolayer
  FeSe on SrTiO3": a FeSe–SrTiO3 (TiO2-terminated) superlattice, DFT binding 0.7 eV per Fe2Se2, no
  Tc computed. Conceptually the same "double interface" idea as my 42622 design (and turn 7's
  double-interface estimate, optimistic max 145 K); my Ruddlesden–Popper-blocked variant with Sr apical
  to Se is structurally different but not a conceptual invention. Ten years on, no one has made it.
- Oxide-spacer FeSe bulk that does exist: LiFeO2Fe2Se2 (anti-PbO LiFeO2 spacer, hydrothermal, ~43 K;
  Lu et al., PRB 89, 020507(R) (2014), arXiv:1309.3833) and (Li,Fe)OHFeSe (42–43 K). Both sit on the Noji/Kajitani
  spacing saturation (~46 K), the same ceiling as Lix(NH3)yFe2Se2 (46 K).
- 2024–2026 bulk Fe-based reports found: (THA)xFeSe, electrochemically intercalated FeSe with c≈18.4 Å
  (Chin. Phys. Lett. 43, 050710 (2026)): bulk diamagnetic Tc 42.0–44.2 K, resistive onset 50.7–55.4 K, zero
  resistance 33 K — the Noji/Kajitani ~46 K plateau again; 1048-type Ca10(Ir4As8)(Fe2-xIrxAs2)5 (16 K, pressure
  kills SC; SUST 2026, doi:10.1088/1361-6668/ae7032). No bulk compound above 56 K at ambient pressure.
- Coh et al. Table I is the right calibration for my design: in their FeSe–SrTiO3 superlattice DFT gives a =
  3.87–3.90 Å and Se height 1.37–1.39 Å (optimum), whereas my RP-blocked 42622 cell forces a≈3.96–3.98 Å and
  h=1.57–1.73 Å — the Ruddlesden–Popper Sr4M2O6 block is the wrong spacer; a TiO2-terminated perovskite
  slab (Coh's proposal) keeps the geometry right but is prior work and remains unsynthesised after 10 years.
