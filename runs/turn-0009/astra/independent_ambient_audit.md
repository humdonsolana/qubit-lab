# Independent ambient-pressure audit

**Audit date: October 10, 2026. Scope: literature/source audit only; no hardware, no new material calculations, no candidate submission.** Primary articles and available supplements were inspected directly. “Latest” below means latest relevant evidence located, not a guarantee of exhaustive coverage.

## Bottom line: is an ambient candidate above 133 K actually supported?

- **Neither requested prediction paper supplies a >133 K ambient-pressure result.** Ordered MgAlFeH6 is reported as **approximately 130 K**, not an exact 133+ K value. The fluorite paper's highest ambient prediction is **77.62 K**; its maximum tabulated prediction is **106.04 K at 31 GPa**, not ambient.
- **Mg2IrH6 remains a >133 K theoretical candidate** (predictions up to 170 K at zero pressure), **not an experimentally established or retained ambient superconductor**. Sinha's 2026 synthesis/decompression experiment did not obtain it. A newer September 2026 computational proposal likewise says it has not been synthesized.
- Thus: **theoretical support for a metastable >133 K ambient candidate exists; experimentally verified >133 K ambient performance is not supported by the evidence audited here.** This is a scoped conclusion, not a survey proving absence across all materials. [1–6]

## 1. MgAlFeH6 — DOI 10.1038/s41524-026-02040-x

Xu et al., *npj Computational Materials* 12, 183; first published **March 28, 2026**, with publisher-listed version of record **May 21, 2026**. [1]

| Audit item | Verified result |
|---|---|
| Tc and pressure | **Tc ≈130 K at ambient/zero pressure** for the ordered F-43m structure, from anisotropic Eliashberg gap extrapolation. Tested empirical Coulomb parameters are 0.10, 0.125 and 0.15; EPC λ≈2.1. The article does **not** tabulate an exact Tc for each parameter; reporting additional numerical precision would be unjustified. |
| Disorder qualification | Random Mg/Al alloy: **≈40 K**, estimated using the electronic DOS descriptor, **not** a full Eliashberg calculation. Do not transfer the ordered-lattice 130 K prediction to a random substitution product. |
| Local dynamical stability | No imaginary harmonic phonons; supplementary SSCHA dispersions at **150 and 300 K** also support local stability. Supplementary NPT AIMD uses **300 K, zero pressure**, 288 atoms. |
| Thermodynamic stability | **Metastable, approximately 0.11 eV/atom above the reported hull/decomposition reference.** Negative elemental formation energy (~−0.10 eV/atom) does not establish hull stability. The stated competing products are AlH3, Mg2FeH6, AlFe3H and H2. |
| Synthesis / retention | A **prediction**, not reported synthesis or measured superconductivity of MgAlFeH6. Synthesized parent Mg2FeH6 is not evidence that the Al-substituted ordered target exists. Higher hydrogen pressure/high-pressure preparation and Al implantation are suggestions; no validated synthesis pressure or recovered-sample lifetime is supplied. |

Sources: article Results, Fig. 2 and random-alloy discussion [1]; supplement Figs. S3–S4 [2]. **Finite simulation survival and local phonon stability do not establish macroscopic retention, diffusion barriers, hydrogen-loss resistance or a service lifetime.**

## 2. Fluorite AXH8 — DOI 10.1002/advs.202512696

Huang et al., *Advanced Science* 12(44), e12696; online **September 4, 2025**. Exact values below are the **self-consistent Eliashberg** entries in Supporting Information **Table S3**, not rounded abstract values and not the separate McMillan/Allen–Dynes columns. Pressure is the tabulated lowest **dynamically stable** pressure. [3–4]

