# Independent nickelate audit — Turn 0005

**As of 2026-10-10.** Primary-source audit of the three requested papers; not a global record survey. **Verdict: these papers justify a nickelate thin-film engineering direction, but not a numerical Tc prediction for a new unmeasured composition, and not room-temperature superconductivity.** No candidate composition was specified in this request.

## 1. arXiv:2512.04708 — verified, now published

Zhou et al., *Superconductivity onset above 60 K in ambient-pressure nickelate films*, **National Science Review 13, nwag151 (2026)**, **DOI 10.1093/nsr/nwag151**. arXiv v1: **2025-12-04**; v2: **2026-03-11**. Published full text in PMC lists online publication **2026-03-10**. [1–3]

**Material/architecture:** nominal **(La,Pr)3Ni2O7**, coherently compressively strained on **SrLaAlO4(001)** with an insulating monolayer-nickelate buffer. The >60-K-onset film characterized by XRD is **3 unit cells**, **6.98 nm including buffer**. GAE growth uses 800–850 °C, strong ozone/oxygen oxidation and no post-annealing. This is not ambient-pressure bulk material. [2,3, Fig. 4, Methods]

**Composition precision:** Fig. 1e explicitly gives dataset La:Pr ratios **67:33, 65:35, 55:45** (nominal cation formulas La2.01Pr0.99, La1.95Pr1.05, La1.65Pr1.35, respectively). The retrieved textual caption does not assign a specific ratio to S1 versus S2; this audit does not guess their individual assignments from symbols. No calibrated absolute oxygen content for S1 is supplied in the retrieved main text. Nominal O7 is therefore not proof of exact measured oxygen stoichiometry. [2,3, Fig. 1e]

| Criterion | Sample | Temperature |
|---|---|---:|
| Resistive onset: departure from normal-state linear-in-T fit | S1 | ~63 K |
| Measured zero: resistance below noise | S1 | ~30 K |
| Resistive onset | S2 | ~56 K |
| Measured zero: resistance below noise | S2 | ~37 K |
| Diamagnetic/vortex-melting onset, two-coil mutual inductance, zero field | Magnetic measurement | ~23 K |

**Do not combine 63-K onset and 37-K zero into one sample.** The 44-K/S1 and 42-K/S2 zero-axis intercepts are extrapolated transition-edge fits, not measured zeros. The ~80% pickup-signal drop is not a bulk superconducting volume fraction; complete screening is geometrically precluded. The authors interpret the ~23-K magnetic transition as robust global phase coherence. The 63-K operational transport onset is interpreted as initial pairing, not direct proof of global phase coherence at 63 K. [2,3, Figs. 1–2, Discussion]

## 2. La2SmNi2O7 — s41563-026-02695-3

Osada et al., *Bridging ambient- and high-pressure superconductivity in La2LnNi2O7 films*, **Nature Materials**, published **2026-08-18**; matched author manuscript **arXiv:2608.17745v1**. [4,5]

Ozone-annealed **~4-nm La2SmNi2O7/SrLaAlO4(001)** has **41-K onset**, resistance reduced to 10% at **28 K**, and **~6-K zero resistance**. As-grown material is insulating. No film diamagnetic transition is demonstrated in the retrieved manuscript; introductory diamagnetism references concern earlier bulk studies. [5, pp. 4–5, Fig. 2]

At **16 GPa**, upper resistive transitions reach **67 K/Sm** and **73 K/Nd**, with two-step transitions. These are neither ambient-pressure nor zero-resistance temperatures; final resistance is described as close to zero. Smaller-ion substitution does not monotonically emulate pressure: ambient onsets are **Pr 47, Nd 42, Sm 41, Eu 10, Dy 20 K**, generally decreasing with substitution-induced lattice compression. [5, pp. 5,7–8]

## 3. Interlayer hybridization — s41563-026-02750-z

Zhang et al., *Interlayer hybridization promotes superconductivity in bilayer nickelates*, **Nature Materials**, published **2026-09-23**. Earlier manuscript: **arXiv:2604.14701v2**, **2026-04-17**, titled *Interlayer hybridization enables superconductivity in bilayer nickelates*. [6,7]

Published Fig. 1 identifies **LaPr2Ni2O7+δ**, not La2PrNi2O7. The earlier manuscript reports **SC1/SC2 = 7/8 nm**, **~30-K onset**, **SC1 ~10-K zero**; these numerical sample details are **preprint-derived**, since the subscription main text was inaccessible for complete version-of-record comparison. Published Fig. 1/Supplement Note 2 confirm an **~1-nm amorphous PrBa2Cu3O7 cap**, insulating cap-only controls and negligible transport changes upon capping. [6–9]

Published XAS/RIXS results associate superconductivity with coherent **dz²–pz–dz² interlayer hybridization**, suppressed static spin order and damped spin excitations, within a **narrow oxygen/strain-tuned regime**. Electronic interlayer coherence is not itself a Meissner measurement or superconducting phase-stiffness temperature. The paper supplies no quantitative new-composition-to-Tc predictor. [6]

## Turn 5 decision and confidence

**Audit inference:** supports interface/strain/oxygen engineering, but challenges transferring measured onset temperatures to a new La/Pr/Sm mixture from chemical-pressure, hopping or strange-metal correlations alone. Label an unmeasured composition **“Tc unestablished”**; specify thickness, interface, strain and oxygen configuration and separately measure onset, zero resistance and magnetic phase coherence. A composition-specific validated calculation or experiment is needed for a numerical prediction. No empirical Tc was invented; no candidate or QPU job was submitted.

**Confidence:** high for measurements and publication status; moderate for mechanistic extrapolation. Limitations: no independently established S1/S2 cation-ratio assignment or absolute oxygen content; hybridization numerical transport details are from its dated author manuscript, not the paywalled published main text.

## Exact primary sources

1. arXiv record/version history: https://arxiv.org/abs/2512.04708
2. Published Zhou et al. full text, DOI 10.1093/nsr/nwag151: https://pmc.ncbi.nlm.nih.gov/articles/PMC13218385/
3. Versioned Zhou et al. manuscript: https://arxiv.org/pdf/2512.04708v2
4. Osada et al. publisher record: https://www.nature.com/articles/s41563-026-02695-3
5. Osada et al. author manuscript: https://arxiv.org/pdf/2608.17745v1
6. Zhang et al. publisher record/abstract: https://www.nature.com/articles/s41563-026-02750-z
7. Zhang et al. earlier manuscript: https://arxiv.org/pdf/2604.14701v2
8. Published Fig. 1: https://www.nature.com/articles/s41563-026-02750-z/figures/1
9. Published supplementary information, Note 2: https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41563-026-02750-z/MediaObjects/41563_2026_2750_MOESM1_ESM.pdf

**Work/files:** inspected primary publisher records, published open full text, dated author PDFs and published supplementary controls. Wrote `/workspace/runs/turn-0005/astra/nickelate_audit_independent.md`; also wrote ancillary `permission_probe.txt` while checking folder access. Direct shell downloads were not saved because the shell UID lacked directory write permission; the report was successfully saved through the file tool.
