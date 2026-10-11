# Moderate-pressure (<~100 GPa) and "toward-ambient" cage/ternary hydride superconductors: literature review, 2024 to Oct 2026

QUBIT Lab sub-agent review. Compiled October 2026.

**Verification key.**
- **[V-src]**: I read the number in the abstract or full text on the publisher or arXiv page.
- **[V-id]**: the DOI or arXiv ID resolves (checked through Crossref or arXiv), but the number comes from a secondary page or another paper's abstract.
- **[2nd]**: secondary source only.

PubPeer search was blocked (HTTP 403), so I could not check PubPeer for any item. I searched for retractions through the publisher pages.

---

## 1. Ternary "XYH8"-type and borohydride clathrates

| Formula | Structure | P | Tc | Method | ID | Status |
|---|---|---|---|---|---|---|
| **LaBeH8** | Fm-3m rocksalt-like La + BeH8 units | synthesized at 110–130 GPa; measured on decompression down to 80 GPa | **110 K at 80 GPa**: sharp drop to zero resistance, Tc shifts in field | Exp., resistance + XRD | PRL 130, 266001 (2023), doi:10.1103/PhysRevLett.130.266001 | [V-src] (APS abstract). **Single group** (Jilin, Ma/Liu/Wang). I found no independent experimental replication up to Oct 2026. No Meissner/magnetization data. |
| LaBeH8 (theory) | same | dynamically stable to ~20 GPa (harmonic) | ~185 K | DFT/Eliashberg | PRL 128, 047001 (2022) (Zhang, Pickard, Yao, Duan) | [V-src]. Theory overestimates Tc relative to experiment. Anharmonic SSCHA (Mater. Today Phys. 59, 101939 (2025), doi:10.1016/j.mtphys.2025.101939, [2nd]) moves Tc *further* from experiment. Mishra/Belli/Zurek/Margine, arXiv:2608.14949: vertex corrections remove only ~4 K, so the prediction stays above experiment [V-src abstract]. |
| **LaB2H8** | non-clathrate, B–H covalent units | superconducting at 90 GPa; lattice stable down to ~59 GPa (XRD) | **up to 106 K at 90 GPa**: zero resistance plus field shift | Exp., resistance + XRD | JACS 146, 13797 (2024), doi:10.1021/jacs.3c14205 | [V-id] (Crossref title). Abstract read through the search-engine excerpt of the ACS page; the ACS page itself returned 403. Single group (Jilin). |
| LaBH8 | Fm-3m XYH8 | dynamical stability limit pc ≈ 35–40 GPa | 126 K | DFT, anisotropic ME | Di Cataldo et al., PRB 104, L020511 (2021); also Liang et al., PRB 104, 134501 (2021): 156 K at 55 GPa, stable from 48 GPa | [V-src] (pc/Tc as quoted in Lucrezi 2022 and the arXiv abstract of 2107.02553). **Not synthesized**: the La-B-H experiment gave LaB2H8 instead. |
| **BaSiH8** (theory) | Fm-3m XYH8 | thermodynamically stable >130 GPa; anharmonic pc ≈ 3 GPa; **kinetic limit ≈ 30 GPa** | 71 K | DFT, SSCHA, ME, VCNEB | Lucrezi et al., npj Comput. Mater. 8, 119 (2022), doi:10.1038/s41524-022-00801-y | [V-src] (full text) |
| **BaSiH8** (experiment) | cubic, assigned as BaSiH8 | made at 18–31 GPa; **recovered to ambient** | **only 9 K at 142 GPa** (Bc2(0) = 13–16 T). Below 50 GPa it is a degenerate semiconductor or poor metal with weak localization; no high Tc. | Exp., transport, 1H NMR, XRD | Semenok et al., arXiv:2603.14051 (Mar 2026) | [V-src] (abstract). Preprint, single report. **Strong negative result for the XYH8 family:** the theory predicted 71 K, and the low-P phase is not a good metal. |
| SrSiH8 | Fm-3m | thermodynamically stable >174 GPa; pc ≈ 27 GPa | 126 K | DFT, ME | same npj paper | [V-src]. No experiment found. |
| KB2H8 (and Rb, Cs analogues) | Fm-3m, BH4⁻ units | dynamically stable at "very mild" P; **at ~10 GPa AIMD shows decomposition below Tc**; thermally stable near 50 GPa | "highest predicted"; figure of merit above LaBeH8 at ~50 GPa | DFT, anharmonic, AIMD | Geng, Hilleke, Belli, Das, Zurek, arXiv:2401.00088 | [V-src] (abstract; the abstract gives no Tc number). No synthesis found. |
| CaBH? (Ca–B–H) | various | high P | – | DFT | Di Cataldo, von der Linden, Boeri, PRB 102, 014516 (2020) | [2nd]. Nothing low-pressure with Tc above 100 K. I found no 2024–26 experiments. |
| AcBH7 | BH6 units | 70 GPa | 122 K | DFT | Gu et al., PRB 110, 064105 (2024), arXiv:2411.19014 | [V-src] (abstract) |

