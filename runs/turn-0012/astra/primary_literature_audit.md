# Turn 12 — Astra independent primary-literature audit

**Audit date:** 2026-10-11 (sandbox UTC date). **Scope:** literature and public-data inspection only. No candidate invention, Fable calculation reuse, QE, QPU, or new superconducting calculations. Source numbers below are predictions unless explicitly marked experimental. This is a bounded audit, not a claim of an exhaustive 2026 literature census.

## Executive recommendation

For a modest numerical audit, start with **Nepal–Wang Supplementary Tables S10–S17: 381 dynamically stable DFPT rows in a 4,071,134-byte, 28-page PDF** [N2]. I independently parsed 381 seven-field rows and ranked the published Tc column; these are not my Tc calculations. `extract_stable_tables.py` reproduces the extraction to standard output. Preserve MP identifier, space group, formation energy, coupling, frequency, and Tc; do not equate formation energy with energy above hull.

For **known experimental-crystal provenance and selection-funnel auditing**, use the small MC3D CSVs [M2–M3], especially `Table_D.csv` (949 rows; 82,402 bytes). **Important: these CSVs do NOT contain Tc, lambda, or omega_log**. They cannot by themselves reproduce the superconductivity ranking. For that, use the paper's Tables I/II and supplementary property tables, or the larger EPW/AiiDA archive. Do not spend tens of GB downloading the full archive first.

**Best conditional high-Tc lead in the audited MC3D paper:** hole-stabilized BaB2, **61.6 K anisotropic**, not pristine BaB2. **Best unflagged undoped Table-II entry:** W2N3, **33.7 K anisotropic**. **Strong near-hull stable lead in the requested boron/carbon study:** TaNbC2, **28.387 K** tabulated; rounded **28.4 K** in the paper. No audited source establishes ambient room-temperature superconductivity. These materials are published prior work, not new lab candidates. [M1; N1–N2]

## 1. Requested 2026 boron/carbon paper

Nepal and Wang, *Machine-learning guided search for phonon-mediated superconductivity in boron and carbon compounds*, npj Computational Materials 12, 152. Published **2026-03-04**, version of record **2026-04-13**, DOI **10.1038/s41524-026-01962-w**. The work reports **417** computed compounds and CGCNN/ALIGNN screening. Its pool includes both experimental and theoretical Materials Project structures; it is **not exclusively a screen of known experimental crystals**. [N1]

### Published stable-table numbers, directly transcribed from SI

| Material / MP ID | SG | lambda | omega_log (K) | Tc (K) | Interpretation |
|---|---:|---:|---:|---:|---|
| B2CN / mp-1008525 | 160 | 1.66 | 577 | **60.733** | Highest Tc in the parsed stable tables; theoretical/metastable lead, not established experimental superconductivity |
| B13C2 / mp-576 | 166 | 0.97 | 835 | **39.304** | Tabulated prediction, not evidence of measured superconductivity |
| B2CN / mp-1008526 | 156 | 1.11 | 566 | **34.900** | Different polymorph; do not merge by formula |
| B24Mo7 / mp-1228730 | 187 | 1.33 | 359 | **28.901** | Tabulated prediction; synthesis/phase viability not established here |
| TaNbC2 / mp-1217924 | 166 | 1.41 | 326 | **28.387** | Main text identifies approximately 0.02 eV/atom above hull |
| Nb3B3C / mp-29979 | 63 | 1.22 | 229 | **16.438** | Main text: 0.018 eV/atom above hull; crystal previously synthesized, superconductivity unmeasured in this report |

Source: SI S12–S14 [N2]; context/hull statements: [N1]. **60.733 K is a published supplementary number, not an invented extrapolation.** The main text says B2CN phases have energies above hull up to **0.35 eV/atom**; I did not independently verify a phase-specific hull value for mp-1008525. Therefore it ranks above TaNbC2 by tabulated Tc but below it in practical confidence. Formation energies in the SI are not hull energies.

### Conditional unstable-phase lead

