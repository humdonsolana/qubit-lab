# Bulk bilayer nickelate crystals under pressure and chemical substitution (2025 to Oct 2026): literature review

**Method.** I used fetch_url and web search only; I ran no calculations.

**What "verified" means here.** I read these primary pages or abstracts directly:
- Li et al., Nature 2026 (96 K paper)
- Sun et al., Nature 2023 (80 K paper)
- Ko et al., Nature 2025, and its Author Correction
- arXiv:2609.00542, 2510.12359, 2510.13342, 2607.03363 and 2604.13875

Everything else comes from search excerpts or reference lists and is marked UNVERIFIED.

## Key numbers
| System | Tc (K) | P (GPa) | Probe | Ref |
|---|---|---|---|---|
| La1.57Sm1.43Ni2O7-δ crystal | **96 onset, no zero resistance** | 21.6, 26.8, 29.6 | R | Li et al., Nature 649, 871 (2026), doi:10.1038/s41586-025-09954-4 |
| La2SmNi2O7 crystal | 92 onset, 73 zero resistance (21.6 GPa); Meissner signal at 60 K (20.6 GPa) | ~21 | R, DC χ | same |
| La3-xSmxNi2O7 polycrystals, 0≤x≤1.5 | max onset 89 (x=0.9 and x=1.5) | higher P needed as x rises | R | arXiv:2510.13342 (journal version PRB 113, 174512 is UNVERIFIED) |
| La3-xNdxNi2O7 polycrystals, x≤2.4 | ~93 onset (R, x=2.1 and 2.4); **98±2 K by RF transmission (x=2.4)** | high | R, RF | arXiv:2510.12359, published as doi:10.1038/s41467-026-76534-z |
| La3Ni2O7 crystal | 80 | 14.0–43.5 | R, mutual inductance | Sun et al., Nature 621, 493 (2023), doi:10.1038/s41586-023-06408-7 |
| La5Ni3O11 (hybrid 1212) | ~64 (UNVERIFIED value) | dome | R | Shi et al., Nat. Phys. 21, 1780 (2025) |
| La4Ni3O10 crystal | ~30 (UNVERIFIED value) | ~50 | R | Li et al., Adv. Mater. 37, e07365 (2025); Zhu et al., Nature 631, 531 (2024) |
| La3Ni2O7, 1313 polymorph | ~3.6 onset (UNVERIFIED) | ~24 | R | PRX 2026, doi:10.1103/jc35-gj2l (UNVERIFIED) |

## 1. The 96 K Sm paper (Li et al., Nature 2026; published online 2 Dec 2025)
- **Composition giving 96 K:** La1.57Sm1.43Ni2O7-δ. The 96 K onset was seen in three crystals:
  - crystal #1 (annealed) at 26.8 GPa
  - crystal #2 (as-grown) at 29.6 GPa
  - crystal #3 at 21.6 GPa

  The authors say zero resistance was "not yet achieved … probably due to oxygen defects". **The 96 K value is a resistive onset only.**
- **Bulk superconductivity is shown only at x=1.0 (La2SmNi2O7):** 92 K onset and 73 K zero resistance at 21.6 GPa (helium medium), plus a DC Meissner signal at 60 K and 20.6 GPa.
- **Tc vs Sm content:** x=0 gives ~80 K, x=1 gives 92 K, x=1.43 gives 96 K. The authors link higher Tc under pressure to a larger in-plane lattice distortion at ambient pressure.
- **Independent check:** Sun/Wang's polycrystal work (arXiv:2510.13342) finds the maximum onset saturating at 89 K for x=0.9 and x=1.5. Sm shrinks both c and a. The ground state changes from metallic at x=0 to **insulating at x=1.5**, and the pressure needed for SC rises with x.
- **Ambient-pressure behaviour:**
  - Crystals are flux-grown at ambient pressure.
  - The structure keeps P2₁/m symmetry. The pseudo-cell is Cmcm with a≈20.3, b≈5.46, c≈5.36 Å.
  - Annealing at 1.5 bar O2 for 10 days gives δ≈0.00–0.02 (TGA).
  - **Not superconducting at ambient pressure.**
- **Structure under pressure:** low-temperature high-pressure diffraction shows that both the monoclinic and the tetragonal phase can support SC.
  - An independent group (arXiv:2607.03363) sees monoclinic → orthorhombic at ~15 GPa and → tetragonal at ~21 GPa.
  - The same group finds no CDW satellite reflections at low temperature.
- **Follow-ups (Nd):** 93 K by transport and 98±2 K by RF (arXiv:2510.12359). The Nature Communications version reportedly gives an RF signal at ~100.5 K for x=2.1 (UNVERIFIED; excerpt only).
- **Other rare earths:** I found no crystal paper with Pr, Eu or Gd substitution that exceeds 96 K. Li et al. grew La3-xRxNi2O7 crystals for R = Pr to Er, but report only EDS for them.
- **Kriener et al. (arXiv:2604.13875; high-pressure synthesis):** more octahedral tilting shifts the SC phase to higher pressure, and simultaneous hole doping reverses that shift.

## 2. Stabilising I4/mmm at ambient pressure by chemistry
- **La2SrNi2O7-δ (arXiv:2609.00542, Wen group, 1 Sep 2026):**
  - Made by high-pressure high-temperature flux synthesis.
  - XRD and STEM show I4/mmm with a 180° Ni-O-Ni bond.
  - Metallic with a low-temperature upturn; no density wave.
  - **Neither pressure nor oxygen variation induces SC.**
  - DFT: the Sr holes go into Ni dz², giving a large γ pocket and pushing that band far from half filling, which weakens the interlayer antiferromagnetic pairing.
