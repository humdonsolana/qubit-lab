# Turn 10 independent numeric validation

**11 October 2026 — `/workspace/runs/turn-0010/astra`.** PASS for numerical reproduction of the supplied SC1/SC2 before/after CSV analysis; this is **not** an independent transport experiment or a verification of the publisher's figure caption. No literature fetch, QPU submission, candidate submission or paid resource was used. Platform billing is not exposed, so an exact dollar total cannot be certified.

## Inputs and independent method

Read `transport_reanalysis.py`, `/tmp/astra10/transport_results.json`, `transport_manifest.json`, all four named original CSVs and `binned_transport.csv`. Source citations are these local artifacts; the manifest's Figshare file identifiers are 67351044 (SC1 before), 67351038 (SC1 after), 67351053 (SC2 before), and 67351047 (SC2 after). Full SHA-256 hashes, byte sizes and counts are in `outputs/transport_summary.json`. All four CSVs match the manifest exactly. Additional local `67351080.csv` and `67351077.csv` are byte-identical to SC1-before and SC2-before respectively; they are not additional independent measurements.

Wrote `independent_transport_audit.py` without importing or executing the original transport functions. It uses standard-library CSV parsing, `statistics.median`, explicit linear interpolation and independent threshold enumeration. Reproduce with `python independent_transport_audit.py > /tmp/astra10_independent.json`; it reads the supplied inputs from `/tmp/astra10` and does not write the repository. The compact archived summary was subsequently checked against the independent computed main values, sensitivity ranges and hashes.

Exact algorithm reproduced:
1. Drop missing x/y, retain **strict `0 < x < 80 K`**. No missing/nonfinite values were present. Raw → retained → 0.5-K-bin counts: SC1 before **1283→436→141**; after **1020→153→138**; SC2 before **110→39→32**; after **2005→506→155**.
2. Bin using nearest-integer `round(x/bw)` with ties to even, **not floor intervals**. Take x and y medians separately, then sort by median x. Temperatures are median x, not nominal bin centers.
3. Interpolate R at 50 K between binned data; no normal-state fit. General interpolation clamps outside the endpoint domain, but all reference temperatures here are inside the retained domain.
4. Restrict crossing candidates to binned temperatures <= reference. Select the highest-T adjacent pair satisfying **Rlow < threshold <= Rhigh**, then linearly interpolate. This reproduces the original first downward crossing on cooling; no monotonic smoothing or extrapolation to zero.

**246 reported numeric fields** (all main, separately varied bins/references and sample changes) agree within **2.8422e-14**. **932 binned x/y cells** agree within **5.6843e-14**, with no structural/null mismatches. Independent float parsing accounts for last-bit differences. [Sources: original script/results/binned CSV; independent calculation.]

## Main results: 0.5 K bins, reference R(50 K)

All temperatures below are **operational normalized crossings**, not superconducting onset or author-defined zero. Resistance units follow the supplied analysis's ohm/square convention, not independently verified CSV metadata.

| Curve | R(50 K) | T90 | T50 | T10 | T1% | T90−T10 | R(5 K) |
|---|---:|---:|---:|---:|---:|---:|---:|
| SC1 before |125.935509|34.932720|26.485953|18.131859|12.477781|16.800861|0.006592|
| SC1 after |159.759385|34.472311|24.773041|18.949792|11.309716|15.522520|0.317438|
| SC2 before |130.228568|35.244174|25.011002|10.834027|6.125270|24.410148|0.457273|
| SC2 after |186.856321|34.860835|25.876654|10.042786|4.870384|24.818049|2.029948|

After−before **T50**: SC1 **−1.712911 K**, SC2 **+0.865651 K**. T10 changes have opposite signs: **+0.817933**, **−0.791240 K**. R(50 K) ratios: **1.268581**, **1.434834**. These disagree with a blanket claim of identical numerical midpoint thresholds; they do not refute an author claim using a different onset/zero definition. [Source: independently recomputed CSV results.]

Absolute threshold crossings at **0.01 / 0.1 / 1 ohm/square**:
- SC1 before: **6.740862 / 9.331001 / 12.153607 K**; after: **absent / absent / 10.033546 K**.
- SC2 before: **2.763165 / 3.811728 / 5.803077 K**; after: **absent / absent / 3.887259 K**.

These are sensitivity scenarios, **not measured instrument noise floors and not author zero-resistance temperatures**. A normalized 1% crossing still corresponds to approximately 1.26–1.87 ohm/square in these curves.

## Sensitivity and after-curve low-temperature offset

Independently recomputed **all nine** combinations of bins **0.25/0.5/1 K** and references **40/50/60 K**. The JSON records separate bin-only, reference-only and joint ranges for all fractional crossings, Rref and widths, plus absolute-threshold ranges and R(5 K).