**Ca5B3N6:** lambda **1.5**, omega_log **372 K**; **35 K** with mu* **0.16**, **42.4 K** with mu* **0.10**. Energy above hull approximately **0.03 eV/atom**. However, the harmonic structure is unstable at H and is stabilized computationally using electronic smearing **0.06 Ry**, with coupling evaluated at broadening **0.10 Ry**. The experimental structural reference has partial Ca occupancy; it is not a measurement of superconductivity in the modeled stoichiometric compound. Treat this as a **smearing-conditioned prediction**, not proof of ambient low-temperature stability. [N1]

Do **not** automatically classify the **27.9 K Sc2C3** result as ambient: the text mixes “ambient or moderate pressure,” and its illustrated stabilization includes **30 GPa**. Pressure/smearing/distortion branches must be kept separate. [N1]

### Methodological risks worth testing

- **Numerical stabilization is not physical stabilization.** My inference: increasing electronic smearing changes occupations and phonons; it is not a demonstrated replacement for anharmonic free-energy calculations or an experimentally realized dopant/structure. Distinguish SCF smearing from double-delta integration broadening. [N1]
- The convergence ansatz fits `Tc = exp(-A sigma^(1/3) + B)` and uses **A approximately 12–13**, calibrated to MgB2, as a convergence threshold. My inference: this is a useful diagnostic, not a universal proof of k/q convergence in different Fermi surfaces. [N1]
- The study's Tc treatment is isotropic, with the displayed Allen–Dynes-type formula; do not present it as an anisotropic Migdal–Eliashberg calculation. Small random splits and improvements against calculated labels do not establish experimental accuracy or chemical-family transfer. [N1]
- **Data consistency flags to audit, not silently repair:** SI includes mp-12062 AgB2 with **positive formation energy 0.52 eV/atom**, despite the stated negative-formation-energy selection; mp-1212439 Hf5Al3C has omega_log **2988 K**; mp-109894 ZrC has lambda **0.01** and Tc **0.405 K**. Check these against raw files and the exact Tc/broadening conventions before training. I have not determined whether they are transcription, numerical, or selection-history issues. [N1–N2]

## 2. Requested 2025 MC3D landscape study

Bercx et al., *Charting the Landscape of Bardeen-Cooper-Schrieffer Superconductors in Experimentally Known Compounds*, **PRX Energy 4, 033012**, published **2025-08-29**, DOI **10.1103/sb28-fjc9**; associated preprint **arXiv:2503.10943**. This is principally **direct high-throughput DFT/EPW screening**, not itself an ML-only candidate screen; it is a valuable label/provenance source for ML. [M1; M4]

**Version warning:** the user's `2025.39` archive shorthand resolves to the latest record `0kqen-w8h90`. API inspection gives **version index 4**, publication **2025-11-04**, `is_latest=true`; earlier records are dated **2025-03-13**, **2025-07-03**, and **2025-07-04**. These are dataset revisions, not by themselves correction notices. [M2–M3]

The archive reports **4533** nonmagnetic metals initially screened, **250** dynamically stable high-quality structures, **140** with anisotropic results, and **24** previously unknown superconductors predicted above **10 K** anisotropically. Predictions use fixed **mu* = 0.13**. [M1–M2]

| Published Table-II material | Allen–Dynes fine-grid (K) | Isotropic ME (K) | Anisotropic ME (K) | Qualification |
|---|---:|---:|---:|---|
| BaB2 | 21.4 | 33.0 | **61.6** | Stabilized with **0.065 holes/unit cell**; pristine phase unstable |
| W2N3 | 20.2 | 26.3 | **33.7** | Highest entry outside flagged magnetic/source/doping sections |
| Be2B | 7.7 | 10.9 | **22.1** | Unflagged Table-II entry; prediction, not measurement |
| ZrRuSb | 8.9 | 9.9 | **13.2** | Nonmagnetic half-Heusler lead discussed in detail |
| TaRu3C | 16.5 | 21.0 | **25.0** | Explicitly **potentially magnetic** in Table II |
| NbRu3C | 17.5 | 21.8 | **24.9** | Explicitly **potentially magnetic** |

Source: published Table II [M1]. The magnetic caveat should travel with the headline TaRu3C number, even though the abstract highlights it.