| Compound | P (GPa) | Tc (K), μ*=0.10 | Tc (K), μ*=0.15 |
|---|---:|---:|---:|
| AcRhH8 | **0** | **77.62** | 63.90 |
| BaRhH8 | **0** | **51.65** | 35.48 |
| AcIrH8 | **3** | **63.90** | 44.79 |
| BaIrH8 | **3** | **67.82** | 53.12 |
| AcOsH8 | 17 | 66.35 | 50.67 |
| LaRhH8 | 24 | 94.28 | 81.54 |
| CeOsH8 | 31 | 106.04 | 88.89 |
| LaOsH8 | 35 | 83.01 | 65.37 |

**Ambient is not 3 GPa.** The abstract's “near ambient” language must not make AcIrH8/BaIrH8 ambient candidates.

**Hull qualification:** Despite broad title/abstract wording, Results and Fig. 1 explicitly put **AcRhH8 6 meV/atom above the hull at 0 GPa**, reaching hull stability at **10 GPa**. BaRhH8 is reported on the hull at 0 GPa. The main text claims the other seven compounds lie on their hulls at their lowest stable pressures. However, **SI Fig. S1 captions show hull diagrams at 10 GPa for AcIrH8/BaIrH8, 20 for AcOsH8, 25 for LaRhH8, 30 for CeOsH8, and 35 for LaOsH8**, rather than all Table S3 thresholds. These displayed diagrams do **not independently document every claimed threshold**; preserve that internal documentation limitation instead of silently equating phonon thresholds with proven hull boundaries. [3–4]

**Status:** All eight target phases are computational proposals in this paper. No synthesis, measured Tc, pressure-release recovery or long-term retention is reported. Stability evidence is harmonic phonons and static calculated enthalpy hulls; no target-phase anharmonic/free-energy or retention validation was located in the inspected article/supplement. [3–4]

## 3. Mg2IrH6 — newest relevant status located

**Sinha et al., arXiv:2602.23675v1, submitted February 27, 2026**: the current arXiv record lists only v1 and no journal reference. Mg2IrH6 is described as dynamically stable at zero pressure but **~60 meV/atom thermodynamically metastable**, with predicted Tc **up to 170 K**. This is not a measured Tc. [5]

The experiment instead forms insulating cubic **Mg2IrH7 near/above 40 GPa**, alongside a likely Mg2IrH5-related hexagonal phase. On room-temperature decompression the cubic H7 phase survives only to **~20 GPa**, then returns to cubic **Mg2IrH5**. Transport remains insulating across the transition; **no spontaneous metallic/superconducting Mg2IrH6 intermediate was observed**. This is a **negative result for the tested simple decompression route**, not a refutation of superconductivity in a successfully isolated H6 phase. [5]

**Later located item:** Lee, **September 7, 2026**, Zenodo preprint DOI **10.5281/zenodo.22642971** (record version labelled rev. 4): a DFT reproduction/electrochemical-insertion proposal, explicitly stating Mg2IrH6 remains unsynthesized. Its bare insertion energy is **+0.66 eV per H**; it does not measure superconductivity or demonstrate electrochemical synthesis. Treat it as unreviewed proposed processing, not experimental replication. [6]

**Do not confuse the August 20, 2026 JACS result with Ir:** DOI **10.1021/jacs.6c08889** concerns **Mg2RhH6**, reporting **24 K near 30 GPa** and **29 K after synthesis at 53 GPa**—neither Mg2IrH6 nor ambient >133 K validation. [7]

## 4. Retractions, comments and replication checks — bounded results

