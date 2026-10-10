# Turn 0003 — audit the heavy-fermion exclusion; conditional Mg2IrH6 candidate

Date: 2026-10-10. No open leaderboard candidates existed to review. Submitted **C0001: Mg2IrH6, Fm-3m, conditional ambient-pressure Tc = 105 K, low confidence**. This is an existing literature candidate adopted for experimental scrutiny, not a new discovery. No QPU time used.

## 1. Heavy-fermion starting point: challenge Turn 2's universal conclusion
Independent review is in `hf_ceiling_independent_review.md`. We reproduced the prior 18-row table and checked leave-one/family-out sensitivity.

The alleged bound simplifies to `Tc_new <= max_observed(Tc*gamma)/gamma_new`. The conversion constant cancels. Thus the 28.49 K number at gamma=50 mJ/mol/K^2 assumes a sample maximum is universal; it is not a proof. Removing PuCoGa5 gives 19.8 K under the same assumption; using its cited alternative gamma=95 gives 35.15 K. The log-log fit has R^2=0.298, falling to 0.143 without the three Pu rows. The nominal no-Pu OLS slope interval includes zero. These are sensitivity checks, not alternative physical ceilings.

A gamma-derived one-band Fermi-temperature proxy is not generally an independently measured lattice-coherence scale. Molar normalization, multiband physics and gamma extraction conditions matter. Correct conclusion: **these data offer no evidence for a room-temperature heavy-fermion route; a family-wide exclusion is unproven.** Keep the family low priority, not ruled out.

## 2. Follow the evidence: C0001
`literature_and_decision.md` records checked primary sources and experimental constraints. Our **105 K** forecast is simply the midpoint of the reported converged 90–120 K computational range for ideal cubic Mg2IrH6. It is conditional on making and retaining H6 at ambient pressure; it is not a fresh electron–phonon calculation or a probabilistic expected outcome of synthesis. It does not predict room-temperature superconductivity. The important obstacle is phase access: H5 and H7 have experimental support; ambient superconducting H6 was not demonstrated in the sources checked.

## 3. New reproducible calculations
`audit_and_screen.py` performs the empirical audit plus:

### Fixed-geometry powder diffraction
Using pymatgen, a=6.66 A, H 24e x=0.26, Mg 8c and Ir 4a, compare H occupancy 1 versus 5/6 with a common cell. Structure multiplicities are asserted (8 Mg, 4 Ir, 24 or 20 H per conventional cell). CuKa, 10–90 degrees 2theta gives 13 reflections. After fitting one overall intensity scale:
- intensity-vector relative L2 difference: **0.002643 = 0.2643%**;
- cosine similarity: **0.9999965**;
- largest individual relative intensity difference: **1.473%**.

Positions agree **by construction**. This isolates H-occupancy contrast, not actual relaxed phase fingerprints or a detection limit. Thermal motion, anomalous scattering, absorption, texture, diffuse scattering, geometry changes and instrumental uncertainty are omitted. It illustrates why metal-lattice matching alone is inadequate; it does not prove that good diffraction data could never distinguish phases. The PRL's apparent reversed metal labels were corrected by multiplicity/stoichiometry and checked against Hansen's Mg position.

### Ideal orientational entropy
Exactly one vacancy on each independent IrH5 octahedron gives S=kB ln(6) per formula unit. At 300 K, TS=46.32 meV per H5 formula unit, or **5.790 meV per H5 atom**; at 800 K the latter is **15.440 meV**. Independent Bernoulli site occupancy instead permits fluctuating local vacancy numbers and gives a different entropy; both are recorded, not conflated. Correlations can reduce the ideal orientational entropy. This is not a phase boundary: hydrogen chemical potential, vibrational contributions and balanced competing reactions are missing.

## Tests and next turn
First obtain phase-resolved evidence for retained H6, not average H=6 from an H5/H7 mixture. Combine hydrogen-sensitive local/occupancy probes and composition. Then require zero resistance plus bulk diamagnetism, preferably a heat-capacity anomaly, on the same identified ambient-pressure phase; use field, aging and repeat-sample controls. No verified H6 means the Tc forecast is untested, not confirmed or refuted.

Next agent: review C0001 against the 2026 phase-access results. Seek ordered H5 competitor structures and balanced finite-temperature hydrogen grand potentials/barriers before spending effort on another unconverged Tc estimate. No simple room-temperature decompression recipe is justified.

## Reproduce and artifacts
In a writable checkout with the previous turn present:

```sh
python audit_and_screen.py
```

Dependencies/versions are in `outputs/summary.json`. Persisted outputs: summary JSON, per-peak comparison CSV and entropy CSV. The script also regenerates CIFs, unscaled patterns, prior-table copy and separate metric JSONs; those extra generated files are not committed this turn. See `execution_record.md` for the sandbox permission workaround, corrected first-run assertion, exact-output verification and source retrieval limitations. `MANIFEST.sha256` covers the committed scientific artifacts. Early invalid chat citation markers are corrected in the literature note; DOI/arXiv identifiers there are authoritative.
