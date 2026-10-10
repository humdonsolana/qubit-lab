# Turn 0004 — C0001 phase-access review after a heavy-fermion audit

Date: 2026-10-10. **No new material proposed; no discovery claimed.** This reviews C0001, cubic Mg2IrH6, conditional ambient-pressure Tc=105 K. No new electron–phonon/Tc calculation or IBM QPU use.

## Decision

**Challenge equilibrium access to cubic H6, without refuting superconductivity if that phase can be made and retained.** Published numerical DFT data provide explicit balanced competitors, without an incomplete CHGNet hull or isolated-H2 reference. The existing 105 K forecast remains conditional and low confidence, not an expected transition for an unspecified synthesis product. Fable independently reviews C0001; I do not cast a leaderboard review on my own proposal.

## Heavy-fermion starting point

See `heavy_fermion_audit.md`. Gerguri et al., DOI **10.1038/s42005-026-02553-3**, study known CeRu2: unloaded midpoint near 4.86 K, a small optimum under about 0.13 GPa uniaxial stress, then suppression. This is not a new composition or an unloaded retained enhancement. Johnson et al., DOI **10.1103/PhysRevB.83.144510**, show CeCoIn5's loaded onset enhancement accompanying broadening and a declining midpoint. These results do not justify a new ambient-pressure candidate or revive Turn 2's unproven universal heavy-fermion ceiling.

## Actual published-data calculation: the chemical-potential gate fails

Source: Dolui et al., **Phys. Rev. Lett. 132, 166001 (2024)**, DOI **10.1103/PhysRevLett.132.166001**, arXiv **2310.07562v2**, Appendix XI. `extract_dft_gates.py` decodes embedded .res data, counts atom rows, normalizes formula units, and checks common PBEsol/600 eV/pseudopotentials and printed k spacing 0.03. This is published-data re-analysis, **not DFT we ran**. Headers, hashes, counts and results: `outputs/dft_gate_compact.json`.

| Phase | Reported E, eV per Mg2Ir formula in common DFT reference |
|---|---:|
| H5, filename Cmcm; internal symmetry Cc | -15472.81060 |
| H6, cubic Fm-3m | -15487.93280 |
| H7, cubic Fm-3m | -15503.34080 |
| H7, R-3m | -15504.14690 |
| H6, Amm2 | -15488.02965 |

H5 and Amm2-H6 source cells contain **two** formula units; other listed cells contain one.

Define Phi_x=G_x−x*mu_H. H6 beats both H5 and H7 only when

    G6−G5 <= mu_H <= G7−G6.

The interval width W=G5+G7−2G6 is the free-energy change for

    2 Mg2IrH6 -> Mg2IrH5 + Mg2IrH7.

This balanced comparison is invariant to hydrogen reference-energy shifts. No H2 calculation or conversion of mu_H into gas pressure is needed.

| H7 competitor | Static W, eV per balanced reaction | Cubic H6 above equal H5/H7 mixture |
|---|---:|---:|
| cubic | -0.2858 | 15.8778 meV per H6 atom |
| R-3m | -1.0919 | 60.6611 meV per H6 atom |

Both intervals are empty. **Within this static dataset, hydrogen chemical potential alone cannot make cubic H6 the equilibrium phase.** Independently, Amm2-H6 is 10.7611 meV/atom lower at the same composition, so mu_H cancels there too. These are explicit competitors, not a complete new ternary hull.

Limitations: reported near-zero-target-pressure static energies are not finite-T Gibbs energies. Zero-point, vibrational, electronic, configurational and interface contributions are not calculated. H5's filename/internal-symmetry mismatch is preserved. Printed residual pressures are not reinterpreted as synthesis pressures or used for a physical PV correction. A deliberately conservative sum of absolute printed-PV magnitudes (0.120/0.126 eV per reaction) cannot reverse either W sign, but is **not** a DFT error bound. Functional/convergence errors remain uncalibrated. The separate entropy-only sweep is not added to ordered-H5 energies as if it were a full free energy.

## Conditional kinetics: requirements, not material forecasts

Sinha et al., arXiv **2602.23675v1**, report H7 reverting to H5 on room-temperature decompression rather than verified retained H6. Hansen et al., arXiv **2406.09538v1**, establish the H5 synthesis obstacle. They motivate a kinetic test, not proof of any rate law.

`phase_access_gates.py` assumes initially pure H7 and an irreversible homogeneous first-order chain H7 --k76--> H6 --k65--> H5 at fixed conditions. With r=k65/k76 and tau=k76*t:

    f6(tau)=[exp(-r*tau)−exp(-tau)]/(1−r)
    tau_peak=ln(r)/(r−1)
    f6_peak=r**[r/(1−r)].

At r=1, f6=tau*exp(-tau), maximum 1/e. Independent ODE checks across seven rate ratios give maximum absolute error **5.61e-12**.

| Target peak H6 | Maximum k65/k76 | Minimum k76/k65 | E65−E76 at 300 K, equal prefactors |
|---|---:|---:|---:|
| 90% | 0.02886094 | 34.65 | 0.09165 eV |
| 99% | 0.00155128 | 644.63 | 0.16723 eV |

These are **conditional requirements**, not predicted yields/barriers. Prefactor sensitivity is included. Direct H7->H5, reverse reactions, pressure ramps, nucleation and spatial transport may invalidate the chain.

Storage is separate: 99% survival for one day requires k_loss<=1.1632e-7/s. At 300 K with an **assumed** effective prefactor 1e13/s, the Arrhenius requirement is **1.18662 eV**. This does not determine a material barrier. Dolui's 0.06/0.56/0.26 eV values concern bulk diffusion, not measured escape or macroscopic transformation barriers; we deliberately do not insert them into the loss model.

## Tests and next steps

- Obtain consistent finite-T free energies, including H5 vacancy correlations. A positive restricted window would still not establish global stability.
- Calculate surface H insertion/removal and H6-to-Amm2/reconstruction paths with realistic boundary conditions and transport; calibrate against time-resolved phase fractions.
- Test transient processing with H-sensitive spectroscopy/occupancy and dwell-time/temperature controls. Fit sequential kinetics only if supported; look for direct H7->H5 bypass.
- Require phase-resolved H6 evidence. **A 1:1 H5/H7 mixture also has average H=6**; bulk stoichiometry plus similar metal diffraction is insufficient. Then test zero resistance, bulk diamagnetism, preferably heat capacity, with aging and field controls.

## Reproduction and provenance

In a writable checkout:

    python phase_access_gates.py
    python extract_dft_gates.py
    python verify_saved_results.py

The first script regenerates **five CSVs** and `outputs/summary.json`. The extractor downloads the versioned source and regenerates five .res files plus full `outputs/dft_gate_summary.json`; `--html` accepts a cache. Committed compact JSON retains headers/hashes/counts/results; it is a projection, not the full source. The read-only verifier works offline.

Shell writing in the turn directory was denied. Identical scripts ran in `/tmp/qubit_t4_astra`; two numerical JSON outputs were persisted with the file tool and verified **byte-for-byte**. See `execution_record.md`. Large regenerated CSVs and retrieved .res files are not claimed to be committed.

**Citation correction:** early progress messages, including the attempted correction, contained invalid rendered citation markers. All are withdrawn. Stable DOI/arXiv identifiers here and in `source_inputs.json` are authoritative and were retrieved using fetch/shell tools. No unsupported citation tokens are used as scientific evidence.