**Internal negative controls / model discrepancy:** Table I predicts RuO2 at **34.0 K anisotropic** while listing experimental **Tc <0.3 K**; Nb3Sn at **35.6 K** against **17.9–18.3 K**; MgB2 at **36.8 K** against **39.0 K**. These are author-reported comparison numbers, not independently rechecked measurements. The paper explicitly warns about omitted spin fluctuations, fixed Coulomb repulsion, and Kohn–Sham electronic spectra. Thus “DFT-confirmed” is not experimental confirmation. The ±**10^21 cm^-3** rigid-band sensitivity analysis is useful but not a full disorder/defect/phase-stability test. [M1]

### Actual small CSV downloads inspected

All four have exactly five columns: **Formula; Spacegroup; Source Database; Source ID; MC3D Link**. Counts are data rows excluding header.

| File | Bytes | Rows | Role |
|---|---:|---:|---|
| Table_A.csv | 896325 | 10195 | Unique experimental structures |
| Table_B.csv | 396981 | 4533 | Nonmagnetic metals |
| Table_C.csv | 139447 | 1599 | Initial coarse-screen Tc >1 K selection, but Tc values absent |
| Table_D.csv | 82402 | 949 | EPW pipeline selection |

These sizes/counts/columns were independently read from API metadata and pandas parsing [M2–M3]. `Table_D.csv` MD5: **687e55231ad73ded033381c60c15478d**. Sum A–D: **1,515,155 bytes**. Audit the funnel using structure/source IDs, not formula-only joins. The full latest archive is **25,196,179,044 bytes**; it was not downloaded.

## 3. Newer primary comparisons, through this audit date

- **2025-01-09:** Gibson et al., *Accelerating superconductor discovery through tempered deep learning of the electron-phonon spectral function*, DOI **10.1038/s41524-024-01475-4**. BETE-NET uses **818** dynamically stable computed materials. Its important warning: an apparently competitive baseline Tc MAE **2.84 K** accompanies **R2 = -0.08**. MAE alone hides poor ranking/generalization. GitHub's `database.json` is **89,104,840 bytes**, not a tiny table; no download was attempted. [G1; G2]
- **2026-01-27**, version of record **2026-02-19:** *Developing a complete AI-accelerated workflow for superconductor discovery*, DOI **10.1038/s41524-026-01964-8**. BEE-NET advertises **0.87 K** MAE **against DFT Allen–Dynes labels**, not experimental Tc; **741** final compounds, **69** predicted at least **20 K**. Experimental reality check: ordered Be2Hf2Nb changes from initial prediction **14.9 K** to refined **9.3 K** (mu* **0.21**); the synthesized material is reported fully superconducting below approximately **2 K**. Be2HfNb2 has two heat-capacity jumps, indicating a multiphase sample. Authors state the modeled spectral range stops at **100 meV** and is trained at ambient pressure. [G3]
- **2026-05-28**, version of record **2026-08-24:** *Guided diffusion for the discovery of new superconductors*, DOI **10.1038/s41524-026-02117-7**. This is newer than both requested studies, but generative rather than known-crystal-only screening. **773** DFT candidates above **5 K**, extending to approximately **35 K**. Of **18** synthesis attempts, **9** show superconductivity above **4.2 K**, but Tc is lower than predicted and **the predicted structures generally did not form**: mostly disordered BCC solutions or mixtures of known phases. The approximately **5.3 K** signal in Re4TaZr is attributed to **Re2Zr**, not validation of the predicted ternary crystal. This is direct experimental evidence of a workflow failure mode, not a formal refutation of all predictions. [G4]

## 4. Corrections, retractions, comments, refutations, replication — bounded check

For **each of N1, M1, G1, G3, G4**, inspected available publisher/primary pages and Crossref DOI metadata. No `update-to` entry appeared in the Crossref records; npj relations were empty, while MC3D's journal record linked its preprint. No correction/retraction banner was observed on the four inspected npj article pages. The APS landing page returned **403**; the published PDF was read from the institutional repository instead. This is **not** proof of a clean status or independent replication.