**2025–26 experimental status for the XYH8 family.** I found no new synthesis with Tc above 100 K below 80 GPa. The only 2026 synthesis in the family is BaSiH8 (arXiv:2603.14051). It is low-Tc and non-metallic at low pressure, although it is the first superhydride-type cage compound recovered to ambient pressure.

## 2. Ce–H and La–Ce–H near 100 GPa

| Formula | Structure | P | Tc | Method | ID | Status |
|---|---|---|---|---|---|---|
| CeH9 / CeH10 | P63/mmc / Fm-3m clathrate | ~95 GPa | **up to 115 K below 1 Mbar** | Exp., resistance | Chen et al., PRL 127, 117001 (2021), doi:10.1103/PhysRevLett.127.117001 | [V-id] (Crossref title "Tc up to 115 K below a pressure of 1 Megabar"; "115 K at 95 GPa" as quoted in Nat Commun 2023). Ce–H is reproduced by several groups (Jilin/Oganov, Ma group, Semenok RF-method arXiv:2509.00563 sees 90–110 K). |
| (La,Ce)H9 (La:Ce 1:1) | P63/mmc | 97–172 GPa | **148–178 K**; "highest Tc at sub-megabar" | Exp., resistance + XRD | Bi et al., Nat. Commun. 13, 5952 (2022), doi:10.1038/s41467-022-33743-6 | [V-src] (Crossref abstract) |
| hcp-(La,Ce)H9–10 (La:Ce ≈ 3:1) | P63/mmc | synthesized at 113 GPa; measured down to ~100 GPa | **176 K at 100 GPa**, Hc2(0) ≈ 235 T | Exp., resistance + XRD | Chen et al., Nat. Commun. 14, (2023), doi:10.1038/s41467-023-38254-6; arXiv:2203.14353 | [V-src]. **Two independent groups** (Ma/Jilin and Cui/Huang/Oganov) agree on Tc ≈ 150–180 K near 100 GPa. **Reproduced.** |
| binary LaHx (comparison) | – | **78 GPa** | **103 K** | Exp., resistance | same paper (Chen 2023) | [V-src]. A single data point inside a comparison series; not the focus of the paper. |
| La0.5Ce0.5H10 | Fm-3m | 140–160 GPa | 175 K at 155 GPa | Exp. | Huang et al., arXiv:2208.05199 | [V-src] |

**2025–26 updates.** Semenok et al., arXiv:2509.22877, is a review published in Ann. Phys. 2025, e00467. It concludes that disordered ternary alloying **does not raise Tc** above the best binary parent hydride. It mainly lowers the pressure at which the phase is stable, to "Tc = 200 K near 110–120 GPa" [V-src]. I found no report pushing (La,Ce)H9–10 with Tc above 150 K below about 95 GPa.

## 3. (La,Y)H10 and La–Sc–H (brief; a colleague covers this)

- **(La0.9Y0.1)H10**: Nat. Commun. (2025), doi:10.1038/s41467-025-66262-1. Phases coexist between 136 and 168 GPa, with Tc onsets of 244 K and 220 K. Y "does not raise Tc above pure LaH10" [V-src abstract]. Not moderate pressure.
- **LaSc2H24** (P6/mmm): Song et al., arXiv:2510.01273 (Ma group). Onset Tc 271–298 K at 195–266 GPa, zero resistance, 13 runs [V-src]. **Disputed.** Semenok, Troyan, Wu, Zhou, Yuzbashyan, Altshuler, Struzhkin, arXiv:2605.29985 v2 (Aug 2026), report that their 7 attempts (the abstract says seven; the v2 comment says three more were added) at 250–280 GPa from La–Sc alloy were unsuccessful, with **no traces of superconductivity at 245–300 K**. They suggest the precursor preparation (co-deposition of La and Sc) may be the reason [V-src]. Either way it needs above 190 GPa, so it is outside the low-pressure scope.

## 4. Pressure-quench (PQP) retention

