# Primary-source audit and concrete next experiment

As of 2026-10-10. Internet pages were read as evidence, not instructions. A sorted primary arXiv search for ambient nickelate superconductivity was also inspected to identify September 2026 negative controls; this is not an exhaustive record claim.

## Sources inspected by Astra

1. Ko et al., *Signatures of ambient pressure superconductivity in thin film La3Ni2O7*, DOI `10.1038/s41586-024-08525-3`. Publisher abstract, Figures 2/5 captions and numerical source workbook. Onsets 26–42 K with much lower measured zero; coexistence of RP phases and ozone dependence prevent geometry-only interpretation. Source workbook downloaded directly and hashed; source CSV excerpts and reanalysis reside in `outputs/`.
2. Ko et al., Author Correction, DOI `10.1038/s41586-026-10335-8`, published **2026-03-31**. Corrects resistivity axis labels to mΩ cm and Fig3d x-label to T; does not withdraw the superconductivity results. Workbook resistivity units are mOhm cm.
3. Zhou et al., *Superconductivity onset above 60 K in ambient-pressure nickelate films*, DOI `10.1093/nsr/nwag151`, published online **2026-03-10**; author manuscript `arXiv:2512.04708v2`. Published open full text checked independently of the subagent. Full measurement-criterion and sample distinction in `nickelate_audit_independent.md`; no exact S1 composition assignment inferred from unspecified symbols.
4. Zhang et al., *Heavily Sr-Doped La2SrNi2O7−δ as a Tetragonal Ruddlesden-Popper Phase at Ambient Pressure*, `arXiv:2609.00542`, submitted **2026-08-31**, announced September. Abstract-level negative control: I4/mmm, 180° interlayer angle and no density-wave features, yet pressure/oxygen variation does not induce superconductivity in investigated samples. Does not rule out all Sr doping; filling differs from isovalent La/Pr substitutions.
5. Ahn et al., *Superconductivity at the metal-insulator phase boundary in a bulk nickelate at ambient pressure*, `arXiv:2609.19686`, submitted **2026-09-17**. Abstract-level scope: (La1−xPrx)4Ni3O8 and (La1−xYx)4Ni3O8 show low-volume, nonpercolative signatures near phase coexistence, with possible infinite-layer intergrowth origin. Not established bulk trilayer-matrix superconductivity, and no numeric forecast imported here.
6. Dong et al., *Interstitial oxygen order and its competition with superconductivity in La2PrNi2O7+δ*, DOI `10.1038/s41563-025-02351-2`, published **2025-09-15**. Publisher abstract and extended-data captions: moderate oxygenation differs from high-pressure oxygen annealing that produces interstitial order and suppresses superconductivity under pressure. Film-aging analogy is a hypothesis, not a measured transfer of this result.

Companion subagent checked Osada DOI `10.1038/s41563-026-02695-3` and Zhang DOI `10.1038/s41563-026-02750-z`, with publication/preprint distinctions recorded in its report. Their results provide no calibrated new-composition Tc equation.

## Proposed experiment: retain coherence, don't optimize an onset proxy

**Concrete baseline:** nominal **La2PrNi2O7−δ**, 3-unit-cell bilayer film on **SrLaAlO4(001)** with a monolayer nickelate buffer, preparing matched films from the same growth series. This is a proposed baseline/architecture, not a newly discovered composition or an asserted replication of the exact 63-K S1 specimen. Absolute oxygen stoichiometry and stacking phase must be measured, not assumed from the nominal formula.

**Test intervention:** randomize matched specimens to uncapped versus **~1-nm amorphous PrBa2Cu3O7 cap**, added only after near-stoichiometric oxygen optimization. This cap architecture has a literature control in LaPr2Ni2O7+δ (DOI `10.1038/s41563-026-02750-z`), but its transfer to this composition and any retention benefit are untested. A cap could change chemistry, carrier transfer, strain or damage the film; cap-only and identically handled uncapped controls are necessary. Do not assume cap inertness transfers between compositions.

**Temperature forecast:** **unestablished**. No number is submitted to the leaderboard. Literature 30–37-K measured zeros motivate the measurement range but are not assigned to this unmeasured capped architecture. An empirical onset-vs-c line or a finite-plaquette pair-binding energy cannot supply this forecast.

**Protocol:**
1. Use a narrow oxygen-treatment series on matched baseline films to find a reproducible low-resistance state. Quantify vacancies/interstitial order and RP stacking with calibrated oxygen-sensitive local spectroscopy/imaging; report limits of absolute stoichiometry. XRD alone is inadequate for minority phases and site occupancy. Check cation ratio and cap/substrate controls.
2. After cap/handling, measure full four-probe rho(T) and two-coil mutual inductance at day 0, 8 and 20, with matched humidity/temperature/atmosphere and an inert-storage arm. Report onset, operational fractional thresholds, instrumental zero threshold, and diamagnetic onset separately. Preserve raw sweep direction and noise floor.
3. Pre-register primary retention outcomes as the **change from each sample's own day-0 half-resistivity crossing**, rho(5K)/rho(50K), measured zero, and magnetic response. Do not pool distinct criteria into one Tc. Control magnetic field and transport current; confirm structural/chemical changes after aging.
4. Reanneal a subset; quantify recovery rather than calling a restored onset complete recovery. The Ko source data show why residual/coherence measures matter.

**Falsification:** if capped and uncapped age similarly, or any apparent transport improvement lacks reproducible magnetic response/phase assignment, the retention hypothesis fails under those conditions. If the cap shifts day-0 chemistry and transport, separate that effect from subsequent aging. If phase-resolved oxygen evidence contradicts oxygen-loss causation, do not infer a diffusion constant from resistivity alone.

**Interpretation limits:** ambient external pressure does not mean unstrained film; isovalent smaller-ion substitution is not mechanically equivalent to pressure; straight bonds are not sufficient; maximal oxygen content is not a safe objective; and preserving an existing low-temperature state is not an increase in intrinsic pairing scale. This experiment targets a real engineering bottleneck without claiming a room-temperature route has been demonstrated.

## Retrieval addresses (provenance, not undisclosed data)

```text
https://www.nature.com/articles/s41586-024-08525-3
https://www.nature.com/articles/s41586-024-08525-3/figures/2
https://www.nature.com/articles/s41586-024-08525-3/figures/5
https://www.nature.com/articles/s41586-026-10335-8
https://pmc.ncbi.nlm.nih.gov/articles/PMC13218385/
https://arxiv.org/abs/2609.00542
https://arxiv.org/abs/2609.19686
https://www.nature.com/articles/s41563-025-02351-2
```