- **Tetragonal La4Ni3O10 microcrystals:** no density wave and no SC up to 160 GPa (doi:10.1038/s41467-025-57264-0; UNVERIFIED).
- **Tetragonal, oxygen-rich La3Ni2O7 crystals:** no SDW and no SC; reported as "SDW rather than tetragonal structure is prerequisite" (UNVERIFIED).
- **La2BaNi2O7:** predicted to be I4/mmm (Rhodes & Wahl, PRMaterials 8, 044801, 2024). I found no synthesis report.
- **Ca, Ce, Th or co-substitution:** I found no bulk report giving ambient-pressure SC. A review, arXiv:2603.17657, reportedly states the solubility limits and that no aliovalent bulk sample superconducts (UNVERIFIED).
- **Takeaway:** a straight Ni-O-Ni bond without the right dz² filling is not enough. Isovalent smaller rare earths raise tilts and the critical pressure (Kriener; 2510.13342) instead of stabilising I4/mmm.

## 3. Pressure-quench and hysteresis
- **I found no report of nickelate SC retained at ambient pressure after a pressure quench.**
- Sun 2023 (Extended Data Fig. 5g,h) includes a χ measurement at 5.3 GPa taken during decompression. The figure is paywalled and I could not read the result.
- Other reports say SC is reversible on unloading and disappears below ~15–17 GPa (Zhou et al., arXiv:2311.12361; UNVERIFIED detail).
- In 1313-type crystals, transport shows hysteresis below ~12 GPa (Puphal et al., PRL 133, 146002, 2024; UNVERIFIED).
- **Gap:** I found no quantitative width for Amam→I4/mmm hysteresis on decompression.

## 4. Hybrid, trilayer and >100 K claims
- Records, all UNVERIFIED values: hybrid 1212 La5Ni3O11 ≈64 K; trilayer La4Ni3O10 ≈30 K; 1313 polymorph only a few K (PRX 2026).
- **The only claim near or above 100 K is RF-detected:** 98±2 K in La0.6Nd2.4Ni2O7 (arXiv:2510.12359), and ~100.5 K in the Nature Communications version (UNVERIFIED).
  - Transport onset is only ~93 K.
  - There is no zero resistance or Meissner effect at ≥96 K, and no independent replication.
  - **Status: a signature, not an established Tc.**

## 5. Retractions, corrections and replication
- **Sun et al., Nature 2023:** the Nature page shows no correction or retraction (checked). The original paper says "signatures" and assigns the high-pressure phase to Fmmm. Later work (Wang et al., JACS 146, 7506, 2024, cited by Li et al.) assigns I4/mmm. Early replications reported filamentary SC or a low volume fraction (arXiv:2311.12361). Zero resistance and bulk SC were later shown by many groups, including Zhang et al., Nat. Phys. 20, 1269 (2024) and Li et al., NSR 12, nwaf220 (2025).
- **Li et al., Nature 2026 (96 K):** the Nature page shows no notice (checked). The caveats are the missing zero resistance at 96 K and the independent polycrystal ceiling of 89 K.
- **Ko et al., Nature 638, 935 (2025):** **Author Correction, Nature 652, E8 (31 Mar 2026), doi:10.1038/s41586-026-10335-8.**
  - It fixes the resistivity unit (mΩ cm⁻¹ → mΩ cm) and the Fig. 3d x-axis label.
  - The issue was flagged by E. Talantsev and Y. Nievergelt.
  - The conclusions are unchanged.
- **Zhou et al., NSR 2026 (ambient-pressure films):** I did not reach the article page, so I cannot state its corrections status. Its numbers (onset 63 K, zero resistance 37 K) are UNVERIFIED.
- **Could not reach:** PubPeer (HTTP 403 Forbidden), Retraction Watch, and Crossmark records. There may be PubPeer threads on these papers that I could not see.

## 6. Structure of the SC phase and why a smaller rare earth helps
- **Ni-O-Ni angle along c:** ~168° at ambient pressure becomes 180° in the SC high-pressure phase. The 180° bond is confirmed directly in tetragonal La2SrNi2O7 (2609.00542).
- **Apical Ni-O distances:** Sun 2023 Extended Data Fig. 1 gives d1–d4 vs pressure from DFT-relaxed positions in XRD lattices. The apical distance is ≈2.30 Å at ambient and ≈2.1 Å near 30 GPa; these exact values are UNVERIFIED because the figure is paywalled.
- **c-axis:** Tc rises linearly as c shrinks, at **≈ −28 K/Å** (arXiv:2510.12359, bulk data).
- **Leading explanation:** a smaller rare earth compresses c. That strengthens interlayer dz² coupling (J⊥, t⊥) through the inner apical oxygen. Supporting evidence: Nd raises T_SDW (2510.12359), and Sm's Tc gain saturates once c stops shrinking (2510.13342).
  - **Alternative descriptor:** larger in-plane distortion at ambient pressure (Li et al.).
  - **Cost:** a higher pressure is needed to reach the SC phase, and the sample becomes insulating at high substitution.

## Confidence
- **High:** the Section 1 numbers, the Ko correction, La2SrNi2O7 (no SC), the Nd/Sm polycrystal trends, and the absence of notices on the two Nature bulk papers.
- **Medium:** structural numbers.
- **Low:** hybrid and trilayer records, quench/hysteresis completeness, and the NSR film and PubPeer status.