| Curve | T50 range: bins only, reference 50 K | T50 range: references only, bins 0.5 K | Joint T50 range |
|---|---:|---:|---:|
| SC1 before |26.485728–26.485953|25.985842–27.026147|25.982978–27.029332|
| SC1 after |24.773041–24.773878|24.494154–25.118796|24.494154–25.129967|
| SC2 before |25.011002–25.011002|24.421876–25.649347|24.421876–25.649347|
| SC2 after |25.867648–25.876654|25.362054–26.362684|25.345915–26.366680|

Matched-scenario after−before T50 ranges remain **negative SC1 (−1.907351 to −1.488649 K)** and **positive SC2 (+0.706231 to +0.941328 K)**. Reference choice affects T90/width strongly: joint width ranges **13.990639–24.774691 K** (SC1 before), **12.369549–23.570272** (SC1 after), **22.391836–28.937893** (SC2 before), **23.348537–28.105314** (SC2 after). Bin robustness is not evidence for reference-independent onset.

After curves retain finite low-T resistance:
- SC1 after: raw T<=5 K has **12 points**, R range **0.237980–0.309680**, median **0.269060**; lowest binned R **0.265405**.
- SC2 after: raw T<=5 K has **38 points**, R range **0.278239–1.957896**, median **0.387515**; lowest binned R **0.300851**. Its lowest raw temperature is **1.982 K**, versus **1.1859 K** for SC1 after.

Both after curves lack 0.01/0.1-ohm crossings in every bin/reference scenario. Cannot distinguish measurement/contact offset, residual sample resistance or another cause from these CSVs alone. As a **diagnostic only**, subtracting raw T<=2.5-K median offsets (**0.265185**, **0.304209**) shifts T50 to **24.780998**, **25.894673 K**, but creates 0.01/0.1 crossings at **2.548841/6.147321** and **2.121170/2.543966 K**. This illustrates why arbitrary baseline subtraction cannot establish physical zero. The uncorrected data remain the main result. [Source: original after CSVs and independent offset calculation.]

## Spin-model audit and archive

Read `bilayer_spin_benchmark.py` and `/tmp/astra10/spin_simulation.json`. Independently built the 16×16 spin-1/2 Hamiltonian using diagonal SzSz terms and bit-flip S+S− matrix elements, rather than the supplied Pauli construction. For Jleg=1, rungs (0,2)/(1,3), legs (0,1)/(2,3), checked

**E0 = −(Jp+1)/2 − sqrt(Jp²−Jp+1)**

at **Jp=0,0.25,0.5,1,2,4,8**. Maximum analytic-minus-stored error **4.9738e-14**; analytic-minus-independent-diagonalization error **5.3291e-15**. At Jp=2, E0 **−3.232050807568877**, independent gap **1.732050807568874**. Stored Aer energy **−3.21826171875 ±0.01570848049** is consistent with that energy at the stated shot uncertainty; shots were not rerun. This spin-only small model has **no charge transport, electronic pairing, material calibration or finite-T transition**; it does **not** establish superconductivity or predict Tc.

Archived `outputs/spin_simulation.json` verbatim through `write_file`; verified byte equality, **3840 bytes**, SHA-256 **a7de0a2fee1276731296e5d9a1424bba1607e66fcc98bc412d230d1b027f0e5d**.

## Provenance, retraction/refutation and confidence

Numerical provenance passes against the supplied manifest, but physical **Fig1c before/after assignment and units are inherited labels**, not independently rechecked publisher metadata. Local `october_paper.txt` is Han et al., arXiv:2610.01757, with an X-ray energy profile in Fig1c; it is not the transport source. `weak_links.txt` is unrelated graph theory. Neither was used as transport evidence.

Checked the existing local `independent_film_audit.md` source/status section: it reports no verified retraction encountered for Zhang et al. DOI **10.1038/s41563-026-02750-z**, but incomplete external comment/failed-replication searches and inaccessible PubPeer. That inherited bounded statement is **not current status clearance**. No new external search was performed as this was a local numeric task. No experimental replication or refutation is claimed. Analytic spin agreement is independently established here; it cannot validate any experimental superconductivity claim.

**Confidence:** high in masks, bin medians, interpolation, operational crossings, sensitivity ranges and spin energies for these inputs; limited in original figure attribution, offset mechanism, instrument zero criterion and external replication/status. Files written via `write_file`: this report, `independent_transport_audit.py`, `outputs/transport_summary.json`, and the verbatim `outputs/spin_simulation.json`. Raw transport inputs remain in `/tmp/astra10`; archived hashes/file IDs plus the independent script support reproduction while those inputs are available.