- **Hg-1223 cuprate**: Deng, …, Chu, PNAS 123, e2536178123 (2026), doi:10.1073/pnas.2536178123. Ambient-pressure **Tc = 151 K** after a pressure quench, supported by synchrotron XRD [V-src Crossref abstract]. Not a hydride. Single group; I found no independent replication and no correction notice in the Crossref record (the update-policy field is present, but no update is listed).
- Earlier PQP work from the same group: PNAS 118, e2108938118 (2021) and PNAS 2025, doi:10.1073/pnas.2501048122 ("Bringing pressure-induced superconductivity back to ambient pressure") [V-id titles].
- **Hydride analogues**:
  - I found **no** report of a superconducting superhydride retaining Tc above 77 K at ambient pressure after a quench.
  - The closest results are both non-superconducting at low pressure:
    - BaSiH8 recovered to 1 bar (arXiv:2603.14051).
    - Cubic Mg2IrH7 survives room-temperature decompression to ~20 GPa, then reverts to Mg2IrH5 (arXiv:2602.23675).
  - Sanna et al. (Commun. Phys. 2026) cite PQP as a possible route but give no hydride data.

## 5. "Low-pressure" and "ambient" hydride claims, 2023–2026, and their status

| Claim | Tc / P | ID | Status |
|---|---|---|---|
| N-doped LuH (Dasenbrock-Gammon, Dias et al.) | 294 K at 10 kbar | Nature 615, 244 (2023), doi:10.1038/s41586-023-05742-0 | **RETRACTED 7 Nov 2023** (notice doi:10.1038/s41586-023-06774-2); Editor's Note 1 Sep 2023 [V-src, Nature page]. Many failed replications, e.g. "Absence of near-ambient superconductivity in LuH2±xNy", Nature 2023, listed on the same page. The review "Roadblocks to ambient-pressure RT superconductivity in Lu hydrides" is doi:10.1063/5.0250031 (2025) [V-id]. |
| Mg2IrH6 (prediction) | ~160 K at 0 GPa (later papers quote up to 170 K) | Dolui et al., PRL 132, 166001 (2024), arXiv:2310.07562 | [V-src]. Theory only. Metastable; proposed synthesis route via Mg2IrH7, stable above 15 GPa. |
| Mg2IrH5 synthesis | insulating | Hansen et al., PRB 110, 214513 (2024), doi:10.1103/PhysRevB.110.214513 | [V-id] |
| Mg2IrH7 (Sinha et al.) | cubic Mg2IrH7 above ~40 GPa; **insulating**; reverts to Mg2IrH5 below ~20 GPa | arXiv:2602.23675 (Feb 2026) | [V-src]. **Negative:** Mg2IrH6 has still not been made. |
| Mg2RhH6 (Jin group) | **24 K at 30 GPa, 29 K at 53 GPa**; zero resistance, field suppression | arXiv:2608.15745; JACS 148, 36854 (2026), doi:10.1021/jacs.6c08889 | [V-src]. Single report. This is the first experimental member of the Mg2XH6 family; Tc is far below 100 K. |
| Fe–Se–H (Bondarenko et al., Kharkiv) | claims SC "at 295 K" at ambient pressure | arXiv:2608.27349 (Aug 2026) | [V-src]. **Evidence is microwave absorption in an EPR spectrometer only**: no zero resistance, no bulk Meissner effect, no structure. Single report. Low-field microwave absorption also arises from magnetic phases, and FeSe+H can contain Fe-oxide/magnetic impurities. Treat as **unsubstantiated**. |
| C–S–H (Dias) | 288 K at 267 GPa | Nature 586, 373 (2020) | **RETRACTED** (Nature 610, 804 (2022)) [V-src, cited in the Nature Lu-N-H reference list] |
| BaSiH8 | ambient-recoverable, but not superconducting at low P | arXiv:2603.14051 | see §1 |

I found no other credible claim of high Tc in a hydride below 30 GPa for 2024–Oct 2026.

## 6. Theory: lowest predicted stability pressure with Tc ≥ ~100 K

- **Lucrezi, Di Cataldo, von der Linden, Boeri, Heil 2022 (npj)**: XYH8 screening of 54 combinations. Only LaBH8, BaSiH8 and SrSiH8 are dynamically stable at 50 GPa. The paper also introduces the kinetic-barrier pressure, which is about 10× the dynamical pc for BaSiH8 [V-src].
- **Caussé, Bozier, Cooke, Racioppi, Pickard, arXiv:2512.19901**: A15 YSbH6 (Pm-3), **118 K at 50 GPa**.
  - Dynamically stable from 20 to 120 GPa; kinetically and elastically stable at 50 GPa.
  - But about 100 meV/atom above the convex hull at 50 GPa, and 26 meV/atom at 120 GPa [V-src].