Explicit broad-search queries combined each exact DOI with `correction retraction comment refutation` (or replication). **Search limitation:** Google returned redirect/challenge text and Bing returned unrelated results despite the exact DOI queries; these broad-search responses are not adequate evidence that no notices exist. Therefore **formal comments/refutations and independent replications remain incompletely searched**, and I do not certify their absence. Crossref metadata can also be incomplete. No retraction was found in the limited reliable checks; none of the high-Tc predictions listed here is treated as independently experimentally replicated.

Distinguish external repudiation from the primary authors' own limitations: MC3D includes substantial experimental discrepancies and magnetic/source flags; BEE-NET experiments fall far below headline predictions; the May 2026 study reports failed formation of predicted ordered structures. Those findings are documented above, not hidden behind a generic “no retraction” statement.

## 5. Recommended bounded numerical follow-up (no new physics calculation)

1. Run `extract_stable_tables.py` to obtain the **381-row** SI table. Check exact row count, unique MP IDs, missing values, lambda/Tc consistency, omega_log outliers, and formation-energy sign. Preserve source table and PDF page.
2. Cross-reference the **60.733 K B2CN** row and **28.387 K TaNbC2** row against main Table I and raw convergence data before treating either as a target. Use TaNbC2 and Nb3B3C as the practical near-hull subgroup, not a global “highest Tc wins” ranking.
3. Download MC3D `Table_D.csv`; audit source/phase identity and funnel overlap. Then manually transcribe the small published Tables I/II or obtain the supplementary label table before attempting a numerical Tc comparison. Never infer labels from selection membership.
4. Keep separate columns for pressure, doping, structural/magnetic status, mu*, Tc estimator, and experimental outcome. Family/phase-grouped held-out evaluation and precision–recall are more informative than a pooled random-split MAE alone.

## Primary sources and reproducible download locations

- **[N1]** Publisher: https://www.nature.com/articles/s41524-026-01962-w
- **[N2]** Supplement (28-page PDF): https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41524-026-01962-w/MediaObjects/41524_2026_1962_MOESM1_ESM.pdf
- **[N3]** Figshare metadata: https://api.figshare.com/v2/articles/28557776 ; one raw file `B_C_Superconductivty.tar.gz`, **7,360,051,258 bytes**, published **2025-03-17**. Not downloaded.
- **[M1]** DOI: https://doi.org/10.1103/sb28-fjc9 ; published PDF institutional mirror: https://iris.polito.it/retrieve/41cca4a4-17b5-44de-9b90-23da0dab406d/sb28-fjc9.pdf
- **[M2]** Archive: https://archive.materialscloud.org/record/2025.39 ; current API: https://archive.materialscloud.org/api/records/0kqen-w8h90 ; versions: https://archive.materialscloud.org/api/records/0kqen-w8h90/versions
- **[M3]** Direct small CSV download: https://archive.materialscloud.org/api/records/0kqen-w8h90/files/Table_D.csv/content ; replace `Table_D.csv` with A/B/C as needed. README: https://archive.materialscloud.org/api/records/0kqen-w8h90/files/README.md/content
- **[M4]** Crossref: https://api.crossref.org/works/10.1103/sb28-fjc9
- **[G1]** https://www.nature.com/articles/s41524-024-01475-4
- **[G2]** Authors' repository: https://github.com/henniggroup/BETE-NET ; tree metadata inspected through GitHub API.
- **[G3]** https://www.nature.com/articles/s41524-026-01964-8 ; authors' code/data pointer: https://github.com/henniggroup/BEE-NET
- **[G4]** https://www.nature.com/articles/s41524-026-02117-7 ; authors' dataset pointer: https://huggingface.co/datasets/paprakash/GuidedMatDiffusion_data (pointer verified in article; contents not downloaded).
- Crossref check pattern: `https://api.crossref.org/works/<DOI>` for the four npj DOIs above.

**Confidence:** high in directly inspected numbers, CSV schema/counts, and the distinction between prediction and measurement; moderate in practical lead ranking; limited in broad notice/replication coverage and phase-specific viability. Files written: this report and the extraction script. The sandbox denied shell creation of new working-directory files, so files were written through the prescribed `write_file` tool; downloads were read in memory. No large raw archives were downloaded.