- The Nature article and fluorite deposited full text displayed no retraction/correction notice in the material inspected. Both exact-DOI **Crossref** records had no `update-to` entry and empty `relation`; **OpenAlex** marked both `is_retracted:false`. These checks support **“no notice found,” not an unconditional clean bill of health**. [8–9]
- OpenAlex targeted searches for `MgAlFeH6 retraction`, `MgAlFeH6 comment`, `AcRhH8 comment`, each DOI plus `retraction`, and `2602.23675 comment` returned zero indexed results. The fluorite paper's three indexed citing works were not identified as replication/comment papers; the MgAlFeH6 record had zero indexed citations. Formula search located an April 2026 generic Tc-framework preprint, not an experimental replication. [9]
- **PubPeer was attempted for both DOIs but returned HTTP 403**; absence of discussion could **not** be verified. Ordinary Google/DuckDuckGo searches were blocked/challenged; Bing returned irrelevant results and was discarded. Bibliographic API searches therefore cannot exclude unindexed comments or failed attempts.
- No target-specific formal refutation or independent experimental replication of MgAlFeH6/these AXH8 predictions was located in accessible records. **Sinha's negative Mg2IrH6 access result is explicitly included above.** Its arXiv page had no withdrawal notice. Lee's proposal had no withdrawal notice in the inspected record; the later Mg2RhH6 record was not flagged retracted and its Crossref record carried no update notice. [5–9]

## 5. What each kind of “stability” establishes

1. **Harmonic dynamical stability:** local small-displacement curvature at the chosen pressure/structure; real phonons do not exclude a lower-energy phase or activated decomposition.
2. **Thermodynamic hull stability:** relative static enthalpy against the competing phases actually searched. Above-hull structures are metastable; finite-temperature entropy, quantum nuclei and omitted phases can change the result.
3. **Retention / recoverability:** kinetic survival of the correct composition and structure after synthesis/decompression over relevant times. It needs separate barrier/kinetic evidence or recovered-sample experiments; neither a harmonic spectrum nor a static hull proves it.

The requested evidence itself illustrates the distinctions: MgAlFeH6 is locally stable but above hull; AcRhH8 is phonon-stable at zero pressure but slightly above hull; Sinha's insulating H7 phase loses hydrogen on decompression rather than yielding retained H6. [1–5]

## Verified source links

1. [MgAlFeH6 primary article](https://www.nature.com/articles/s41524-026-02040-x)
2. [MgAlFeH6 supplementary PDF](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41524-026-02040-x/MediaObjects/41524_2026_2040_MOESM1_ESM.pdf)
3. [Fluorite article DOI](https://doi.org/10.1002/advs.202512696); [deposited primary full-text XML actually read](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12667446/fullTextXML)
4. [Fluorite supplementary-files ZIP actually read](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12667446/supplementaryFiles), containing `ADVS-12-e12696-s001.docx`, Tables S2/S3 and Fig. S1 captions.
5. [Sinha current arXiv record](https://arxiv.org/abs/2602.23675); [v1 primary full text](https://arxiv.org/html/2602.23675v1)
6. [Lee September 2026 proposal](https://doi.org/10.5281/zenodo.22642971); [primary repository metadata](https://zenodo.org/api/records/22642971)
7. [Mg2RhH6 experimental paper](https://doi.org/10.1021/jacs.6c08889); [publisher-deposited abstract/metadata actually read](https://api.crossref.org/works/10.1021/jacs.6c08889)
8. Crossref exact records: [MgAlFeH6](https://api.crossref.org/works/10.1038/s41524-026-02040-x), [fluorites](https://api.crossref.org/works/10.1002/advs.202512696).
9. OpenAlex records/search: [MgAlFeH6](https://api.openalex.org/works/https://doi.org/10.1038/s41524-026-02040-x), [fluorites](https://api.openalex.org/works/https://doi.org/10.1002/advs.202512696), [fluorite citing works](https://api.openalex.org/works?filter=cites:W4414028386&per-page=100), [Mg2IrH6 date-sorted search](https://api.openalex.org/works?search=Mg2IrH6&sort=publication_date:desc&per-page=25). Retraction flags/searches are secondary indexing checks, not physical evidence.

**Confidence:** high in the extracted Tc/pressure numbers and in the distinction between prediction and demonstrated synthesis; moderate in reported static stability because this audit did not reproduce calculations; limited/moderate in absence-of-comment/replication findings because PubPeer and general search were inaccessible. **File written:** `runs/turn-0009/astra/independent_ambient_audit.md`. No QPU use or candidate submission.