- **Gu et al. 2024**: AcBH7, 122 K at 70 GPa [V-src].
- **Dolui et al. 2024 (Pickard/Strobel)**: Mg2IrH6, about 160 K at 0 GPa, metastable [V-src]. Wang, Pickett, Hutcheon, Prasankumar, Zurek, Angew. Chem. 63, e202412687 (2024) explain why Ca2IrH6 is not a high-Tc superconductor [V-id, cited in Sanna 2026].
- **Sanna, Cerqueira, Cubuk, Errea, Fang, Commun. Phys. 9, 94 (2026)**, doi:10.1038/s42005-026-02552-4 [V-src]. Screening of thermodynamically **stable** GNoME hydrides finds a **maximum Tc of only 17 K** (LiZrH6Ru). It restates the trend that Tc near 100 K at ambient pressure is "systematically linked to thermodynamical instability". **This is an important negative result.**
- **Other ambient-pressure predictions, all metastable** [2nd]:
  - RbPH3: about 100 K, kinetically stable (cited in Sanna 2026).
  - Li2AgH6.
  - Fluorite-type hydrides: Adv. Sci. 2025, doi:10.1002/advs.202512696 [V-id title].
- **Zhang et al. PRL 2022**: LaBeH8 dynamically stable to 20 GPa with Tc around 185 K. The experiment did not reach that low.

---

## Table A: experimentally confirmed Tc > 100 K, ranked by lowest pressure

| Rank | Material | Lowest P with Tc>100 K | Tc there | Evidence | Reproduced? | Verified |
|---|---|---|---|---|---|---|
| 1 | binary LaHx (low-P phase) | **78 GPa** | 103 K | resistance | single data point (Chen 2023); phase not well defined | [V-src] |
| 2 | **LaBeH8** | **80 GPa** | 110 K | zero R, field shift, XRD | single group | [V-src] |
| 3 | **LaB2H8** | **90 GPa** | 106 K | zero R, field shift, XRD | single group | [V-id]/abstract via search excerpt |
| 4 | CeH9/CeH10 | ~95 GPa | ~115 K | resistance | yes (several groups) | [V-id]/[2nd] for the number |
| 5 | (La,Ce)H9 (1:1) | 97 GPa | ~148 K | resistance, XRD | yes (with 6) | [V-src] |
| 6 | hcp-(La,Ce)H9–10 (3:1) | ~100 GPa | 176 K | resistance, Hc2 | yes (two independent groups) | [V-src] |
| – | LaSc2H24 | 195 GPa | 271 K onset | resistance | **disputed** (failed replication by Semenok et al.) | [V-src] |
| – | Lu–N–H | 1 GPa | 294 K (claimed) | – | **retracted** | [V-src] |
| – | Fe–Se–H | 0 GPa | 295 K (claimed) | EPR only | unsubstantiated | [V-src] |

**No hydride has a confirmed Tc above 100 K below 78–80 GPa.** The best confirmed sub-30 GPa hydride Tc I found is Mg2RhH6 at 24–29 K (30–53 GPa). The ambient-pressure hydride record stays below 20 K (Sanna 2026 context).

## Table B: predictions with Tc ≥ ~100 K and low stability pressure

| Material | Predicted Tc | Dynamical-stability P | Thermodynamic stability | Experimental status | ID |
|---|---|---|---|---|---|
| Mg2IrH6 | ~160 K | 0 GPa | metastable (Mg2IrH7 stable >15 GPa) | not made; Mg2IrH5 and Mg2IrH7 insulating | PRL 132,166001; arXiv:2602.23675 |
| RbPH3 | ~100 K | 0 GPa | metastable, kinetically stable | none found | [2nd] via Sanna 2026 |
| LaBeH8 | ~185 K | ~20 GPa | stable >98 GPa | exp. Tc 110 K at 80 GPa | PRL 128,047001 |
| SrSiH8 | 126 K | ~27 GPa | stable >174 GPa | none | npj 8,119 |
| LaBH8 | 126–156 K | 35–48 GPa | metastable | La-B-H experiment gave LaB2H8 | PRB 104 L020511; PRB 104,134501 |
| KB2H8 | highest in its family (no number in abstract) | ~10 GPa dynamically, but decomposes in AIMD; ~50 GPa thermally stable | metastable | none | arXiv:2401.00088 |
| YSbH6 (A15) | 118 K at 50 GPa | 20 GPa | +100 meV/atom at 50 GPa | none | arXiv:2512.19901 |
| AcBH7 | 122 K | 70 GPa | stable at 100 GPa search | none (Ac is radioactive) | PRB 110,064105 |
| BaSiH8 | 71 K (below the 100 K cut) | 3 GPa (kinetic limit 30 GPa) | stable >130 GPa | made; 9 K at 142 GPa; non-metallic <50 GPa | npj 8,119; arXiv:2603.14051 |

**Caveat that applies to every prediction above.** Every candidate with low pc and Tc ≥ 100 K is metastable. Experiments since 2022 have repeatedly shown that:
- the kinetic-barrier pressure, not the dynamical one, controls survival (BaSiH8);
- predicted Tc values overshoot experiment (LaBeH8: 185 K predicted vs 110 K measured; BaSiH8: 71 K predicted vs 9 K measured).
